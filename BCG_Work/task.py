import matplotlib.pyplot as plt
# from matplotlib.ticker import ScalarFormatter
import seaborn as sns
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Set plot style
sns.set(color_codes=True)

client_df = pd.read_csv('./client_data (1).csv')
price_df = pd.read_csv('./price_data (1).csv')

# Print the first 3 rows in the client_df and price_df
# print("\n\n----------------------------------------- First 3 rows of client dataframe -----------------------------------------")
# print(client_df.head(3))
# print("-------------------------------------------------------------------------------------------------------------------------")
# print("\n\n----------------------------------------- First 3 rows of price dataframe -----------------------------------------")
# print(price_df.head(3))
# print("-------------------------------------------------------------------------------------------------------------------------")

# # Print out the info of the data in the client_df e.g datatype
# print("\n\n----------------------------------------- DataTypes used in the client data -----------------------------------------")
# print(client_df.info())
# print("-------------------------------------------------------------------------------------------------------------------------")

# # Print out the info of the data in the price_df e.g datatype
# print("\n\n----------------------------------------- DataTypes used in the price data -----------------------------------------")
# print(price_df.info())
# print("-------------------------------------------------------------------------------------------------------------------------")

# # Print the Descriptive statistics of the data in client_df
# print("\n\n----------------------------------------- Descriptive Statistics of the data in client -----------------------------------------")
# print(client_df.describe())
# print("-------------------------------------------------------------------------------------------------------------------------")
# # Print the Descriptive statistics of the data in price_df
# print("\n\n----------------------------------------- Descriptive Statistics of the data in price -----------------------------------------")
# print(price_df.describe())
# print("-------------------------------------------------------------------------------------------------------------------------")

def plot_stacked_bars(dataframe, title, size = (18, 10), rot=0, legend = "upper right"):
    """
    Plot stacked bars with annotations
    """
    ax = dataframe.plot(
        kind = "bar",
        stacked = True,
        figsize = size,
        rot = rot,
        title = title
    )
    # Annotate bars
    annotate_stacked_bars(ax, textSize = 15)
    # Rename Legend
    plt.legend(["Retention", "Churn"], loc = legend)
    # Labels
    plt.ylabel("Company base (%)")
    # plt.show()
    
    
def annotate_stacked_bars(ax, pad = 0.99, colour = "white", textSize = 13):
    """
    Add value annotations to the bars
    """
    
    # iterating over the plotted rectangles/bars
    for plots in ax.patches:
        # Calculate annotation
        value = str(round(plots.get_height(), 1))
        # If value is 0 do not annotate
        if value == "0.0":
            continue
        ax.annotate(
            value,
            ((plots.get_x() + plots.get_width()/2 * pad-0.05), (plots.get_y() + plots.get_height()/2) * pad),
            va='center',
            color = colour,
            size = textSize
        )

'''
Churning Status
'''   
churn = client_df[['id', 'churn']]
# print("\n\nChurn ----> \n", churn)
# print("\n\n")
churn.columns = ['Companies', 'churn']
# print("churn.columns --> \n", churn.columns)
churn_total = churn.groupby(churn['churn']).count()
# print("\nchurn totals --> \n", churn_total)
churn_percentage = churn_total / churn_total.sum() * 100
# print("\nchurn perc --> \n", churn_percentage)
# plot_stacked_bars(churn_percentage.transpose(), "Churning status", (5, 5), 0, legend="lower right")

'''   
Channel Sales
'''
channel = client_df[['id', 'channel_sales', 'churn']]
# channel1 = channel.groupby([channel['channel_sales'], channel['churn']])['id'].count()
# print("Channel Before ------> \n\n", channel1)
channel = channel.groupby([channel['channel_sales'], channel['churn']])['id'].count().unstack(level=1).fillna(0)
# print("\n\n\nChannel After ------> \n\n", channel)
channel_churn = (channel.div(channel.sum(axis=1), axis=0) * 100).sort_values(by=[1], ascending=False)
# print("\n\n\nChannel Churn ------> \n\n", channel_churn)
plot_stacked_bars(channel_churn, 'Sales Channel', rot=30)



        
def plot_distribution(dataframe, column, ax, bins = 50):
    """
    Plot variable distribution in a stacked histogram of churned or retained company
    """
    # Create a temporal dataframe with the data to be plot
    temp = pd.DataFrame({
        "Retention": dataframe[dataframe['churn'] == 0][column], 
        "Churn": dataframe[dataframe['churn'] == 1][column]
        })
    
    # Plot the histogram
    temp[["Retention", "Churn"]].plot(
        kind = 'hist',
        bins = bins,
        ax = ax,
        stacked = True
    )
    # X-axis label
    ax.set_xlabel(column)
    # Change the x-axis to plain style
    ax.ticklabel_format(style = 'plain', axis = 'x')
    
        
consumption = client_df[['id', 'cons_12m', 'cons_gas_12m', 'cons_last_month', 'imp_cons', 'has_gas', 'churn']]

# # print('consumptions --> \n', consumption)
# axe = axs.ravel()
# plt.tight_layout()
fig, axs = plt.subplots(nrows=4, figsize=(18, 25))
plot_distribution(consumption, 'cons_12m', axs[0])
plot_distribution(consumption[consumption['has_gas'] == 't'], 'cons_gas_12m', axs[1])
plot_distribution(consumption, 'cons_last_month', axs[2])
plot_distribution(consumption, 'imp_cons', axs[3])
# plt.show()

consumption = client_df[['id', 'cons_12m', 'cons_gas_12m', 'cons_last_month', 'imp_cons', 'has_gas', 'churn']]
fig, axs = plt.subplots(nrows=4, figsize=(18, 25))
# Plot histogram
sns.boxplot(consumption["cons_12m"], ax=axs[0], orient="h")
sns.boxplot(consumption[consumption["has_gas"] == "t"]["cons_gas_12m"], ax=axs[1], orient="h")
sns.boxplot(consumption["cons_last_month"], ax=axs[2], orient="h")
sns.boxplot(consumption["imp_cons"], ax=axs[3], orient="h")


# Remove scientific notation
for ax in axs[2:]:
    ax.xaxis.set_major_formatter(plt.matplotlib.ticker.ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style='plain', axis='x')
    # ax.xaxis.set_major_formatter(plt.matplotlib.ticker.ScalarFormatter(useMathText=True))
    # plt.gca().xaxis.set_major_formatter(ScalarFormatter())
    # ax.set_xticks(ax.get_xticks()[:-1], [f"{int(x):,}" for x in ax.get_xticks()[:-1]]);
    # ax.ticklabel_format(style='plain', axis='x')
    # Set x-axis limit
    axs[0].set_xlim(-200000, 2000000)
    axs[1].set_xlim(-200000, 2000000)
    axs[2].set_xlim(-20000, 100000)
    

plt.show()