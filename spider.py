import scrapy

class ClassSpider(scrapy.Spider):
    name = "ClassSpider"
    start_urls=[
        "https://d20pfsrd.com/classes/core-classes/cleric"
    ]

    def parse(self, response):
        pagetitle = response.url.split("/")[-1]
        with open("export-%s.txt"%pagetitle, "w") as file:
            for i in range(4):
                headers = response.css("h%s::text"%(i+1)).extract()
                for line in headers:
                    if not "OGN" in line and len(line) > 3:
                        file.write("h%s - "%(i+1)+line+"\n") 
            for line in response.css("p::text").extract(): 
                if "\n" not in line and len(line) > 20: 
                    file.write("p - "+line+"\n")