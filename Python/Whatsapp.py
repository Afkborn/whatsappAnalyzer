#logging
from ast import expr_context
import logging

from matplotlib.style import use




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
from time import sleep, time
from urllib import request
from os.path import exists
from os import mkdir

#XPATH
from Python import XPATH as XP

#Database
from Python.DatabasePerson import DatabasePerson

class Whatsapp:
    def __init__(self,username , debugEnable=False, profileName = "profile1"):
        self.WPURL = "https://web.whatsapp.com/"
        self.personObj = []
        self.username = username
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

        self.myDb = DatabasePerson()

        #load db
        self.personObj = self.myDb.loadDB()


        self.__startBrowser()

        self.login()
        

    def print_all_person(self):
        for i in self.personObj:
            print(i.getName())

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
        print(f"{name} is not in personObj")
        logging.error(f"{name} is not in personObj")
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

    def scroolChatPaneSide(self,y):
        """Sohbet panelinde scrool yapmaya yarayan fonksiyon. Y ne kadar scrool yapılacağını belirtir."""
        script = f"""
        function getElementByXpath(path){{
            return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        }}
        myObj1 = getElementByXpath('//*[@id="main"]/div[3]/div/div[2]')
        myObj1.scrollBy(0,{y})
        """
        if self.browser.current_url == self.WPURL:
            self.browser.execute_script(script)

    def getMaxScroolChatPaneSide(self):
        script = f"""
        function getElementByXpath(path){{
            return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        }}
        myObj1 = getElementByXpath('//*[@id="main"]/div[3]/div/div[2]')
        return myObj1.scrollHeight"""
        if  self.browser.current_url == self.WPURL:
            maxScroolChatPaneSide = self.browser.execute_script(script)
            logging.info(f"Max scrool new chat part pane side is {maxScroolChatPaneSide}")
            return maxScroolChatPaneSide

    def clickNewChatButton(self):
        """Yeni sohbet oluştur butonuna tıklar"""
        script = f"""var myObj = document.querySelector('[title="Yeni sohbet"]');
        myObj.click()"""
        if  self.browser.current_url == self.WPURL:
            self.browser.execute_script(script)
            logging.info("New chat button is clicked")
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
                if self.myDb.get_person_with_name(myPerson.getName()) == None:
                    self.myDb.addPerson(myPerson)
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
                        just_name = name.split(",")[0]
                        print(f"Find person! name: {just_name}                          ",end="\r")
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
            if self.myDb.get_person_with_name(myPerson.getName()) == None:
                self.myDb.addPerson(myPerson)
            count += 1
        logging.info("Getting person from last conversations ended")
        logging.info(f"{count} person added")
    

    def clickPeopleInNewChatSide(self,name):
        """Yeni sohbet ekranındaki arama kısmına verilen ismi yazar ve verilen isimle eşleşen bir kişi varsa tıklar ardından True döner."""
        xpath = '//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[1]/div/label/div/div[2]'
        searchBox = self.browser.find_element_by_xpath(xpath)
        searchBox.send_keys(name)
        sleep(0.2)
        for i in range(1,10):
            xpath = f'//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div[2]/div/div/div/div[{i}]/div/div/div[2]/div[1]/div/span'
            try:
                findObj = self.browser.find_element_by_xpath(xpath)
                if findObj.text == name:
                    findObj.click()
                    sleep(0.2)
                    logging.info(f"Click people in new chat side success, name: {name}")
                    return True
            except Exception as e:
                pass
        logging.info(f"{name} not found")
        return False

    def clickNameBar(self):
        # buranın bu şekilde yapılmasının sebebi ileride mouse konumuna tıklamak değil xpath veya farklı bir yöntem bularak kesin bir bulma yöntemi kullanılacka.
        self.__clickXY(390,28)
        logging.info("Clicked name bar")

    def __clickXY(self,x,y):
        """tarayıcıda istenilen yere tıklamak için kullanılıyor"""
        action = ActionChains(self.browser)
        action.move_by_offset(x,y)
        action.click()
        action.perform()
        action.reset_actions()

    def downloadPictureFromURL(self,url,location):
        """url den resim indirmeye yarayan fonksiyon"""
        logging.info(f"Downloading picture from url: {url}")
        try:
            request.urlretrieve(url, location)
            logging.info(f"Picture downloaded from url: {url}")
        except Exception as e:
            logging.info(f"Picture download failed from url: {url}")
            logging.info(e)
        logging.info("Downloading picture from url ended")

    def createFolder(self,folderLocation):
        """Verilen isimde bir klasör oluşturur"""
        if not exists(folderLocation):
            mkdir(folderLocation)
            logging.info(f"Folder created: {folderLocation}")
        else:
            logging.info(f"Folder already exist: {folderLocation}")


    def getMessagePerson(self,person:Person,istenilenSayi:int):
        if self.browser.current_url == self.WPURL:
            if person.getType() == "Person":
                self.clickNewChatButton()
                if self.clickPeopleInNewChatSide(person.getName()):
                    mesajSayisi = 0
                    mesajListesi = []
                    mesaj_icerik_sha256 = []
                    while mesajSayisi <= istenilenSayi:
                        for i in range(36):
                            
                            #mesaj
                            try:
                                mesaj_icerik = self.browser.find_element_by_xpath(f'//*[@id="main"]/div[3]/div/div[2]/div[3]/div[{i}]/div/div/div/div[1]/div/span[1]/span').text
                                tarih_gonderici = self.browser.find_element_by_xpath(f'//*[@id="main"]/div[3]/div/div[2]/div[3]/div[{i}]/div/div/div/div[1]').get_attribute("data-pre-plain-text")
                                
                                tarih_hepsi = tarih_gonderici[:19].replace(" ","") #[19:55, 06.03.2022]
                                tarih_epoch = datetime.strptime(tarih_hepsi, '[%H:%M,%d.%m.%Y]')
                                tarih_epoch = int(tarih_epoch.timestamp())
                                gonderici = tarih_gonderici[20:].replace(" ","").replace(":","") #Emmoğlu:
                                alici = self.username
                                if (self.username == gonderici):
                                    alici = person.getName()
                                mesaj = WhatsappMessage(gonderici,alici,mesaj_icerik,0,tarih_epoch)
                                mesaj_sha256 = mesaj.getSha256()
                                if mesaj_sha256 not in mesaj_icerik_sha256:
                                    mesajListesi.append(mesaj)
                                    mesaj_icerik_sha256.append(mesaj_sha256)
                                    mesajSayisi += 1
                            except Exception as e:
                                pass

                            #fotoğraf
                            try:
                                #//*[@id="main"]/div[3]/div/div[2]/div[3]/div[14]/div/div[1]/div/div/div[1]/div[1]/div[2]/img
                                #//*[@id="main"]/div[3]/div/div[2]/div[3]/div[26]/div/div[1]/div/div/div[1]/div[1]/div[2]/img

                                #//*[@id="main"]/div[3]/div/div[2]/div[3]/div[23]/div/div[1]/span[1]
                                #//*[@id="main"]/div[3]/div/div[2]/div[3]/div[23]/div/div[1]/div
                                fotograf_src = self.browser.find_element_by_xpath(f'//*[@id="main"]/div[3]/div/div[2]/div[3]/div[{i}]/div/div/div/div[1]/div/div/div[1]/div[1]/div[2]/img').get_attribute("src")
                                fotograf_src = fotograf_src.replace("blob:","")
                                fotograf_src_hash = fotograf_src.replace("https://web.whatsapp.com/","")
                                mesaj = WhatsappMessage("gonderici","alici","FOTOGRAF",1,0)
                                mesaj.setSrc(fotograf_src)
                                if fotograf_src_hash not in mesaj_icerik_sha256:
                                    mesajListesi.append(mesaj)
                                    mesaj_icerik_sha256.append(mesaj_sha256)
                                    mesajSayisi += 1
                                #src="blob:https://web.whatsapp.com/7762b3eb-312b-4625-83b7-191c2e792fda"

                            except Exception as e:
                                pass




                            #çıkartma


                        
                            # emoji
                        self.scroolChatPaneSide(-300)
                    #mesajListesi sort by date with newest first
                    mesajListesi.sort(key=lambda x: x.getDate(),reverse=True)
                    for mesaj in mesajListesi:
                        print(mesaj)
                #//*[@id="main"]/div[3]/div/div[2]/div[3]/div[33]/div/div/div/div[1]/div/span[1]/span
                #//*[@id="main"]/div[3]/div/div[2]/div[3]/div[35]/div/div/div/div[1]/div/span[1]/span
                #//*[@id="main"]/div[3]/div/div[2]/div[3]/div[36]/div/div/div/div[1]/div/span[1]/span

    def getPersonDetailWithName(self,name):
        """Kişi hakkındaki bilgileri çeker. Hakkımda ve telefon numarası."""
        if self.browser.current_url == self.WPURL:
            myPerson = self.getPersonWithName(name) #fonksiyona verilen name adındaki objeyi al
            if myPerson != None:
                print(f"Getting person detail with name: {myPerson.getName()}, id: {myPerson.getID()}")
                if myPerson.getType() == "Person":
                    self.clickNewChatButton() 
                    if self.clickPeopleInNewChatSide(myPerson.getName()):
                        #get detail
                        self.clickNameBar()
                        sleep(1)
                        try:
                            telephoneNumber = self.browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[1]/div[2]/div/span/span').text
                            telephoneNumber = telephoneNumber.replace(" ","")
                        except:
                            telephoneNumber = None
                        try:
                            statText = self.browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[2]/span/span').text
                            #sqlite illegal chracter fix
                            statText = statText.replace("'","")
                            statText = statText.replace("\\","")
                            statText = statText.replace("/","")
                            statText = statText.replace("\"","")
                            statText = statText.replace("<","")
                            statText = statText.replace(">","")
                            statText = statText.replace("|","")
                            statText = statText.replace("*","")
                            statText = statText.replace("?","")
                        except:
                            statText = None

                        try:
                            profilePictureXpath = self.browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[1]/div[1]/div/img')
                            profilePictureLink = profilePictureXpath.get_attribute('src')
                            print("profile picture link: ",profilePictureLink)
                            #E:\Github\python-16-whatsappAnalyzer\Picture
                            #elf.chromeDriverPath = getcwd() + fr"\{C.get_chrome_driver_loc()}"
                            self.createFolder(getcwd() + fr"\Picture\{myPerson.getName()}")
                            profilePictureLoc =  getcwd() +  fr"\Picture\{myPerson.getName()}\pp{self.get_time_log_config()}.jpg"
                            self.downloadPictureFromURL(profilePictureLink,profilePictureLoc)
                            profilePicture = profilePictureLoc
                        except:
                            print("Profile picture not found")
                            logging.info("Profile picture not found")
                            profilePicture = None

                        myPerson.setProfilePicture(profilePicture)
                        myPerson.setStatusText(statText)
                        myPerson.setTelephoneNumber(telephoneNumber)


                        #//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[1]/div[1]/div/img
                        #//*[@id="app"]/div[1]/div[1]/div[2]/div[3]/span/div[1]/span/div[1]/div/section/div[1]/div[1]/div/div/span
                        self.myDb.updatePerson(myPerson)
                    else:
                        logging.info("Person not found")
                        print("Person not found")
                else:
                    print(f"{myPerson.getName()} is a group.")
                    logging.info(f"{myPerson.getName()} is a group.")
            else:
                print(f"'{name}' is not found in person list.")
                logging.info(f"'{name}' is not found in person list.")
        else:
            print("You are not in Whatsapp")
            logging.error("You are not in Whatsapp")
    
        
        
