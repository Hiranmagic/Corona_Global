import scrapy
import json
from datetime import datetime
import csv

class covidIndia19(scrapy.Spider):
    name = 'covid_cor'
    allowed_domains = ['www.covid19india.org']
    itemlist = []

    def start_requests(self):
        yield scrapy.Request(url='https://api.covid19india.org/data.json', callback=self.parse)

    # def parse_id(self, response):
    def parse(self, response):
        data = json.loads(response.body) 
        # with open('sample1.json', 'w') as file:
        #     file.write(json.dumps(data))

        states = data.get('statewise')
        # print('State : -', states)

        for state in states:
            items = {}
            if state.get("state") != 'Total':
                 if state.get("confirmed") > '0':
                                        
                    items["State"] = state.get("state")
                    items["Total Cases"] = state.get("confirmed")
                    items["New Cases"] = state.get("deltaconfirmed")
                    items["Active"] = state.get("active")
                    items["Recovered"] = state.get("recovered")
                    items["New Recovered"] = state.get("deltarecovered")
                    items["Deceased"] = state.get("deaths")
                    items["New Deaths"] = state.get("deltadeaths")
                    items["State-wise Last Update"] = state.get("lastupdatedtime")
                    self.itemlist.append(items)

        for state in states:
            if state.get("state") == 'Total':
                        
                items["State"] = state.get("state")
                items["Total Cases"] = state.get("confirmed")
                items["New Cases"] = state.get("deltaconfirmed")
                items["Active"] = state.get("active")
                items["Recovered"] = state.get("recovered")
                items["New Recovered"] = state.get("deltarecovered")
                items["Deceased"] = state.get("deaths")
                items["New Deaths"] = state.get("deltadeaths")
                items["State-wise Last Update"] = state.get("lastupdatedtime")
                self.itemlist.append(items)
        
        
        now = datetime.now() # current date and time
        day = now.strftime("%d%m")
        time = now.strftime("%H%M")
   
        with open("CovidInd_Statewise_" + day + "_" + time + ".csv","x", newline="") as f:
            writer = csv.DictWriter(f,['State', 'Total Cases', 'New Cases', 'Active', 'Recovered', 'New Recovered', 'Deceased', 'New Deaths',  'State-wise Last Update'])
            writer.writeheader()
            for data in self.itemlist:
                writer.writerow(data)

