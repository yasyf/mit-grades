def clean_assignment(assignment):
  try:
    assignment_dict = {}
    assignment_dict['grade'] = float(assignment['gradeString']) / assignment['maxPointsTotal']
    assignment_dict['name'] = assignment['name']
    assignment_dict['dropped'] = assignment.get('dropped', False)
    return assignment_dict
  except:
    return {}

def clean_courses(courses):
  return filter(lambda c: 'msid' in c, courses)

def clean_categories(categories):
  return filter(lambda c: c['name'].lower() != 'uncategorized', categories)

def clean_summed_totals(summed_totals):
  return filter(lambda t: t['avg'] > 0, summed_totals)
