# pingTwitter
Python app that monitors user-defined Twitter accounts for activity. A Pushover alert is triggered if a monitored account shows no activity. Useful for monitoring bots.

The script uses BeautifulSoup to scrape and store the total number of tweets for each account in `pingTwitter.json`. If the number does not change then a Pushover alert is triggered. Use crontab and run this every hour to make sure bot accounts are up and running.

Set your Pushover keys: `client = Client("<pushover client>", api_token="<api token>")`

Set the accounts to monitor: `accts = ['account 1', 'account 2']`
