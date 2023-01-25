# Crunchyroll Calendar

Automates creating a google calendar by scraping crunchyroll's agenda. It's not perfect,
but it does the job well enough.

Caveats :

- I can't really predict the future, so when an anime ends (say episode 13 has been released on week 1), then the calendar will show the next episode in the run (in my example, on week 2, it'll show episode 14 even though that episode doesn't exist). It's because I'm taking the previous week's planning, and updating the episode numbers for the current week.
- That same caveat applies to the start of an anime as well. Given how hard crunchyroll makes it to scrape them, I don't really want to parse the season planning page (especially since they are often late on publishing it)
- This calendar was generated on the french version of crunchyroll. I'm still sharing here, because France is a big anime market, maybe some fellow baguettes will enjoy it.
- This is for the premium calendar only. Since I made it for me, I don't see the point in the free version since I am paying for a subscription.

Running the project :

- Clone the repo
- Install `poetry`
- Download the chrome driver at https://sites.google.com/chromium.org/driver/?pli=1
- Put the path to the folder containing the driver in you `$PATH` environment variable.
- (Optional) export the `DATA_DIR` environment variable (it's where data will be stored, especially google credentials)
- Generate a file called `credentials.json` for the google calendar credentials. Follow google's documentation
  - Scope required : `https://www.googleapis.com/auth/calendar`
- Run `poetry install && poetry run python3 -m crunchyroll_calendar`

Alternatively, there is a docker image available at `sbordeyne/crunchyroll_calendar:1.0.0`

Build using `docker build --platform=linux/amd64 -t sbordeyne/crunchyroll_calendar:1.0.0 ./Dockerfile`
