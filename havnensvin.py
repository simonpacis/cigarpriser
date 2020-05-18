from scraper import *

print("Running havnensvin scraper.")

class Scraper:
	def __init__(self):
		self.store = "Havnens Vin"
		self.url = "https://havnens-vin.dk/tobak/cigar.html"
		self.url_absolute = ""
		self.main_select = "#narrow-by-list"
		self.main_anchor_select = "a"
		self.product_select = ".product-item"
		self.product_url_select = "a"
		self.product_name_select = ".page-title span"
		self.product_price_select = '.price-wrapper span'
		self.product_middle_extract = True
		self.product_middle_select = '.product.overview'
		self.product_middle_length_seperate_for_non_numeric = True
		self.product_middle_gauge_seperate_for_non_numeric = True
		self.product_middle_get_type = False


	def get_brand(self, href):
	    if(len(href.contents) > 1):
	        brand = BeautifulSoup(str(href.contents[1]), 'html5lib').select_one('div')
	        if((brand, 'contents')):
	            try:
	                return brand.contents[0]
	            except:
	                return "unknown"
	        else:
	            return "unknown"
	    else:
	        return "unknown"	

	def has_product_check(self, hrefsoup):
		return True

	def get_price(self, product):
		return float(re.sub("[^\d.]+", "", ((product.select_one(self.product_price_select).contents[0].split(",")[0]).replace(".",""))))

	def get_length(self, product_middle):
		start = product_middle.find("Længde : ") + len("Længde : ")
		end = product_middle.find("mmR")
		return product_middle[start:end].strip()

	def get_non_numeric_length(self, product_middle):
		start = product_middle.find("Længde i mm:") + len("Længde i mm:")
		end = start + 6
		length = str(product_middle[start:end].strip())
		return re.sub("[^\d.]+", "", length)

	def get_gauge(self, product_middle):
		start = product_middle.find("Ring : ") + len("Ring : ")
		end = product_middle.find("mmS")
		return str(product_middle[start:end].strip())

	def get_non_numeric_gauge(self, product_middle):
		start = product_middle.find("Diameter i mm:") + len("Diameter i mm:")
		end = start + 4
		return str(product_middle[start:end].strip())

	def gauge_calculations(self, gauge):
		return int(round((float(gauge.strip()))*2.546))


scraper = Scraper()

parse(scraper)