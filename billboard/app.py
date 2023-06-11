import pandas as pd
import logging
from leapcell import Leapcell, LeapcellField
import sys
leapclient = Leapcell("http://localhost:8080", "xxx")
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def process_table(year):
    df = pd.read_csv('rwd-billboard-data/data-process/billboard200/billboard-200-{}.csv'.format(year))
    table = leapclient.table(
        "test1/myproject", table_id="1667524261138726912", field_type="name")
    # date,title,artist,current,previous,peak,weeks
    for index, row in df.iterrows():
        data = {
            "date": row["date"],
            "title": row["title"],
            "artist": row["artist"],
            "current": row["current"],
            "previous": row["previous"],
            "peak": row["peak"],
            "weeks": row["weeks"],
            "year": year
        }
        table.create(data)
        logging.info("Insert %s", data)
        
