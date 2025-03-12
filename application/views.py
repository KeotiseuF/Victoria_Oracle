from django.shortcuts import render
from .utils.match import get_daily_match, get_tomorrow_match

def home(request):
  daily_match = get_daily_match()
  return render(request, 'home.html', {'daily_match': daily_match})

def calendar(request):
  tomorrow_match = get_tomorrow_match()
  return render(request, 'calendar.html', {'tomorrow_match': tomorrow_match})