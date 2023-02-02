from random import *
from pymongo import MongoClient
from bson.objectid import ObjectId
import logging
import pymongo.errors
import os
import gridfs
from cgitb import lookup
from pymongo import MongoClient
from faker import Faker
import time
import multiprocessing as mp
import numpy as np
import uuid
from random import randint
uid = uuid.uuid1()


def migration_logger(name):
    """ creates a logger object

    Args:
        name (string): log file name

    Returns:
        obj: retuns logger object after initialization
    """
    logger = logging.getLogger(name)
    logging.basicConfig(filename=name + '.log', level=logging.INFO,
                        format="%(levelname)s %(asctime)s-%(message)s")

    return logger


client = MongoClient(
    '<connection_string>')
db = client.fmisgrid3
data_files = gridfs.GridFS(db)
FILES_LOCATION = "<file_location>"
log_hm = migration_logger("migration")


def insert_grid_fs(faker, num):
    """ insert into grid fs collection

    Args:
        faker (obj): generates fake data
        num (int): to run the function in loop
    """
    for _ in range(num):
        text_info = faker.lexify(
            text='????????????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        file_name = str(uuid.uuid4()) + ".txt"
        file_id = faker.numerify(text='##%###%###%##%##%')
        client_id = randint(1, 100)
        """TODO - Use bulk insert in for loop
        """
        insert_data = data_files.put(
            text_info, encoding='utf-8', filename=file_name, clientId=client_id)


def fetch_grid_fs(limit):
    """fetches the grid fs record

    Args:
        limit (int): number of records to fetch
    """
    data = db.fs.files.find({}, {"_id": 1, "clientId": 1, "filename": 1}).sort(
        "_id", pymongo.DESCENDING).limit(limit)
    for i in data:
        file_name = i["filename"]
        destination = FILES_LOCATION + "/" + str(i["clientId"])
        save_file(file_name, i['_id'], destination)


def save_file(file_name, _id, destination):
    """ creates file with gridfs data

    Args:
        file_name (str): filename
        _id (objectId): objectId of file
        destination (string): file destination
    """
    try:
        if not os.path.exists(destination):
            os.makedirs(destination)
        with open(destination + "/" + file_name, 'w') as f:
            f.write(str(data_files.get(_id).read()))
            log_hm.info("File with _id  : " + str(_id) + " and name " +
                        file_name + " migrated to " + destination)

    except Exception as e:
        print(str(e))
        logger = logging.getLogger()
        log_hm.error(str(_id) + " :: " + str(file_name) + " :: " + str(e))


def start_processor(k):
    for _ in range(1, k):
        pool = mp.Pool(mp.cpu_count())
        params = np.random.random((10, 3)) * 100.0
        ts = time.time()
        for i in range(0, params.shape[0]):
            pool.apply_async(insert_grid_fs, args=(fake, i))
        pool.close()
        pool.join()
        count = db['fs.chunks'].count_documents({})
        print('Number of documents inserted: ', count)


if __name__ == '__main__':
    fake = Faker()

    # use fetch_grid_fs to fetch and save files
    fetch_grid_fs(10)

    # to insert data into grid fs for testing
    # start_processor(10000)
