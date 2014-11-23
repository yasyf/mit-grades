import mechanize, requests, json
from bs4 import BeautifulSoup
from helpers.calculators import *
from helpers.cleaners import *

class API(object):
  API_ROOT = 'https://learning-modules.mit.edu/service'
  UI_ROOT = 'https://learning-modules.mit.edu/portal'
  ACTIONS = {
    'courses': '/membership/groups',
    'course': '/gradebook/gradebook?uuid=STELLAR:{uuid}&autocreate=false',
    'permissions': '/gradebook/role/{gradebook_id}?includePermissions=true',
    'categories': '/gradebook/assignmentcategories/{gradebook_id}?includeDeleted=true&includeAggregation=true',
    'grading': '/gradebook/gradingSchemes/{gradebook_id}',
    'assignments': '/gradebook/student/{gradebook_id}/{person_id}/1?includeGradeInfo=true&includeAssignmentMaxPointsAndWeight=true&includePhoto=false&includeGradeHistory=false&includeCompositeAssignments=true&includeAssignmentGradingScheme=true'
    }

  def __init__(self, kerberos, password):
    self.kerberos = kerberos
    self.password = password
    self.set_browser()

  def set_browser(self):
    self.browser = mechanize.Browser()
    self.browser.set_handle_robots(False)
    self.browser.open(API.UI_ROOT)
    self.browser.select_form(nr=1)
    self.browser.submit()
    self.browser.select_form(nr=1)
    self.browser["j_username"] = self.kerberos
    self.browser["j_password"] = self.password
    self.browser.submit()
    self.browser.select_form(nr=0)
    response = self.browser.submit().read()

    self.authenticated = ('MIT Learning Modules' in response)

  def get_user(self):
    url = "http://web.mit.edu/bin/cgicso?options=general&query={}".format(self.kerberos)
    soup = BeautifulSoup(requests.get(url).text)
    pre = soup.find("pre")
    user = {}
    if pre.text.find("No matches") == -1:
      l = [[y.strip() for y in x.split(":")] for x in pre.text.split("\n")]
      user = {x[0]:x[1] for x in l if len(x) == 2}
    if user.get('name'):
      componenets = user['name'].split(',')
      user['name'] = componenets[1].strip().split(' ')[0] + ' ' + componenets[0]
    return user

  def get(self, action, **kwargs):
    url = API.API_ROOT + API.ACTIONS[action].format(**kwargs)
    data = json.loads(self.browser.open(url).read())
    return data.get('data') or data.get('response') or data

  def get_grades(self):
    grades = {}
    for course in clean_courses(self.get('courses')['docs']):
      uuid, number = course['uuid'], course['msid']
      gradebook_id = self.get('course', uuid=uuid)['gradebookId']
      person_id = self.get('permissions', gradebook_id=gradebook_id)['person']['personId']
      categories_data = self.get('categories', gradebook_id=gradebook_id)
      categories_data = clean_categories(categories_data)
      if not categories_data:
        continue
      categories = {x['categoryId']:(x['name'], x['weight'], float(x['totalAverage'] or 0)) for x in categories_data}
      grading_scheme = self.get('grading', gradebook_id=gradebook_id)[0].get('gradeOptions', {})
      assignments = self.get('assignments', gradebook_id=gradebook_id, person_id=person_id)['studentAssignmentInfo']

      averages = calculate_averages(number, assignments, categories)
      summed_totals, total_total = calculate_summed_totals(averages, assignments, categories)
      letter = calculate_letter(total_total, grading_scheme)

      grades[number] = {'sums': summed_totals, 'total': total_total, 'letter': letter}

    return grades
