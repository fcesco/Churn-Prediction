
 #  ____  ____   _    ____  _  __
 # / ___||  _ \ / \  |  _ \| |/ /
 # \___ \| |_) / _ \ | |_) | ' /
 #  ___) |  __/ ___ \|  _ <| . \
 # |____/|_| /_/   \_\_| \_\_|\_\

# You need to start your pyspark or pyspark notebook calling the databricks library:
# pyspark notebook: IPYTHON_OPTS="notebook --ip=0.0.0.0" /root/spark/bin/pyspark --packages com.databricks:spark-csv_2.10:1.1.0 --executor-memory 4G --driver-memory 4G &
# pyspark:  pyspark --packages com.databricks:spark-csv_2.10:1.2.0

import pandas as pd
import numpy as np
from datetime import timedelta
from datetime import datetime
#import statsmodels.api as sm
#from statsmodels import tsa
from os import walk
from pyspark import SparkContext
from pyspark.mllib.classification import LogisticRegressionWithSGD
from pyspark.ml import tuning
from pyspark.ml import Pipeline
from pyspark.mllib.tree import RandomForest, RandomForestModel
import json
import boto
import pandas as pd
from pyspark.sql import SQLContext
from pyspark.sql.types import *
from pyspark import SparkContext


def drop_columns(df, list_columns):
    for column in list_columns:
        df = df.drop(column)
    return df

def drop_features(stream_table, user_table):
    '''
    drop feaures hardcoded in the function
    Args:
        user_table: table with user information
        stream_table: stream with streams information
    '''

    stream_drop = ['_id', 'source_ip', 'page', 'created_at', 'title', 'text', 'message',\
                   'friends', 'place', 'secret', 'base_uri', 'media_ring', 'bucket', 'video', \
                   'audio', 'live', 'closed', 'stop_live_count', 'play_live_time', 'stop_vod_count',\
                   'play_vod_time', 'size', 'live_at', 'origin_id', 'origin_ip', 'live_confirm_time', \
                   'facebook_post_time', 'facebook_post_id', 'offline_at', 'closed_at', 'id', 'name', 'type', \
                   'public', 'likes_views', 'time', 'short_url', 'device_locale', 'file_name']

    user_drop = ['enabled', 'last_ip', 'latitude', 'longitude', 'fb_name', 'fb_email', \
                 'fb_access_token', 'fb_extended_access_token', 'email', 'fb_expires_at', 'fb_issued_at', \
                 'user_friends', 'latest_page', 'languages', 'device_locale', 'public_profile', 'secure_browsing',\
                 'type', 'allowed_viewers', 'facebook_id', 'created_at','bucket','fb_locale']

    user_table = user_table[user_table['type']=='user']
    user_table = drop_columns(user_table, user_drop)
    stream_table = drop(stream_table, stream_drop)
    return stream_table, user_table

def drop_impression(impression):
    '''
    Drop not desired features from impression tables
    Arg:
        impression: impression table
    Return:
        impression table without not desired columns
    '''

    drop_list = ['time','distinct_id','app_release','carrier','city','ios_ifa','lib_version','manufacturer','model','name','os','os_version','radio','region','screen_height','screen_width','wifi','account_status','audio','broadcaster_id','broadcaster_name','facebook_post_id','page','public','screen','stream_message','type','video','facebook_id','locale','mp_country_code','mp_device_model','mp_lib','elapsed','app_version','brand']
    impression = drop_columns(impression, drop_list)
    return impression

def create_churn(df, limit):
    '''
    Define churn column using the limit in input and return the modified dataframe
    Args:
        df: dataframe
        limit: day to define churn in integers
    Return:
        df
    '''

    max_date = df['last_login'].max()
    limit_churn = max_date - np.timedelta64(limit, 'D')
    df['churn'] = (df['last_login'] < limit_churn).astype(int)
    df.drop('last_login', axis=1, inplace=1)
    return df



if __name__=='__main__':
    sc = SparkContext()
    sqlContext = SQLContext(sc)
