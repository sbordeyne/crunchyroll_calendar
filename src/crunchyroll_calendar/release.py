from datetime import datetime, date, timedelta
from dataclasses import dataclass


@dataclass
class Release:
    url: str
    episode: int
    name: str
    hour: int
    minute: int
    day: int  # day of the week, 1=Monday 7=Sunday

    @property
    def datetime_start(self) -> datetime:
        today = date.today()
        start_of_week = today - timedelta(today.isoweekday() - 1)
        show_day = start_of_week + timedelta(self.day - 1)
        return datetime(
            show_day.year, show_day.month, show_day.day,
            self.hour, self.minute, 0, 0
        )

    @property
    def datetime_end(self) -> datetime:
        return self.datetime_start + timedelta(minutes=20)

    @property
    def event_name(self) -> str:
        return f'{self.episode + 1} - {self.name}'
