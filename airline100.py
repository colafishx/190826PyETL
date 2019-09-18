import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

url = 'https://www.worldairlineawards.com/worlds-top-100-airlines-2019/'
response = requests.get(url)
html = BeautifulSoup(response.text)
print('get url contents')
airline = html.find_all('h4',class_="mb-0 text-responsive-h4")
airlist = [v.text for v in airline]
print('airline=',airlist)
ranking = html.find_all('h6', class_='mb-0 text-responsive-h4 font-weight-regular')
ranklist = [v.text for v in ranking]
print('2019 ranking=',ranklist)
ranking18 = html.find_all('span', class_='font-weight-bold')
rank18 = [v.text for v in ranking18]
print('2018 ranking=',rank18)

data = {'airline':airlist,
        '2019 ranking':ranklist,
        '2018 ranking':rank18}
print(data, sep='n')
try:
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.transpose()
    df.to_csv('air_ranking19.csv', encoding='utf-8-sig', index=False)
except:
    pass
print('mission completed. run time=', time.process_time())