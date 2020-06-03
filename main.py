from selenium import webdriver
import time
import random
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

class Crawlsystem(object):
  def __init__(self):
    self.proxy_list = list()

  def get_proxy_list(self):
    path = self.base_dir + "proxies.txt"
    with open(path) as proxy_file:
      self.proxy_list = [row.rstrip('\n') for row in proxy_file]

  def get_random_proxy(self):
    random_idx = random.randint(1, len(self.proxy_list) - 1)
    proxy_ip = self.proxy_list[random_idx]
    return proxy_ip

  def set_driver(self):
    random_proxy_ip = "http://" + self.get_random_proxy()        
    webdriver.DesiredCapabilities.CHROME['proxy'] = {
        "httpProxy":random_proxy_ip,
        "ftpProxy":random_proxy_ip,
        "sslProxy":random_proxy_ip,
        "proxyType":"MANUAL",
    }    
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) ' \
        'Chrome/80.0.3987.132 Safari/537.36'
    chrome_option = webdriver.ChromeOptions()
    chrome_option.add_argument('--no-sandbox')
    chrome_option.add_argument('--disable-dev-shm-usage')
    chrome_option.add_argument('--ignore-certificate-errors')
    chrome_option.add_argument("--disable-blink-features=AutomationControlled")
    chrome_option.add_argument(f'user-agent={user_agent}')
    chrome_option.headless = True
    
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', options = chrome_option)
    return driver

  def main(self):
    driver = self.set_driver()
    driver.get("https://www.marktplaats.nl/c/auto-s/c91.html")
    container = driver.find_elements_by_class_name("l1-category-feed-container")
    btn_div = container.find_elements_by_class_name("show-more-feed-link")
    more_btns = btn_div.find_elements_by_class_name("mp-Button")
    # more_btn = btn_div.find_element_by_xpath(".//span[1]")
    print(more_btns)
    for x in range(len(more_btns)):
      if more_btns[x].is_displayed():
          driver.execute_script("arguments[0].click();", more_btns[x])
          time.sleep(1)

    page_source = driver.page_source
    print(page_source)
