from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import csv
import time


def go_main(driver):
    driver.get("https://www.nseindia.com/")

    # ждем всплывающее окно и закрываем его
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#myModal > div > div > div.modal-header > button')))
    except:
        pass
    driver.find_element(By.CSS_SELECTOR, '#myModal > div > div > div.modal-header > button').click()

# настраиваем драйвер
options = webdriver.ChromeOptions()
proxy_server_url: str | None = None # прокси на усмотрение (формат 0.0.0.0)
if proxy_server_url:
    options.add_argument(f'--proxy-server={proxy_server_url}')
options.add_experimental_option('excludeSwitches', ['enable-logging', "enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(f'user-agent={UserAgent().random}')

driver = webdriver.Chrome(options=options)

go_main(driver)
time.sleep(1)

# определяем пункты меню
market_data = driver.find_element(By.XPATH, '//*[@id="link_2"]')
pre_open_market = driver.find_element(By.XPATH, '//*[@id="main_navbar"]/ul/li[3]/div/div[1]/div/div[1]/ul/li[1]/a')

# совершаем действия над ними
ActionChains(driver).move_to_element(market_data).perform()
ActionChains(driver).click(pre_open_market).perform()
time.sleep(1)

# парсим
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'symbol-word-break')))
names = driver.find_elements(By.CLASS_NAME, 'symbol-word-break')

file = open('data.csv', 'w', newline='')
writer = csv.writer(file, delimiter=';')
for i in range(len(names)):
    writer.writerow([driver.find_element(By.XPATH, f'//*[@id="livePreTable"]/tbody/tr[{i+1}]/td[2]').text,
          driver.find_element(By.XPATH, f'//*[@id="livePreTable"]/tbody/tr[{i+1}]/td[7]').text])
file.close()
time.sleep(1)

# переходим на главную страницу
go_main(driver)
time.sleep(1)

# переключаемся на NIFTY BANK
driver.find_element(By.ID, 'tabList_NIFTYBANK').click()
time.sleep(1)

# скролим и кликаем на view all
view_all = driver.find_element(By.LINK_TEXT, 'View All')
driver.execute_script('arguments[0].scrollIntoView({behavior: "smooth", block: "center", inline: "center"});', view_all)
view_all.click()
time.sleep(1)

# выбираем пункт меню
dropdown = driver.find_element(By.ID, 'equitieStockSelect')
for item in Select(dropdown).options:
    if item.text == 'NIFTY ALPHA 50':
        item.click()
        break
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'symbol-word-break')))
time.sleep(1)

# скролим таблицу перебором всех элементов
table = driver.find_elements(By.CLASS_NAME, 'symbol-word-break')
for item in table:
    driver.execute_script('arguments[0].scrollIntoView({behavior: "smooth"});', item)
time.sleep(1)

driver.close()
