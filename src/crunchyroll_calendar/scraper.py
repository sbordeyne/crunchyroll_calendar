from datetime import date, datetime, timedelta
from typing import List

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from crunchyroll_calendar.release import Release


class Scraper:
    URL = 'https://crunchyroll.com/fr/simulcastcalendar'

    def __init__(self):
        options = Options()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        self.driver = Chrome(options=options)
        self.driver.get(f'{self.URL}?filter=premium&date={self._date}')
        self.days = self.driver.find_elements(By.XPATH, '//div[@class="day-content"]')

    @property
    def _date(self) -> str:
        today = date.today()
        week_offset = today.isoweekday() - 1 + 7
        last_week_monday = today - timedelta(days=week_offset)
        return last_week_monday.isoformat()

    def get_releases(self, day_index: int) -> List[Release]:
        day = self.days[day_index]
        release_nodes = day.find_elements(By.XPATH, './/article[contains(concat(" ",normalize-space(@class)," ")," release ")]')
        releases = []
        for node in release_nodes:
            episode = node.get_attribute('data-episode-num')
            slug = node.get_attribute('data-slug') or ''
            name = node.find_elements(By.XPATH, './/cite')[0].text
            time_node = node.find_elements(By.XPATH, './/time')[0]
            time = datetime.fromisoformat(time_node.get_attribute('datetime').split('+')[0])
            try:
                episode = int(episode or 1)
                releases.append(
                    Release(
                        f'https://crunchyroll.com/fr/{slug}', episode, name,
                        time.hour, time.minute, day_index + 1,
                    )
                )
            except ValueError:
                try:
                    for e in episode.split('-'):
                        episode = int(e)
                        releases.append(
                            Release(
                                f'https://crunchyroll.com/fr/{slug}', episode, name,
                                time.hour, time.minute, day_index + 1,
                            )
                        )
                except ValueError:
                    continue

        return releases
