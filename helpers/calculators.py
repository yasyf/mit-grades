from adjustments import drop_lowest

def calculate_averages(number, assignments, categories):
  averages = {k:[] for k in categories.keys()}
  for assignment in assignments:
    try:
      averages[assignment['categoryId']].append((float(assignment['gradeString']) / assignment['maxPointsTotal'], assignment['weight']))
    except:
      continue

  for k, v in averages.items():
        name = categories[k][0]
        if name in drop_lowest.get()[number]:
          drop = drop_lowest.get()[number][name]
          if len(v) > drop:
            averages[k] = list(sorted(v))[drop:]
  return averages

def calculate_summed_totals(averages, categories):
  summed_totals = []
  total_weight = sum([x[1] for x in categories.values()])

  for k,average in averages.items():
    category = categories[k]
    avg = sum([x[0] for x in average]) / (len(average) or 1)
    total = {'name': category[0], 'avg': avg, 'weight': category[1] / total_weight}
    summed_totals.append(total)

  values = sum(averages.values(), [])
  total_total = sum([x[0]*x[1] for x in values]) / (sum([x[1] for x in values]) or 1)
  summed_totals.insert(0, {'name': 'Weighted Total', 'avg': total_total})

  return summed_totals, total_total

def calculate_letter(total, grading_scheme):
  grade_options = list(sorted(grading_scheme, key=lambda x: x['lowerBound']))
  index = 0
  while total > grade_options[index]['lowerBound']:
    index += 1
    if index is len(grade_options) - 1:
      break
  return grade_options[index]['gradeString']
