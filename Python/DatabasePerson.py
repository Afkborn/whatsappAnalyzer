from os import getcwd
from os.path import exists

import sqlite3 as sql
from unicodedata import name # sqlite3 is a module

#Models
from Python.Model.WhatsappMessage import WhatsappMessage

from Python.Model.Person import Person



#log
import logging


CREATETABLEPERSON = """CREATE TABLE IF NOT EXISTS persons (id	INTEGER PRIMARY KEY,isim TEXT NOT NULL,type TEXT NOT NULL,find_place TEXT NOT NULL, status_text TEXT, telephone_number TEXT, profile_picture TEXT );"""



class DatabasePerson:
    __isLoaded = False
    __dbName = "database.db"
    __persons = list()
    __dbLen = 0
    __dbLoc = fr"{getcwd()}\Database\{__dbName}"

    def __init__(self):
        self.checkDB()


    def getDbName(self) -> str:
        """Database adını döner"""
        return self.__dbName

    def getIsLoadDb(self) -> bool:
        """Database'in yüklenip yüklenmediğini döner"""
        return self.__isLoaded

    def getDbLen(self):
        """Databasede kayıtlı olan kişilerin uzunluğunu döner"""
        return self.__dbLen

    def getPersonList(self) -> list:
        """Person listesini döner"""
        return self.__persons

    def getDbLoc(self) -> str:
        return self.__dbLoc

    def setDbName(self,dbName:str):
        self.__dbName = dbName
    
    def checkDB(self):
        """Database dosyasını kontrol eder, eğer konumda database yoksa o konumda bir database dosyası oluşturmaya yarayan createDb çalışır"""
        if not exists(self.__dbLoc):
            #Konumda yoksa
            self.__create_persons_table()
            

    def loadDB(self):
        """Database dosyasını yüklemeye yarar."""
        self.__persons.clear()
        self.db = sql.connect(self.__dbLoc)
        self.im = self.db.cursor()

        self.im.execute("SELECT name FROM sqlite_master")
        tableNames = self.im.fetchall()
        newTableNames = []
        for i in tableNames:
            i = str(i).replace("(","").replace(")","").replace("'","").replace(",","")
            newTableNames.append(i)
        tableNames = newTableNames
        
        if "persons" in tableNames : 
            self.im.execute("SELECT * FROM persons")
            allDb = self.im.fetchall()
            for i in allDb:
                # (id	INTEGER PRIMARY KEY,isim TEXT NOT NULL,type TEXT NOT NULL,find_place TEXT NOT NULL, status_text TEXT, telephone_number TEXT, profile_picture TEXT );"""
                id, isim, person_type, find_place, status_text, telephone_number, profile_picture = i
                #(1, '+359 87 750 1142', '0', '0', 'None', 'None', 'None')
                person_type = int(person_type)
                find_place = int(find_place)
                myPerson = Person(isim,person_type,find_place,id,status_text,telephone_number,profile_picture)
                self.__persons.append(myPerson)


            self.__isLoaded = True
        else:
            self.im.execute(CREATETABLEPERSON)
            self.db.commit()
            self.__isLoaded = True
        self.db.close()
        print("Database yüklendi. Toplam kişi sayısı:",len(self.__persons))
        return self.__persons

    def __create_persons_table(self):
        """kayıtlı konumda (öğrenmek için getDbLoc fonksiyonu kullanılabilir) database oluşturur. """
        print(self.__dbLoc)
        self.db = sql.connect(self.__dbLoc)
        self.im = self.db.cursor()
        self.im.execute(CREATETABLEPERSON)
        self.db.commit()
        self.db.close()
        logging.log("Database created.")
        self.__isLoaded = True
        self.__dbLen = 0

    def getPersonsLenFromDB(self) -> int:
        """Database'de kayıtlı olan persons listesinin uzunluğunu döner."""
        self.db = sql.connect(self.__dbLoc)
        self.im = self.db.cursor()
        self.im.execute("select last_insert_rowid() from persons")
        self.__dbLen = len(self.im.fetchall())
        self.db.close() 
        return self.__dbLen 


    def addPerson(self,person:Person):
        """Database'e ürün ekler."""
        self.db = sql.connect(self.__dbLoc)
        self.im = self.db.cursor()
        KEY = f"isim,type,find_place,status_text,telephone_number,profile_picture"
        VALUES = f"""
        '{person.getName()}',
        '{person.getTypeDB()}',
        '{person.getFindPlaceDB()}',
        '{person.getStatusText()}',
        '{person.getTelephoneNumber()}',
        '{person.getProfilePicture()}'
        """
        self.im.execute(f"INSERT INTO persons({KEY}) VALUES({VALUES})")
        person.setID(self.im.lastrowid)
        logging.info(f"Person added to database. Person name: {person.getName()} Person ID: {person.getID()}")
        self.db.commit()
        self.db.close()

    def updatePerson(self,person:Person):
        """Database'de kişiyi günceller."""
        self.db = sql.connect(self.__dbLoc)
        self.im = self.db.cursor()
        self.im.execute(f"UPDATE persons SET isim='{person.getName()}',type='{person.getTypeDB()}',find_place='{person.getFindPlaceDB()}',status_text='{person.getStatusText()}',telephone_number='{person.getTelephoneNumber()}',profile_picture='{person.getProfilePicture()}' WHERE id={person.getID()}")
        logging.info(f"Person updated. Person name: {person.getName()} Person ID: {person.getID()}")
        self.db.commit()
        self.db.close()


    def get_person_with_id(self,id:int) -> Person:
        """id ile kişi getirir."""
        self.db = sql.connect(self.__dbLoc)
        self.im = self.db.cursor()
        self.im.execute(f"SELECT * FROM persons WHERE id = {id}")
        person = self.im.fetchone()
        id, isim, person_type, find_place, status_text, telephone_number, profile_picture = person
        myPerson = Person(id, isim, person_type, find_place, status_text, telephone_number, profile_picture)
        self.db.close()
        return myPerson

    def get_person_with_name(self,name:str) -> Person:
        """isim ile kişi getirir."""
        self.db = sql.connect(self.__dbLoc)
        self.im = self.db.cursor()
        self.im.execute(f"SELECT * FROM persons WHERE isim = '{name}'")
        person = self.im.fetchone()
        if person is None:
            return None
        id, isim, person_type, find_place, status_text, telephone_number, profile_picture = person

        myPerson = Person(id, isim, person_type, find_place, status_text, telephone_number, profile_picture)
        self.db.close()
        return myPerson
