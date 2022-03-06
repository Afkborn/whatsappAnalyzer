#logging
import logging
from time import sleep, time

#Compatibility
from Python import Compatibility as C

#Module
from Python.Model.WhatsappMessage import WhatsappMessage
from Python.Model.Person import Person
#Selenium
from selenium.webdriver import Chrome,ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException

#genel 
from os import getcwd, path
from datetime import datetime

#XPATH
from Python import XPATH as XP

class Whatsapp:
    def __init__(self, debugEnable=False, profileName = "profile1"):
        self.WPURL = "https://web.whatsapp.com/"
        self.personObj = []
        self.debugEnable = debugEnable
        self.set_logging()

        if not C.check_compatibility():
            print("Not compatible with this PC, detail in log file")
            exit()

        self.chromeDriverPath = getcwd() + fr"\{C.get_chrome_driver_loc()}"
        
        #start selenium
        

        self.options = ChromeOptions()   
        self.__profileName = profileName
        self.__profileLoc = getcwd() + fr"/Profile/{self.__profileName}"     
        self.options.add_argument(f"user-data-dir={self.__profileLoc}")
        self.options.add_argument("--lang=tr")
        self.options.add_argument("--log-level=3")
        self.options.headless = not debugEnable

        self.__startBrowser()

        self.login()
        


    def get_time_log_config(self):
        return datetime.now().strftime("%H_%M_%S_%d_%m_%Y")

    def set_logging(self):
        if self.debugEnable:
            logging.basicConfig(filename=fr'Log/log_{self.get_time_log_config()}.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
            logging.info("Logging is set")

    def __startBrowser(self):
        self.browser = Chrome(executable_path=self.chromeDriverPath,options=self.options)

        self.browser.set_window_position(0,0)
        #WEB 1008X635 PX
        self.browser.set_window_size(1024,768)
        logging.info("Browser is started, size is setted, position is setted, options are setted. (Chrome,0,0,1024,768)")


    def login(self):
        self.getPage(self.WPURL)
        while True:
            try:
                if self.browser.find_element_by_xpath(XP.login_control_xpath).text == XP.login_control_message:
                    logging.info("Login success")
                    return True
            except NoSuchElementException as e:
                logging.error("No Such Element Exception")
            sleep(0.5)

        

    def getPage(self,URL : str):
        if self.browser.current_url == URL:
            pass
        else:
            self.browser.get(URL)
            logging.info("Page is opened")

    def scroolPaneSide(self,y):
        script = f"""myElement = document.getElementById('pane-side')
        myElement.scrollBy(0,{y})"""
        if  self.browser.current_url == self.WPURL:
            self.browser.execute_script(script)

    def getMaxScroolPaneSide(self):
        script = f"""myElement = document.getElementById('pane-side')
        return myElement.scrollHeight"""
        if  self.browser.current_url == self.WPURL:
            maxScroolPaneSide = self.browser.execute_script(script)
            logging.info(f"Max scrool pane side is {maxScroolPaneSide}")
            return maxScroolPaneSide

    def getPersonObjList(self):
        """Person objelerini döner"""
        return self.personObj

    def getPersonWithName(self,name) -> Person:
        """Adı verilen kullanıcının person objesini döner"""
        for i in self.personObj:
            iName = i.getName()
            if iName == name:
                return i

        
    def checkName(self,name):
        """name değişkenin self.personObj içinde olup olmadığını kontrol eder eğer var ise True, yok ise False döner."""
        for i in self.personObj:
            iName = i.getName()
            if iName == name:
                return True
        return False

    def scroolNewChatPartPaneSide(self,y):
        """Yeni sohbet oluştur panelinde scrool yapmaya yarayan fonksiyon. Y ne kadar scrool yapılacağını belirtir."""
        script = f"""
        function getElementByXpath(path){{
            return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        }}
        myObj1 = getElementByXpath('//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[2]')
        myObj1.scrollBy(0,{y})
        """
        if self.browser.current_url == self.WPURL:
            self.browser.execute_script(script)

    def getMaxScroolNewChatPartPaneSide(self):
        script = f"""
        function getElementByXpath(path){{
            return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        }}
        myObj1 = getElementByXpath('//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[2]')
        return myObj1.scrollHeight"""
        if  self.browser.current_url == self.WPURL:
            maxScroolNewChatPartPaneSide = self.browser.execute_script(script)
            logging.info(f"Max scrool new chat part pane side is {maxScroolNewChatPartPaneSide}")
            return maxScroolNewChatPartPaneSide

    def clickNewChatButton(self):
        """Yeni sohbet oluştur butonuna tıklar"""
        script = f"""var myObj = document.querySelector('[title="Yeni sohbet"]');
        myObj.click()"""
        if  self.browser.current_url == self.WPURL:
            self.browser.execute_script(script)
            sleep(0.1)
    

    def getPersonFromNewChatPart(self):
        """Yeni sohbet ekranından kişileri çekmeye yarayan fonksiyon. """
        logging.info("Getting person from new chat part started")
        self.clickNewChatButton()
        sleep(0.5)
        nameSet = set()
        maxScroll = int(self.getMaxScroolNewChatPartPaneSide())
        for _ in range(int(maxScroll / 100)+1):
            for i in range(17):
                try:
                    #//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[2]/div[2]/div/div/div[7]/div/div/div[2]/div[1]/div/span
                    name = self.browser.find_element_by_xpath(f'//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[2]/div[2]/div/div/div[{i}]/div/div/div[2]/div[1]/div/span').text
                    nameSet.add(name)
                except:
                    pass
            self.scroolNewChatPartPaneSide(400)
        logging.info("Getting person from new chat part scroll ended")
        nameList = list(nameSet)
        count = 0
        for i in nameList:
            if not self.checkName(i):
                myPerson = Person(i,0,1)
                self.personObj.append(myPerson)
                count += 1
        logging.info("Getting person from new chat part ended")
        logging.info(f"{count} person added")


    def getPersonFromLastConversations(self):
        """Son sohbetler ekranından kişileri çekmeye yarayan fonksiyon. """
        logging.info("Getting person from last conversations started")
        nameSet = set()
        maxScrool = int(self.getMaxScroolPaneSide())
        for _ in range(int(maxScrool / 100)+1):

            for i in range(1,17):
                try:
                    try:
                        #//*[@id="pane-side"]/div[1]/div/div/div[11]/div/div[1]/div[2]/div[1]/div[1]/span
                        name = self.browser.find_element_by_xpath(f'//*[@id="pane-side"]/div[1]/div/div/div[{i}]/div/div[1]/div[2]/div[1]/div[1]/span').text

                        #//*[@id="pane-side"]/div[1]/div/div/div[11]/div/div/div[1]/div/div/div/span                        
                        gp = self.browser.find_element_by_xpath(f'//*[@id="pane-side"]/div[1]/div/div/div[{i}]/div/div/div[1]/div/div/div/span').get_attribute('data-testid')
                    except:
                        pass
                    if gp == "default-group":
                        name = f"{name},GROUP"
                    elif gp == "default-user":
                        name = f"{name},PERSON"

                    if not ",PERSON,PERSON" in name:
                        nameSet.add(name)
                        print(name)
                except:
                    pass
            self.scroolPaneSide(100)
        logging.info("Getting person from last conversations scrool ended")
        count = 0
        for i in nameSet:
            if ",PERSON" in i:
                name = i.replace(',PERSON',"")
                myPerson = Person(name,0,0)
            else:
                name = i.replace(",GROUP","")
                myPerson = Person(name,1,0)
            self.personObj.append(myPerson)
            count += 1
        logging.info("Getting person from last conversations ended")
        logging.info(f"{count} person added")
        
        
