from event.round_event import RoundEvent


class RoundEventWarheadDetonated(RoundEvent):
    def __init__(self, time, event, log_type, message):
        super().__init__(time, event, log_type, message)
        self._id = None

    def export(self, cursor, round_id):
        cursor.execute("INSERT INTO event(round, time) VALUES (%s, %s) RETURNING id", (round_id, self.time()))
        self._id, = cursor.fetchone()

        cursor.execute(
            "INSERT INTO event_warhead_detonated(event) VALUES (%s)", (self._id,)
        )

    def _parse(self):
        pass
