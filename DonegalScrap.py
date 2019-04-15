from urllib.request import urlopen as _request
from bs4 import BeautifulSoup as _soup

from ProductModel import Products

import os

import csv

class GetAllUrls:
    

    
    def __init__(self):
        self.urls = []
        self.client = _request("http://donegal.com.pl/gb/")
        self.pageHtml = self.client.read()
        self.client.close()
        self.pageSoup = _soup(self.pageHtml,"html.parser")
    
        self.menuLinks = self.pageSoup.find_all("li",{"class":"category glowna"})
        self.saleMenuLink = self.pageSoup.find_all("li",{"class":"link glowna"})
        
        print(len(self.menuLinks))
        i = 0
        for item in self.menuLinks:
            if not item.div:
                print(item.a["href"])
                for saleHrefs in self.saleMenuLink:
                    self.urls.append(saleHrefs.a["href"])
                break
            hrefs = item.div.ul.find_all("a")
            for href in hrefs:
                self.urls.append(href["href"])
            i = i+1 
        
    def GetAllProductUrls(self):
        return self.urls
        
class DonegalScrap:
   
    def __init__(self,url):
        self.productList = []  
        
        self.client = _request(url)

        self.pageHtml = self.client.read()

        self.client.close()

        self.pageSoup = _soup(self.pageHtml,"html.parser")

        self.products = self.pageSoup.find_all("article",{"class":"product-miniature js-product-miniature"})
        
        self.category = self.pageSoup.h6.text + "/" + self.pageSoup.find("div",{"class":"block-category"}).h1.text

        for item in self.products:
            product = Products()
            product.productId = item["data-id-product"]
            product.productImage = item.div.img["data-full-size-image-url"]
            product.productTitle = item.div.div.div.a.text.encode("utf-8","ignore")  
            product.productReference = item.div.find("div",{"class":"product-reference"}).label.text + item.div.find("div",{"class":"product-reference"}).span.text
            product.productPrice = item.div.find("div",{"class":"product-prices"}).div.span.text 
            self.productList.append(product)
            
    def createNewFolder(self):
        self.directory = "./OutputsDonegal/"
        try:
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)
        except OSError:
            print("Error:" + self.directory)
            
    def writeToCSV(self,extension = "csv"):
        existsCSVFile = os.path.isfile('./OutputsDonegal/DonegalProducts.csv')
        self.createNewFolder()
        if not existsCSVFile:
            with open("./OutputsDonegal/DonegalProducts.csv","w",newline='') as csvfile:
                fileWriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                fileWriter.writerow(["ProductId","ProductCategory","ProductTitle","ProductReference","ProductPrice","ProductImageUrl"])
                for item in self.productList:
                    fileWriter.writerow([item.productId,self.category,item.productTitle,item.productReference,item.productPrice,item.productImage])
        else:
            with open("./OutputsDonegal/DonegalProducts.csv","a",newline='') as csvfile:
                fileWriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                fileWriter.writerow([])
                for item in self.productList:
                    fileWriter.writerow([item.productId,self.category,item.productTitle,item.productReference,item.productPrice,item.productImage])

    def printItems(self):
        for item in self.productList:
           item.printModel()
