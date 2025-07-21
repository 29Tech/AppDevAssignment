class User:
    status_active = 1

    def __init__(self, email, password, date_created):
        self.id = email  # Using email as the unique identifier
        self.email = email
        self.password = password
        self.status = User.status_active
        self.date_created = date_created
        self.date_updated = date_created
