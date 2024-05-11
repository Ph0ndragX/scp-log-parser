import round


class RoundsLoader:
    def __init__(self, directory):
        self._directory = directory

    def load(self):
        return [
            round.Round(log_filename) for log_filename in self._directory.iterdir() if
            log_filename.name.startswith("Round")
        ]
