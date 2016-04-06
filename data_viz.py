import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve
import seaborn as sns
plt.style.use('ggplot')

def save_categorical_plots(table, y_column):
    for column in table.columns:
        if column != y_column:
            if len(table[column].unique()) <= 3:
                categorical_bar(column, y_column, table)

def categorical_bar(x_column, y_column, table):
    temp = pd.crosstab(table[x_column], table[y_column].astype(bool))
    temp.plot(kind='bar', stacked=True, color=['red','blue'])
    plt.ylabel('users count')
    plt.savefig('pictures/'+x_column+'.png')

def save_violin_plots(table, y_column):
    for column in table.columns:
        if column != y_column and column !=  '_id' and column != 'facebook_id':
            if len(table[column].unique()) > 3:
                violin_plot(column, y_column, table)

def violin_plot(x_column, y_column, table):
    sns.violinplot(x=y_column, y=x_column, data=table, bw=.1)
    plt.ylim([0,table[x_column].mean()*15])
    plt.show()

def roc_curve_models(models):
    for model in models:
        plt.plot(model.fpr, model.tpr, label = model.name)
    plt.title('ROC curve of the models')
    plt.xlabel('FPR')
    plt.ylabel('TPR')
    plt.legend(loc='best')
    plt.show()

def plot_feature_importances(forest, table):
    importances = forest.feature_importances_
    std =np.std([tree.feature_importances_ for tree in forest.estimators_],
                axis=0)
    indices = np.argsort(importances)[::-1][:-5]
    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(table.shape[1]-5), importances[indices], color='r',
            yerr=std[indices], align="center")
    plt.xticks(range(table.shape[1]-5), table.columns[indices], rotation=45)
    plt.xlim([-1, table.shape[1]-5])
    plt.show()
