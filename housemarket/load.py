from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from sqlalchemy.orm import sessionmaker
import traceback


class HouseDatabase:
    def __init__(self, pw, host="127.0.0.1", port=3306, dbName="HOUSES", user="mysql"):
        url = URL.create(
            drivername="postgresql",
            username=user,
            host=host,
            database=dbName,
            password=pw,
            port=port,
        )

        self.engine = create_engine(url)
        self.session = sessionmaker(bind=self.engine)()

    def createTable(self, metadata):
        metadata.create_all(self.engine)

    def dropTable(self, metadata):
        metadata.create_all(self.engine)

    def addEntry(self, propertyDetails):
        try:
            self.session.add(propertyDetails)
            self.session.commit()
            print(propertyDetails)
        except Exception as e:
            print("Duplicate Entry")
            # traceback.print_exc()
