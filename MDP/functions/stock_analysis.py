import pandas as pd
import matplotlib.pyplot as plt


def stock_analysis():
    data = pd.read_csv(f'data/adding_stock', sep=" ", header=None)

    print(data)

    plt.plot(data[1], color="black")

    plt.xlabel("Maximum stock level")
    plt.ylabel('Cost rate')
    plt.title('')
    plt.savefig(f'graphs/Adding_stock.pdf')
    plt.show()
