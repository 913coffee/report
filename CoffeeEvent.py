from CoffeeUtil import seconds_nice
from datetime import timedelta
import dateutil.parser
import re

class CoffeeEvent:

    def __init__(self, event):
        self.event_id = event["id_str"]
        self.created_at = event["created_at"]
        self.text = event["text"]
        self.screen_name = event["user"]["screen_name"]

    def get_id(self):
       return self.event_id

    def spaced_time_to_iso(self, d):
       return d[0:19].replace(" ", "T") + "Z"

    def posted_date(self):
        return self.posted_datetime().date()

    def posted_datetime(self):
        """ report the datetime.datetime instance of when this event was posted."""
        subtract_magnitude = 7 * 60 * 60 # 7 hours
        if "This was from yesterday" in self.text:
            subtract_magnitude += 24 * 60 * 60 # 1 day
        date = self.spaced_time_to_iso(self.created_at)
        d = dateutil.parser.parse(date)
        d = d - timedelta(seconds=subtract_magnitude)
        return d

    def has_measurement(self):
        return self.measurement() != None

    def measurement_seconds(self):
        return self.measurement().seconds

    def measurement(self):
        """ report the timedelta of how long the coffee run took."""
        measurement = re.search('(\d+):(\d\d)\.(\d\d)', self.text)
        if measurement:
            minutes = int(measurement.group(1))
            seconds = int(measurement.group(2))
            milliseconds = int(measurement.group(3)) * 10
            return timedelta(minutes=minutes,seconds=seconds,milliseconds=milliseconds)
        else:
            return None

    def get_link(self):
        return 'https://twitter.com/%s/status/%s' % (self.screen_name, self.event_id)

    def get_text(self, n=140):
       assert n >= 3
       if len(self.text) > n:
           return self.text[:n-3] + "..."
       return self.text

    def as_oneline_with_link(self):
        return '%(day)-9s %(date)s %(measurement)-7s %(text)-45s %(link)s' % \
            { "day": self.posted_date().strftime('%A'),
              "date": self.posted_date(),
              "measurement": seconds_nice(self.measurement().seconds),
              "text": self.get_text(n=45),
              "link": self.get_link()
            }

    def as_oneline_with_bar(self, scaling=20):
        return '%(day)-9s %(date)s %(measurement)-7s %(bar)s' % \
            { "date": self.posted_date(),
              "day": self.posted_date().strftime('%A'),
              "measurement": seconds_nice(self.measurement().seconds),
              "bar": "*" * (self.measurement().seconds/scaling)
            }
