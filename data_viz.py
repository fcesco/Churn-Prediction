import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import roc_curve
import seaborn as sns
plt.style.use('ggplot')

def save_categorical_plot(table, y_column):
    for column in table.columns:
        if column != y_column:
            if len(table[column].unique()) <= 3:
                categorical_bar(column, y_column, table)

def categorical_bar(x_column, y_column, table):
    temp = pd.crosstab(table[x_column], table[y_column].astype(bool))
    temp.plot(kind='bar', stacked=True, color=['red','blue'])
    plt.ylabel('users count')
    plt.savefig('pictures/'+x_column+'.png')


def plot_swarm_violin(x_column, y_column, table):
    sns.violinplot(x=y_column, y=x_column, data=table, bw=.1)
    plt.show()

def roc_curve_models(models):
    for model in models:
        plt.plot(fpr, tpr, label = model.name)
    plt.title('ROC curve of the models')
    plt.legend(loc=best)
    plt.show()

def plot_continuos_variables(df, column, y_column):
    '''
    plot histogram of continuos variable
    '''
    churn = df[df[y_column]==1][column]
    no_churn = df[df[y_column==0]][column]
    plt.hist(churn, bins=20, histtype='stepfilled', normed=True, color='r', label='Churn')
    plt.hist(no_churn, bins=20, histtype='stepfilled', normed=True, color='b', alpha=0.5, label='Engaged users')
    plt.title("%s churn/engaged users Histogram")
    plt.xlabel("Value")
    plt.ylabel("Quantity")
    plt.legend()
    plt.show()

def plot_binary_variables(df, column, y_column):
    plt.hist(x, n_bins, normed=1, histtype='bar', stacked=True)
    ax1.set_title('stacked bar')
