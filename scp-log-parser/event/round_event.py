class RoundEvent:
    def __init__(self, time, event, log_type, message):
        self._time = time
        self._event = event
        self._log_type = log_type
        self._message = message

    def export(self, cursor, round_id):
        print("Error, exporting this event not yet implemented: " + str(self))

    def time(self):
        return self._time

    def event(self):
        return self._event

    def log_type(self):
        return self._log_type

    def message(self):
        return self._message

    def _parse_player_id_name(self, player_id_name):
        parts = player_id_name.split(" ")
        player_id = parts[-1][1:(len(parts[-1]) - 1)]  # Remove parentheses
        player_name = " ".join(parts[:-1])
        return player_id, player_name
