from datetime import timedelta
import dateutil.parser
import re

class CoffeeEvent:

    def __init__(self, event_id, created_at, text):
        self.event_id = event_id
        self.created_at = created_at
        self.text = text

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


    def measurement(self):
        """ report the millisecond count of how long the coffee run took."""
        measurement = re.search('(\d+):(\d\d)\.(\d\d)', self.text)
        if measurement:
            minutes = int(measurement.group(1))
            seconds = int(measurement.group(2))
            milliseconds = int(measurement.group(3)) * 10
            return timedelta(minutes=minutes,seconds=seconds,milliseconds=milliseconds)
            # total = milliseconds + 1000*seconds + 60*1000*minutes
            # return total
        else:
            return None

