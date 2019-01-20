'''Script para ajudar os amigos a alcançarem suas metas de comentários'''

from time import sleep
from typing import Any
from argparse import ArgumentParser
from traceback import format_exc
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement


def get_args() -> dict:
    parser = ArgumentParser(
        description='Script para ajudar a alcançar a meta dos amigos!')

    parser.add_argument('url',
                        help='URL da publicação.')
    parser.add_argument('-u',
                        dest='email',
                        help='Email da sua conta.',
                        required=True)
    parser.add_argument('-p',
                        dest='password',
                        help='Senha da sua conta.',
                        required=True)
    parser.add_argument('-v',
                        dest='verbose',
                        action='store_true',
                        help='Habilita o modo verboso.')

    return vars(parser.parse_args())


def get_driver() -> Chrome:
    prefs = prefs = {'profile.default_content_setting_values.notifications': 2}

    chrome_options = ChromeOptions()
    chrome_options.add_experimental_option('prefs', prefs)

    driver = Chrome(options=chrome_options)
    driver.maximize_window()

    return driver


def login(driver: Chrome, email: str, password: str):
    driver.get('https://www.facebook.com')

    email_field = driver.find_element_by_id('email')
    passwd_field = driver.find_element_by_id('pass')
    login_btn = driver.find_element_by_id('u_0_2')

    email_field.send_keys(email)
    passwd_field.send_keys(password)

    login_btn.submit()


def get_comment_input(driver: Chrome) -> WebElement:
    comment_css = '[contenteditable=true]'
    driver.execute_script(f'document.querySelector("{comment_css}").focus()')

    return driver.find_element_by_css_selector(comment_css)


def send_comment(comment_input: WebElement, content: Any):
    comment_input.send_keys(str(content))
    comment_input.send_keys(Keys.ENTER)
    sleep(15)


def is_blocked(driver: Chrome) -> bool:
    selector = '[role=dialog] [data-tooltip-display=overflow]'
    return len(driver.find_elements_by_css_selector(selector)) != 0


if __name__ == "__main__":
    args = get_args()
    goal = int(input('Digite a meta do parça: '))

    driver = get_driver()
    login(driver, args['email'], args['password'])
    driver.get(args['url'])
    try:
        comment_input = get_comment_input(driver)

        for count in range(0, goal):
            if is_blocked(driver):
                print('Você está bloqueado temporariamente!')
                break

            send_comment(comment_input, count)

            if count > 0 and count % 20 == 0:
                sleep(5 * 60)
    except Exception:
        print('Ops! Algo deu errado, tente novamente!')

        if args.get('verbose'):
            print(format_exc())
    finally:
        driver.close()
