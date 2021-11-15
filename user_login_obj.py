class user_login_obj:

    def __init__(self, LOGIN, login_email, user_role):
        # Purpose of this class is to have one location for the user login info 
        # such as LOGIN, login email and user role.

        self.login = LOGIN
        self.email = login_email
        self.role = user_role
    
    def SetLogin(self, LOGIN):
        self.login = LOGIN

    def SetEmail(self, login_email):
        self.email = login_email

    def SetRole(self, user_role):
        self.role = user_role

    def GetLogin(self):
        return self.login
    
    def GetEmail(self):
        return self.email

    def GetRole(self):
        return self.role

    



