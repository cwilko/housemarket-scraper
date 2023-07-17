from rightmove_webscraper import RightmoveData


class HouseScraper:
    def requestData(self, regionCode, maxPrice, maxBedrooms=3, maxDaysSinceAdded=None):
        age = ""
        if maxDaysSinceAdded is not None:
            age = f"&maxDaysSinceAdded={maxDaysSinceAdded}"
        url = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%{regionCode}&maxBedrooms={maxBedrooms}&maxPrice={maxPrice}&propertyTypes={age}&includeSSTC=true&mustHave=&dontShow=retirement&furnishTypes=&keywords="

        print(f"Loading data... {url}")
        return RightmoveData(url).get_results.drop_duplicates("url")
