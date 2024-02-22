import logging
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains

from utilits import log_print

download_directory = "/home/user/Autorun/SBIS_contacts"
options = ChromeOptions()
options.add_argument('--allow-profiles-outside-user-dir')
options.add_argument('--enable-profile-shortcut-manager')
options.add_argument('--profile-directory=Profile 3')
options.add_argument(r'user-data-dir=.\User')
options.add_argument("--headless")  # Выполнение в фоновом режиме без открытия браузера
options.add_argument("--window-size=600,2000")
driver = Chrome(options=options)
driver.implicitly_wait(5)

version = driver.capabilities['browserVersion']
driver_version = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
logging.debug(f"Chrome Version: {version}")
logging.debug(f"ChromeDriver Version: {driver_version}")

SBIS_LOGIN = 'leartest'
SBIS_PASSWORD = 'Leartest2007!'

input_today_name = "ws-input_" + datetime.now().strftime('%Y-%m-%d')


@log_print
def move_and_click(element):
    target = ActionChains(driver).move_to_element(element)
    time.sleep(0.2)
    target.click().perform()
    return True


def xpath_find(xpath: str):
    return driver.find_element(By.XPATH, xpath)


def xpath_finds(xpath: str):
    return driver.find_elements(By.XPATH, xpath)


def find_and_click(xpath: str):
    return move_and_click(xpath_find(xpath))


def force_click(xpath: str):
    driver.execute_script("arguments[0].click();", xpath_find(xpath))


def scroll_down():
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight + 500)")


@log_print
def sbis_login(login, password):
    time.sleep(2)
    login_box = driver.find_element(By.NAME, input_today_name)
    login_box.send_keys(login)

    submit_button_xpath = "//span[@class='controls-BaseButton controls-Button_filled controls-Button_radius-filled controls-Button_hoverIcon controls-Button_clickable controls-Button_filled_style-primary controls-Button_bg-contrast controls-Button_circle_height-4xl controls-fontsize-m controls-Button_button__wrapper-fontsize-m controls-Button_filled_shadow-big controls-notFocusOnEnter auth-AdaptiveLoginForm__loginButton controls-margin_left-m ws-flex-shrink-0 controls-inlineheight-4xl controls-Button-inlineheight-4xl controls-Button_filled_4xl']"
    submit_button = xpath_find(submit_button_xpath)
    move_and_click(submit_button)
    time.sleep(1)

    password_box = driver.find_elements(By.NAME, input_today_name)[1]
    move_and_click(password_box)
    password_box.send_keys(password)

    submit_button = xpath_find(submit_button_xpath)  # ДА, ТАК НАДО
    move_and_click(submit_button)
    time.sleep(5)

    if input_field := driver.find_element(By.NAME, input_today_name):
        code = input("Authorization required. Type SBIS code\n>>")
        input_field.send_keys(code)

    return True


@log_print
def billing_reclaim():
    try:  # Если при загрузке найден элемент со страницы авторизации, выполняет скрипт авторизации
        driver.get(r'https://reg.tensor.ru/#ws-nc=Tabs=list;Menu=Clients;Клиенты=%7B"NavigationPosition":"Clients#list","application_type":"all","ФильтрТипКлиенты":"notLiquidated","WhoInvited":null,"ФильтрРазделСтатистики":null,"ПериодСтатистики":null,"phone":"all","FaceType":"ORG","Product":null,"Владелец":null,"ДатаКнц":"2024-02-13","ДатаНач":"2023-02-13","Категория":"все","КатегорияРаспределения":null,"Период":"4","Регион":"58","Тип":null,"pageNum":0,"pageCount":20,"usePages":"parts"%7D')
        if len(xpath_finds("//div[@class='auth-AuthTemplate__browserWarning']")) > 0:
            sbis_login(SBIS_LOGIN, SBIS_PASSWORD)
            driver.get(r'https://reg.tensor.ru/#ws-nc=Tabs=list;Menu=Clients;Клиенты=%7B"NavigationPosition":"Clients#list","application_type":"all","ФильтрТипКлиенты":"notLiquidated","WhoInvited":null,"ФильтрРазделСтатистики":null,"ПериодСтатистики":null,"phone":"all","FaceType":"ORG","Product":null,"Владелец":null,"ДатаКнц":"2024-02-13","ДатаНач":"2023-02-13","Категория":"все","КатегорияРаспределения":null,"Период":"4","Регион":"58","Тип":null,"pageNum":0,"pageCount":20,"usePages":"parts"%7D')

        page_capacity_button = "//select[@class='ws-native-select']"
        button_1000 = "//div[@title='1000']"
        arrow_button = "//span[@title='Перейти к последней странице']"
        choose_all_checkbox = "//td[@class='ws-browser-checkbox-holder']"
        reclaim_button = '//div[@title="Закрепить за другим"]'
        list_of_reasons = "//div[@sbisname='ИдПричиныЗакрепления']"
        reason = "//div[contains(text(), 'Первоначальное закрепление')]"
        employee = "//div[@title='Руководитель']"

        force_click(page_capacity_button)
        force_click(button_1000)
        time.sleep(15)
        scroll_down()
        find_and_click(arrow_button)
        time.sleep(60)
        find_and_click(choose_all_checkbox)
        force_click(reclaim_button)
        find_and_click(list_of_reasons)
        find_and_click(reason)
        find_and_click(employee)
        time.sleep(2)
        return True

    except Exception as e:
        logging.info(e)
        if '--headless' in options.arguments:
            return None
        time.sleep(36000)
        return False

    finally:
        driver.quit()


if __name__ == '__main__':
    billing_reclaim()
