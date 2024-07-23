import html2text
import configparser
import sqlalchemy as sa
import pandas as pd

##### PATHS  #####
CHROMA_DATA_PATH='chroma_db'

# Parser
PARSER = html2text.HTML2Text()
PARSER.ignore_links = False

##### Create db engine #######
# config = configparser.ConfigParser()

#read the config file:
# config.read("db.config")
# db = config['DB']

#3306: default MySQL port:
# con_string = f"mysql+mysqlconnector://{db.get('user')}:{db.get('pw')}@{db.get('host')}:3306/{db.get('schema')}"
#ENGINE = sa.create_engine(con_string, echo=True)
