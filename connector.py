import pymongo
from dotenv import load_dotenv
load_dotenv()
import os
from pymongo import MongoClient
   
def connect():
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    client = pymongo.MongoClient("mongodb+srv://"+ user +":"+ password +"@cluster0-doqes.mongodb.net/test?retryWrites=true&w=majority")
    return client.DataProject