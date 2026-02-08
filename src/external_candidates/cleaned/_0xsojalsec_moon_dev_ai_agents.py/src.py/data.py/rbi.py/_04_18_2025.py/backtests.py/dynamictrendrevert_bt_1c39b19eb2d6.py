# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_18_2025\backtests\DynamicTrendRevert_BT.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


class DynamicTrendRevert(Strategy):
    risk_per_trade = 0.01  # 1% risk per trade

    def init(self):
        # Calculate required indicators using TA-Lib
        self.ema50 = self.I(talib.EMA, self.data.Close, timeperiod=50, name="EMA 50")
        self.ema200 = self.I(talib.EMA, self.data.Close, timeperiod=200, name="EMA 200")
        self.adx = self.I(
            talib.ADX,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=14,
            name="ADX 14",
        )
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14, name="RSI 14")
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=14,
            name="ATR 14",
        )

    def next(self):
        # Check if we have enough historical data
        if len(self.data) < 200 or len(self.rsi) < 2:
            return

        # Get current indicator values
        current_ema50 = self.ema50[-1]
        current_ema200 = self.ema200[-1]
        current_adx = self.adx[-1]
        current_rsi = self.rsi[-1]
        current_atr = self.atr[-1]
        prev_ema50 = self.ema50[-2]
        prev_ema200 = self.ema200[-2]
        prev_rsi = self.rsi[-2]

        # Check for NaN values in indicators
        if np.isnan(
            [
                current_ema50,
                current_ema200,
                prev_ema50,
                prev_ema200,
                current_adx,
                current_atr,
            ]
        ).any():
            return

        # 🌙✨ Moon Dev Entry Logic ✨🌙
        ema_crossover = (current_ema50 > current_ema200) and (prev_ema50 <= prev_ema200)
        adx_valid = current_adx > 25

        if not self.position and ema_crossover and adx_valid:
            entry_price = self.data.Close[-1]
            stop_loss = entry_price - 1.5 * current_atr
            risk_amount = self.equity * self.risk_per_trade
            risk_per_share = entry_price - stop_loss

            if risk_per_share > 0:
                position_size = int(round(risk_amount / risk_per_share))
                if position_size > 0:
                    self.buy(size=position_size, sl=stop_loss, tag="MoonDevEntry")
                    print(
                        f"🌙✨ MOON DEV LONG SIGNAL! ✨🌙 | Price: {entry_price:.2f} | Size: {position_size} | SL: {stop_loss:.2f} | RSI: {current_rsi:.2f}"
                    )

        # 🚀🌑 Moon Dev Exit Logic 🌑🚀
        if self.position and (current_rsi < 70 and prev_rsi >= 70):
            self.position.close()
            print(f"🚀🌑 MOON DEV EXIT SIGNAL! 🌑🚀 | Price: {self.data.Close[-1]:.2f} | RSI: {current_rsi:.2f}")


# Data preprocessing
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
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

# Launch Moon Dev Backtest 🌕🚀
bt = Backtest(data, DynamicTrendRevert, cash=1_000_000, exclusive_orders=True)
stats = bt.run()
print(stats)
print(stats._strategy)
