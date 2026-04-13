#text formatting function
def f(format, text = ''):
    formatters = { 
        'gray': "\033[30m",
        'grey': "\033[30m",
        'green': "\033[32m",
        'clear': "\033c",
        'blue': "\033[34m",
        'white': "\033[0m",
        '###': "\033[30m###\033[0m",
        'red': "\033[31m",
        'magenta': "\033[31m",
        'cyan': "\033[36m",
        'lime': "\033[92m",
        'yellow': "\033[93m",
        'light blue': "\033[94m",
        "bright red": "\033[91m"
    }
    try:
        return formatters[format] + text + "\033[0m"
    except:
        return
    
def ftime(time):
    day = time / 24
    week = time // 7
    weekday = week % 7
    hour = time % 24
    american_time = hour % 12
    if hour > 11:
        am_pm = "PM"
    else:
        am_pm = "AM"
    weekdays = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
        7: "Sunday"
    }
    return f"{american_time}:00 {am_pm} {weekdays[weekday]}, Week {week}"