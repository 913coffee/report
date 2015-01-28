class CoffeeHistory:
    events_by_date = {}

    def retrieve_for_date(self, date):
        return self.events_by_date.get(date,None)

    def consider(self, event):
        if event.has_measurement() and event.posted_date() not in self.events_by_date:
            self.events_by_date[event.posted_date()] = event

    def earliest(self):
        earliest = None
        for e in self.events_by_date.values():
            if earliest == None or e.posted_datetime() < earliest:
                earliest = e.posted_datetime()
        return earliest

    def latest(self):
        latest = None
        for e in self.events_by_date.values():
            if latest == None or e.posted_datetime() > latest:
                latest = e.posted_datetime()
        return latest

    def fastest(self, n):
        return self.ordered()[:n]

    def slowest(self, n):
        return self.ordered()[-n:]

    def ordered(self):
        return sorted(self.events_by_date.values(), key = lambda e: e.measurement_seconds())

    def summary(self):
        return {
            "earliest": self.earliest().date(),
            "latest": self.latest().date(),
            "num_events": len(self.events_by_date)
        }
