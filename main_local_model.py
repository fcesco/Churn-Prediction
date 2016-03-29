from churn import *
from models_comparison import *
from data_viz import *
impression_path = '/Users/Fra/Documents/Streamago/Streamago_churn_study/\
    churn_analysis/stream impression/'
edges_path = '/Users/Fra/Documents/Streamago/Streamago_churn_study/\
    churn_analysis/graph/notify.csv'

if __name__=="__main__":
    churn_days = 10

    stream_table, user_table = import_data()
    stream_table, user_table = filter_time(stream_table, user_table, churn_days)
    stream_table, user_table = drop_features(stream_table, user_table)
    user_table = clean_user(user_table)
    user_table = create_churn(user_table, churn_days)
    merged_data = stream_user_merging(stream_table, user_table)
    merged_data = impression_user_merging('/Users/Fra/Documents/Streamago/\
    Streamago_churn_study/churn_analysis/stream impression/', merged_data)
    # merged_data = merged_data.fillna(-1)
    # X, y, user_id = Xy_create(merged_data, 'churn', '_id')
    # X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y,
    #     test_size=0.3, random_state=0)
    # smox, smoy = smooting(X_train, y_train)
