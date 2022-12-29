### SCRAPING PROFILE FROM LINKEDIN WEBSITE ####
### Author: Phuoc Nguyen ####
### Date: 26/09/2022 ###
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import app_2
from time import sleep
from bs4 import BeautifulSoup
import csv
import os.path
import shutil
from selenium.webdriver.common.action_chains import ActionChains

# Init Webdriver
driver = webdriver.Chrome()
URL = "https://www.linkedin.com/login"
driver.get(URL)
print('Finish init web driver')
sleep(1)

#Send keys to email field
email_field = driver.find_element_by_id("username")
email_field.send_keys(app_2.username)
print('Finish key in email')
sleep(2)

# Send keys to password field
password_field = driver.find_element_by_id('password')
password_field.send_keys(app_2.password)
print('Finish key in password')
sleep(3)

# Press Login button
login_field = driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button')
login_field.click()
print('Finish loging in')
sleep(30)#waiting security check

# Send keys to search field
search_field = driver.find_element_by_xpath('//*[@id="global-nav-typeahead"]/input')
# search_query = input('What profile do you want to scrap: ')
search_field.send_keys('Data Engineering people')
search_field.send_keys(Keys.RETURN)
print('Finish Searching Key')
sleep(5)

# Def get one URL using BeatifulSoup
def GetURL():
    page_source = BeautifulSoup(driver.page_source)
    profiles = page_source.find_all('a',class_ = 'app-aware-link')
    all_profile_URL = []
    for profile in profiles:
        profile_URL = profile.get('href')
        if profile_URL not in all_profile_URL and profile_URL.find('miniProfile') != -1 :
            all_profile_URL.append(profile_URL)
    return all_profile_URL

# Def get all URL
def getURLsonPage():
    number_of_page = 1# input('What do number page do you want extract: ')
    URL_all_page = []

    for page in range(int(number_of_page)):
        try:
            URLs_one_page = GetURL()
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            sleep(5)
            next_button = driver.find_element_by_class_name('artdeco-pagination__button--next')
            next_button.click()
            URL_all_page = URL_all_page + URLs_one_page
            sleep(2)
        except:
            continue
    return URL_all_page


URLs_all_page = getURLsonPage()
print(URLs_all_page)
import datetime
current_time = str(datetime.datetime.now()).split()
file_name = 'output' + '_' + current_time[0]   + '.csv'
with open(file_name,'w',newline = '',encoding='utf-8') as file_output:
    headers = ['Name','Job Title','Location','URL']
    writer = csv.DictWriter(file_output,delimiter = ',',lineterminator='\n',fieldnames=headers)
    writer.writeheader()
    for linkedin_URL in URLs_all_page:
        try:
            driver.get(linkedin_URL)
            sleep(2)
            page_source = BeautifulSoup(driver.page_source,"html.parser")
            info_div = page_source.find('div',class_="mt2 relative")

            name = info_div.find('h1').get_text().strip()
            print(' - Profile name is: ',name)

            title = info_div.find('div',class_ = "text-body-medium break-words").get_text().strip()
            print(' - Profile title is: ', title)

            location = info_div.find('div',class_ = "pv-text-details__left-panel pb2" ).find('span',class_="text-body-small inline t-black--light break-words").get_text().strip()
            print(' - Profile location is: ', location)
            print('\n')
            sleep(3)

            writer.writerow({headers[0]: name, headers[1]: title, headers[2]: location, headers[3]: linkedin_URL})
        except:
            print('write to csv file error')
            continue

        ### Download pdf profile

        # driver.get(linkedin_URL)
        try:
            sleep(5)
            more_button = driver.find_element_by_xpath("//div[@class='pvs-profile-actions ']/div[button/@aria-label='More actions']")
            driver.implicitly_wait(10)
            ActionChains(driver).move_to_element(more_button).click(more_button).perform()
            sleep(5)
            print('click More Button')
            save_to_pdf = driver.find_element_by_xpath("//div[@class='pvs-profile-actions ']/div[button/@aria-label='More actions']/div/div/ul/li[3]/div[span[text()='Save to PDF']]")
            driver.implicitly_wait(10)
            ActionChains(driver).move_to_element(save_to_pdf).click(save_to_pdf).perform()
            sleep(10)
            print('click SAVE button')
            dl_path = 'C:/Users/DONGPHO/Downloads/Profile.pdf'
            target_path = 'D:/Python_Porforio/Linkedin_Scrap/pdf_profile/'+ name +'.pdf'
            if os.path.exists(dl_path):
                shutil.move(dl_path, target_path)
            else:
                print('Do not pdf of profile: ' ,name)
        except:
            print('download pdf file error: ',name)
            break







