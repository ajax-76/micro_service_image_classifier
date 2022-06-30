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
import sys

print('script is initialized')
redis_host = os.environ['REDIS_HOST']
redis_port = os.environ['REDIS_PORT']
redis_password = os.environ['REDIS_PASSWORD']
mongo_url = os.environ['MONGO_URL']

# print(mongo_url)

redis_client = redis.Redis(host=redis_host, port=redis_port, db=0,password = redis_password)
mongo_client = MongoClient(mongo_url)
db = mongo_client["YELLOW_BACKS_DB"]
p = redis_client.pubsub()
p.subscribe('product_upload_classifier')

while True:
    message = p.get_message()
    if message and not message['data'] == 1:
        cache_value = redis_client.hgetall(message["data"])
        console.log(cache_value)
        col = db[cache_value[b'type']+"_products"]
        if str(cache_value[b'step'].decode("utf-8"))=="2":
            try:
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
            except:
                print('error')  
                del_data= redis_client.delete(message["data"])  
            #os.execv(sys.executable, ['python3'] + sys.argv)
                # do something with the message
    time.sleep(0.001)  # be nice to the system :)



# for message in p.listen():
#     if message and not message['data'] == 1:
        


        # get product data and url 
    
# d =p.get_message()
# print(d)
