from feature_engineering import *
from models_comparison import *
from data_viz import *

IMPRESSION_PATH = '/Users/Fra/Documents/Streamago/Streamago_churn_study/\
churn_analysis/stream impression/'

EDGES_PATH = '/Users/Fra/Documents/Streamago/Streamago_churn_study/\
churn_analysis/graph/notify.csv'


RANDOM_FOREST_PARAMS = {"max_depth": [9,7,5,3, None],
                              "max_features": sp_randint(1, 11),
                              "min_samples_split": sp_randint(1, 11),
                              "min_samples_leaf": sp_randint(1, 11),
                              "bootstrap": [True, False],
                              "n_estimators": range(10, 200, 10),
                              "criterion": ["gini", "entropy"]
                              }

EXTRA_TREES_PARAMS = {"n_estimators": range(10, 200, 10),
                        "max_features": sp_randint(1, 11),
                        "max_depth": range(1, 10, 1),
                        "min_samples_split": [2, 4, 6],
                        "min_samples_leaf": [1, 2, 4, 5]
                        }

GRADIENT_BOOST_PARAMS = {"loss": ['deviance', 'exponential'],
                            "learning_rate": list(np.arange(0.01, 0.8, 0.1)),
                            "n_estimators": range(10, 200, 10),
                            "max_depth": range(1, 10, 1),
                            "min_samples_split": [2, 4, 6],
                            "min_samples_leaf": [1, 2, 4, 5]
                            }

SVM = {"C": list(np.arange(0.01, 1, 0.05)),
                            "kernel": ['poly', 'rbf', 'sigmoid'],
                            "degree": range(3, 10, 1),
                            "coef0": list(np.arange(0.01, 2, 0.1))
                            }

def data_munging_engineering():
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
    return merged_table

def model_choice(merged_table):
    X, y, user_id, facebook_id = Xy_create(merged_table, 'churn', '_id', 'facebook_id')
    rndF_param = ModelParams(RandomForestClassifier(), RANDOM_FOREST_PARAMS, 'Random Forest')
    extra_param = ModelParams(ExtraTreesClassifier(), EXTRA_TREES_PARAMS, 'extra')
    grd_param = ModelParams(GradientBoostingClassifier(), GRADIENT_BOOST_PARAMS, 'gradient_boos')
    models =  [rndF_param, extra_param, grd_param]
    model_comparator = ModelComparator(models, X, y, 'recall')
    model_comparator.compare_models()
    return model_comparator

if __name__=="__main__":
    munging = False
    #Data Munging / Feature engineering
    if munging == True:
        merged_table = data_munging_engineering()
    else:
        merged_table = pd.read_pickle('merged_table')
    #Models Comparison
    mod_comp = model_choice(merged_table)
