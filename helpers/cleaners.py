def clean_assignment(assignment):
  try:
    assignment_dict = {}
    assignment_dict['grade'] = float(assignment['gradeString']) / assignment['maxPointsTotal']
    assignment_dict['name'] = assignment['name']
    return assignment_dict
  except:
    return {}

