import re
import datetime


class PropertyIndex:
    def __init__(self, propertyData, region):
        self.region = region
        self.index = propertyData.apply(self.createPropertyDict, axis=1).tolist()

    def getDict(self):
        return {v["id"]: v for v in self.index}

    def createPropertyDict(self, x):
        return {
            "id": str(self.parseId(x["url"])),
            "created_on": datetime.date.today().strftime("%Y-%m-%d"),
            "location": x["address"],
            "region": self.region,
            "type": x["type"].replace("for sale", ""),
            "price": self.parsePrice(x["price"]),
            "bedrooms": self.parseBedrooms(x["number_bedrooms"]),
            "agent": self.parseAgent(x["agent_url"]),
            "description": x["description"],
            "sold": "FREE",
            "sold_on": datetime.date.today().strftime("%Y-%m-%d"),
        }

    def parseRegion(self, region):
        if str(region) == "nan":
            region = "Unknown"
        return region

    def parsePrice(self, price):
        if str(price) == "nan":
            price = 0
        return price

    def parseId(self, url):
        # use the regex to find the integer in the string
        match = re.search("(?<=\/)\d+(?=#)", url)
        # if there is a match, return the integer as an int
        if match:
            return int(match.group())
        # otherwise, return None
        else:
            return None

    def parseAgent(self, url):
        if url is None:
            return "No Agent"
        # Define a regex pattern that matches the 3rd path section of a url
        # The pattern consists of four groups:
        # - The first group matches the protocol (http, https, ftp) followed by ://
        # - The second group matches the domain name and any subdomains
        # - The third group matches the first section of the path, which is anything after the first / and before the next /
        # - The fourth group matches the 3rd path section of the url, which is anything after the second / and before the third / or the end of the string
        pattern = r"http://([^/]+)/([^/]+)/([^/]+)/([^/]+)(/|$)"

        # Use re.search to find the first match of the pattern in the url
        match = re.search(pattern, url)

        # If there is a match, return the 4th group, which is the 3rd path section of the url
        if match:
            return match.group(4)
        else:
            return None

    def parseBedrooms(self, bedrooms):
        try:
            i = int(bedrooms)
            return i
        except ValueError:
            return 0
