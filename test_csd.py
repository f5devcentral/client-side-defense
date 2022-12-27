"""This python script is used to test a simple web site login in python 3.x using selenium. 
Update APIToken, protected_domain, tenant_name and LB URL in the below code."""


import json
import time
import requests
from requests.structures import CaseInsensitiveDict
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# user input params
tenant_name = "treino"
protected_domain = "f5-hyd-demo.com"
api_token = "sample"
site_url = "https://automation-csd.f5-hyd-demo.com"

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# headers section
token = api_token
headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Authorization"] = "APIToken " + token
        

def get_transactions_count(tenant, starttime, endtime, headers):
    """Get transaction details in CSD dashboard."""
    url = "https://{0}.console.ves.volterra.io/api/shape/csd/namespaces/system/detected_domains?" \
          "start_time={1}&end_time={2}".format(tenant, starttime, endtime)
    req = requests.get(url, headers=headers)
    return req.json()["customer"]["transactionCount"]


def get_formfields(tenant, starttime, endtime, headers):
    """Get Form field details in CSD dashboard."""
    url = "https://{0}.console.ves.volterra.io/api/shape/csd/namespaces/system/formFields?" \
          "start_time={1}&end_time={2}".format(tenant, starttime, endtime)
    req = requests.get(url, headers=headers)
    return req.json()['form_fields']


def get_scriptlist(tenant, starttime, endtime, headers):
    """Get 3rd party script details in CSD dashboard."""
    url = "https://{0}.console.ves.volterra.io/api/shape/csd/namespaces/system/scripts?" \
          "start_time={1}&end_time={2}".format(tenant, starttime, endtime)
    req = requests.get(url, headers=headers)
    return req.json()['scripts']


def test_csd_flow(target, count, headless=True):
    """Lib to send website traffic using Chrome browser and validate requests."""
    # wait 2 mins for DNS before sending traffic
    print("================ Waiting 2 mins before sending traffic. ==================")
    time.sleep(120)

    endtime1 = int(time.time())
    starttime1 = endtime1 - 900
    
    # get last transaction details before sending traffic
    count_before = get_transactions_count(tenant_name, starttime1, endtime1, headers)
    
    # start sending traffic using selenium
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # send requests as per provided count
    for num in range(count):
        print("================ Opening Website:{0} - {1}th time for login. ==================".format(site_url, num))
        driver.get(target)

        print("================ Providing inputs for login. ==================")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[text()='Open Login']"))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "username"))).send_keys("abc")
        driver.find_element("id", 'password').send_keys("abc")
        driver.find_element("xpath", value="//button[text()='Login']").click()
        print("================ Unable to login, so check your credentials. ==================")
        time.sleep(2)

    driver.close()
    transactions_found = False
    
    # check every 2 mins for new transactions 10 times
    for iter_num in range(20):
        time.sleep(120)
        endtime2 = int(time.time())
        starttime2 = endtime1 - 1800

        # get last transaction details after traffic
        count_after = get_transactions_count(tenant_name, starttime2, endtime2, headers)

        # validate transaction field count is increased
        if count_after > count_before:
            print("================ Transactions before - {0} ==================".format(count_before))
            print("================ Transactions after sending CSD traffic - {0} ==================".format(count_after))

            transactions_found = True
            # validate form fields
            form_json = get_formfields(tenant_name, starttime1, endtime2, headers)
            print("================ Found below form_fields ==============")
            print(form_json)

            # validate script fields
            script_json = get_scriptlist(tenant_name, starttime1, endtime2, headers)
            print("================ Found below script fields ==============")
            print(script_json)
            break
    
    # validate if new CSD requests are detected
    assert transactions_found

# call the above lib with params
test_csd_flow(site_url, count=5)
