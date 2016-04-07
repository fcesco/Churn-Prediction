from datetime import timedelta
import pandas as pd
import numpy as np
import seaborn as sns
from datetime import datetime
import statsmodels.api as sm
import statsmodels.api as sm
import psycopg2 as pg2
import pandas.io.sql as pdsql
from statsmodels import tsa
from os import walk
import operator
from scipy.stats import randint as sp_randint
from sklearn import cross_validation
from collections import Counter


#It is needed to add it because in the impression tables there are no
#columns' name
IMPRESSION_COLUMN_NAME = ['time', 'distinct_id', 'app_release', 'app_version', 'carrier', 'city', 'ios_ifa', 'lib_version', 'manufacturer', 'model', 'name', 'os', 'os_version', 'radio', 'region',  'screen_height', 'screen_width', 'wifi', 'account_status', 'audio', 'broadcaster_id', 'broadcaster_name', 'candies_sent', 'comments_sent', 'facebook_post_id', 'mode', 'page',  'public', 'screen', 'stream_duration', 'stream_id', 'stream_message', 'type', 'video', 'views_on_join', 'facebook_id', 'gender', 'locale', 'mp_country_code', 'mp_device_model', 'mp_lib', 'elapsed', 'app_version', 'screen_dpi', 'brand']

STREAM_DROP = ['_id', 'source_ip', 'page', 'created_at', 'title', 'text', 'message', 'friends', 'place', 'secret', 'base_uri', 'media_ring', 'bucket', 'video', 'audio', 'live', 'closed', 'stop_live_count', 'play_live_time', 'stop_vod_count', 'play_vod_time', 'size', 'live_at', 'origin_id', 'origin_ip', 'live_confirm_time', 'facebook_post_time', 'facebook_post_id', 'offline_at', 'closed_at', 'id', 'name', 'type', 'public', 'likes_views', 'time', 'short_url', 'device_locale', 'file_name']

USER_DROP = ['max_duration', 'session_duration', 'max_width', 'max_height', 'max_bitrate', 'max_video_duration', 'max_audio_duration','enabled', 'last_ip', 'latitude', 'longitude', 'fb_name', 'fb_email', 'fb_access_token', 'fb_extended_access_token', 'email', 'fb_expires_at', 'fb_issued_at', 'user_friends', 'latest_page', 'languages', 'device_locale', 'public_profile', 'secure_browsing', 'type', 'allowed_viewers', 'created_at', 'bucket', 'fb_locale','valid_token', 'public']

IMPRESSION_DROP = ['time', 'distinct_id', 'app_release', 'carrier', 'city', 'ios_ifa', 'lib_version', 'manufacturer', 'model', 'name', 'os', 'os_version', 'radio', 'region', 'screen_height', 'screen_width', 'wifi', 'account_status', 'audio', 'broadcaster_id', 'broadcaster_name', 'facebook_post_id', 'page', 'public', 'screen', 'stream_message', 'type', 'video', 'facebook_id', 'locale', 'mp_country_code', 'mp_device_model', 'mp_lib', 'elapsed', 'app_version', 'brand']

def drop_features(stream_table, user_table):
    '''
    drop feaures hardcoded in the function
    Args:
        stream_table: stream containing streams information (Pandas DataFrame)
        user_table: table with containing information (Pandas DataFrame)
    Return:
        stream_table: stream containing streams information without not
            significant values (pandas DataFrame)
        user_table: table containing user information without not
            significant (Pandas DataFrame)
    '''

    user_table = user_table[user_table['type'] == 'user']
    user_table.drop(USER_DROP, axis=1, inplace=True)
    stream_table.drop(STREAM_DROP, axis=1, inplace=True)
    return stream_table, user_table


def drop_impression(impression):
    '''
    Drop not desired features from impression tables
    Arg:
        impression: impression table (pandas DataFrame)
    Return:
        impression table without not desired columns (pandas DataFrame)
    '''

    impression.drop(drop_list, axis=1, inplace=True)
    return impression


def create_churn(df, limit):
    '''
    Define churn column using the limit in input and return the modified
    dataframe
    Args:
        df: dataframe containing user informations (pandas DataFrame)
        limit: day to define churn in integers (int)
    Return:
        df dataframe containing user information and whether or not is churn
            (pandas DataFrame)
    '''
    max_date = df['last_login'].max()
    limit_churn = max_date - np.timedelta64(limit, 'D')
    df['churn'] = (df['last_login'] < limit_churn).astype(int)
    return df


def filter_time(stream, user, days):
    '''
    Limit informations of the users and streams in order to simulate that we do
    not know about the future.
    Args:
        stream: streams dataframe (pandas DataFrame)
        user: users dataframe (pandas DataFrame)
        days: days we want to cut our information (int)
    Return:
        stream: streams dataframe limited on informations (pandas DataFrame)
        user: users dataframe with limited informations (pandas DataFrame)
    '''

    max_date = user['last_login'].max()
    upper_limit_date = max_date - np.timedelta64(days, 'D')
    lower_limit_date = max_date - np.timedelta64(days*2, 'D')
    user = user[user['created_at'] < upper_limit_date]
    stream = stream[stream['created_at'] < upper_limit_date]
    #we take user that did not already churn
    user = user[user['last_login'] > lower_limit_date]
    return stream, user


def clean_user(df):
    '''
    Clean the user dataframe
    Args:
        df: user dataframe (pandas DataFrame)
    Return:
        df: cleaned user dataframe (pandas DataFrame)
    '''
    df.facebook_id = df.facebook_id.astype(int)
    df = df[df['last_login'].notnull()]
    df['publish_actions'] = df['publish_actions'].replace([None], [-1])
    df['publish_actions'] = df['publish_actions'].astype(int)
    df = pd.get_dummies(df, columns=['gender'])
    df.drop('gender_female', axis=1, inplace=True)
    df = integerize(df, 'manage_pages')
    df = integerize(df, 'publish_actions')
    df.drop('last_login', axis=1, inplace=1)
    return df


def stream_user_merging(stream, user):
    '''
    Merge stream information into the user table
    Args:
        stream: stream table (pandas DataFrame)
        user: user table (pandas DataFrame)
    Return:
        user: user table (pandas DataFrame)
    '''
    stream = pd.get_dummies(stream, columns=['broadcaster'])
    stream = integerize(stream, 'mux')
    user = group_join(stream, user, 'user_id', 'mux', '_id', 'sum')
    user = group_join(stream, user, 'user_id', 'width', '_id', 'max')
    user = group_join(stream, user, 'user_id', 'height', '_id', 'max')
    user = group_join(stream, user, 'user_id', 'bit_rate', '_id', 'mean')
    user = group_join(stream, user, 'user_id', 'saved', '_id', 'sum')
    user = group_join(stream, user, 'user_id', 'play_vod_count', '_id', 'sum')
    user = group_join(stream, user, 'user_id', 'play_live_count', '_id', 'sum')
    user = group_join(stream, user, 'user_id', 'publish_count', '_id', 'mean')
    user = group_join(stream, user, 'user_id', 'unpublish_count', '_id', 'mean')
    user = group_join(stream, user, 'user_id', 'duration', '_id', 'sum')
    user = group_join(stream, user, 'user_id', 'save_count', '_id', 'sum')
    user = group_join(stream, user, 'user_id', 'comments_count', '_id', 'sum')
    user = group_join(stream, user, 'user_id', 'likes_count', '_id', 'sum')
    user = group_join(stream, user, 'user_id', 'deleted', '_id', 'mean')
    user = group_join(stream, user, 'user_id', 'facebook_comments', '_id', 'sum')
    user = group_join(stream, user, 'user_id', 'facebook_likes', '_id', 'sum')
    user = group_join(stream, user, 'user_id', 'comments', '_id', 'sum')
    user = group_join(stream, user, 'user_id', 'likes', '_id', 'sum')
    user = group_join(stream, user, 'user_id', 'wait', '_id', 'sum')
    user = group_join(stream, user, 'user_id', 'calls', '_id', 'sum')
    user = user.fillna(-1)
    return user

    for (dirpath, dirnames, filenames) in walk(impression_path):
        filenames = [impression_path+filename for filename in filenames if
        not filename[0] == '.']


def impression_user_merging(impressions_folder, df, churn_days):
    '''
    Merge impressions features with the df table
    Args:
        impression_folder: Path to the impression folder (string)
        df: table of the df features (pandas DataFrame)
    Return:
        df: table with impression table (pandas DataFrame)
    '''
    total_candies_sent = pd.Series(name='candies_sent')
    total_comments_sent = pd.Series(name='comments_sent')
    limit_date = df['last_login'].max() - np.timedelta64(churn_days, 'D')
    for (dirpath, dirnames, filenames) in walk(impressions_folder):
        filenames = [impressions_folder+filename for filename in filenames if
        not filename[0] == '.']
        for filename in filenames:
            date = datetime.strptime(filename[-12:-4], '%Y%m%d')
            if date < limit_date:
                impression = pd.read_table(filename, engine='python', header=None,
                    names=IMPRESSION_COLUMN_NAME)
                temp_candies_sent = impression.groupby(by='distinct_id')\
                ['candies_sent'].sum()
                temp_comments_sent = impression.groupby(by='distinct_id')\
                ['comments_sent'].sum()
                total_candies_sent = total_candies_sent.add(temp_candies_sent,
                    fill_value=0)
                total_comments_sent = total_comments_sent.add(temp_comments_sent,
                    fill_value=0)
    df = df.join(total_comments_sent, on='_id')
    df = df.join(total_candies_sent, on='_id')
    df['candies_sent'] = df['candies_sent'].fillna(-1)
    df['comments_sent'] = df['comments_sent'].fillna(-1)
    return df


def group_join(df_group, df_merge, by_column, column_group, merge_on, func):
    '''
    Group the first data frame using the function defined and then join it on
    the first declared dataframe.
    Args:
        df_group: dataframe used for grouping purposes (pandas DataFrame)
        df_merge: dataframe to merge with the dataframe grouped (pandas DataFrame)
        by_column: column name used for the group by (string)
        column_group: column nane used for the grouping funcition (string)
        merge_on: column name used for the merging (string)
        func: string which defines function to use for the grouping (string)
    Return:
        df_merge: dataframe with added information (pandas DataFrame)
    '''

    if func == 'sum':
        temp = df_group.groupby(by=by_column)[column_group].sum()
    elif func == 'min':
        temp = df_group.groupby(by=by_column)[column_group].min()
    elif func == 'max':
        temp = df_group.groupby(by=by_column)[column_group].max()
    elif func == 'mean':
        temp = df_group.groupby(by=by_column)[column_group].mean()
    df_merge = df_merge.join(temp, on=merge_on)
    return df_merge


def integerize_join(df, column, df_merge):
    '''
    Change boolean values of dataframe column to integers replacing null values
    to -1.
    Join the result to df_merge
    Args:
        df: dataframe (pandas DataFrame)
        column: column to integerize (string)
        df_merge: dataframe to merge with column (pandas DataFrame)
    Return:
        df_merge: return the merged dataframe (pandas DataFrame)
    '''

    temp = df[column].replace([None], [-1], regex=True)
    df[column] = df[column].astype(int)
    df_merge.join(temp)
    return df_merge


def integerize(df, column):
    '''
    Change boolean values of dataframe column to integers replacing null values
    to -1.
    Args:
        df: dataframe (pandas DataFrame)
        column: column to integerize (string)
    Return:
        df_merge: return the merged dataframe (pandas Dataframe)
    '''
    df[column] = df[column].replace([None], [-1], regex=True)
    df[column] = df[column].astype(int)
    return df


def import_data():
    '''
    Query data from postgres database
    Args:
        None
    Return:
        streams: table streams (pandas DataFrame)
        users: table users (pandas DataFrame)
    '''
    conn = pg2.connect(database='Fra', user='Fra')
    cur = conn.cursor()
    stream_table = 'mongodb.stream'
    user_table = 'mongodb.user'
    streams = pdsql.read_sql("SELECT * FROM %s;" % stream_table, conn)
    users = pdsql.read_sql("SELECT * FROM %s;" % user_table, conn)
    return streams, users


def n_connections(edges_path, df):
    '''
    Add number of followers and following
    Args:
        edges_path: path to the edges file (string)
        df: dataframe which contains users and stream values (pandas DataFrame)
    Return:
        df: dataframe with connections information (pandas DataFrame)
    '''
    edges = pd.read_table(edges_path, sep = ',')
    edges = edges[edges.exists == True]
    following = Counter(edges.follower.values)
    followed = Counter(edges.followed.values)
    following = pd.Series(following, name='following')
    followed = pd.Series(followed, name='followed')
    df = df.join(following, on='facebook_id')
    df = df.join(followed, on='facebook_id')
    return df



def Xy_create(df, column_y, column_id, column_facebook_id):
    '''
    Return X and y ready for the model and user_id to keep track of the users
    will churn.
    Args:
        df: data frame (pandas DataFrame)
        column_y: column where there is endogenous variable (string)
        column_id: column where there are users id (string)
    Return:
        X: exogenous variable (numpy matrix)
        y: endogenous variable (numpy matrix)
        user_id: serie of the user id (pandas Serie)
    '''
    y = df[column_y]
    df.drop(column_y, axis=1, inplace=True)
    user_id = df[column_id]
    facebook_id = df[column_facebook_id]
    df.drop(column_facebook_id, axis=1, inplace=True)
    df.drop(column_id, axis=1, inplace=True)
    X = df.values
    return X, y, user_id, facebook_id
