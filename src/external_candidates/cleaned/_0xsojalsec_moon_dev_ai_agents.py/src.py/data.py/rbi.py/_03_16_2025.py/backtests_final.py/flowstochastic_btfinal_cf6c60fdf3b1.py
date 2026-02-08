# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_16_2025\backtests_final\FlowStochastic_BTFinal.py
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy


class FlowStochastic(Strategy):
    risk_percent = 0.01  # 1% risk per trade

    def init(self):
        # Calculate indicators using TA-Lib and pandas_ta
        # Chaikin Money Flow (CMF)
        cmf = ta.cmf(self.data.High, self.data.Low, self.data.Close, self.data.Volume, length=20)
        self.cmf = self.I(lambda: cmf, name="CMF")
        self.cmf_ma = self.I(talib.SMA, self.cmf, timeperiod=20, name="CMF_MA")

        # Stochastic Oscillator
        self.stoch_k, self.stoch_d = self.I(
            talib.STOCH,
            self.data.High,
            self.data.Low,
            self.data.Close,
            fastk_period=14,
            slowk_period=3,
            slowk_matype=0,
            slowd_period=3,
            slowd_matype=0,
            name=["%K", "%D"],
        )

        # Average True Range
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=14,
            name="ATR",
        )

    def next(self):
        # Require at least 2 periods for crossover check
        if len(self.stoch_k) < 2 or len(self.cmf) < 20:
            return

        # Entry conditions
        stoch_cross_down = (self.stoch_d[-2] > self.stoch_k[-2]) and (self.stoch_d[-1] < self.stoch_k[-1])
        cmf_above_ma = self.cmf[-1] > self.cmf_ma[-1]

        if not self.position and stoch_cross_down and cmf_above_ma:
            entry_price = self.data.Close[-1]
            atr_value = self.atr[-1]

            # Calculate risk management
            stop_loss = entry_price - atr_value
            take_profit = entry_price + 1.5 * atr_value

            # Position sizing calculation
            risk_amount = self.equity * self.risk_percent
            risk_per_share = entry_price - stop_loss
            position_size = int(round(risk_amount / risk_per_share))

            if position_size > 0:
                self.buy(size=position_size, sl=stop_loss, tp=take_profit)
                print(f"🌙✨ Moon Dev Signal: LONG {position_size} @ {entry_price:.2f}")
                print(f"   🛑 SL: {stop_loss:.2f} | 🎯 TP: {take_profit:.2f} 🌙")

        # Exit condition: Stochastic crossover up
        if self.position and (self.stoch_k[-2] < self.stoch_d[-2]) and (self.stoch_k[-1] > self.stoch_d[-1]):
            self.position.close()
            print(f"🌑 Moon Dev Exit: Closing @ {self.data.Close[-1]:.2f} 🚀")


# Data preparation
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")

# Clean and format data
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    },
    inplace=True,
)
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)

# Execute backtest
bt = Backtest(data, FlowStochastic, cash=1_000_000, exclusive_orders=True)
stats = bt.run()
print(stats)
print(stats._strategy)
