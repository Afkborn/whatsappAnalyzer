class Person:
    def __init__(self,
    name : str,
    type : int,
    findPlace : int, 
    id : int = None, 
    statusText : str = None, 
    telephoneNumber : str = None,
    profilePicture : str = None):
        """Person sınıfından bir obje oluşturur. birinci parametre objenin adını ikinci parametre objenin tipini belirtir. type: 0=>person, 1=>Group    findPlace: 0=>last conversation, 1=>new chat side"""
        self.__name = name
        self.__id = id
        self.__typeDB = type
        if type == 0:
            self.__type = "Person"
        else:
            self.__type = "Group"
        self.__findPlaceDB = findPlace
        if findPlace == 0:
            self.__findPlace = "LastConversation"
        else:
            self.__findPlace = "NewChatSide"

        self.statusText = statusText
        self.telephoneNumber = telephoneNumber
        self.profilePicture = profilePicture


    def getID(self) -> int:
        """return id"""
        return self.__id
    def setID(self,id) -> int:
        """set id"""
        self.__id = id
        return self.__id

    def getName(self) -> str:
        """return name"""
        return self.__name
    def getType(self) -> str:
        """return type (Person,Group)"""
        return self.__type
    def getFindPlace(self) -> str:
        """return find place (conversation, new chat side)"""
        return self.__findPlace

    def getFindPlaceDB(self) -> int:
        return self.__findPlaceDB
    def getTypeDB(self) -> int:
        return self.__typeDB


    def setTelephoneNumber(self,telephoneNumber) -> str:
        """set telephone number"""
        self.telephoneNumber = telephoneNumber
        return self.telephoneNumber

    def getTelephoneNumber(self) -> str:
        """return telephone number"""
        return self.telephoneNumber

    def setStatusText(self,statText) -> str:
        """set status text"""
        self.statusText = statText
        return self.statusText

    def getStatusText(self) ->str:
        """return status text"""
        return self.statusText

    def setProfilePicture(self,profilePicture) -> str:
        """set profile picture"""
        self.profilePicture = profilePicture
        return self.profilePicture

    def getProfilePicture(self) -> str:
        """return profile picture"""
        return self.profilePicture
    
