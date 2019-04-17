import sys
from configparser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from swagger_server.models.social.models import *

parser = ConfigParser()
parser.read('swagger_server/models/social/connexion.ini')
POSTGRES_ENGINE = 'postgres://' + parser.get('postgres', 'username') + ':' + parser.get('postgres', 'password') \
                  + '@' + parser.get('postgres', 'host') + ':' + parser.get('postgres', 'port') \
                  + '/' + parser.get('postgres', 'database')
sys.path.append(parser.get('sys-path', 'exposures'))
engine = create_engine(POSTGRES_ENGINE)
Session = sessionmaker(bind=engine)
