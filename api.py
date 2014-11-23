import mechanize, requests
from bs4 import BeautifulSoup

class API(object):
  API_ROOT = 'https://learning-modules.mit.edu/service'
  UI_ROOT = 'https://learning-modules.mit.edu/portal'

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
      user = {x[0]:x[1] for x in l if len(x) is 2}
    if user.get('name'):
      componenets = user['name'].split(',')
      user['name'] = componenets[1].strip().split(' ')[0] + ' ' + componenets[0]
    return user
