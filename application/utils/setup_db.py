from ..models import Match

def delete_duplicate_match():
  all_match = Match.objects.all()
  clean_match = []
  is_duplicate = False

  for match in all_match:
    if len(clean_match) == 0:
      clean_match.append({'home': match.home, 'day': int(match.match_date.strftime('%d'))})
    else:
      for c_match in clean_match:
        if c_match['home'] == match.home and c_match['day'] == int(match.match_date.strftime('%d')):
          print('Duplicate: ' + match.home + ' - ' + match.away + ' delete OK!' , 'ID: ' + str(match.id))
          Match.objects.get(id=match.id).delete()
          is_duplicate = True
      if is_duplicate == False:
        clean_match.append({'home': match.home, 'day': int(match.match_date.strftime('%d'))})