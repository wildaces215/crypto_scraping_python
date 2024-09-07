from datetime import datetime
from bs4 import *
import schedule
import requests
import time
import csv
import os




def get_crypto_prices():
    url = "https://crypto.com/price"
    response = requests.get(url,headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.content,'html.parser')

    rows = soup.find('tbody').find_all('tr')[:50]
    data = []
    for row in rows:
        name = row.find('p',class_="css-rkws3").text
        ticker = row.find('span',class_='css-1jj7b1a').text
        price = row.find('p',class_="css-5a8n3t").text
        data.append([name,ticker,price])
    return data

def save_to_csv(data):
    output_dir = os.path.join("csv", "output")
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"crypto_prices_{timestamp}.csv"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Symbol', 'Price'])  # Write header
        writer.writerows(data)
    print(f"Data saved to {filepath}")


def run_cron_job_functions():
    data = get_crypto_prices()
    save_to_csv(data)

schedule.every(2).minutes.do(run_cron_job_functions)
while True:
    schedule.run_pending()
    time.sleep(1)
