from TwitterAPI import TwitterAPI
from sqlalchemy import create_engine
#Secret API codes
API_KEY = 'AFuNXw2BOSv2q6CaFHVt7J203'
API_SECRET = 'htKlqfNY66HjDbl1QgV3aoVmb8MSQfUdjeIGtAIiZFJUXLu65B'
ACCESS_TOKEN = '3195815604-1IpIGAHQ4gf8QtcyIpN5QExtP3Puu2QymFNMKLv'
ACCESS_TOKEN_SECRET = '3mYL1exnSAkC2wieSHAteDdGvFuB0DMV4bVytagT2eh2i'
db_string = 'postgres://qezrrpjrtqszjx:c449456bd12b16ce08aa06c05efbce571aa32587194a742e282d81a263a02176@ec2-107-20-133-82.compute-1.amazonaws.com:5432/darb70iqk42ige'

def get_api():
    api = TwitterAPI(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return api
def get_db():
    db = create_engine(db_string)
    return db
