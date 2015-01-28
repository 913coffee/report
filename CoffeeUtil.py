from datetime import timedelta
from math import sqrt

# present seconds in a human readable form
def seconds_nice(total_seconds):
    minutes, seconds = divmod(total_seconds, 60)
    return '%dm%02ds' % (minutes, seconds)

# yield all dates from start to end
def dates_from_to(start, end, skipweekends=True):
    now = start
    while now <= end:

        doyield = True
        if (skipweekends and now.isoweekday() in [6, 7]):
           doyield = False

        if doyield:
            yield now

        now += timedelta(days=1);

# yield all week numbers from start to end
def weeks_from_to(start, end):
    now = start
    while now <= end:
        yield int(now.strftime('%W'))
        now += timedelta(days=7);

# calculate statistics on numbers in a list
def calcstats(list):
    n = len(list)
    avg = sum(list) / n
    pop_var = sum([(s-avg)**2 for s in list])/n
    return {
        "min": min(list),
        "max": max(list),
        "avg": avg,
        "n": n,
        "stddev": sqrt(pop_var)
    }

