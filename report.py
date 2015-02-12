#!/usr/bin/python

from CoffeeEvent import CoffeeEvent
from CoffeeHistory import CoffeeHistory
from CoffeeUtil import seconds_nice, dates_from_to, weeks_from_to, calcstats
from datetime import timedelta
from string import Template
import json
import sys

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
      history.consider(CoffeeEvent(event))


# start the report
summary = history.summary()

list_of_seconds = []
list_of_seconds_for_day = {}
list_of_seconds_for_week = {}

if show_all_events:
    print
    print "All events"
    print "-"*20

curr_week_num = None
i = 1
for date in dates_from_to(summary["earliest"], summary["latest"]):
   event = history.retrieve_for_date(date)

   if show_all_events:
       event_week_num = date.strftime('%W')
       if curr_week_num is None or event_week_num != curr_week_num:
           print
           print "Week", int(event_week_num)
           curr_week_num = event_week_num

   # no event for this date?
   if event == None:
       if show_all_events:
           print '          %-3s %-9s %s' % ("", date.strftime('%A'), date)
       continue

   if show_all_events:
       print '    Event %-3d %s' % (i, event.as_oneline_with_bar())


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
print "Fastest:"
print
for event in history.fastest(5):
   print "*", event.as_oneline_with_link()

print
print "Slowest:"
print
for event in history.slowest(5):
   print "*", event.as_oneline_with_link()

print
print "Weeks"
print "-"*20
measurements = 0
weeks_with_measurements = 0
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
    measurements += stats["n"]
    weeks_with_measurements += 1

if weeks_with_measurements > 0:
   print
   print 'For the %d weeks with measurements, there are %.1f measurements per week on average' % (
       weeks_with_measurements,
       measurements/float(weeks_with_measurements)
   )

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

