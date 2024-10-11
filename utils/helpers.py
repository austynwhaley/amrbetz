from datetime import date
from utils.matchups import *

def get_current_week_matchups():
    today = date.today()
    for week, (start_date, end_date) in date_ranges_by_week.items():
        if start_date <= today <= end_date:
            return week, matchups_by_week[week]
    return None, [] 

def get_current_game_week():
    today = date.today()

    for week, (start_date, end_date) in date_ranges_by_week.items():
        if start_date <= today <= end_date:
            return week
    
    return None 