from datetime import datetime
class Log:
    def __init__(self):
        pass

    def savechats(self, sessionID, usermessage, botmessage, intent, dbConn):

        self.now = datetime.now()
        self.date = self.now.date()
        self.current_time = self.now.strftime("%H:%M:%S")

        chat_dict = {"sessionID":sessionID,"User Intent" : intent ,"User": usermessage, "Bot": botmessage, "Date": str(self.date) + "/" + str(self.current_time)}
        records = dbConn.chat_records
        records.insert_one(chat_dict)

    def save_cases(self, search, botmessage, dbConn):

        query = {"search": search}
        cases_dict = {"search":search,"cases": botmessage}
        values = {"$set": cases_dict}
        records = dbConn.cases_records
        records.update_one(query, values)

    def get_cases(self, search, botmessage, dbConn):
        records = dbConn.cases_records
        print(records.find_one({'search': search}))
        return records.find_one({'search': search})

