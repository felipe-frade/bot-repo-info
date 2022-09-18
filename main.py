# selenium 3
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sys
from time import sleep, time

import env
import sql

parameters = sys.argv

options = webdriver.ChromeOptions()
options.add_argument("--disable-popup-blocking")
options.add_argument("--headless")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

wait_120 = WebDriverWait(driver, 120)
wait_60 = WebDriverWait(driver, 60)
wait_30 = WebDriverWait(driver, 30)
wait_20 = WebDriverWait(driver, 20)
wait_10 = WebDriverWait(driver, 10)
inicio = time()

def error_env(info = ''):
    print("Falta variáveis de ambiente")
    print(info)
    driver.quit()
    quit()

def log_git():
    if(not hasattr(env, 'USER_GIT') or not hasattr(env, 'PASS_GIT')):
        error_env()
    try:
        driver.find_element(By.ID, 'login_field').send_keys(env.USER_GIT)
        driver.find_element(By.ID, 'password').send_keys(env.PASS_GIT)
        driver.find_element(By.CSS_SELECTOR, '[type="submit"]').click()

        wait_30.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[href="https://github.com/"]')))
    except:
        return False
    return True

def only_number(text):
    return ''.join(re.findall(r'\d', text))

def get_devs(repo):
    driver.get(f"""{repo}/graphs/contributors""")
    wait_30.until(EC.presence_of_element_located((By.CSS_SELECTOR, env.EL_DEVS)))
    DEVS = driver.find_elements(By.CSS_SELECTOR, env.EL_DEVS)
    COMMITS = driver.find_elements(By.CSS_SELECTOR, env.EL_DEVS_COMMITS)
    LINES_ADD = driver.find_elements(By.CSS_SELECTOR, env.EL_DEVS_LINES_ADD)
    LINES_DEL = driver.find_elements(By.CSS_SELECTOR, env.EL_DEVS_LINES_DEL)
    print(DEVS)
    INFOS_DEVS = []
    for index, DEV in enumerate(DEVS):
        INFOS_DEV = {
            "repo": repo,
            "developer":  DEVS[index].get_attribute("href"),
            "commits_link": COMMITS[index].get_attribute("href"),
            "commits": only_number(COMMITS[index].text),
            "lines_add": only_number(LINES_ADD[index].text),
            "lines_del": only_number(LINES_DEL[index].text)
        }
        INFOS_DEVS.append(INFOS_DEV)
        
    return INFOS_DEVS

def main():
    if(not hasattr(env, 'TABLE_INFO')):
        error_env('TABLE_INFO')
        
    repo = ''
    print(parameters)
    if(len(parameters) == 2):
        repo = parameters[1]
    else:
        repo = env.repo
    
    driver.get(repo)
    wait_60.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[href="https://github.com/"]')))
    if(len(driver.find_elements(By.ID, 'login_field')) > 0):
        log_git()
        
    devs = get_devs(repo)
    sql.insert_repo_info_db(repo, devs)
    print(devs)
        
main()

driver.quit()
exit()