from DonegalScrap import DonegalScrap, GetAllUrls

def callToScrap(url):
    donegalScrap = DonegalScrap(url=url)
    donegalScrap.writeToCSV()

AllUrls = GetAllUrls()


urls = AllUrls.GetAllProductUrls()

for url in urls:
    print(url)
    callToScrap(url)

