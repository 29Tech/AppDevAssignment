class Detail:
    count_id = 0

    def __init__(self, accountid, accountname, doc, accountemail):
        Detail.count_id += 1
        self.__detail_id = Detail.count_id
        self.__accountname = accountname
        self.__doc = doc
        self.__accountid = accountid
        self.__accountemail = accountemail

    def get_detail_id(self):
        return self.__detail_id
    
    def get_accountid(self):
        return self.__accountid
    
    def get_accountname(self):
        return self.__accountname

    def get_doc(self):
        return self.__doc

    def get_accountemail(self):
        return self.__accountemail
    
    def set_detail_id(self, detail_id):
        self.__detail_id = detail_id
    
    def set_accountid(self, accountid):
        self.__accountid = accountid

    def set_accountname(self, accountname):
        self.__accountname = accountname

    def set_doc(self, doc):
        self.__doc = doc

    def set_accountemail(self, accountemail):
        self.__accountemail = accountemail
