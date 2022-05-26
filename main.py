from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from pymongo import MongoClient
import gspread



browser = webdriver.Chrome('driver/chromedriver.exe')

file = open('config.txt')
lines = file.readlines() #leer config.txt
username = lines[0]
password = lines[1]


browser.get('https://www.linkedin.com/login')

file = open('config.txt')
lines = file.readlines()
username = lines[0]
password = lines[1]
elementID = browser.find_element_by_id('username')
elementID.send_keys(username)

elementID = browser.find_element_by_id('password')
elementID.send_keys(password)

elementID.submit()


time.sleep(3)


c = MongoClient()
db = c.test8

visitingProfileID = 'https://www.linkedin.com/company/13011942/admin/analytics/followers/?anchor=org-view-followers'
browser.get(visitingProfileID)
time.sleep(3)
buttonSeeAll = browser.find_element(By.CLASS_NAME, 'org-view-page-followers-module__modal-button')
buttonSeeAll.click()


linkList = set()
profiles = list()
modal = browser.find_element(By.CLASS_NAME, 'scaffold-finite-scroll')
for a in range(4000):
    browser.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', modal)
    time.sleep(1)
tm1 = browser.find_elements(By.CSS_SELECTOR, "a.ember-view.link-without-hover-visited")
for i in tm1:
    if i.get_attribute('href') not in linkList:
        print('entré')
        db.profiles.insert_one({"link": i.get_attribute('href')})
    linkList.add(i.get_attribute('href'))

    print(len(linkList))
print(linkList)

followers = list()


for i in linkList:
         try:
            browser.get(i)
            time.sleep(0.1)
            browser.get(i)
            time.sleep(0.1)
            name = browser.find_element(By.CSS_SELECTOR, 'h1.top-card-layout__title').get_attribute('innerHTML')
            time.sleep(0.1)
            jobTitle = browser.find_element(By.CLASS_NAME, 'text-body-medium.break-words').get_attribute('innerHTML')
            time.sleep(0.1)
            location = browser.find_element(By.CLASS_NAME,
                                                'text-body-small.inline.t-black--light.break-words').get_attribute(
                    'innerHTML')
            profile = [name, str(jobTitle), location, i]
            time.sleep(0.1)
            followers.append(profile)
            profile_mongo = {
                   "name": name,
                    "job_title": jobTitle,
                    "location": location,
                    "link": i
                }
            db.profiles.insert_one(profile_mongo)
            time.sleep(3)
         except:
             print('not found')
             continue

credentials = {
    "type": "service_account",
    "project_id": "scrapper-linkedin-347215",
    "private_key_id": "de3c91823a5705dd6a30a0b976be9e748e0cf9ef",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC/L7D/NfUZHdfA\n5P+Hve6bZBw45L6Ci1CNlfjYAjxUOqjehHee0e7AXtaOLsaJ0MwfmZxo+iVKPgWD\nxiToNOrVoGfreekNpZyqUNcLoobLfr71VDgRNGkgCVNZSn/+DeHp40mcntrAq76F\nq1nQ/avUwM6/9AVMyQVXeIpaFA5yrYfpRzJnJrrmkK2Tu0ZAVN3tCZSLLnKQZze6\n6Wn7rENYQ5+/UZRy/0GdmOqXdqexP0PcOasUpPbD2rxj5WDX4aW//2L8al8OXT8W\n8+z3lW9X+hvhQ1uikU+uHj74Z/txbkdQHoQpFnVyPj786B9xgbcNnkf3B2LRodUO\nMxxImNOdAgMBAAECggEACTGSadte42vPdbutXAoyoK9SOhwp2x426/ATzNNiskw1\n1al6FR2URRTqbWDrdDIhtr1My7GHvIe5/Sm4mZ/90PMLPEQbBGh73abQiIMyxzNb\nnHGF1rH2Ai/gnbEa8Y0aWYRwBEORUmWP3l6sjYO9URhKeOmTnasnAhtOT+GaBkKj\niK29B6a6gIc4HR5PH4nGZcSZI55gPJn11GjtahhqbCm16wgmZANNR9uF04Z8U4Bs\nv15ME6V59bxlhqhnuIin4jxlWo1RTJD+cR94YaYx84i7uOcqA4l1PkUskALQ1dBc\nOU4SvtcIBUwDsRh7jEUoTx21JPqs8m5GHJFY7ZLMMwKBgQD8vJfGhUZkhRcijWTj\nIYhskziHoEVoJaqTKvlxlkUp/+ggqIFzMDmRmeyMT7xQq1x1yIN7NTtHXS2nKIF+\nozbuEgYEC+cGwLiRU8FCUZo3T0cBKqps9zACYUyHFEZr2/kKptV+kyHUnW1MkOJB\nGv4Y2BAqgk2EwhMGT6slwS5xawKBgQDBp6WoH8tJPbcQa2UxN1a0FClGaWLRZP58\nfDfK/Gzdbkds/tgjMnhAGwCr2h8o7OMRrZm4ThYCKIvBwzbZzaKZ4GVcQ1rdAPpW\nGsWx097m0yc+fAn442Qps8lTEXfM3Ljwp/YfDwx7HQchCipzlGVFkFRhENOK3xXk\nPiYKB+epFwKBgDyZc8Lz/dboWo28XW5ggfeWrT1H3pyEO4wiB8GGiHrzk1MRVEis\nTYFt6NwT2lF1ZSwQsgX+04HfA61K9xHITMl0pOCfgfuKhjbCYFpoepO8fIf5FPgf\npPFNJy5UXDZMfkBhlFtPKBN009pB+x4lPLv0QpwOtkuYxTsEK0NYOKyVAoGBAJ8k\nR0Vng2aX+fXbW9hbMrxgCR9dAaE0jtH8PtloIYrC0p2mvDYIhruftSiE4rB+I4hm\nknncaceyTE+aPlw02hf8SS/OBkCySgcyjx45D+e+xHRb+NH5BFok7iB+rWXESZMz\nZFZXxpjx3Obw9LvwylylZEI0UrO/6rybuiTqJB1XAoGBAI5DwI7Hlbyv9aQAvLL5\nmPsa47rGdhepdvn1eCy62mKzfGEmvPdhRBx0oIkQfUNYAFkivYJmPaAI4Ngy2YlI\nhzCeO+5h8+vg2UKgYhpUCnPMScUT3Ib8x+l7HkFs7/wdae9gOwJ1ngg6g07/h27j\nuqZNZNMYf4++y2zcN6g8U8MW\n-----END PRIVATE KEY-----\n",
    "client_email": "botsito@scrapper-linkedin-347215.iam.gserviceaccount.com",
    "client_id": "101670878597849016125",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/botsito%40scrapper-linkedin-347215.iam.gserviceaccount.com"
}

gc = gspread.service_account_from_dict(credentials)

sh = gc.open("linkedin-followers")
ws = sh.get_worksheet(0)
#ws.update('A2', followers)