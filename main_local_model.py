from churn import *
from models_comparison import *
from data_viz import *
from models_comparison import *

IMPRESSION_PATH = '/Users/Fra/Documents/Streamago/Streamago_churn_study/\
churn_analysis/stream impression/'

EDGES_PATH = '/Users/Fra/Documents/Streamago/Streamago_churn_study/\
churn_analysis/graph/notify.csv'

DECISION_TREE_PARAMS = {"max_depth": [9,7,5,3, None],
                          "max_features": sp_randint(1, 11),
                          "min_samples_split": sp_randint(1, 11),
                          "min_samples_leaf": sp_randint(1, 11),
                          "max_leaf_nodes" : [1,2,3,4,5,6,7,8, None]}

RANDOM_FOREST_PARAMS = {"max_depth": [9,7,5,3, None],
                              "max_features": sp_randint(1, 11),
                              "min_samples_split": sp_randint(1, 11),
                              "min_samples_leaf": sp_randint(1, 11),
                              "bootstrap": [True, False],
                              "criterion": ["gini", "entropy"]}

SDG_PARAMS = {"loss" : ['hinge', 'log', 'modified_huber','squared_hinge'],
                        "penalty" : ['l2', 'l1', 'elasticnet'],
                         "alpha": list(np.arange(0.000001, 10, 0.00001))}

GRADIENT_BOOST_PARAMS = {"loss": ['deviance', 'exponential'],
                            "learning_rate": list(np.arange(0.01, 10, 0.8)),
                            "n_estimators": range(10, 100, 10),
                            "max_depth": range(1, 10, 1),
                            "min_samples_split": [2, 4, 6],
                            "min_samples_leaf": [1, 2, 4, 5]}

if __name__=="__main__":
    #Data Munging / Feature engineering
    churn_days = 10
    stream_table, user_table = import_data()
    user_table = create_churn(user_table, churn_days)
    stream_table, user_table = filter_time(stream_table, user_table, churn_days)
    user_table = impression_user_merging(IMPRESSION_PATH, user_table, churn_days)
    stream_table, user_table = drop_features(stream_table, user_table)
    user_table = clean_user(user_table)
    merged_table = stream_user_merging(stream_table, user_table)
    merged_table = n_connections(EDGES_PATH, merged_table)
    merged_table = merged_table.fillna(-1)


    #Data visualization




    #X, y, user_id, facebook_id = Xy_create(merged_table, 'churn', '_id', 'facebook_id')

    #Models Comparison
    # tree_param = ModelParams(DecisionTreeClassifier(), DECISION_TREE_PARAMS)
    # rndF_param = ModelParams(RandomForestClassifier(), RANDOM_FOREST_PARAMS)
    # sdg_param = ModelParams(SGDClassifier(), SDG_PARAMS)
    # grd_param = ModelParams(GradientBoostingClassifier(), GRADIENT_BOOST_PARAMS)
    # models = [tree_param, rndF_param, sdg_param, grd_param]
    # model_comparator = ModelComparator(models, X, y, 'recall')
    # model_comparator.compare_models()
