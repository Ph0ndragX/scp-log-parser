from event.round_event import RoundEvent


class RoundEventStart(RoundEvent):
    def __init__(self, time, event, log_type, message):
        super().__init__(time, event, log_type, message)

    def export(self, cursor, round_id):
        cursor.execute("UPDATE round SET start_time = %s WHERE id = %s", (self.time(), round_id))
