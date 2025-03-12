from selenium import webdriver
from selenium.webdriver.common.by import By
from .browser import manage_browser
from datetime import datetime, timedelta, date
from ..models import Sport, Competition, Match, Prediction

def get_hockey_match(daily_date = datetime.today()):
  valid_championship = [
    'Etats-Unis - NHL',
    'Suède - SHL',
    'Finlande - Liiga',
  ]

  browser: webdriver.Chrome = manage_browser('https://www.matchendirect.fr/hockey/' + daily_date.strftime('%d-%m-%Y'), None, False)
  match_panel = browser.find_elements(By.CLASS_NAME, 'tournament')
  number_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
  hockey_match = []
  id_championship = 0

  for mp in match_panel:
    championship = mp.find_element(By.CSS_SELECTOR, 'th.time').text.strip()
    if championship in valid_championship:
      id_match = 0
      hour = mp.find_elements(By.CSS_SELECTOR, 'td.time')
      equipe1 = mp.find_elements(By.CSS_SELECTOR, 'td.teams .home')
      equipe2 = mp.find_elements(By.CSS_SELECTOR, 'td.teams .away')
      hockey_match.append({"name": championship, 'matches': []})
      match_date = None

      for h in hour:
        text_hour = h.text
        hockey_match[id_championship]['matches'].append({'home': equipe1[id_match].text, 'away': equipe2[id_match].text})
        if text_hour[0] in number_list:
          match_date = datetime(
            year = int(daily_date.strftime('%Y')),
            month = int(daily_date.strftime('%m')),
            day = int(daily_date.strftime('%d')),
            hour = int(text_hour.split(':')[0]),
            minute = int(text_hour.split(':')[1].strip())
          )
          hockey_match[id_championship]['matches'][id_match]['match_date'] = match_date
        else:
          hockey_match[id_championship]['matches'][id_match]['match_date'] = match_date
        id_match += 1
      id_championship += 1
  manage_browser('', browser)
  return(hockey_match)

def create_match(championship: list, day: str):
  for champ in championship:
    championship_id = Competition.objects.get(name=champ['name']).id
    for match in champ['matches']:
      Match.objects.create(home=match['home'], away=match['away'], match_date=match['match_date'], championship_id=championship_id)
  print(day + ' match save.')

def get_db_match(params_date = datetime.today()):
  year = int(params_date.strftime('%Y'))
  month = int(params_date.strftime('%m'))
  day = int(params_date.strftime('%d'))

  matches = Match.objects.filter(match_date__date=date(year, month, day)).order_by('championship_id')
  data_to_display = []

  for match in matches:
    championship = match.championship.name
    id_championship = 0
    is_match_add = False

    if len(data_to_display) != 0:
      while len(data_to_display) != (id_championship):
        for champ in data_to_display:
          if championship == champ['name'] and is_match_add == False:
            data_to_display[id_championship]['matches'].append({'home': match.home, 'away': match.away, 'match_date': match.match_date })
            is_match_add = True
          id_championship += 1
      if is_match_add == False:
        data_to_display.append({'name': championship, 'matches': [{'home': match.home, 'away': match.away, 'match_date': match.match_date }]})
        is_match_add = True
      is_match_add = False
    else:
      data_to_display.append({'name': championship, 'matches': [{'home': match.home, 'away': match.away, 'match_date': match.match_date }]})
  return data_to_display

def get_daily_hockey_match():
  daily_hockey_match: list = get_db_match()
  if len(daily_hockey_match) == 0:
    daily_hockey_match = get_hockey_match()
    create_match(daily_hockey_match, 'Daily')
  return(daily_hockey_match)

def get_tomorrow_hockey_match():
  tomorrow_date = datetime.now() + timedelta(1)
  tomorrow_hockey_match: list = get_db_match(tomorrow_date)
  if len(tomorrow_hockey_match) == 0:
    tomorrow_hockey_match = get_hockey_match(tomorrow_date)
    create_match(tomorrow_hockey_match, 'Tomorrow')
  return(tomorrow_hockey_match)