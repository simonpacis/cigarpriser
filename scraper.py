from bs4 import BeautifulSoup
import requests
import csv
import re
import sys

class Cigar:
  def __init__(self, name, price, url, brand, length, gauge, cigar_type, store):
    self.store = store
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


headers = requests.utils.default_headers()
headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
cigars = []
def parse(scraper):
    global cigars
    req = requests.get(scraper.url, headers)
    soup = BeautifulSoup(req.content, 'html5lib')
    i = 1
    for link in soup.select(scraper.main_select):
        for href in link.find_all(scraper.main_anchor_select):
            url = href.get("href").strip()
            brand = scraper.get_brand(href)

            req = requests.get(scraper.url_absolute + url, headers)
            hrefsoup = BeautifulSoup(req.content, 'html5lib')
            if not(scraper.has_product_check(hrefsoup)):
                break
            product_list = hrefsoup.select(scraper.product_select)
            for product in product_list:
                product_url = product.select_one(scraper.product_url_select).get("href").strip()
                product_req = requests.get(scraper.url_absolute + product_url, headers)
                productsoup = BeautifulSoup(product_req.content, 'html5lib')
                name = productsoup.select_one(scraper.product_name_select).contents[0]
                price = scraper.get_price(product)
                url = product_url
                print("Scraping cigar " + str(i) + " with url " + url)
                if(scraper.product_middle_extract):
                    product_middle = productsoup.select_one(scraper.product_middle_select)
                    if(product_middle):

                        product_middle = product_middle.get_text()
                        length = scraper.get_length(product_middle)
                        if(scraper.product_middle_length_seperate_for_non_numeric):
                            if(length.isnumeric() == False):
                                length = scraper.get_non_numeric_length(product_middle)
                                
                            if(length.isnumeric() == False):
                                print("Length is not numeric. Setting to 0")
                                length = 0

                        if(scraper.product_middle_get_type):
                            cigar_type = scraper.get_type(product_middle)
                        else:
                            cigar_type = "Unknown"

                        gauge = scraper.get_gauge(product_middle)
                        if(scraper.product_middle_gauge_seperate_for_non_numeric):
                            if(gauge.isnumeric() == False):
                                gauge = scraper.get_non_numeric_gauge(product_middle)
                            if(gauge.isnumeric() == False):
                                print("Gauge is not numeric. Setting to 0.")
                                gauge = str(0)

                        gauge = scraper.gauge_calculations(gauge)

                else:
                    length = 0
                    cigar_type = "Unknown"
                    gauge = 0

                cigars.append(Cigar(name, price, url, brand, length, gauge, cigar_type, scraper.store))
                i = i + 1


import havnensvin
import cognachuset

with open('results/results.csv', mode='w') as cigar_file:
    cigar_writer = csv.writer(cigar_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    cigar_writer.writerow(["Name", "Price", "Url", "Brand", "Length (mm)", "Gauge (ring)", "Type", "Store"])
    for cigar in cigars:
        cigar_writer.writerow([cigar.name, cigar.price, cigar.url, cigar.brand, cigar.length, cigar.gauge, cigar.cigar_type, cigar.store])