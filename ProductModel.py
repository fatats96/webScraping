# MY PRODUCT MODEL
class Products:
    
    def __init__(self):
        self.productId = 0
        self.productImage = ""
        self.productTitle = ""
        self.productReference = ""
        self.productPrice = ""
    
    def printModel(self):
        print(self.productId + " - " + self.productTitle + " - " + self.productReference + " - " + self.productPrice+ " - " + self.productImage + " \n "   )        
