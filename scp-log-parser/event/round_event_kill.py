from event.round_event import RoundEvent


class RoundEventKill(RoundEvent):
    def __init__(self, time, event, log_type, message):
        super().__init__(time, event, log_type, message)
        self._id = None
        self._killer_id = None
        self._killer_name = None
        self._killer_type = None
        self._killed_id = None
        self._killed_name = None
        self._killed_type = None
        self._parse()

    def killer_id(self):
        return self._killer_id

    def killer_name(self):
        return self._killer_name

    def killer_type(self):
        return self._killer_type

    def killed_id(self):
        return self._killed_id

    def killed_name(self):
        return self._killed_name

    def killed_type(self):
        return self._killed_type

    def update_scp_killer(self, rnd):
        if self._specific == "Decayed in the Pocket Dimension":
            scp = rnd.scp("SCP-106")
            self._killer_id = scp["id"]
            self._killer_name = scp["name"]
            self._killer_type = "SCP-106"

    def export(self, cursor, round_id):
        cursor.execute("INSERT INTO event(round, time) VALUES (%s, %s) RETURNING id", (round_id, self.time()))
        self._id, = cursor.fetchone()

        cursor.execute(
            "INSERT INTO event_kill("
            "event, team_kill, killer_id, killer_name, killer_type, killed_id, killed_name, killed_type, specific"
            ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (self._id, self._team_kill, self._killer_id, self._killer_name, self._killer_type, self._killed_id,
             self._killed_name, self._killed_type, self._specific)
        )

    def print(self):
        print(
            f"{self._killer_name} ({self._killer_id}) as {self._killer_type} killed {self._killed_name} ({self._killed_id}) as {self._killed_type} (is team kill: {self._team_kill})")

    def _parse(self):
        self._team_kill = self.event() == "Teamkill"

        kill_msg, self._specific = self.message().split(".", 1)
        if kill_msg is None or self._specific is None:
            raise Exception("Failed parsing round kill message: " + self.message())

        self._specific = self._specific.strip()[len("Specific death reason: "):-1]

        killed_id_text, killed_type_text, killer_text = kill_msg.split(",")

        self._killed_id, self._killed_name, self._killed_type = self._parse_killed_text(killed_id_text.strip(),
                                                                                        killed_type_text.strip())
        self._killer_id, self._killer_name, self._killer_type = self._parse_killer_text(killer_text.strip())

    def _parse_killed_text(self, killed_id, killed_type_text):
        player_id, player_name = self._parse_player_id_name(killed_id)
        return player_id, player_name, killed_type_text[len("playing as "):]

    def _parse_killer_text(self, killer_text):
        if killer_text == "has died":
            return None, None, None

        killed_prefix_text = "has been teamkilled by " if self._team_kill else "has been killed by "

        player_text, player_type = killer_text[len(killed_prefix_text):].split(" playing as: ")
        player_id, player_name = self._parse_player_id_name(player_text)
        return player_id, player_name, player_type
