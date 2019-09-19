from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import re
import datetime as dt

# for return flights
def date_range(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + dt.timedelta(n)


start_date = dt.date.today() + dt.timedelta(days=1)
end_date = dt.date.today() + dt.timedelta(days=301)
chrome_options = Options()
chrome_options.add_argument("--headless")
for i in date_range(start_date, end_date):
    return_date = i
    driver = Chrome("./chromedriver", chrome_options=chrome_options)
    (driver
     .get("https://www.google.com/flights?hl=en#flt=/m/07dfk./m/0ftkx."
          +return_date.strftime("%Y-%m-%d")+";c:TWD;e:1;sd:1;t:f;tt:o"))
    print('enter homepage for TKO to TPE')
    time.sleep(5)
    (driver
     .find_element_by_xpath('//*[@class="gws-flights-results__dominated-toggle '
                            'flt-subhead2 gws-flights-results__collapsed"]').click())
    print('expand button pushed')
    time.sleep(5)

    print('scraping etd...')
    dep_arr_time = driver.find_elements_by_class_name("gws-flights-results__times")
    dep_etd_list = [return_date.strftime("%Y-%m-%d")
                    + ' ' + v.text.replace(' h ', ':').replace(' m', '').split()[0]
                    for v in dep_arr_time]
    print('ETD=', dep_etd_list)

    print('scraping duration...')
    dur_times = driver.find_elements_by_class_name('gws-flights-results__duration')
    dep_dur_list = [v.text.replace(' h ', ':').replace(' m', '') for v in dur_times]
    print('duration=', dep_dur_list)

    print('scraping eta...')   
    dep_eta_list = [v.text.replace(' h ', ':').replace(' m', '').split()[-1]
                    .replace('+1', '').replace('+2', '') for v in dep_arr_time]
    print('ETA_fin=', dep_eta_list)

    print('scraping departure airline...')
    dep_air = driver.find_elements_by_class_name('gws-flights-results__carriers')
    dep_air_list= [v.text.replace("Separate tickets booked together\n","").split('\n')[0] for v in dep_air]
    for i in range(len(dep_air_list)):
        dep_air_list[i] = re.sub(',.*', '', dep_air_list[i])
        i += 1
    print('departure airline=', dep_air_list)

    print('scraping dept prices...')
    price = driver.find_elements_by_class_name('gws-flights-results__price')
    dep_price_list = [v.text.replace('NT$', '').replace(',', '') for v in price if v.text != '']
    print('price=', dep_price_list)

    print('scraping dept stops...')
    stops = driver.find_elements_by_class_name('gws-flights-results__stops')
    dep_stops_list = [v.text.replace('Non-stop', '0').replace(' stop', '').replace('s', '') for v in stops]
    print('dept stops=', dep_stops_list)

    print('making data frame...')
    data = {'ret_airline': dep_air_list,
            'ret_etd': dep_etd_list,
            'ret_eta': dep_eta_list,
            'ret_duration': dep_dur_list,
            'ret_stops': dep_stops_list,
            'ret_price': dep_price_list}
    print('saving data frame to csv...')
    try:
        df = pd.DataFrame.from_dict(data, orient='index')
        df = df.transpose()
        df.to_csv('E:\DB103RichardC\AItinery\dataHUB\googleFlight\\return\google_flight_ret' + return_date.strftime("%Y-%m-%d") + '.csv', encoding='utf-8-sig', index=False)
    except:
        pass
    finally:
        print(return_date.strftime("%Y-%m-%d")+'csv file done. Mission run time=', time.process_time())
        driver.close()
