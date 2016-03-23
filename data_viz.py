import matplotlib.pyplot as plt
import pandas as pd
plt.style.use('ggplot')



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
