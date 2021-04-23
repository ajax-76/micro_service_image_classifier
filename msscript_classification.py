import tensorflow as tf
import numpy as np
from tensorflow import keras
from PIL import Image
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
import io
import uuid
from pymongo import MongoClient
import redis
import json
import os
import time

print('script is initialized')
redis_host = os.environ['REDIS_HOST']
redis_port = os.environ['REDIS_PORT']
redis_password = os.environ['REDIS_PASSWORD']
mongo_url = os.environ['MONGO_URL']

# print(mongo_url)

redis_client = redis.Redis(host=redis_host, port=redis_port, db=0,password = redis_password)
mongo_client = MongoClient(mongo_url)
db = mongo_client["YELLOW_BACKS_DB"]
col = db["PRODUCT"]

# redis_client = redis.Redis(host='204.48.30.159', port=6379, db=0,password = 'hB9i2REJQsuf+3uJfPMmdjQeU8tGdkMJUM4riZNRy+pGVwJ372DKIAsS9MRdAb5aoshL0EqJp1TQ621')
# mongo_client = MongoClient('mongodb://yb_debug_admin:ybdebug_101@68.183.88.220:27017/admin')
# db = mongo_client["YELLOW_BACKS_DB"]
# col = db["PRODUCT"]
#cache_value = redis_client.hgetall("cd47a360-9fa0-11eb-8b23-777c4db526b9")
#print(cache_value)

#val=col.find_one({"_id":"82960770-9fa6-11eb-bfbc-bddb9fd26dcd"})
#print(val)
p = redis_client.pubsub()
p.subscribe('product_upload_classifier')

while True:
    message = p.get_message()
    if message and not message['data'] == 1:
        cache_value = redis_client.hgetall(message["data"])
        if str(cache_value[b'step'].decode("utf-8"))=="2":
            import detectron as det
            import classification as clsf
            image_url = cache_value[b'image_url'].decode("utf-8")
            print(image_url)
            image_batch,image_details = det.crop_images(image_url)
            imageclassifierdetailslist = clsf.result(image_batch)
            #imageclassifierdetailslist=[]
            print("ml image processed")
            pid=message["data"].decode("utf-8")
            val=col.update_one({"_id":pid},{"$set":{"ml_classified_info":imageclassifierdetailslist,"check":True,"ml_detectron_info":image_details}})
            del_data= redis_client.delete(message["data"])
            print(del_data)
                # do something with the message
    time.sleep(0.001)  # be nice to the system :)



# for message in p.listen():
#     if message and not message['data'] == 1:
        


        # get product data and url 
    
# d =p.get_message()
# print(d)