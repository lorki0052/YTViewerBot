from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from threading import Thread
import time
import os
import socket
import random
import sys
from termcolor import colored
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from progress.bar import Bar
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent


number_of_viewers = 0

def create_viewer(site_url, time_view, proxy_port, show_browser):
    global number_of_viewers
    # To use Tor's SOCKS proxy server with chrome, include the socks protocol in the scheme with the --proxy-server option
    # PROXY = "socks5://127.0.0.1:9150" # IP:PORT or HOST:PORT

    torexe = os.popen(r'C:\Users\Amaimon\Desktop\Tor Browser\Browser\TorBrowser\Tor\tor.exe')
    PROXY = "socks5://localhost:" + proxy_port # IP:PORT or HOST:PORT
    
    options = Options()
    #options.headless = True
    options.add_argument("--incognito")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--mute-audio")
    options.add_argument('--blink-settings=imagesEnabled=false')

    if "n" in show_browser:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        
    options.add_argument('window-size=1920x1080')
    ua = UserAgent()
    options.add_argument('--user-agent='+ua.random)
  
    #LOG-LEVEL
    # INFO = 0, 
    # WARNING = 1, 
    # LOG_ERROR = 2, 
    # LOG_FATAL = 3.

    options.add_argument("--log-level=3")
    options.add_argument('--proxy-server=%s' % PROXY)

    driver = webdriver.Chrome(chrome_options=options, executable_path=r'chromedriver.exe')
    driver.get(site_url + "?autoplay=1")

    #Если открылся и вопсроизвелся ютуб - return number_of_view (1)
    #driver.refresh()
    driver.implicitly_wait(20)
    if(len(driver.find_elements_by_xpath("//*[@id=\"movie_player\"]"))>0):
        #автовопросизведение ролика
        driver.refresh()
        driver.find_element_by_xpath("//*[@id=\"movie_player\"]").click()
        number_of_viewers+=1

    time.sleep(int(time_view))
    #ОТКЛЮЧИТЬ НА РЕЛИЗЕ
    #driver.save_screenshot(str(random.random())+".png")

    driver.close()
    driver.quit()

def renew_tor_identity():
    try:
        s = socket.socket()
        s.connect(('localhost', 9051))
        s.send('AUTHENTICATE "my_password"\r\n'.encode())
        resp = s.recv(1024)

        if resp.startswith(b'250'):
            s.send("signal NEWNYM\r\n".encode())
            resp = s.recv(1024)

            if resp.startswith(b'250'):
                print (colored("IP-адреса сменились успешно", "green"))
            else:
                print ("response 2:", resp)

        else:
            print ("response 1:", resp)

    except Exception as e:
        print (colored("Невозможно сменить IP-адреса: ", e ) , "red")

def progress_bar_info(time_view):
    bar = Bar(colored('Идет просмотр(с):', "green"), max=int(time_view))
    for i in range(int(time_view)):
        time.sleep(1)
        bar.next()
    bar.finish()

def main():
    print('''
 ----------------------------------------
     __     __      __      __         
 \ \   / /      \ \    / /         
  \ \_/ /__  _   \ \  / /   _  ___ 
   \   / _ \| | | \ \/ / | | |/ _ \;
    | | (_) | |_| |\  /| |_| |  __/
    |_|\___/ \__,_| \/  \__,_|\___|

 ----------------------------------------                                                          
    ''')
    #number_of_viewers = 0
    print(colored("Запусти отдельно tor-браузер!\n", "yellow"))
    site_url = input("Введите Youtube - URL (https://youtu.be/ID_VIDEO):\n")
    time_view = input("Укажите время просмотра в секундах:\n")
    show_browser = input("Отображать окна браузера?(y/n):\n")

    while True:
        viewer = Thread(target=create_viewer, args=(site_url, time_view, "9052", show_browser,))
        viewer1 = Thread(target=create_viewer, args=(site_url, time_view, "9053", show_browser,))
        viewer2 = Thread(target=create_viewer, args=(site_url, time_view,"9054", show_browser,))
        viewer3 = Thread(target=create_viewer, args=(site_url, time_view, "9055", show_browser,))

        info = Thread(target=progress_bar_info, args=(time_view,))

        viewer.start()
        time.sleep(2)

        viewer1.start()
        time.sleep(2)

        viewer2.start()
        time.sleep(2)

        viewer3.start()
        time.sleep(2)

        info.start()

        viewer.join()
        viewer1.join()
        viewer2.join()
        viewer3.join()

        info.join()

        print (colored("Количество просмотров: " + str(number_of_viewers), "green"))
        renew_tor_identity()
        time.sleep(20)

if __name__== "__main__":
  main()