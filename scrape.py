import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import pandas as pd
from requests.exceptions import HTTPError
import sys
import math

#calculating the total number of pages in the floorsheet
url = "http://www.nepalstock.com/"
request = requests.get(url)
soup = BeautifulSoup(request.text, 'lxml')
total_transactions = soup.find(text="Total Transactions")
total_transactions = total_transactions.parent.parent.next_sibling.next_sibling.text
total_transactions = total_transactions.replace(",", "")
total_iteration = math.ceil(int(total_transactions)/500)
print(f"total iterations = {total_iteration}")

table_list = list()
subgroup = "floorsheet"
r_list = list()
mistake_count = 0
print("index")

for index in range(1,total_iteration+1):

    url = f"""http://www.nepalstock.com/main/floorsheet/index/
    {index}/?contract-no=&stock-symbol=&buyer=&seller=&_limit=500/"""
    while True:
        try:
            r = requests.get(url)
            print(f"{index}", end = "\r")
            sys.stdout.flush()
            if r.status_code == 200 :  
                break

        except requests.exceptions.RequestException as e:  
            mistake_count += 1
            if mistake_count > 3:
                print(e)
                sys.exit()
                continue

    r_list.append(r)

    for r in r_list:
        soup = BeautifulSoup(r.text, "lxml")
        table = soup.find("table", class_="table my-table").contents
        table = list(filter(lambda a : a!='\n', table)) #removing the newlines
        
        for row in table[2:-3]:
            datas = row.find_all("td")
            row = [x.text for x in datas]
            row[5:] = [float(x) for x in row[5:]] #converting quantity rate and amount to float
            table_list.append(row)

columns = ['S.N.', 'Contract No','Stock Symbol', 'Buyer Broker',
           'Seller Broker', 'Quantity', 'Rate', 'Amount']
df = pd.DataFrame(table_list, columns=columns)

date = datetime.now()
df.to_csv(f"datas/floorsheet_{date.date()}_{date.weekday()}.csv")

