from bs4 import BeautifulSoup
import requests
import csv
import re
import sys

class Cigar:
  def __init__(self, name, price, url, brand, length, gauge, cigar_type):
    self.name = name
    self.price = price
    self.url = url
    self.brand = brand
    self.length = length
    self.cigar_type = cigar_type
    self.gauge = gauge
    if(self.brand in self.name):
    	self.name = self.name.replace(self.brand, "").strip()

    if(self.cigar_type in self.name):
    	self.name = self.name.replace(self.cigar_type, "").strip()

# Set headers

print("Running cognachuset scraper.")



headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
url = "https://www.cognachuset.dk/shop/cigarer-75s1.html"
req = requests.get(url, headers)
soup = BeautifulSoup(req.content, 'html5lib')

cigars = []
i = 1
for link in soup.select('.SubMenu_Productmenu_Table tr'):
	for href in link.find_all('a'):
		
		url = href.get("href");
		brand = href.contents[0][2:].strip()
		req = requests.get("https://cognachuset.dk" + url, headers)
		hrefsoup = BeautifulSoup(req.content, 'html5lib')
		product_list = hrefsoup.select('.BackgroundColor1_Productlist tr')
		for product in product_list:
			print("Scraping cigar " + str(i))
			name = product.select_one('.name a').contents[0]
			price = float(re.sub("[^\d.]+", "", (product.select_one('.price').contents[0].replace(",","."))))
			url = "https://cognachuset.dk" + product.select_one('.productlist-product-middle a').get('href')

			product_middle = str(product.select_one('.productlist-product-middle'))

			start = product_middle.find("Længde : ") + len("Længde : ")
			end = product_middle.find("mm")
			length = product_middle[start:end].strip()
			if(length == ""):
				length = 0

			start = product_middle.find("Type : ") + len("Type : ")
			end = product_middle.find("Længde")
			cigar_type = product_middle[start:end]
			cigar_type = cigar_type.replace("<br/>", "").strip()
			if(cigar_type == ""):
				cigar_type = "Unknown"

			start = product_middle.find("Ring : ") + len("Ring : ")
			end = product_middle.find("mm)")
			gauge = str(product_middle[start:end].strip())
			gauge = gauge.split(" ", 1)[0]
			if("/" in gauge):
				gauge = gauge.split("/", 1)[0]
			if(gauge == ""):
				gauge = 0
			if("(" in gauge):
				#2,546
				gauge = float(gauge.replace("(", "").strip())
				gauge = round(float(gauge) * 2.546) #From mm to gauge
				gauge = int(gauge)

			cigars.append(Cigar(name, price, url, brand, length, gauge, cigar_type))
			i = i + 1
			


			

with open('results/cognachuset.csv', mode='w') as cigar_file:
	cigar_writer = csv.writer(cigar_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	cigar_writer.writerow(["Name", "Price", "Url", "Brand", "Length (mm)", "Gauge (ring)", "Type"])
	for cigar in cigars:
		cigar_writer.writerow([cigar.name, cigar.price, cigar.url, cigar.brand, cigar.length, cigar.gauge, cigar.cigar_type])
