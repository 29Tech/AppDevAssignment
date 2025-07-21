class Sub:
    count_id = 0

    def __init__(self, first_name, last_name, gender, email, remarks):
        Sub.count_id += 1
        self.__sub_id = Sub.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__gender = gender
        self.__email = email
        self.__remarks = remarks

    def get_sub_id(self):
        return self.__sub_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_gender(self):
        return self.__gender

    def get_email(self):
        return self.__email

    def get_remarks(self):
        return self.__remarks


    def set_sub_id(self, sub_id):
        self.__sub_id = sub_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_gender(self, gender):
        self.__gender = gender

    def set_email(self, email):
        self.__email = email

    def set_remarks(self, remarks):
        self.__remarks = remarks
