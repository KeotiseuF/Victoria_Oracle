from .direct_match import get_tomorrow_hockey_match, get_daily_hockey_match

def get_tomorrow_match():
  tomorrow_match: list = get_tomorrow_hockey_match()
  return(tomorrow_match)

def get_daily_match():
  daily_match: list = get_daily_hockey_match()
  return(daily_match)
