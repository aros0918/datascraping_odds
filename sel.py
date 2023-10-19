import sys
import os
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QLabel, QLineEdit, QPushButton, QComboBox
from PyQt5.QtGui import QFont
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import TimeoutException
# from bs4 import BeautifulSoup
# import requests
import time
import csv

def start_selenium():
        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 10)
        driver.get("https://www.oddsportal.com/login") 
        driver.execute_script("return document.readyState")
        try:
                loginname = driver.find_element(By.NAME, "login-username")
                loginname.clear()
                loginname.send_keys(username_entry.text())
        except NoSuchElementException:
                dialog = MyDialog()
                dialog.show()
        
        password = driver.find_element(By.NAME, "login-password")
        password.clear()
        password.send_keys(password_entry.text())
        loginsubmit = driver.find_element(By.NAME, "login-submit")
        loginsubmit.click()
        driver.execute_script("return document.readyState")
        
        league = dropdown_button1.currentText().split(":")[1][1:]
        season = dropdown_button2.currentText()

        for item in data:
                if item[1] == league:
                        if item[3] == season:
                                url = item[4]
        driver.get(url)
        driver.execute_script("return document.readyState")
        time.sleep(1)
        page_urls = [url]
        try:
                pages = driver.find_elements(By.XPATH, "//main/div[2]/div[4]/div[5]/div/a")
                for i in range(len(pages)-2):
                        page_urls.append(url + "#/page/" + str(i+2))
        except NoSuchElementException:
                page_urls = [url]

        apple = []
        matchs_links = []
        for page_url in page_urls:
                driver.get(page_url)
                driver.execute_script("return document.readyState")
                time.sleep(2)
                try:
                        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//main/div[2]/div[4]/div/div/a[not(contains(@class, 'pagination-link'))]")))
                except TimeoutException:
                        dialog = MyDialog()
                        dialog.show()
                scroll_interval = 1
                total_scroll_time = 10
                total_scrolls = int(total_scroll_time/scroll_interval)
                
                for _ in range(total_scrolls):
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                match_links = driver.find_elements(By.XPATH, "//main/div[2]/div[4]/div/div/a[not(contains(@class, 'pagination-link'))]")
                apple.append(len(match_links))
                for match_link in match_links:
                        matchs_links.append(match_link.get_attribute('href'))
                driver.back()
                driver.execute_script("return document.readyState")
        print(apple)
        file_path = "./result/" + league + " " + str(season) + ".csv"
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file) 
                writer.writerow(['Date', 'Bet Type', 'Fixture', 'Home Score', 'Away Score', 'Opening Odds','Closing Odds'])
                hometeam = ""
                homescore = ""
                awayteam = ""
                awayscore = ""
                date = ""

                for j in range(len(matchs_links)):
                        link = matchs_links[j]
                        driver.get(link)
                        driver.execute_script("return document.readyState")
                        time.sleep(5)
                        try:
                                elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//main/div[2]/div[2]/div[2]/div[1]/p[2]")))
                        except TimeoutException:
                                dialog = MyDialog()
                                dialog.show()
                        try:
                                hometeam = driver.find_element(By.XPATH, "//main/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/span").text
                        except NoSuchElementException:
                                hometeam = ""
                        try:
                                homescore = driver.find_element(By.XPATH, "//main/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div").text
                        except NoSuchElementException:
                                homescore = ""
                        try:
                                awayteam = driver.find_element(By.XPATH, "//main/div[2]/div[2]/div[1]/div[3]/div[1]/span").text
                        except NoSuchElementException:
                                awayteam = ""
                        try:
                                awayscore = driver.find_element(By.XPATH, "//main/div[2]/div[2]/div[1]/div[3]/div[2]/div").text
                        except NoSuchElementException:
                                awayscore = ""
                        try:
                                date_real = driver.find_element(By.XPATH, "//main/div[2]/div[2]/div[2]/div[1]/p[2]").text
                                date = date_real.split(" ")[1] + "/" + date_real.split(" ")[0] + "/" + date_real.split(" ")[2][:-1]
                        
                        except NoSuchElementException:
                                date = ""
                        fixture = hometeam + " - " + awayteam
                        
                        bet1_closing = ""
                        betx_closing = ""
                        bet2_closing = ""
                        bet1_opening = ""
                        betx_opening = ""
                        bet2_opening = ""
                        try:
                                elements = driver.find_elements(By.XPATH, "//main/div[2]/div[3]/div/div/div")
                        except NoSuchElementException:
                                dialog = MyDialog()
                                dialog.show()
                        
                        print(len(elements))
                        for i in range(len(elements)):
                                if "Pinnacle" in elements[i].text:
                                        print(elements[i].text)
                                        try:
                                                elements = driver.find_elements(By.XPATH, "//main/div[2]/div[3]/div/div/div") 
                                        except NoSuchElementException:
                                                bet1_closing = "0"
                                                betx_closing = "0"
                                                bet2_closing = "0"
                                                bet1_opening = "0"
                                                betx_opening = "0"
                                                bet2_opening = "0"
                                        try:
                                                scroll = driver.find_element(By.XPATH, "//main/div[2]/div[3]/div/div/div"+"["+str(i+1)+"]"+"/div[2]/div/div/p") 
                                                driver.execute_script("arguments[0].scrollIntoView();", scroll)
                                        except NoSuchElementException:
                                                bet1_closing = "0"
                                                betx_closing = "0"
                                                bet2_closing = "0"
                                                bet1_opening = "0"
                                                betx_opening = "0"
                                                bet2_opening = "0"
                                        try:
                                                bet1_closing = driver.find_element(By.XPATH, "//main/div[2]/div[3]/div/div/div"+"["+str(i+1)+"]"+"/div[2]/div/div/p").text
                                        except NoSuchElementException:
                                                bet1_closing = "0"
                                        try:                                             
                                                betx_closing = driver.find_element(By.XPATH, "//main/div[2]/div[3]/div/div/div"+"["+str(i+1)+"]"+"/div[3]/div/div/p").text
                                        except NoSuchElementException:
                                                betx_closing = "0"
                                        try:
                                                bet2_closing = driver.find_element(By.XPATH, "//main/div[2]/div[3]/div/div/div"+"["+str(i+1)+"]"+"/div[4]/div/div/p").text
                                        except NoSuchElementException:
                                                bet2_closing = "0"
                                        time.sleep(1)
                                        try:
                                                driver.find_element(By.XPATH, "//main/div[2]/div[3]/div/div/div"+"["+str(i+1)+"]"+"/div[2]/div/div/p").click()
                                                try:
                                                        bet1_opening = driver.find_element(By.XPATH, "//main/div[2]/div[3]/div/div/div[2]/div[3]/div[2]/div[2]").text
                                                except NoSuchElementException:
                                                        bet1_opening = driver.find_element(By.XPATH, "//main/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[2]").text
                                        except ElementClickInterceptedException:
                                                bet1_opening = "0"
                                        
                                        time.sleep(1)
                                        try:
                                                driver.find_element(By.XPATH, "//main/div[2]/div[3]/div/div/div"+"["+str(i+2)+"]"+"/div[3]/div/div/p").click()
                                                try:
                                                        betx_opening = driver.find_element(By.XPATH, "//main/div[2]/div[3]/div/div/div[2]/div[3]/div[2]/div[2]").text
                                                except:
                                                        betx_opening = driver.find_element(By.XPATH, "//main/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[2]").text
                                        except ElementClickInterceptedException:
                                                betx_opening = "0"    
                                        
                                        time.sleep(1)
                                        try:
                                                driver.find_element(By.XPATH, "//main/div[2]/div[3]/div/div/div"+"["+str(i+2)+"]"+"/div[4]/div/div/p").click()
                                                try:
                                                        bet2_opening = driver.find_element(By.XPATH, "//main/div[2]/div[3]/div/div/div[2]/div[3]/div[2]/div[2]").text
                                                except NoSuchElementException:
                                                        bet2_opening = driver.find_element(By.XPATH, "//main/div[2]/div[3]/div/div/div[2]/div[2]/div[2]/div[2]").text
                                        except ElementClickInterceptedException:
                                                bet2_opening = "0"
                                        writer.writerow([date, '1', fixture, homescore, awayscore, bet1_opening, bet1_closing])
                                        writer.writerow([date, 'X', fixture, homescore, awayscore, betx_opening, betx_closing])
                                        writer.writerow([date, '2', fixture, homescore, awayscore, bet2_opening, bet2_closing])
        driver.quit()

class MyDialog(QDialog):
       def __init__(self):
           super().__init__()
           self.initUI()

       def initUI(self):
           self.setWindowTitle("Net Error")
           self.setGeometry(100, 100, 300, 200)

           label = QLabel("Your net is too slow!", self)
           label.move(50, 50)
           label.setFont(font)
           button = QPushButton("Close", self)
           button.move(100, 100)
           button.clicked.connect(self.close)        
data = []
league_list = []
with open('main.csv', 'r', encoding='latin-1') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
                data.append(row)
                league_list.append(row[0] + " : " + row[1])

league_set = sorted(set(league_list))

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("FootBall Betting Odds")

font = QFont()
font.setPointSize(15)

username_label = QLabel("Username:", window)
username_label.move(20, 20)
username_label.setFont(font)
username_entry = QLineEdit(window)
username_entry.move(120, 20)
username_entry.setFont(font)

password_label = QLabel("Password:", window)
password_label.move(20, 60)
password_label.setFont(font)
password_entry = QLineEdit(window)
password_entry.setEchoMode(QLineEdit.Password)
password_entry.move(120, 60)
password_entry.setFont(font)

def handle_selection_change(index):
        dropdown_button2.clear()
        selected_league = dropdown_button1.currentText()
        selected_leagues = selected_league.split(":")
        selected_lg = selected_leagues[1]
        for item in data:
                if item[1] == selected_lg[1:]:
                        dropdown_button2.addItem(item[3])

league_label = QLabel("league:", window)
league_label.move(25, 100)
league_label.setFont(font)
dropdown_button1 = QComboBox(window)
dropdown_button1.move(120, 100)
dropdown_button1.setFixedWidth(350) 
dropdown_button1.setFont(font)
for league_item in league_set:
        dropdown_button1.addItem(league_item)
dropdown_button1.currentIndexChanged.connect(handle_selection_change)

season_label = QLabel("season:", window)
season_label.move(25, 140)
season_label.setFont(font)
dropdown_button2 = QComboBox(window)
dropdown_button2.setFixedWidth(350) 
dropdown_button2.move(120, 140)

selected_league = dropdown_button1.currentText()
selected_leagues = selected_league.split(":")
selected_lg = selected_leagues[1]
for item in data:
        if item[1] == selected_lg[1:]:
                dropdown_button2.addItem(item[3])
dropdown_button2.setFont(font)

start_button = QPushButton("Start", window)
start_button.move(120, 180)
start_button.clicked.connect(start_selenium)
start_button.setFont(font)

window.setGeometry(100, 100, 500, 250)
window.show()
sys.exit(app.exec_())




##########################################
# data = []
# with open('leagues.csv', 'r', encoding='latin-1') as file:
#         csv_reader = csv.reader(file)
#         for row in csv_reader:
#                 data.append(row)
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
# }
# final_data = [['nation', 'league', 'count', 'season', 'leaguelink']]
# for item in data:
#         url = item[3]
#         resp = requests.get(url, headers=headers)
#         html_content = resp.text
#         soup = BeautifulSoup(html_content, 'html.parser')
#         elements = soup.find_all('option')
#         count = len(elements)
#         for i in range(len(elements)):
#                 season = elements[i].text[21:-17]
#                 final_data.append([item[0], item[2], count, season, elements[i].get('value')])
# file_path = './final.csv'
# with open(file_path, 'w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file) 
#         for row in final_data:
#                 writer.writerow(row)