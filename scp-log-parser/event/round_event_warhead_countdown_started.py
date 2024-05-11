from event.round_event import RoundEvent


class RoundEventWarheadCountdownStarted(RoundEvent):
    def __init__(self, time, event, log_type, message):
        super().__init__(time, event, log_type, message)
        self._id = None
        self._player_started_id = None
        self._player_started_name = None
        self._parse()

    def export(self, cursor, round_id):
        cursor.execute("INSERT INTO event(round, time) VALUES (%s, %s) RETURNING id", (round_id, self.time()))
        self._id, = cursor.fetchone()

        cursor.execute(
            "INSERT INTO event_warhead_countdown_started(event, player_started_id, player_started_name) VALUES (%s, %s, %s)",
            (self._id, self._player_started_id, self._player_started_name)
        )

    def _parse(self):
        self._player_started_id, self._player_started_name = self._parse_player_id_name(
            self.message()[:-len(" started the Alpha Warhead detonation.")])
