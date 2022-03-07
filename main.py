from time import sleep
from Python.Whatsapp import Whatsapp


from Python.Model.Person import Person
if __name__ == "__main__":

    whatsapp = Whatsapp("Bilgehan",True)
    input("Giriş yapıldı devam et.")
    sleep(0.3)
    
    myPerson = whatsapp.getPersonWithName("Emmoğlu")
    whatsapp.getMessagePerson(myPerson,50)
    # for person in  whatsapp.getPersonObjList():
    #     if (person.getProfilePicture() == "None"):
    #         whatsapp.getPersonDetailWithName(person.getName())
    # whatsapp.getPersonFromLastConversations()
    # whatsapp.getPersonFromNewChatPart()

