class UserView:

    id : int
    email : str
    password : str
    
    def __init__(self, user):
        self.id = user.id
        self.email = user.email
        self.password = user.password