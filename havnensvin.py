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


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext


# Set headers

print("Running havnensvin scraper.")


headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
url = "https://havnens-vin.dk/tobak/cigar.html"
req = requests.get(url, headers)
soup = BeautifulSoup(req.content, 'html5lib')

cigars = []
i = 1
for link in soup.select('#narrow-by-list'):
	for href in link.find_all('a'):
		url = href.get("href").strip();
		brand = "unknown"
		if(len(href.contents) > 1):
			brand = BeautifulSoup(str(href.contents[1]), 'html5lib').select_one('div')
			if(hasattr(brand, 'contents')):
				brand = brand.contents[0]
			else:
				continue
		else:
			continue
		req = requests.get(url, headers)
		hrefsoup = BeautifulSoup(req.content, 'html5lib')
		product_list = hrefsoup.select('.product-item')
		for product in product_list:
			
			product_url = product.select_one("a").get("href").strip()
			product_req = requests.get(product_url, headers)
			productsoup = BeautifulSoup(product_req.content, 'html5lib')
			name = productsoup.select_one('.page-title span').contents[0]
			price = float(re.sub("[^\d.]+", "", ((product.select_one('.price-wrapper span').contents[0].split(",")[0]).replace(".",""))))
			url = product_url
			print("Scraping cigar " + str(i) + " with url " + url)
			product_middle = productsoup.select_one('.product.overview')
			if(product_middle):
				product_middle = product_middle.get_text()

				start = product_middle.find("Længde : ") + len("Længde : ")
				end = product_middle.find("mmR")
				length = product_middle[start:end].strip()
				if(length.isnumeric() == False):
					start = product_middle.find("Længde i mm:") + len("Længde i mm:")
					end = start + 6
					length = str(product_middle[start:end].strip())
					length = re.sub("[^\d.]+", "", length)
				if(length.isnumeric() == False):
					print("Length is not numeric. Setting to 0")
					length = 0
					#continue
					#sys.exit(0)

				#print(length)

				#start = product_middle.find("Type : ") + len("Type : ")
				#end = product_middle.find("Længde")
				#cigar_type = product_middle[start:end]
				#cigar_type = cigar_type.replace("<br/>", "").strip()
				#if(cigar_type == ""):
				cigar_type = "Unknown"

				#print(cigar_type)

				start = product_middle.find("Ring : ") + len("Ring : ")
				end = product_middle.find("mmS")
				gauge = str(product_middle[start:end].strip())
				if(gauge.isnumeric() == False):
					start = product_middle.find("Diameter i mm:") + len("Diameter i mm:")
					end = start + 4
					gauge = str(product_middle[start:end].strip())
				if(gauge.isnumeric() == False):
					print("Gauge is not numeric. Setting to 0.")
					gauge = str(0)
					#continue
					#sys.exit(0)
				gauge = float(gauge.strip())
				gauge = round(float(gauge) * 2.546) #From mm to gauge
				gauge = int(gauge)
				#print(gauge)

			else:
				length = 0
				cigar_type = "Unknown"
				gauge = 0

			cigars.append(Cigar(name, price, url, brand, length, gauge, cigar_type))
			i = i + 1
			


			

with open('results/havnensvin.csv', mode='w') as cigar_file:
	cigar_writer = csv.writer(cigar_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	cigar_writer.writerow(["Name", "Price", "Url", "Brand", "Length (mm)", "Gauge (ring)", "Type"])
	for cigar in cigars:
		cigar_writer.writerow([cigar.name, cigar.price, cigar.url, cigar.brand, cigar.length, cigar.gauge, cigar.cigar_type])
