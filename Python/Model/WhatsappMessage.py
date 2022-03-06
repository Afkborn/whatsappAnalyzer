import time
class WhatsappMessage:
    def __init__(self, 
    sender : str, 
    receiver : str,
    message : str,
    type : int, 
    send_time : int , 
    receive_time : int = 0, 
    read_time : int = 0):
        """
sender : str
receiver : str
message : str
type :  0 = message, 1 = image, 2 = video, 3 = audio, 4 = contact, 5 = location, 6 = sticker, 7 = voice, 8 = file, 9 = link, 10 = other
send_time : int
receive_time : int
read_time : int
    """
        
        self.sender = sender
        self.message = message
        self.receiver = receiver
        
        if type == 0:
            self.type = "MESSAGE"
        elif type == 1:
            self.type = "IMAGE"
        elif type == 2:
            self.type = "VIDEO"
        elif type == 3:
            self.type = "AUDIO"
        elif type == 4:
            self.type = "CONTACT"
        elif type == 5:
            self.type = "LOCATION"
        elif type == 6:
            self.type = "STICKER"
        elif type == 7:
            self.type = "VOICE"
        elif type == 8:
            self.type = "FILE"
        elif type == 9:
            self.type = "LINK"
        elif type == 10:
            self.type = "OTHER"

        self.send_time_epoch = send_time
        self.send_time_datetime = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(send_time))
        self.receive_time_epoch = receive_time
        self.receive_time_datetime = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(receive_time))
        self.read_time_epoch = read_time
        self.read_time_datetime = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(read_time))


    def __str__(self):
        if self.type == "MESSAGE":
            return f"{self.sender} -> {self.receiver} : {self.message}"
        elif self.type == "IMAGE":
            return f"{self.sender} -> {self.receiver} : IMAGE"
        elif self.type == "VIDEO":
            return f"{self.sender} -> {self.receiver} : VIDEO"
        elif self.type == "AUDIO":
            return f"{self.sender} -> {self.receiver} : AUDIO"
        elif self.type == "CONTACT":
            return f"{self.sender} -> {self.receiver} : CONTACT"
        elif self.type == "LOCATION":
            return f"{self.sender} -> {self.receiver} : LOCATION"
        elif self.type == "STICKER":
            return f"{self.sender} -> {self.receiver} : STICKER"
        elif self.type == "VOICE":
            return f"{self.sender} -> {self.receiver} : VOICE"
        elif self.type == "FILE":
            return f"{self.sender} -> {self.receiver} : FILE"
        elif self.type == "LINK":
            return f"{self.sender} -> {self.receiver} : LINK"
        elif self.type == "OTHER":
            return f"{self.sender} -> {self.receiver} : OTHER"
        # return  self.sender + " to " + self.receiver + " on " + self.send_time_datetime + "\n\t" + self.message
