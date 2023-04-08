class Portfolio:
    def __init__(self, closing_values):
        super().__init__()

        self.netValues = []
        self.dates = []
        self.closing_values = closing_values
        self.funds = [2000.0, 2000.0, 2000.0, 2000.0, 2000.0]
        self.funds_per_slot = [2000.0, 2000.0, 2000.0, 2000.0, 2000.0]
        self.coins = [0, 0, 0, 0, 0]
        self.capital_gains = 0.0
        self.lastValue = [0, 0, 0, 0, 0]
        self.currencyNames = ["BitCoin", "DogeCoin", "Ethereum", "LiteCoin", "XRP"]
        # Buy weights for cryptos
        self.bitcoin_buy_weights = [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
        self.dogecoin_buy_weights = [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
        self.ethereum_buy_weights = [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
        self.litecoin_buy_weights = [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
        self.xrp_buy_weights = [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
        # Sell weights for cryptos
        self.bitcoin_sell_weights = [-0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01]
        self.dogecoin_sell_weights = [-0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01]
        self.ethereum_sell_weights = [-0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01]
        self.litecoin_sell_weights = [-0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01]
        self.xrp_sell_weights = [-0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01]
        # Profit loss for all cryptos
        self.bitcoin_profit_loss = self.precalculateProfitLoss(closing_values[0])
        self.dogecoin_profit_loss = self.precalculateProfitLoss(closing_values[1])
        self.ethereum_profit_loss = self.precalculateProfitLoss(closing_values[2])
        self.litecoin_profit_loss = self.precalculateProfitLoss(closing_values[3])
        self.xrp_profit_loss = self.precalculateProfitLoss(closing_values[4])
        # Buy signals
        self.buySignals = [0, 0, 0, 0, 0]
        # Sell signals
        self.sellSignals = [0, 0, 0, 0, 0]

    def precalculateProfitLoss(self, currency_closing):
        res = []
        res2 = []
        for x in range(128, 2991):
            res = self.profitLoss(currency_closing, x)
            res2.append(res)
        return res2

    def profitLoss(self, currency_closing, day):
        res = []
        if currency_closing[day - 1] != 0.0:
            res.append((currency_closing[day] - currency_closing[day - 1]) / \
                       currency_closing[day - 1])
        else:
            res.append(0)
        if currency_closing[day - 2] != 0.0:
            res.append((currency_closing[day] - currency_closing[day - 2]) / \
                       currency_closing[day - 2])
        else:
            res.append(0)
        if currency_closing[day - 4] != 0.0:
            res.append((currency_closing[day] - currency_closing[day - 4]) / \
                       currency_closing[day - 4])
        else:
            res.append(0)
        if currency_closing[day - 8] != 0.0:
            res.append((currency_closing[day] - currency_closing[day - 8]) / \
                       currency_closing[day - 8])
        else:
            res.append(0)
        if currency_closing[day - 16] != 0.0:
            res.append((currency_closing[day] - currency_closing[day - 16]) / \
                       currency_closing[day - 16])
        else:
            res.append(0)
        if currency_closing[day - 32] != 0.0:
            res.append((currency_closing[day] - currency_closing[day - 32]) / \
                       currency_closing[day - 32])
        else:
            res.append(0)
        if currency_closing[day - 64] != 0.0:
            res.append((currency_closing[day] - currency_closing[day - 64]) / \
                       currency_closing[day - 64])
        else:
            res.append(0)
        if currency_closing[day - 128] != 0.0:
            res.append((currency_closing[day] - currency_closing[day - 128]) / \
                       currency_closing[day - 128])
        res.append(0)
        return res

    # profit and loss values vs buy weights or sell weights
    def determineBuySignals(self, bitcoin, dogecoin, ethereum, litecoin, xrp):
        self.buySignals = [0, 0, 0, 0, 0]
        for x in range(8):
            if bitcoin[x] > self.bitcoin_buy_weights[x]:
                self.buySignals[0] += 1
            if dogecoin[x] > self.dogecoin_buy_weights[x]:
                self.buySignals[1] += 1
            if ethereum[x] > self.ethereum_buy_weights[x]:
                self.buySignals[2] += 1
            if litecoin[x] > self.litecoin_buy_weights[x]:
                self.buySignals[3] += 1
            if xrp[x] > self.xrp_buy_weights[x]:
                self.buySignals[4] += 1

    def determineSellSignals(self, bitcoin, dogecoin, ethereum, litecoin, xrp):
        self.sellSignals = [0, 0, 0, 0, 0]
        for x in range(8):
            if bitcoin[x] < self.bitcoin_sell_weights[x]:
                self.sellSignals[0] += 1
            if dogecoin[x] < self.dogecoin_sell_weights[x]:
                self.sellSignals[1] += 1
            if ethereum[x] < self.ethereum_sell_weights[x]:
                self.sellSignals[2] += 1
            if litecoin[x] < self.litecoin_sell_weights[x]:
                self.sellSignals[3] += 1
            if xrp[x] < self.xrp_sell_weights[x]:
                self.sellSignals[4] += 1

    def purchaseCurrency(self, currency, day, buy_signals, sell_signals):
        # the currency has a closing value of 0.01 or more
        if self.closing_values[currency][day] > 0.01:
            # there are more buy signals than sell signals (same number of signals we will not purchase)
            if buy_signals >= sell_signals:
                # we haven’t purchased this currency already
                if self.coins[currency] == 0:
                    # purchase
                    self.coins[currency] = int(self.funds[currency] / self.closing_values[currency][day])
                    self.funds[currency] -= int(self.funds[currency] / self.closing_values[currency][day]) * \
                                            self.closing_values[currency][day]
                    self.lastValue[currency] = self.closing_values[currency][day]

    def sellCurrency(self, currency, day, buy_signals, sell_signals):
        # We have coins to sell
        if self.coins[currency] != 0:
            # There are more sell signals than buy signals
            if buy_signals <= sell_signals:
                # sell
                self.funds[currency] += self.coins[currency] * self.closing_values[currency][day]
                if (self.closing_values[currency][day] - self.lastValue[currency]) > 0:
                    self.capital_gains += ((self.closing_values[currency][day] - self.lastValue[currency]) * self.coins[currency]) * 0.33
                self.coins[currency] = 0


    def simulate(self):
        for i in range(2863):
            self.determineBuySignals(self.bitcoin_profit_loss[i], self.dogecoin_profit_loss[i],
                                     self.ethereum_profit_loss[i], self.litecoin_profit_loss[i],
                                     self.xrp_profit_loss[i])
            self.determineSellSignals(self.bitcoin_profit_loss[i], self.dogecoin_profit_loss[i],
                                      self.ethereum_profit_loss[i], self.litecoin_profit_loss[i],
                                      self.xrp_profit_loss[i])
            for t in range(5):
                self.purchaseCurrency(t, i + 128, self.buySignals[t],
                                      self.sellSignals[t])
                self.sellCurrency(t, i + 128, self.buySignals[t],
                                  self.sellSignals[t])
            self.netValues.append(self.totalValueSpecificDay(i))
            self.dates.append(i)
        self.totalValue()
        self.totalNetValue()

    def reset(self):
        self.capital_gains = 0
        self.dates = []
        self.netValues = []
        for i in range(5):
            self.coins[i] = 0
            self.lastValue[i] = 0
            self.funds[i] = self.funds_per_slot[i]

    def totalValue(self):
        res = 0.0
        for i in range(5):
            res += self.funds[i]
            res += self.coins[i] * self.closing_values[i][2990]
        return res

    def totalNetValue(self):
        res = 0.0
        for i in range(5):
            res += self.funds[i]
            res += self.coins[i] * self.closing_values[i][2990]
        res = res - self.capital_gains
        return res

    def totalValueSpecificDay(self, day):
        res = 0.0
        for i in range(5):
            res += self.funds[i]
            res += self.coins[i] * self.closing_values[i][day]
        return res
