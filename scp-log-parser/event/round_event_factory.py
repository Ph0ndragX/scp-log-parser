import datetime

from event.round_event_disconnected import RoundEventDisconnected
from event.round_event_end import RoundEventEnd
from event.round_event_kill import RoundEventKill
from event.round_event_start import RoundEventStart
from event.round_event_warhead_countdown_started import RoundEventWarheadCountdownStarted
from event.round_event_warhead_detonated import RoundEventWarheadDetonated
from event.round_event_warhead_status_changed import RoundEventWarheadStatusChanged


class RoundEventFactory:
    def __init__(self):
        self._events = [
            "Internal", "Connection update", "Game Event", "Rate Limit", "Kill", "Remote Admin", "Suicide", "Teamkill",
            "AdminChat", "Remote Admin - Misc"
        ]

        self._types = [
            "Logger", "Networking", "Class change", "Administrative", "Warhead", "Permissions", "Data access"
        ]

    def parse(self, log_line):
        log_line_parts = log_line.split("|")
        time = datetime.datetime.strptime(log_line_parts[0].strip(), "%Y-%m-%d %H:%M:%S.%f %z")
        event = log_line_parts[1].strip()
        log_type = log_line_parts[2].strip()
        message = log_line_parts[3].strip()

        if message == "Round has been started.":
            return RoundEventStart(time, event, log_type, message)
        elif message.startswith("Round finished!"):
            return RoundEventEnd(time, event, log_type, message)
        elif event == "Kill" or event == "Teamkill":
            return RoundEventKill(time, event, log_type, message)
        elif "disconnected from IP address" in message:
            return RoundEventDisconnected(time, event, log_type, message)
        elif log_type == "Warhead" and "Alpha Warhead status" in message:
            return RoundEventWarheadStatusChanged(time, event, log_type, message)
        elif log_type == "Warhead" and "started the Alpha Warhead detonation" in message:
            return RoundEventWarheadCountdownStarted(time, event, log_type, message)
        elif log_type == "Warhead" and "Warhead detonated" in message:
            return RoundEventWarheadDetonated(time, event, log_type, message)
