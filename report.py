#!/usr/bin/python

from CoffeeEvent import CoffeeEvent
from CoffeeHistory import CoffeeHistory
from datetime import timedelta
from math import sqrt
from string import Template
import json
import sys

# yield all dates from start to end
def dates_from_to(start, end):
    now = start
    while now <= end:
        yield now;
        now += timedelta(days=1);

# yield all week numbers from start to end
def weeks_from_to(start, end):
    now = start
    while now <= end:
        yield int(now.strftime('%W'))
        now += timedelta(days=7);

# present seconds in a human readable form
def seconds_nice(total_seconds):
    minutes, seconds = divmod(total_seconds, 60)
    return '%dm%02ds' % (minutes, seconds)

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

# capture file names to process, skipping file names starting with "--"
files_to_process = [x for x in sys.argv[1:] if not x.startswith("--")]

# capture command line args
show_all_events = "--show-all" in sys.argv

# store coffee history here
history = CoffeeHistory()

for filename in files_to_process:
  # capture all lines
  all_lines =  file(filename).readlines()

  # skip first line and parse the rest as JSON
  all_events = json.loads("".join(all_lines[1:]));

  for event in all_events:
      history.consider(CoffeeEvent(event["id"], event["created_at"], event["text"]))


# start the report
summary = history.summary()

list_of_seconds = []
list_of_seconds_for_day = {}
list_of_seconds_for_week = {}

if show_all_events:
    print
    print "All events"
    print "-"*20

i = 1
for date in dates_from_to(summary["earliest"], summary["latest"]):
   event = history.retrieve_for_date(date)
   if event == None: continue
   if show_all_events:
       print '%(i)-3d %(day)-9s %(date)s %(measurement)-7s %(bar)s' % { "i": i,
             "date":date,
             "day": date.strftime('%A'),
             "measurement": seconds_nice(event.measurement().seconds),
             "bar": "*" * (event.measurement().seconds/20)
           }

   day = event.posted_date().isoweekday()
   week = int(event.posted_date().strftime('%W'))

   list_of_seconds_for_day[day] = list_of_seconds_for_day.get(day, []) + [event.measurement().seconds]
   list_of_seconds_for_week[week] = list_of_seconds_for_week.get(week, []) + [event.measurement().seconds]
   list_of_seconds += [event.measurement().seconds]
   i += 1

print
print "Overall"
print "-"*20

overall_stats = calcstats(list_of_seconds)
print '%s measurements from %s to %s, with average %s and stddev %s' % (
    overall_stats["n"],
    seconds_nice(overall_stats["min"]),
    seconds_nice(overall_stats["max"]),
    seconds_nice(overall_stats["avg"]),
    seconds_nice(overall_stats["stddev"])
)

print
print "Weeks"
print "-"*20
for week in weeks_from_to(summary["earliest"], summary["latest"]):
    if week not in list_of_seconds_for_week.keys():
        print 'Week %s had 0 measurements.' % (week)
        continue
    stats = calcstats(list_of_seconds_for_week[week])
    print 'Week %d had %d measurements, from %6s to %6s, with average %6s %s' % ( week,
         stats["n"],
         seconds_nice(stats["min"]),
         seconds_nice(stats["max"]),
         seconds_nice(stats["avg"]),
         "*" * (stats["avg"]/20))

print
print "Weekdays"
print "-"*20

weekdaynames = {
  1 : "Monday",
  2 : "Tuesday",
  3 : "Wednesday",
  4 : "Thursday",
  5 : "Friday"
}

for day in sorted(weekdaynames.keys()):
    stats = calcstats(list_of_seconds_for_day[day])
    print '%-10s had %s measurements from %s to %s, with average %s and stddev %s' % (
        weekdaynames[day] + "s",
        stats["n"],
        seconds_nice(stats["min"]),
        seconds_nice(stats["max"]),
        seconds_nice(stats["avg"]),
        seconds_nice(stats["stddev"])
    )

