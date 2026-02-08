# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_21_2025\backtests_final\L-ChannelRSIBreakout_BTFinal.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Data preparation
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
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


class ChannelRSIBreakout(Strategy):
    risk_percent = 0.02
    donchian_period = 20
    rsi_period = 2
    atr_period = 14
    atr_multiplier = 3
    exit_bars = 10

    def init(self):
        self.donchian_high = self.I(talib.MAX, self.data.High, self.donchian_period)
        self.donchian_low = self.I(talib.MIN, self.data.Low, self.donchian_period)
        self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_period)
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, self.atr_period)
        self.high_in_trade = self.low_in_trade = self.entry_bar = 0

    def next(self):
        if not self.position:
            current_close = self.data.Close[-1]

            # Long entry logic
            if current_close > self.donchian_high[-1] and self.rsi[-1] < 30:
                risk_amount = self.risk_percent * self.equity
                atr_value = self.atr[-1]
                if atr_value <= 0:
                    print("🌙⚠️ ATR value zero or negative - skipping trade")
                    return

                entry_price = current_close
                stop_loss = entry_price - self.atr_multiplier * atr_value
                risk_per_share = entry_price - stop_loss
                position_size = int(round(risk_amount / risk_per_share))

                if position_size > 0:
                    self.buy(size=position_size)
                    self.high_in_trade = self.data.High[-1]
                    self.entry_bar = len(self.data)
                    print(
                        f"🌙🚀 BULLISH BREAKOUT! Long {position_size} units at {entry_price:.2f} | RSI {self.rsi[-1]:.1f} ✨"
                    )

            # Short entry logic
            elif current_close < self.donchian_low[-1] and self.rsi[-1] > 70:
                risk_amount = self.risk_percent * self.equity
                atr_value = self.atr[-1]
                if atr_value <= 0:
                    print("🌙⚠️ ATR value zero or negative - skipping trade")
                    return

                entry_price = current_close
                stop_loss = entry_price + self.atr_multiplier * atr_value
                risk_per_share = stop_loss - entry_price
                position_size = int(round(risk_amount / risk_per_share))

                if position_size > 0:
                    self.sell(size=position_size)
                    self.low_in_trade = self.data.Low[-1]
                    self.entry_bar = len(self.data)
                    print(
                        f"🌙📉 BEARISH BREAKDOWN! Short {position_size} units at {entry_price:.2f} | RSI {self.rsi[-1]:.1f} ⚠️"
                    )
        else:
            # Update trailing levels
            if self.position.is_long:
                self.high_in_trade = max(self.high_in_trade, self.data.High[-1])
                trailing_stop = self.high_in_trade - self.atr_multiplier * self.atr[-1]
                if self.data.Low[-1] <= trailing_stop or (len(self.data) - self.entry_bar) >= self.exit_bars:
                    self.position.close()
                    print(
                        f"🌙🛑 Closing long at {self.data.Close[-1]:.2f} | {'Time exit' if (len(self.data) - self.entry_bar) >= self.exit_bars else 'Trail stop'} 🌗"
                    )

            elif self.position.is_short:
                self.l
