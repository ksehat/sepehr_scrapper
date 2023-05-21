import copy
import time
import datetime as dt
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def click_drop_down(driver, element1, xpath):
    try:
        element1.click()
        WebDriverWait(driver, .5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    except:
        click_drop_down(driver, element1, xpath)


def flight_info_one(driver, xpath):
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        result = [x.text for x in driver.find_elements(By.XPATH, xpath)]
    except:
        result = [None]
    return result


def flight_info_scrapper(driver, flight_info):
    root_xpath = []
    capacity = []
    price = []
    dep_time = []
    air_line = []
    flight_no = []
    model = []
    organization = []
    class_type = []
    for i in range(1, len(flight_info) + 1):
        root_xpath = f'(//div)[@class="flight-info"][{i}]'
        capacity.append(
            driver.find_element(By.XPATH, root_xpath + "//div[@class='count iransans-bold-fa-number']").text)
        price.append(driver.find_element(By.XPATH, root_xpath + "//div[@class='price iransans-medium-fa-number']").text)
        dep_time.append(driver.find_element(By.XPATH, root_xpath + "//span[@class='departure-time']").text)
        air_line.append(driver.find_element(By.XPATH, root_xpath + "//span[@class='title']").text)
        flight_no.append(
            driver.find_element(By.XPATH, root_xpath + "//span[@class='number iransans-light-fa-number']").text)
        model.append(driver.find_element(By.XPATH, root_xpath + "//span[@class='airline-name']").text)
        organization.append(
            driver.find_element(By.XPATH, root_xpath + "//div[@class='name iransans-light-fa-number']").text)
        try:
            driver.find_element(By.XPATH, root_xpath + "//img[@class='flag_icon']")
            class_type.append('1')
        except:
            try:
                driver.find_element(By.XPATH, root_xpath + "//img[@class='flag-icon']")
                class_type.append('1')
            except:
                class_type.append('0')

    # capacity = flight_info_one(driver, "//div[@class='count iransans-bold-fa-number']")
    # price = flight_info_one(driver, "//div[@class='price iransans-medium-fa-number']")
    # dep_time = flight_info_one(driver, "//span[@class='departure-time']")
    # air_line = flight_info_one(driver, "//span[@class='title']")
    # flight_no = flight_info_one(driver, "//span[@class='number iransans-light-fa-number']")
    # model = flight_info_one(driver, "//span[@class='airline-name']")
    # organization = flight_info_one(driver, "//div[@class='name iransans-light-fa-number']")
    # class_of_flight = 1 if WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//img[@class="flag-icon"]'))) else 0
    try:
        df = pd.DataFrame({
            'dep_Time': dep_time,
            'airline': air_line,
            'price': price,
            'capacity': capacity,
            'model': model,
            'flightNo': flight_no,
            'organization': organization,
            'class_Type': class_type
        })
    except:
        flight_info(driver)
    return df


def day_by_day_scrawl(driver, data):
    # monitoring_days = data['monitoringDays']
    try:
        monitoring_days = data['monitoringDays']
        df = pd.DataFrame()
        var1 = 1
        day_number_old = None
        action = ActionChains(driver)
        while var1 <= monitoring_days:
            elem1 = driver.find_element(By.XPATH,
                                        f"(//li[@data-analytics='priceCalendarItem'])[{var1}]")
            action.move_to_element(elem1).click().perform()
            time.sleep(2)
            # day_name = driver.find_element(By.XPATH,
            #                                f"//span[@class='text-center iransans-web-fa-number font-size-12 mt-1']").text
            day_number = driver.find_element(By.XPATH,
                                             f"(//span[@class='text-center iransans-web-fa-number font-size-11 month'])[{var1}]").text
            if day_number == day_number_old:
                var1 = var1 - 1 if var1 != 0 else var1
                continue

            num_of_flights = len(driver.find_elements(By.XPATH, f"//div[@class='price iransans-medium-fa-number']"))
            price_list = []
            capacity_list = []
            fly_time_list = []
            title_list = []
            number_list = []
            seller_list = []
            type_list = []
            model_list = []
            if num_of_flights != 0:
                for row_num in range(num_of_flights):
                    price_list.append(driver.find_element(By.XPATH,
                                                          f"(//div[@class='price iransans-medium-fa-number'])[{row_num + 1}]").text)
                    capacity_list.append(driver.find_element(By.XPATH,
                                                             f"(//div[@class='count iransans-bold-fa-number'])[{row_num + 1}]").text.split('نفر')[0])
                    fly_time_list.append(driver.find_element(By.XPATH,
                                                             f"(//span[@class='departure-time iransans-web-fa-number'])[{row_num + 1}]").text)
                    title_list.append(driver.find_element(By.XPATH, f"(//span[@class='title'])[{row_num + 1}]").text)
                    number_list.append(driver.find_element(By.XPATH,
                                                           f"(//span[@class='number iransans-light-fa-number'])[{row_num + 1}]").text)
                    seller_list.append(driver.find_element(By.XPATH,
                                                           f"(//div[@class='name iransans-light-fa-number'])[{row_num + 1}]").text)
                    model_list.append(driver.find_element(By.XPATH,
                                                          f"(//span[@class='airline-name iransans-web-fa-number'])[{row_num + 1}]").text)
                    try:
                        driver.find_element(By.XPATH,
                                            f"/html/body/app-root/app-root/search/div/natayeje-parvaz/div/div/div[2]/carthay-parvazi/span/div[3]/parvaz-charteri/a/div[1]/div/div/div[1]/price/div/div[{row_num + 1}]/img")
                        type_list.append('1')
                    except:
                        type_list.append('0')

            else:
                var1 += 1
                continue

            df_day = pd.DataFrame({
                # 'pkRouteMonitoringResult': pkRouteMonitoringResult * num_of_flights,
                'origin': [data['iataCodeOrigin']] * num_of_flights,
                'destination': [data['iataCodeDestination']] * num_of_flights,
                'scrap_Date': [dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")] * num_of_flights,
                'day': [day_number] * num_of_flights,
                'price': price_list,
                'capacity': capacity_list,
                'dep_Time': fly_time_list,
                'airline': title_list,
                'flightNo': number_list,
                'organization': seller_list,
                'class_Type': type_list,
                'model': model_list
            })

            df = pd.concat([df, df_day])
            var1 += 1
            day_number_old = day_number
        return df
    except:
        print('error occured.')


def sepehr_scrapper(data):
    try:
        url: str = ("https://sepehr360.ir/")
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        # options.add_argument('--headless')
        driver = webdriver.Chrome("C:\Project\Web Scraping/chromedriver", chrome_options=options)
        driver.get(url=url)

        element1 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="firstPageSource"]')))
        click_drop_down(driver, element1, '//*[@id="cdk-overlay-0"]')
        element1.send_keys(data['iataCodeOrigin'], Keys.ARROW_DOWN)
        element1.send_keys(Keys.ENTER)
        element1 = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="firstPageDestination"]')))
        click_drop_down(driver, element1, '//*[@id="mat-autocomplete-1"]')
        element1.send_keys(data['iataCodeDestination'])
        element1.send_keys(Keys.ENTER)

        # Departure date
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,
                                                                    '//*[@id="home-page-search-box"]/form/div[2]/flight-year-calendar/div/div[2]/shamsi-one-way-date-box/div'))).click()
        # Get the list of all available dates in the first page calendar
        list_of_date_elements = driver.find_elements(By.XPATH, '//shamsi-day-calendar//div[@disabled!="true"]')
        # Click the first date available in the calendar
        list_of_date_elements[0].click()
        # Click search button
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="home-page-search-box"]/form/div[3]/button'))).click()
        # Click go to the coleagues website button
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH,
                                        '//*[@id="mainContainer"]/master-container/b2c-oneway-flight-page/header/nav/div/div[2]/top-menu/ul/menu-item[1]/li'))).click()
        # Wait until the calendar is presented
        # WebDriverWait(driver, 20).until(
        #     EC.presence_of_element_located((By.XPATH,
        #                                     '//*[@id="b2b-main-container"]/div/b2b-oneway-flight-search-result-viewer/div[1]/b2b-oneway-flight-calendar-price/div/div[2]')))
        time.sleep(5)
        df = pd.DataFrame()
        df = day_by_day_scrawl(driver, data)
        return df
    except:
        print('There occured an error in the sepehr_scraper.py')
        return None
