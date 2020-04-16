import scrapy
from datetime import datetime
import csv

class CoronaSpider(scrapy.Spider):
    name = 'covid19'
    
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/coronavirus/'] 
    itemlist = [] 
    
    def parse(self, response):
        countries = response.xpath("//table[@id='main_table_countries_today']/tbody[1]/tr")
        
        for country in countries:                 
            items = {}
            items["Country/Region"] =  country.xpath(".//td[1]/nobr/text()").get() or country.xpath(".//td[1]//text()").get()
            items["Total Cases"] = country.xpath(".//td[2]/text()").get()
            items["New Cases"] = country.xpath(".//td[3]/text()").get()
            items["Total Deaths"]  = country.xpath(".//td[4]/text()").get()   
            items["New Deaths"] = country.xpath(".//td[5]/text()").get()
            items["Total Recovered"] = country.xpath(".//td[6]/text()").get()
            items["Active Cases"] = country.xpath(".//td[7]/text()").get()
            items["Serious/Critical"] = country.xpath(".//td[8]/text()").get() 
            items["Total Tests"] = country.xpath(".//td[11]/text()").get()
            self.itemlist.append(items)            
                    
        now = datetime.now() # current date and time
        day = now.strftime("%d%b")
        time = now.strftime("%H%M")
      
        with open("Corona_Worldwide_" + day + "_" + time + "hrs" + ".csv","x", newline="") as f:
            writer = csv.DictWriter(f,['Country/Region', 'Total Cases', 'New Cases', 'Total Deaths', 'New Deaths', 'Total Recovered', 'Active Cases', 'Serious/Critical', 'Total Tests'])
            writer.writeheader()
            for data in self.itemlist:
                writer.writerow(data)
