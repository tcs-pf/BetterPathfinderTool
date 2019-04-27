import scrapy

class ClassSpider(scrapy.Spider):
    name = "ClassSpider"
    download_delay = 10
    start_urls=[
        "https://d20pfsrd.com/classes/core-classes/cleric"
    ]

    def parse(self, response):
        pageparts = response.url.split("/")
        pagetitle = pageparts[-1]
        if(len(pagetitle) < 3):
            pagetitle = pageparts[-2]
        filename = "classes-" + pagetitle
        with open("export-%s.txt"%filename, "w") as file:
            file.write(response.url + "\n")
            for i in range(4):
                headers = response.css("h%s::text"%(i+1)).extract()
                for line in headers:
                    if not "OGN" in line and len(line) > 3:
                        file.write("h%s - "%(i+1)+line+"\n") 
            for line in response.css("p ::text").extract(): 
                if "\n" not in line and len(line) > 2: 
                    file.write("p - "+line+"\n")
        resp = response.css("li > a::attr(href)").extract()
        for line in resp:
            if "http://www.d20pfsrd.com/classes/core-classes" in line and not pagetitle in line and len(line.split("/")) == 7:
                self.log("***Working link at %s"%line)    
                try:
                    pageparts = response.url.split("/")
                    spot = -1
                    if(len(pagetitle) < 3):
                        spots=-2
                    filename = "classes-" + pageparts[spots]
                    f = open("export-%s.txt"%filename, "r")
                    self.log("This file %s already exists!"%filename)
                except:
                    yield response.follow(line, callback=self.parse_second)
            else:
                self.log("Failed to use %s"%line)

            
    def parse_second(self, response):
        pageparts = response.url.split("/")
        pagetitle = pageparts[-1]
        if(len(pagetitle) < 3):
            pagetitle = pageparts[-2]
        filename = "classes-" + pagetitle
        with open("export-%s.txt"%filename, "w") as file:
            file.write(response.url + "\n")
            for i in range(4):
                headers = response.css("h%s::text"%(i+1)).extract()
                for line in headers:
                    if not "OGN" in line and len(line) > 3:
                        file.write("h%s - "%(i+1)+line+"\n") 
            for line in response.css("p ::text").extract(): 
                if "\n" not in line and len(line) > 2: 
                    file.write("p - "+line+"\n")