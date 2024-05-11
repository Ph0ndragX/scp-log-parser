from event.round_event_disconnected import RoundEventDisconnected
from event.round_event_factory import RoundEventFactory
from event.round_event_kill import RoundEventKill
from event.round_event_warhead_countdown_started import RoundEventWarheadCountdownStarted


class Round:
    def __init__(self, filename):
        self._filename = filename
        self._logs = []
        self._id = None
        self._previous_warhead_countdown_started = None
        self._events = self._parse_events()
        self._scps = self._find_scps_in_round()
        self._fill_kill_events_with_killer_scps()

    def id(self):
        return self._id

    def scp(self, scp_name):
        if scp_name not in self._scps:
            print(f"Missing data for {scp_name} in round {self._filename}")
            return {"id": None, "name": None}
        return self._scps[scp_name]

    def export(self, cursor):
        cursor.execute("INSERT INTO round (log_filename) VALUES (%s) RETURNING id", (self._filename.name,))
        self._id, = cursor.fetchone()

        for event in self._events:
            event.export(cursor, self._id)

    def _parse_events(self):
        events_parser = RoundEventFactory()
        events = []
        with self._filename.open(encoding='utf-8') as f:
            for line in f.readlines():
                if line.strip() == "":
                    continue

                event = events_parser.parse(line)
                if event is None:
                    continue

                if isinstance(event, RoundEventWarheadCountdownStarted):
                    is_duplicate = self._previous_warhead_countdown_started is not None and (
                            (event.time() - self._previous_warhead_countdown_started).total_seconds() < 2)
                    if not is_duplicate:
                        self._previous_warhead_countdown_started = event.time()
                    else:
                        continue

                events.append(event)

        return events

    def _find_scps_in_round(self):
        scps = {}
        for e in self._events:
            if isinstance(e, RoundEventKill):
                if e.killer_type() is not None and e.killer_type().lower().startswith("scp"):
                    scps["SCP-" + e.killer_type()[4:]] = {
                        "id": e.killer_id(),
                        "name": e.killer_name()
                    }

                if e.killed_type() is not None and e.killed_type().lower().startswith("scp"):
                    scps["SCP-" + e.killed_type()[4:]] = {
                        "id": e.killer_id(),
                        "name": e.killed_name()
                    }
            if isinstance(e, RoundEventDisconnected):
                if e.disconnected_player_last_class() is not None and e.disconnected_player_last_class().lower().startswith(
                        "scp"):
                    scps["SCP-" + e.disconnected_player_last_class()[3:]] = {
                        "id": e.disconnected_player_id(),
                        "name": e.disconnected_player_name()
                    }

        return scps

    def _fill_kill_events_with_killer_scps(self):
        for e in self._events:
            if isinstance(e, RoundEventKill):
                e.update_scp_killer(self)
