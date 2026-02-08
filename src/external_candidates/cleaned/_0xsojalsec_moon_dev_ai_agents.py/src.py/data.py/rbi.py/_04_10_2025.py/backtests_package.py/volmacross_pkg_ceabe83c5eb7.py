# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_10_2025\backtests_package\VolmaCross_PKG.py
# -*- coding: utf-8 -*-
import pandas as pd
import talib
from backtesting import Backtest, Strategy


# 🌙 MOON DEV DATA PREP 🌙
def load_data(path):
    data = pd.read_csv(path, parse_dates=["datetime"], index_col="datetime")
    # Clean column names
    data.columns = data.columns.str.strip().str.lower()
    # Drop unnamed columns
    data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
    # Map to proper case
    data = data.rename(
        columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume",
        }
    )
    return data


class VolmaCross(Strategy):
    risk_per_trade = 0.01  # 1% risk per trade 🌙

    def init(self):
        # 🌙✨ CORE INDICATORS ✨🌙
        # EMAs
        self.ema50 = self.I(talib.EMA, self.data.Close, timeperiod=50, name="EMA50")
        self.ema200 = self.I(talib.EMA, self.data.Close, timeperiod=200, name="EMA200")

        # Bollinger Bands (20-period, 2 std)
        self.bb_upper, self.bb_middle, self.bb_lower = self.I(
            talib.BBANDS,
            self.data.Close,
            timeperiod=20,
            nbdevup=2,
            nbdevdn=2,
            name=["BB Upper", "BB Middle", "BB Lower"],
        )
        self.bb_width = (self.bb_upper - self.bb_lower) / self.bb_middle

        # RSI (14-period)
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14, name="RSI")

        # Swing Low (20-period)
        self.swing_low = self.I(talib.MIN, self.data.Low, timeperiod=20, name="Swing Low")

        print("🌙✨ VolmaCross Strategy Activated! ✨🌙")

    def next(self):
        current_close = self.data.Close[-1]
        equity = self.equity

        # 🌙 ENTRY CONDITIONS 🌙
        if not self.position:
            # Golden Cross & Low Volatility
            if (self.ema50[-2] < self.ema200[-2] and self.ema50[-1] > self.ema200[-1]) and (self.bb_width[-1] < 1):
                # Risk Management Calculations
                stop_loss = self.swing_low[-1]
                risk_per_share = current_close - stop_loss
                position_size = (equity * self.risk_per_trade) / risk_per_share
                position_size = int(round(position_size))

                if position_size > 0:
                    self.buy(
                        size=position_size,
                        sl=stop_loss,
                        tag="🌙 GOLDEN CROSS ENTRY ✨",
                    )
                    print(f"🚀 LONG ENTRY | Size: {position_size} | Price: {current_close:.2f} | SL: {stop_loss:.2f}")

        # 🌙 EXIT CONDITIONS 🌙
        else:
            # Exit on RSI overbought OR high volatility
            if (self.rsi[-1] > 70) or (self.bb_width[-1] > 2):
                self.position.close()
                print(f"🛑 EXIT SIGNAL | RSI: {self.rsi[-1]:.2f} | BB Width: {self.bb_width[-1]:.2f}")


# 🌙 BACKTEST EXECUTION 🌙
if __name__ == "__main__":
    data = load_data("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")

    bt = Backtest(data, VolmaCross, cash=1_000_000, exclusive_orders=True)

    stats = bt.run()
    print("\n🌕🌖🌗🌘🌑🌒🌓🌔🌕")
    print("MOON DEV BACKTEST COMPLETE!")
    print(stats)
    print(stats._strategy)  # Show strategy-specific metrics
    print("✨ May your profits be lunar-sized! 🌙")
