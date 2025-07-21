class Donation:
    count_id = 0

    def __init__(self, creditcard, date, cvv, name, society, donateamt):
        Donation.count_id += 1
        self.__donation_id = Donation.count_id
        self.__creditcard = creditcard
        self.__date = date
        self.__cvv = cvv
        self.__name = name
        self.__society = society
        self.__donateamt = donateamt

    def get_donation_id(self):
        return self.__donation_id

    def get_creditcard(self):
        return self.__creditcard

    def get_date(self):
        return self.__date

    def get_cvv(self):
        return self.__cvv

    def get_name(self):
        return self.__name

    def get_donateamt(self):
        return self.__donateamt

    def get_society(self):
        return self.__society

    def set_donation_id(self, donation_id):
        self.__donation_id = donation_id

    def set_creditcard(self, creditcard):
        self.__creditcard = creditcard

    def set_date(self, date):
        self.__date = date

    def set_cvv(self, cvv):
        self.__cvv = cvv

    def set_name(self, name):
        self.__name = name

    def set_society(self, society):
        self.__society = society

    def set_donateamt(self, donateamt):
        self.__donateamt = donateamt