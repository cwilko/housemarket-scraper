import psycopg2


class HouseDatabase:
    def __init__(self, pw, host="127.0.0.1", port=3306, dbName="HOUSES", user="mysql"):
        self.db = psycopg2.connect(
            user=user, host=host, port=port, password=pw, database=dbName
        )
        self.cursor = self.db.cursor()

    def createTable(self, tableName):
        try:
            self.cursor.execute(
                f"""CREATE TABLE %s ( 
                ID VARCHAR(10) NOT NULL, 
                DATE DATE NOT NULL, 
                LOCATION VARCHAR(128) NOT NULL, 
                REGION VARCHAR(64),
                TYPE VARCHAR(32) NOT NULL,
                PRICE VARCHAR(16) NOT NULL,
                BEDROOMS VARCHAR(32) NOT NULL,
                AGENT VARCHAR(64) NOT NULL,
                DESCRIPTION VARCHAR(512) NOT NULL,
                SOLD CHAR(4),
                DATESOLD DATE NOT NULL,
                PRIMARY KEY(ID)            
                )"""
                % tableName
            )
        except:
            print(f"Table {tableName} already exists")

    def deleteTable(self, tableName):
        self.cursor.execute(f"""DROP TABLE %s""" % tableName)

    def addEntry(self, tableName, propertyDetails):
        try:
            sql = (
                f"INSERT INTO { tableName } "
                f"(ID,DATE,LOCATION,REGION,TYPE,PRICE,BEDROOMS,AGENT,DESCRIPTION,SOLD,DATESOLD) "
                f"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            )

            val = propertyDetails.get()

            self.cursor.execute(sql, val)
            self.db.commit()
            print(propertyDetails)
        except Exception as e:
            print("Duplicate Entry")

    def addEntries(self, tableName, propertyIndex):
        sql = (
            f"INSERT INTO { tableName } "
            f"(ID,DATE,LOCATION,REGION,TYPE,PRICE,BEDROOMS,AGENT,DESCRIPTION,SOLD,DATESOLD) "
            f"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        )

        val = [propertyDetails.get() for propertyDetails in propertyIndex.index]

        self.cursor.executemany(sql, val)
        self.db.commit()

    def getAll(self, tableName):
        self.cursor.execute(f"SELECT * FROM {tableName}")
        return [x for x in self.cursor.fetchall()]
