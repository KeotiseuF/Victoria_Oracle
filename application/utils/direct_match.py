from selenium import webdriver
from selenium.webdriver.common.by import By
from .browser import manage_browser
from datetime import datetime, timedelta

def get_hockey_match(params:str = ''):
  valid_championship = [
    'Etats-Unis - NHL',
    'Suède - SHL',
    'Finlande - Liiga',
  ]

  browser: webdriver.Chrome = manage_browser('https://www.matchendirect.fr/hockey/' + params, None, False)
  match_panel = browser.find_elements(By.CLASS_NAME, 'tournament')
  number_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
  hockey_match = []
  inc = 0
  for mp in match_panel:
    championship = mp.find_element(By.CSS_SELECTOR, 'th.time').text.strip()
    if championship in valid_championship:
      hour_inc = 0
      hour = mp.find_elements(By.CSS_SELECTOR, 'td.time')
      equipe1 = mp.find_elements(By.CSS_SELECTOR, 'td.teams .home')
      equipe2 = mp.find_elements(By.CSS_SELECTOR, 'td.teams .away')
      hockey_match.append({"name": championship, 'matches': []})
      for h in hour:
        text_hour = h.text
        if text_hour[0] in number_list:
          hockey_match[inc]['matches'].append({'name': equipe1[hour_inc].text + ' - ' + equipe2[hour_inc].text, 'hour': text_hour})
        else:
          text_hour = 'ANNULER'
          hockey_match[inc]['matches'].append({'name': equipe1[hour_inc].text + ' - ' + equipe2[hour_inc].text, 'hour': text_hour, 'cancel': True})
        hour_inc = hour_inc + 1
      inc = inc + 1
  manage_browser('', browser)
  return(hockey_match)

def get_daily_hockey_match():
  daily_hockey_match: list = get_hockey_match()
  return(daily_hockey_match)

def get_tomorrow_hockey_match():
  tomorrow_date = (datetime.now() + timedelta(1)).strftime('%d-%m-%Y')
  tomorrow_hockey_match: list = get_hockey_match(tomorrow_date)
  return(tomorrow_hockey_match)

def get_tomorrow_match():
  tomorrow_match: list = get_tomorrow_hockey_match()
  return(tomorrow_match)

def get_daily_match():
  daily_match: list = get_daily_hockey_match()
  return(daily_match)
