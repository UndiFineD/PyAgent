# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_02_2025\backtests_package\ChannelAccelBreakout_PKG.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class ChannelAccelBreakout(Strategy):
    risk_percent = 0.01  # 1% risk per trade
    stop_loss_pct = 0.02  # 2% stop loss

    def init(self):
        # Moon Dev Indicators Setup 🌙
        self.donchian_upper = self.I(talib.MAX, self.data.High, timeperiod=20)
        self.donchian_lower = self.I(talib.MIN, self.data.Low, timeperiod=20)
        self.roc = self.I(talib.ROC, self.data.Close, timeperiod=14)
        self.volume_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)

        print("✨ Moon Dev Indicators Activated! Channel Breakout System Online ✨")
        print("🌙 Donchian Channel (20) | ROC (14) | Volume SMA (20) Initialized")

    def next(self):
        # Current market conditions 🌐
        price = self.data.Close[-1]
        midpoint = (self.donchian_upper[-1] + self.donchian_lower[-1]) / 2

        # Moon Dev Entry Logic 🚀
        if not self.position:
            breakout_condition = price > self.donchian_upper[-1]
            momentum_condition = self.roc[-1] > self.roc[-2]  # ROC increasing
            volume_condition = self.data.Volume[-1] > self.volume_sma[-1]

            if all([breakout_condition, momentum_condition, volume_condition]):
                # Risk management calculations 🔒
                stop_price = price * (1 - self.stop_loss_pct)
                risk_per_share = price - stop_price
                risk_amount = self.equity * self.risk_percent

                if risk_per_share > 0:
                    position_size = int(round(risk_amount / risk_per_share))
                    if position_size > 0:
                        self.buy(size=position_size, sl=stop_price)
                        print(f"🚀 MOON DEV LAUNCH! BUY {position_size} @ {price:.2f}")
                        print(f"🛡️ Stop Loss Activated: {stop_price:.2f}")
                        print(f"🌕 Current Equity: ${self.equity:,.2f}")

        # Moon Dev Exit Logic 🌗
        else:
            if price < midpoint:
                self.position.close()
                print(f"🌙 LUNAR CYCLE COMPLETE | Exit @ {price:.2f}")
                print(f"✨ New Equity Balance: ${self.equity:,.2f}")


# Data Preparation Ritual 🔮
print("\n🌑 INITIATING MOON DATA CEREMONY...")
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
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
print("🌒 DATA CLEANSED AND CONSECRATED")

# Moon Backtest Initiation 🌕
print("\n🌓 ACTIVATING MOON BACKTEST PROTOCOL...")
bt = Backtest(data, ChannelAccelBreakout, cash=1_000_000, commission=0.002)
stats = bt.run()

print("\n🌌 FINAL MOON MISSION REPORT 🌌")
print("🌕" * 20)
print(stats)
print("\n🌖 STRATEGY PERFORMANCE METRICS:")
print(stats._strategy)
print("\n🌗" * 20)
print("🌙 MOON DEV BACKTEST COMPLETE! May your equity curve reach for the stars! 🚀")
