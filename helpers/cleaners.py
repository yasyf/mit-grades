def clean_assignment(assignment):
  try:
    assignment_dict = {}
    assignment_dict['grade'] = float(assignment['gradeString']) / assignment['maxPointsTotal']
    assignment_dict['name'] = assignment['name']
    return assignment_dict
  except:
    return {}

def clean_courses(courses):
  return filter(lambda c: 'msid' in c, courses)

def clean_categories(categories):
  return filter(lambda c: c['name'].lower() != 'uncategorized', categories)
