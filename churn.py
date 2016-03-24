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
from unbalanced_dataset import SMOTE
from scipy.stats import randint as sp_randint
from sklearn import cross_validation


impression_column_name = ['time', 'distinct_id', 'app_release', 'app_version', 'carrier', 'city', 'ios_ifa', 'lib_version', 'manufacturer', 'model', 'name', 'os', 'os_version', 'radio', 'region',  'screen_height', 'screen_width', 'wifi', 'account_status', 'audio', 'broadcaster_id', 'broadcaster_name', 'candies_sent', 'comments_sent', 'facebook_post_id', 'mode', 'page',  'public', 'screen', 'stream_duration', 'stream_id', 'stream_message', 'type', 'video', 'views_on_join', 'facebook_id', 'gender', 'locale', 'mp_country_code', 'mp_device_model', 'mp_lib', 'elapsed', 'app_version', 'screen_dpi', 'brand']

stream_drop = ['_id', 'source_ip', 'page', 'created_at', 'title', 'text', 'message', 'friends', 'place', 'secret', 'base_uri', 'media_ring', 'bucket', 'video', 'audio', 'live', 'closed', 'stop_live_count', 'play_live_time', 'stop_vod_count', 'play_vod_time', 'size', 'live_at', 'origin_id', 'origin_ip', 'live_confirm_time', 'facebook_post_time', 'facebook_post_id', 'offline_at', 'closed_at', 'id', 'name', 'type', 'public', 'likes_views', 'time', 'short_url', 'device_locale', 'file_name']

user_drop = ['enabled', 'last_ip', 'latitude', 'longitude', 'fb_name', 'fb_email', 'fb_access_token', 'fb_extended_access_token', 'email', 'fb_expires_at', 'fb_issued_at', 'user_friends', 'latest_page', 'languages', 'device_locale', 'public_profile', 'secure_browsing','type', 'allowed_viewers', 'facebook_id', 'created_at','bucket','fb_locale']

impression_drop=['time','distinct_id','app_release','carrier','city','ios_ifa','lib_version','manufacturer','model','name','os',
'os_version','radio','region','screen_height','screen_width','wifi','account_status','audio','broadcaster_id','broadcaster_name','facebook_post_id','page','public','screen','stream_message','type','video','facebook_id','locale','mp_country_code','mp_device_model','mp_lib','elapsed','app_version','brand']

def drop_features(stream_table, user_table):
    '''
    drop feaures hardcoded in the function
    Args:
        user_table: table with user information
        stream_table: stream with streams information
    '''
    user_table = user_table[user_table['type']=='user']
    user_table.drop(user_drop, axis=1, inplace=True)
    stream_table.drop(stream_drop, axis=1, inplace=True)
    return stream_table, user_table

def drop_impression(impression):
    '''
    Drop not desired features from impression tables
    Arg:
        impression: impression table
    Return:
        impression table without not desired columns
    '''
    impression.drop(drop_list, axis=1, inplace=True)
    return impression

# def from_numpy_to_datetime(dt64):
#     ts = (dt64 - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
#     return datetime.utcfromtimestamp(ts)

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

def clean_user(df):
    '''
    Clean the user dataframe
    '''

    df = df[df['last_login'].notnull()]
    df['publish_actions'] = df['publish_actions'].replace([None],[-1])
    df['publish_actions'] = df['publish_actions'].astype(int)
    df = pd.get_dummies(df, columns = ['gender'])
    df = integerize(df, 'manage_pages')
    df = integerize(df, 'valid_token')
    df = integerize(df, 'public')
    df = integerize(df, 'publish_actions')
    return df

def stream_user_merging(stream, user):
    '''
    Merge stream information into the user table
    Args:
        stream: stream table
        user: user table
    Return:
        user: user table

    '''
    stream = pd.get_dummies(stream, columns = ['broadcaster'])
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

def impression_user_merging(impressions_folder, df):
    '''
    Merge impressions features with the df table
    Args:
        impression_folder: Path to the impression folder
        df: table of the df featuresa.
    Return:
        df table with the df
    '''

    total_candies_sent = pd.Series(name = 'candies_sent')
    total_comments_sent = pd.Series(name ='comments_sent')
    for (dirpath, dirnames, filenames) in walk(impressions_folder):
        filenames = [impressions_folder+filename for filename in filenames if not filename[0]=='.']
        for filename in filenames:
            impression = pd.read_table(filename, engine='python', header=None, names = impression_column_name)
            temp_candies_sent = impression.groupby(by='distinct_id')['candies_sent'].sum()
            temp_comments_sent = impression.groupby(by='distinct_id')['comments_sent'].sum()
            total_candies_sent = total_candies_sent.add(temp_candies_sent, fill_value=0)
            total_comments_sent = total_comments_sent.add(temp_comments_sent, fill_value=0)
    df = df.join(total_comments_sent, on = '_id')
    df = df.join(total_candies_sent, on = '_id')
    df['candies_sent'] = df['candies_sent'].fillna(-1)
    df['comments_sent'] = df['comments_sent'].fillna(-1)
    return df

def group_join(df_group, df_merge, by_column, column_group, merge_on, func):
    '''
    Group the first data frame using the function defined and then join it on
    the first declared dataframe.
    Args:
        df_group: Dataframe used for grouping purposes
        df_merge: Dataframe to merge with the dataframe grouped
        by_column: Column name used for the group by
        column_group: Column nane used for the grouping funcition
        merge_on: Column name used for the merging
        func: string which defines function to use for the grouping
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
    Change boolean values of dataframe column to integers replacing null values to -1.
    Join the result to df_merge
    Args:
        df: Pandas dataframe
        column: Column to integerize
        df_merge: Pandas dataframe to merge with column
    Return:
        df_merge: return the merged dataframe
    '''

    temp = df[column].replace([None], [-1], regex=True )

    #df[column].replace(, -1, inplace=True)
    df[column] = df[column].astype(int)
    df_merge.join(temp)
    return df_merge

def integerize(df, column):
    '''
    Change boolean values of dataframe column to integers replacing null values to -1.
    Args:
        df: Pandas dataframe
        column: Column to integerize
    Return:
        df_merge: return the merged dataframe
    '''

    df[column] = df[column].replace([None],[-1],regex=True)
    df[column] = df[column].astype(int)
    return df

def import_data():
    '''
    Query data from postgres database
    Args:
        None
    Return:
        streams: Table streams
        users: Table users
    '''
    conn = pg2.connect(database='Fra', user='Fra')
    cur = conn.cursor()
    stream_table = 'mongodb.stream'
    user_table = 'mongodb.user'
    streams = pdsql.read_sql("SELECT * FROM %s;" % stream_table, conn)
    users = pdsql.read_sql("SELECT * FROM %s;" % user_table, conn)
    return streams, users


# def create_node_value(churn_prob, user_id):
#     churn_prob = pd.DataFrame(data = {'user_id': user_id , 'churn_prob': churn_prob})
#     return churn_prob
#
#
# def weighted_edges(edges_file, impressions_folder, user):
#     '''
#     create weighted edges
#     '''
#     column = ['time', 'distinct_id', 'app_release', 'app_version', 'carrier', 'city', 'ios_ifa', 'lib_version', 'manufacturer', 'model', 'name', 'os', 'os_version', 'radio', 'region',  'screen_height', 'screen_width', 'wifi', 'account_status', 'audio', 'broadcaster_id', 'broadcaster_name', 'candies_sent', 'comments_sent', 'facebook_post_id', 'mode', 'page',  'public', 'screen', 'stream_duration', 'stream_id', 'stream_message', 'type', 'video', 'views_on_join', 'facebook_id', 'gender', 'locale', 'mp_country_code', 'mp_device_model', 'mp_lib', 'elapsed', 'app_version', 'screen_dpi', 'brand']
#     edges = pd.read_csv(edges_file)
#     edges = edges[edges.exists==True]
#     edges.insert(0, 'weight',1)
#     edges = edges[(edges.follower.isin(user.facebook_id.values)) & (edges.followed.isin(user.facebook_id.values))]
#     for (dirpath, dirnames, filenames) in walk(impressions_folder):
#         filenames = [impressions_folder+filename for filename in filenames if not filename[0]=='.']
#         for filename in filenames:
#             impression = pd.read_table(filename, engine='python', header=None, names =column)
#             edges['weight'] += edges.apply(lambda x: weight_edge(x, impression, user), axis = 1)
#     return edges
#
#
# def weight_edge(x, impression, user):
#     if any((impression['broadcaster_id'].isin(user[x['followed']==user['facebook_id']]['_id'])) & (impression['distinct_id'].isin(user[x['follower']==user['facebook_id']]['_id']))):
#         return 1
#     else: return 0

def Xy_create(df, column_y, column_id):
    '''
    Return X and y ready for the model and user_id to keep track of the users will churn.
    Args:
        df: Pandas dataframe
        column_y: column where there is endogenous variable
        column_id: column where there are users id
    Return:
        X: exogenous variable
        y: endogenous variable
        user_id: series of the user id

    '''
    y = df[column_y]
    df.drop(column_y, axis=1, inplace=True)
    user_id = df[column_id]
    df.drop(column_id, axis=1, inplace=True)
    X = df.values
    return X, y, user_id


def smooting(X,y):
    '''
    Smoote the dataset obtaining a balanced dataset
    Args:
        X: exogenous variable
        y: endogenous variable
    Return:
        smox: balaned exogenous variable
        smoy: balanced endogenous variable
    '''
    smote = SMOTE(ratio= float(np.count_nonzero(y_test==0)) / float(np.count_nonzero(y_test==1)), verbose=False, kind='regular')
    smox, smoy = smote.fit_transform(X,y)
    return smox, smoy

if __name__=="__main__":
    impression_path = '/Users/Fra/Documents/Streamago/Streamago_churn_study/stream impression/'
    edges_path = '/Users/Fra/Documents/Streamago/Streamago_churn_study/graph/notify.csv'
    stream_table, user_table = import_data()
    strem_table, user_table = drop_features(stream_table, user_table)
    user_table = clean_user(user_table)
    user_table = create_churn(user_table, 14)
    merged_data = stream_user_merging(stream_table, user_table)
    merged_data = impression_user_merging('/Users/Fra/Documents/Streamago/Streamago_churn_study/stream impression/', merged_data)
    merged_data = merged_data.fillna(-1)
    X, y, user_id = Xy_create(merged_data, 'churn', '_id')
    X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.3, random_state=0)
    smox, smoy = smooting(X_train_best, y_train)

    #
    # rndF = ensemble.RandomForestClassifier()
    # score = cross_validation.cross_val_score(rndF, X_train, y_train)
    # rndF.fit(X_train,y_train)
    # rndF.score(X_test, y_test)
    # #
    # param_dist = {"max_depth": [3, None],
    #           "max_features": sp_randint(1, 11),
    #           "min_samples_split": sp_randint(1, 11),
    #           "min_samples_leaf": sp_randint(1, 11),
    #           "bootstrap": [True, False],
    #           "criterion": ["gini", "entropy"]}
    #
    # n_iter_search = 20
    # random_search = RandomizedSearchCV(rndF, param_distributions=param_dist, n_iter=n_iter_search)
    # random_search.fit(X,y)
    # best_model = random_search.best_estimator_
    # best_features = best_model.feature_importances_.argsort()[::-1]
    # X_best = X[:,best_features[0:15]]
    # X_train_best = X_train[:, best_features[0:15]]
    # X_test_best = X_test[:, best_features[0:15]]
