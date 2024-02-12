import asyncio
import aiohttp
import sys
from datetime import datetime, timedelta
import time  # Імпортуємо модуль для роботи з часом

API_URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date="

async def fetch_currency_rate(session, date):
    date_str = date.strftime('%d.%m.%Y')
    async with session.get(API_URL + date_str) as response:
        if response.status != 200:
            response.raise_for_status()
        data = await response.json()
        rates = {'EUR': None, 'USD': None}
        for rate in data['exchangeRate']:
            if rate.get('currency') in rates:
                rates[rate['currency']] = {'sale': rate.get('saleRate'), 'purchase': rate.get('purchaseRate')}
        return {date_str: rates}

async def fetch_currency_rates(days):
    dates = [datetime.now() - timedelta(days=x) for x in range(days)]
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_currency_rate(session, date) for date in dates]
        start_time = time.time()  # Початок виміру часу
        results = await asyncio.gather(*tasks)
        end_time = time.time()  # Кінець виміру часу
        print(f"Time taken: {end_time - start_time} seconds")  # Вивід часу виконання
        return results

def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("Usage: main.py <days>")
        return

    days = int(sys.argv[1])
    if days < 1 or days > 10:
        print("Error: The number of days should be between 1 and 10.")
        return

    try:
        rates = asyncio.run(fetch_currency_rates(days))
        print(rates)
    except Exception as e:
        print(f"Failed to fetch currency rates: {e}")

if __name__ == "__main__":
    main()
