from event.round_event import RoundEvent


class RoundEventWarheadStatusChanged(RoundEvent):
    def __init__(self, time, event, log_type, message):
        super().__init__(time, event, log_type, message)
        self._id = None
        self._player_changed_id = None
        self._player_changed_name = None
        self._status = None
        self._parse()

    def export(self, cursor, round_id):
        cursor.execute("INSERT INTO event(round, time) VALUES (%s, %s) RETURNING id", (round_id, self.time()))
        self._id, = cursor.fetchone()

        cursor.execute(
            "INSERT INTO event_warhead_status_change("
            "event, player_changed_id, player_changed_name, status) VALUES (%s, %s, %s, %s)",
            (self._id, self._player_changed_id, self._player_changed_name, self._status)
        )

    def _parse(self):
        player_text, status = self.message()[:-1].split(" set the Alpha Warhead status to ")
        self._player_changed_id, self._player_changed_name = self._parse_player_id_name(player_text)
        self._status = status == "True"
