import re
import datetime


class PropertyDetails:
    def __init__(
        self,
        id,
        date,
        location,
        region,
        type,
        price,
        bedrooms,
        agent,
        description,
        sold,
        datesold,
    ):
        self.id = id
        self.date = date
        self.location = location
        self.region = region
        self.type = type
        self.price = price
        self.bedrooms = bedrooms
        self.agent = agent
        self.description = description
        self.sold = sold
        self.datesold = datesold

    def get(self):
        return (
            self.id,
            self.date,
            self.location,
            self.region,
            self.type,
            self.price,
            self.bedrooms,
            self.agent,
            self.description,
            self.sold,
            self.datesold,
        )


class PropertyIndex:
    def __init__(self, propertyData, region):
        self.region = region
        self.index = propertyData.apply(self.createPropertyDetails, axis=1).tolist()

    def getIndex(self):
        return [details.get() for details in self.index]

    def createPropertyDetails(self, x):
        return PropertyDetails(
            id=self.parseId(x["url"]),
            date=datetime.date.today().strftime("%Y-%m-%d"),
            location=x["address"],
            region=self.region,
            type=x["type"].replace("for sale", ""),
            price=self.parsePrice(x["price"]),
            bedrooms=self.parseBedrooms(x["number_bedrooms"]),
            agent=self.parseAgent(x["agent_url"]),
            description=x["description"],
            sold="FREE",
            datesold=datetime.date.today().strftime("%Y-%m-%d"),
        )

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
