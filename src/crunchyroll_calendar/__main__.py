from .calendar import Calendar
from .scraper import Scraper


def main():
    scraper = Scraper()
    calendar = Calendar()
    for day_index in range(7):
        for release in scraper.get_releases(day_index):
            calendar.add_release(release)


if __name__ == '__main__':
    main()
