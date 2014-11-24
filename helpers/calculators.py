from adjustments import drop_lowest
from cleaners import clean_assignment
import collections

def calculate_averages(number, assignments, categories):
  averages = collections.defaultdict(list)
  for assignment in assignments:
    try:
      category_id = assignment['categoryId']
      grade = float(assignment['gradeString']) / assignment['maxPointsTotal']
      averages[category_id].append((grade, assignment['weight']))
    except:
      continue

  for k, v in averages.items():
        name = categories[k][0]
        if name in drop_lowest.get()[number]:
          drop = drop_lowest.get()[number][name]
          if len(v) > drop:
            averages[k] = list(sorted(v))[drop:]

  return averages

def calculate_summed_totals(averages, assignments, categories):
  summed_totals = []
  total_weight = sum([x[1] for x in map(lambda x: categories[x], averages.keys())])

  total_total = 0
  for k, average in averages.items():
    category = categories[k]
    weight = float(category[1]) / total_weight
    avg = sum([x[0]*x[1] for x in average]) / sum([x[1] for x in average])
    items = [clean_assignment(a) for a in assignments if a['categoryId'] == k]
    items = filter(lambda x: x, items)
    total = {'name': category[0], 'avg': avg, 'weight': weight, 'assignments': items}
    summed_totals.append(total)
    total_total += avg * weight

  summed_totals.insert(0, {'name': 'Weighted Total', 'avg': total_total})

  return summed_totals, total_total

def calculate_letter(total, grading_scheme):
  if not grading_scheme:
    return '?'
  grade_options = list(sorted(grading_scheme, key=lambda x: x['lowerBound']))
  index = 0
  while total > grade_options[index + 1]['lowerBound']:
    index += 1
    if index == len(grade_options) - 1:
      break
  return grade_options[index]['gradeString']
