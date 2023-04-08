#!/usr/bin/python
#
# main.py
#
# full implementation of the cryptocurrency prediction assignment by using numerical optimisation

# imports needed to make this script work
import csv
import math
import random
import matplotlib.pyplot as plt
from simanneal import Annealer
from deap import base
from deap import creator
from deap import tools
import timeit
from Portfolio import Portfolio
from simanneal import Annealer # import the annealler from the sim anneal library


# function that will read in all of the cryptocurrenies and will assemble it into workable data
def assembleData(dates, closing_values):
    # read in all of the CSV files to make sure they are working
    bitcoin_rows = readCSVFile('coin_Bitcoin.csv')
    dogecoin_rows = readCSVFile('coin_Dogecoin.csv')
    ethereum_rows = readCSVFile('coin_Ethereum.csv')
    litecoin_rows = readCSVFile('coin_Litecoin.csv')
    xrp_rows = readCSVFile('coin_XRP.csv')

    # create a set of all the dates in all 5 CSVs. skip the first row as it is the header
    # sort the set at the end and turn it into a list
    dateset = set()
    for i in range(1, len(bitcoin_rows)):
        dateset.add(stripTime(bitcoin_rows[i][3]))
    for i in range(1, len(dogecoin_rows)):
        dateset.add(stripTime(dogecoin_rows[i][3]))
    for i in range(1, len(ethereum_rows)):
        dateset.add(stripTime(ethereum_rows[i][3]))
    for i in range(1, len(litecoin_rows)):
        dateset.add(stripTime(litecoin_rows[i][3]))
    for i in range(1, len(xrp_rows)):
        dateset.add(stripTime(xrp_rows[i][3]))
    for i in list(sorted(dateset)):
        dates.append(i)

    # create lists for all 5 currencies that contain all of the closing values that are mapped to the correct date
    # the first row will be the date
    for i in range(5):
        closing_values.append([0.0] * len(dateset))

    # add the closing value of all of the currencies into the closing values 2D list
    mapClosingValues(bitcoin_rows, closing_values, dates, 0)
    mapClosingValues(dogecoin_rows, closing_values, dates, 1)
    mapClosingValues(ethereum_rows, closing_values, dates, 2)
    mapClosingValues(litecoin_rows, closing_values, dates, 3)
    mapClosingValues(xrp_rows, closing_values, dates, 4)


# function that will map the closing value data from the given set of rows to the correct dates in the dataset
def mapClosingValues(rows, closing_values, dates, currency):
    # take the first date from the rows as this will give us our starting index.
    # unlike the stock market, crypto markets work on weekends as well so the dates will be in order
    date = stripTime(rows[1][3])
    starting_index = dates.index(date)

    # go through each of the rows and set the closing value. we skip the first row as it is a header
    for i in range(1, len(rows)):
        closing_values[currency][starting_index + i - 1] = float(rows[i][7])


# function that will take in the given CSV file and will read in its entire contents
# and return a list of lists
def readCSVFile(file):
    # the rows to return
    rows = []

    # open the file for reading and give it to the CSV reader
    csv_file = open(file)
    csv_reader = csv.reader(csv_file, delimiter=',')

    # read in each row and append it to the list of rows.
    for row in csv_reader:
        rows.append(row)

    # close the file when reading is finished
    csv_file.close();

    # return the rows at the end of the function
    return rows


# function that will take a date time and strip out the time from it
def stripTime(str_datetime):
    # datetimes will have the first 10 characters to represent the date so just extract these
    return str_datetime[0:10]

class CAnnealer(Annealer):
    def __init__(self, buy_sell_signals):
        self.buy_sell_signals = buy_sell_signals
        super(CAnnealer, self).__init__(buy_sell_signals)

    def move(self):
        self.buy_sell_signals[random.randint(0, 80)] = random.uniform(-1, 1)
        self.state = self.buy_sell_signals
        portfolio.bitcoin_buy_weights = self.buy_sell_signals[0:8]
        portfolio.dogecoin_buy_weights = self.buy_sell_signals[8:16]
        portfolio.ethereum_buy_weights = self.buy_sell_signals[16:24]
        portfolio.litecoin_buy_weights = self.buy_sell_signals[24:32]
        portfolio.xrp_buy_weights = self.buy_sell_signals[32:40]
        portfolio.bitcoin_sell_weights = self.buy_sell_signals[40:48]
        portfolio.dogecoin_sell_weights = self.buy_sell_signals[48:56]
        portfolio.ethereum_sell_weights = self.buy_sell_signals[56:64]
        portfolio.litecoin_sell_weights = self.buy_sell_signals[64:72]
        portfolio.xrp_sell_weights = self.buy_sell_signals[72:80]

    def energy(self):
        total = 0
        # Reset
        portfolio.reset()
        # Simulate
        portfolio.simulate()
        # Multiply portfolio value by -1
        total = portfolio.totalNetValue() * -1
        return total

if __name__ == '__main__':
    # empty lists for the dates and the closing data we need
    dates = []
    closing_values = []

    # assemble the data that we need and run the appropriate optimisation
    assembleData(dates, closing_values)
    portfolio = Portfolio(closing_values)
    # Precalculate each cryptocurrency
    portfolio.simulate()

    #Setting up and starting simulated annealing
    buy_sell_signals = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                             0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                             0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                             0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                             0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                             0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                             0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                             0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    CAL = CAnnealer(buy_sell_signals)
    CAL.steps = 10000
    funds, buy_sell_signals = CAL.anneal()


    #Printing out the values calculated by the algorithm
    print("The best value of the portfolio minus capital gains is: " + str(CAL.best_energy*-1) + "$")
    print("The last value of the portfolio minus capital gains is: " + str(portfolio.totalNetValue()) + "$")
    print("The best state values are:" + str(CAL.best_state))

    #Printing the cryptocurrencies buy and sell weights for reference
    portfolio.bitcoin_buy_weights = CAL.buy_sell_signals[0:8]
    portfolio.dogecoin_buy_weights = CAL.buy_sell_signals[8:16]
    portfolio.ethereum_buy_weights = CAL.buy_sell_signals[16:24]
    portfolio.litecoin_buy_weights = CAL.buy_sell_signals[24:32]
    portfolio.xrp_buy_weights = CAL.buy_sell_signals[32:40]
    portfolio.bitcoin_sell_weights = CAL.buy_sell_signals[40:48]
    portfolio.dogecoin_sell_weights = CAL.buy_sell_signals[48:56]
    portfolio.ethereum_sell_weights = CAL.buy_sell_signals[56:64]
    portfolio.litecoin_sell_weights = CAL.buy_sell_signals[64:72]
    portfolio.xrp_sell_weights = CAL.buy_sell_signals[72:80]
    print("Bictoin buy weight: " + str(portfolio.bitcoin_buy_weights))
    print("Dogecoin buy weight: " + str(portfolio.dogecoin_buy_weights))
    print("Ethereum buy weight: " + str(portfolio.ethereum_buy_weights))
    print("Litecoin buy weight: " + str(portfolio.litecoin_buy_weights))
    print("XRP buy weight: " + str(portfolio.xrp_buy_weights))
    print("Bictoin sell weight: " + str(portfolio.bitcoin_sell_weights))
    print("Dogecoin sell weight: " + str(portfolio.dogecoin_sell_weights))
    print("Ethereum sell weight: " + str(portfolio.ethereum_sell_weights))
    print("Litecoin sell weight: " + str(portfolio.litecoin_sell_weights))
    print("XRP sell weight: " + str(portfolio.xrp_sell_weights))

    #Matplotlib graph generation
    # Create the plot
    plt.plot(portfolio.dates, portfolio.netValues)

    # Add labels and title
    plt.xlabel('Date (in days)')
    plt.ylabel('Portfolio Value (in dollars)')
    plt.title('Crypto Portfolio Value Over Time')

    # Show the plot
    plt.show()





