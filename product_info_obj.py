class product_info_obj:

    def __init__(self, prod_id, prod_name):
        # Purpose of this class is to have one location for the product search info 
        # such as product ID and name.

        self.id = prod_id
        self.name = prod_name
    
    def SetID(self, prod_id):
        self.id = prod_id

    def SetName(self, prod_name):
        self.name = prod_name

    def GetID(self):
        return self.id

    def GetName(self):
        return self.name
    