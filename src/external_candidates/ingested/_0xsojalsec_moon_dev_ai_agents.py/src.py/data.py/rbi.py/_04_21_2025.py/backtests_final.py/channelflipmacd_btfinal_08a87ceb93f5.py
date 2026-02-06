# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_21_2025\backtests_final\ChannelFlipMACD_BTFinal.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class ChannelFlipMACD(Strategy):
    def init(self):
        self.donchian_upper = self.I(talib.MAX, self.data.High, timeperiod=20)
        self.donchian_lower = self.I(talib.MIN, self.data.Low, timeperiod=20)
        self.macd, _, self.macd_hist = self.I(
            talib.MACD, self.data.Close, fastperiod=12, slowperiod=26, signalperiod=9
        )
        self.sma50 = self.I(talib.SMA, self.data.Close, timeperiod=50)

    def next(self):
        if len(self.data.Close) < 45:  # Ensure enough data for indicators
            return

        current_close = self.data.Close[-1]
        prev_close = self.data.Close[-2] if len(self.data.Close) >= 2 else None
        macd_hist = self.macd_hist[-1]
        prev_macd_hist = self.macd_hist[-2] if len(self.macd_hist) >= 2 else None

        if not self.position:
            # Long entry logic
            if (
                current_close > self.donchian_upper[-1]
                and macd_hist > 0
                and prev_macd_hist is not None
                and prev_macd_hist <= 0
                and current_close > self.sma50[-1]
            ):

                sl = self.donchian_lower[-1]
                risk = current_close - sl
                if risk <= 0:
                    print("🌙 Lunar Warning: Invalid risk calculation for long! ✨")
                    return

                size = int(round((0.01 * self.equity) / risk))
                if size <= 0:
                    print("🌙 Moon Alert: Position size too small! ✨")
                    return

                tp = current_close + 2 * risk
                self.buy(size=size, sl=sl, tp=tp)
                print(
                    f"🌙 LONG ENTRY @ {current_close:.2f} ✨ Size: {size} | Moon Power Activated! 🚀"
                )

            # Short entry logic
            elif (
                current_close < self.donchian_lower[-1]
                and macd_hist < 0
                and prev_macd_hist is not None
                and prev_macd_hist >= 0
                and current_close < self.sma50[-1]
            ):

                sl = self.donchian_upper[-1]
                risk = sl - current_close
                if risk <= 0:
                    print("🌙 Lunar Warning: Invalid risk calculation for short! ✨")
                    return

                size = int(round((0.01 * self.equity) / risk))
                if size <= 0:
                    print("🌙 Moon Alert: Position size too small! ✨")
                    return

                tp = current_close - 2 * risk
                self.sell(size=size, sl=sl, tp=tp)
                print(
                    f"🌙 SHORT ENTRY @ {current_close:.2f} ✨ Size: {size} | Cratering the Market! 💫"
                )


# Data preparation
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
data.columns = [col.strip().lower() for col in data.columns]
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

# Launch Moon Mission 🚀
bt = Backtest(data, ChannelFlipMACD, cash=1_000_000, commission=0.002)
stats = bt.run()
print("\n🌙=== MOON MISSION REPORT ===🌙")
print(stats)
print("\n🌙=== STRATEGY DETAILS ===🌙")
print(stats._strategy)
