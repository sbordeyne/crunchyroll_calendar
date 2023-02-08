from datetime import date, datetime, timedelta
import random
from typing import List

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from crunchyroll_calendar.release import Release
from crunchyroll_calendar.config import username, password


class Scraper:
    CALENDAR_URL = 'https://crunchyroll.com/fr/simulcastcalendar'
    LOGIN_URL = (
        'https://sso.crunchyroll.com/authorize?'
        'client_id=noaihdevm_6iyg0a8l0q&redirect_uri='
        'https%3A%2F%2Fwww.crunchyroll.com%2Fcallback&'
        'response_type=cookie&state=%2F'
    )

    def __init__(self):
        options = Options()
        options.headless = True
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-gpu')  # Last I checked this was necessary.
        self.driver = Chrome(options=options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        ]
        self.driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": random.choice(user_agents)})
        if username and password:
            self.login()
        self.driver.get(f'{self.CALENDAR_URL}?filter=premium&date={self._date}')
        self.days = self.driver.find_elements(By.XPATH, '//div[@class="day-content"]')

    def login(self):
        self.driver.get(self.LOGIN_URL)
        username_field = self.driver.find_element(By.NAME, 'username')
        username_field.send_keys(username)
        password_field = self.driver.find_element(By.NAME, 'password')
        password_field.send_keys(password)
        password_field.send_keys(Keys.ENTER)

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
            in_watchlist = len(node.find_elements(By.CSS_SELECTOR, '.queue-flag.queued')) > 0
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
                        in_watchlist=in_watchlist,
                    )
                )
            except ValueError:
                try:
                    for e in episode.split('-'):
                        episode = int(e)
                        releases.append(
                            Release(
                                f'https://crunchyroll.com/fr/{slug}', episode, name,
                                time.hour, time.minute, day_index + 1, in_watchlist=in_watchlist,
                            )
                        )
                except ValueError:
                    continue

        return releases
