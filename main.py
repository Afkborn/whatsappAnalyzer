from time import sleep
from Python.Whatsapp import Whatsapp

from Python.Model.Person import Person
if __name__ == "__main__":
    whatsapp = Whatsapp(True)
    input("Giriş yapıldı devam et.")
    # whatsapp.getPersonFromLastConversations()
    sleep(0.2)
    whatsapp.getPersonFromNewChatPart()

