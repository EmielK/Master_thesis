import pandas as pd
import matplotlib.pyplot as plt


def sensitivity_analysis():
    # Fill in parameter of interest below.
    param = "b_2"

    data_both = pd.read_csv(f'data/{param}_both', sep=" ", header=None)
    data_back = pd.read_csv(f'data/{param}_back', sep=" ", header=None)
    data_stock = pd.read_csv(f'data/{param}_stock', sep=" ", header=None)

    data_both.columns = [param, "both"]
    data_back.columns = [param, "back"]
    data_stock.columns = [param, "stock"]

    print(data_both)
    print(data_back)
    print(data_stock)

    data = pd.concat([data_both, data_back["back"], data_stock["stock"]],
                     axis=1)

    print(data)

    line1, = plt.plot(data[param], data["both"], label="both", color="black")
    line2, = plt.plot(data[param], data["back"], label="back-order only",
                      linestyle='dashed', color="black")
    line3, = plt.plot(data[param], data["stock"], label="stock only",
                      linestyle='dotted', color="black")
    plt.axvline(x=0.5, ymin=0.01, ymax=1, linestyle="dashed", color="black")

    plt.xlabel(param)
    plt.ylabel('Cost rate')
    plt.title('')
    plt.legend(loc='upper left', handles=[line1, line2, line3])
    plt.savefig(f'graphs/{param}.pdf')
    plt.show()
