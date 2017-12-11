import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def find_by_xpath(locator):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, locator))
    )
    return element

chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.get("http://www.supremenewyork.com/shop/all")
articals = []
articles = driver.find_elements_by_class_name("inner-article");
for article in articles:
    innerhtml = article.get_attribute('innerHTML')
    if not 'sold out' in innerhtml:
        print innerhtml
        article.click()
        add_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, './/fieldset[.//input[@value="add to cart"]]'))
        )
        #all_buttons = []
        #all_buttons = driver.find_element_by_xpath('//*[@id="add-remove-buttons"]/input')
        #add_button = driver.find_element_by_css_selector(".button")
        #add_button = driver.find_element_by_xpath('.//fieldset[.//input[@value="add to cart"]]')
        #add_button = driver.find_element_by_xpath('//*[@id="add-remove-buttons"]/input')
        add_html = add_button.get_attribute('innerHTML')
        print add_html
        if 'add' in add_html:
            #add_button.click()
            add_button.submit()
            time.sleep(3)
            checkout_button = driver.find_element_by_xpath('//*[@id="cart"]/a[2]')
            checkout_html = checkout_button.get_attribute('innerHTML')
            checkout_button.click()
            #all_buttons = driver.find_elements_by_class_name("button checkout");
            #for button in all_buttons:
            #    button_html = button.get_attribute('innerHTML')
            #    print button_html
            #    if 'checkout' in button_html:
            #        checkout_button.click()
            cart_cc = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="cart-cc"]'))
            )

            cart_cc_html = cart_cc.get_attribute('innerHTML')
            #print cart_addr_html
            find_by_xpath('//*[@id="order_billing_name"]').send_keys('K Handsome')
            find_by_xpath('//*[@id="order_email"]').send_keys('handsomek@kk.com')
            find_by_xpath('//*[@id="order_tel"]').send_keys('2040010029')
            find_by_xpath('//*[@id="bo"]').send_keys('520')
            find_by_xpath('//*[@id="oba3"]').send_keys('101')
            find_by_xpath('//*[@id="order_billing_zip"]').send_keys('55414')
            find_by_xpath('//*[@id="order_billing_city"]').send_keys('Minneapolis')
            find_by_xpath('//*[@id="order_billing_state"]').send_keys('MN')
            find_by_xpath('//*[@id="order_billing_country"]').send_keys('USA')
            find_by_xpath('//*[@id="nnaerb"]').send_keys('1111222233334444')
            find_by_xpath('//*[@id="credit_card_month"]').send_keys('12')
            find_by_xpath('//*[@id="credit_card_year"]').send_keys('2017')
            find_by_xpath('//*[@id="rmae"]').send_keys('999')
            find_by_xpath('//*[@id="order_terms"]').click()
        break
driver.quit()
