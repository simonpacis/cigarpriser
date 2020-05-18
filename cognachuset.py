from scraper import *

print("Running cognachuset scraper.")

class Scraper:
	def __init__(self):
		self.store = "Cognachuset"
		self.url = "https://www.cognachuset.dk/shop/cigarer-75s1.html"
		self.url_absolute = "https://cognachuset.dk"
		self.main_select = ".SubMenu_Productmenu_Table tr"
		self.main_anchor_select = "a"
		self.product_select = "#Content_Productlist > table.ProductList_Custom_TBL > tbody > tr"
		self.product_url_select = "a"
		self.product_name_select = "span[itemprop='name']"
		self.product_price_select = "span[itemprop='price']"
		self.product_middle_extract = True
		self.product_middle_select = "div[itemprop='description']"
		self.product_middle_length_seperate_for_non_numeric = False
		self.product_middle_gauge_seperate_for_non_numeric = False

	def get_brand(self, href):
	    try:
	    	return href.contents[0][2:].strip()
	    except:
	    	return "unknown"

	def has_product_check(self, hrefsoup):
		try:
			if(len(hrefsoup.select_one('.NoProcuctsFound')) > 0):
				return False
			else:
				return True
		except:
			return True

	def get_price(self, product):
		return float(re.sub("[^\d.]+", "", (product.select_one('.price').contents[0].replace(",","."))))

	def get_type(self, product_middle):
		start = product_middle.find("Type : ") + len("Type : ")
		end = product_middle.find("Længde")
		cigar_type = product_middle[start:end]
		cigar_type = cigar_type.replace("<br/>", "").strip()
		if(cigar_type == ""):
			cigar_type = "Unknown"
		return cigar_type

	def get_length(self, product_middle):
		start = product_middle.find("Længde : ") + len("Længde : ")
		end = product_middle.find("mm")
		return product_middle[start:end].strip()

	def get_gauge(self, product_middle):
		start = product_middle.find("Ring : ") + len("Ring : ")
		end = product_middle.find("mm)")
		return str(product_middle[start:end].strip())

	def gauge_calculations(self, gauge):
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
		return gauge


scraper = Scraper()

parse(scraper)