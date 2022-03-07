from sys import platform
import winreg
from os.path import exists
from os import mkdir, remove, rename
from os import listdir
from urllib import request
import zipfile

import logging
CHROME_VER = 0
FOLDER_NAME= ["Log","Screenshot","Driver","Profile","Database","Picture"]


def get_software_list(hive, flag):
        aReg = winreg.ConnectRegistry(None, hive)
        aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                            0, winreg.KEY_READ | flag)
        count_subkey = winreg.QueryInfoKey(aKey)[0]
        software_list = []
        for i in range(count_subkey):
            software = {}
            try:
                asubkey_name = winreg.EnumKey(aKey, i)
                asubkey = winreg.OpenKey(aKey, asubkey_name)
                software['name'] = winreg.QueryValueEx(asubkey, "DisplayName")[0]
                try:
                    software['version'] = winreg.QueryValueEx(asubkey, "DisplayVersion")[0]
                except EnvironmentError:
                    software['version'] = 'undefined'
                try:
                    software['publisher'] = winreg.QueryValueEx(asubkey, "Publisher")[0]
                except EnvironmentError:
                    software['publisher'] = 'undefined'
                software_list.append(software)
            except EnvironmentError:
                continue
        return software_list


def check_program_is_loaded(program_name):
    software_list = get_software_list(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + get_software_list(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY) + get_software_list(winreg.HKEY_CURRENT_USER, 0)
    for software in software_list:
        if software['name'] == program_name:
            # print(f"{software['name']} is loaded, version: {software['version']}")
            logging.info(f"{software['name']} is loaded, version: {software['version']}")
            name = software['name']
            program_version = software['version']
            publisher = software['publisher']
            return (name, program_version, publisher)
    logging.fatal(f"{program_name} is not loaded")
    return (None,None,None)


def check_folder():
    for folder in FOLDER_NAME:
        if not exists(folder):
            mkdir(folder)
            logging.info(f"{folder} is created")


def get_file_name_in_folder(folderName):
    file_list = listdir(folderName)
    return file_list

def check_driver_version_chrome(chrome_version):

    for driver in get_file_name_in_folder("Driver"):
        driver_ver = driver.replace(".exe","")
        if driver_ver == chrome_version:
            logging.info(f"Chrome driver installed")
            return True


    #try download
    try:  
        if "chromedriver.exe" in get_file_name_in_folder("Driver"):
            remove("Driver\\chromedriver.exe")
            logging.info("Old chrome driver is removed")
        
        request.urlretrieve(f"https://chromedriver.storage.googleapis.com/{chrome_version}/chromedriver_win32.zip", "Driver/chromedriver_win32.zip")
        logging.info("Chrome driver downloaded successfully")

        with zipfile.ZipFile("Driver/chromedriver_win32.zip", 'r') as zip_ref:
            zip_ref.extractall("Driver")
        logging.info("Chrome driver extracted successfully")
        
        if "chromedriver.exe" in get_file_name_in_folder("Driver"):
            #rename file
            rename(r"Driver\chromedriver.exe", fr"Driver\{chrome_version}.exe")
            logging.info("Chrome driver renamed successfully")
        remove("Driver/chromedriver_win32.zip")
        logging.info(f"Chrome driver installed successfully")
        return True
    except Exception as e:
        print("Error, details in log file")
        logging.fatal("Chrome driver is not installed, error: " + str(e))
        return False



def check_compatibility():
    
    check_folder()

    if platform != "win32":
        logging.fatal("This program is only compatible with Windows")
        return False
    name, program_version, publisher = check_program_is_loaded("Google Chrome")
    global CHROME_VER
    CHROME_VER = program_version
    if name is None or program_version is None or publisher is None:
        logging.fatal("Google Chrome is not installed")
        return False
    
    if not check_driver_version_chrome(program_version):
        logging.fatal("Chrome driver is not installed")
        return False

    logging.info("Compatibility check is successful")
    return True
    


def get_chrome_version():
    return CHROME_VER

def get_chrome_driver_loc():
    #check exist driver
    if f"{CHROME_VER}.exe" in get_file_name_in_folder("Driver"):
        return fr"Driver\{CHROME_VER}.exe"



