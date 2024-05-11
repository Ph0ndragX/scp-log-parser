from event.round_event import RoundEvent


class RoundEventDisconnected(RoundEvent):
    def __init__(self, time, event, log_type, message):
        super().__init__(time, event, log_type, message)
        self._disconnected_id = None
        self._disconnected_name = None
        self._disconnected_last_class = None
        self._parse()

    def disconnected_player_id(self):
        return self._disconnected_id

    def disconnected_player_name(self):
        return self._disconnected_name

    def disconnected_player_last_class(self):
        return self._disconnected_last_class

    def export(self, cursor, round_id):
        pass  # NOOP

    def _parse(self):
        disconnect_msg, last_class_msg = self.message().split("Last class: ")
        self._disconnected_last_class = last_class_msg.strip()[:-1]  # Remove dot

        disconnected_player_name, disconnected_rest = disconnect_msg.strip().split(" disconnected ")

        self._disconnected_id, self._disconnected_name = self._parse_player_id_name(disconnected_player_name.strip())


if __name__ == "__main__":
    e = RoundEventDisconnected(None, None, None,
                               "User (76561198024492377@steam) disconnected from IP address 127.0.0.1. Last class: Spectator.")
    print(e)
