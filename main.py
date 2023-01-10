import requests
from twilio.rest import Client
ACCT_SID = "ACa5c2e5e062b817f965bf9a35a647a7fa"
AUTH_TOKEN = YOUR_AUTH_TOKEN_HERE
MY_NUMBER = YOUR_TWILIO_NUMBER_HERE
STOCK = "TSLA"
COMPANY_NAME = "Tesla"
key = "ALFFDXVZ237URZRP"
news_key = YOUR_NEWS_API_KEY_HERE
days_list = []

parameters_ticker = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": key
}

parameters_news = {
    "q": COMPANY_NAME,
    "apiKey": news_key,
    "pageSize": 3,
}

response = requests.get("https://www.alphavantage.co/query", params=parameters_ticker)
response.raise_for_status()
data = response.json()

for days in data["Time Series (Daily)"]:
    days_list.append(days)


open_day_1 = float(data["Time Series (Daily)"][days_list[0]]["1. open"])
open_day_2 = float(data["Time Series (Daily)"][days_list[1]]["1. open"])
close_day_1 = float(data["Time Series (Daily)"][days_list[0]]["4. close"])
close_day_2 = float(data["Time Series (Daily)"][days_list[1]]["4. close"])
print(close_day_2)
print(close_day_1)
increase = close_day_1 - close_day_2
percentage_change = round((increase/close_day_2) * 100, 2)
print(percentage_change)


if percentage_change > 0:
    change_symbol = "🔺"
else:
    change_symbol = "🔻"

if percentage_change > 5 or percentage_change < -5:
    response = requests.get("https://newsapi.org/v2/top-headlines", params=parameters_news)
    data = response.json()
    for article in data["articles"]:
        title = (article["title"])
        articles = (article["description"])
        client = Client(ACCT_SID, AUTH_TOKEN)

        message = client.messages \
            .create(
                body=f"{STOCK}: {change_symbol}{percentage_change}%\nHeadline: {title}\nbrief: {articles}",
                from_=MY_NUMBER,
                to=YOUR_NUMBER_HERE
            )



print(message.status)
