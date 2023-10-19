import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from bs4 import BeautifulSoup
import requests
import time
import csv
data = []
with open('leagues.csv', 'r', encoding='latin-1') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
                data.append(row)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
}

url = item[3]
resp = requests.get(url, headers=headers)
html_content = resp.text
soup = BeautifulSoup(html_content, 'html.parser')
elements = soup.find_all('option')
count = len(elements)

      
file_path = './test.csv'
with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file) 
        for row in final_data:
                writer.writerow(row)