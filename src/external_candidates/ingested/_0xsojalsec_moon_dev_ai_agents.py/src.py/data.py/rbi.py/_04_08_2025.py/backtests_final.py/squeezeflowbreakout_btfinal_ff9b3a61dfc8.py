# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_08_2025\backtests_final\SqueezeFlowBreakout_BTFinal.py
# 🌙 Moon Dev's SqueezeFlowBreakout Backtest 🌙
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy


class SqueezeFlowBreakout(Strategy):
    risk_per_trade = 0.01  # 1% of equity per trade

    def init(self):
        # 🌀 Bollinger Bands (20-period, 2 std)
        bb_upper, bb_middle, bb_lower = talib.BBANDS(
            self.data.Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
        )
        self.upper_band = self.I(lambda: bb_upper, name="Upper Band")
        self.middle_band = self.I(lambda: bb_middle, name="Middle Band")
        self.lower_band = self.I(lambda: bb_lower, name="Lower Band")

        # 💰 Chaikin Money Flow (20-period)
        self.cmf = self.I(
            lambda: ta.chaikin_money_flow(
                high=self.data.High,
                low=self.data.Low,
                close=self.data.Close,
                volume=self.data.Volume,
                length=20,
            ),
            name="CMF",
        )

        print("🌌 Indicators initialized! Let's ride the moon rockets! 🚀")

    def next(self):
        if self.position:
            return  # Hold existing position

        # 📉 Squeeze detection
        current_upper = self.upper_band[-1]
        current_lower = self.lower_band[-1]
        current_middle = self.middle_band[-1]
        bb_width_pct = ((current_upper - current_lower) / current_middle) * 100

        # 💹 Entry conditions
        cmf_cross = (self.cmf[-2] <= 0) and (
            self.cmf[-1] > 0
        )  # Bullish crossover above zero
        close_breakout = self.data.Close[-1] > current_upper

        if bb_width_pct <= 1.5 and cmf_cross and close_breakout:
            # 🎯 Calculate risk parameters
            entry_price = self.data.Close[-1]
            sl = current_lower
            risk_distance = entry_price - sl
            bb_width = current_upper - current_lower

            if risk_distance <= 0:
                print("⚠️ Zero/negative risk detected! Aborting launch...")
                return

            # 🚀 Position sizing (fixed to use whole units)
            risk_amount = self.equity * self.risk_per_trade
            position_size = risk_amount / risk_distance
            position_size = int(round(position_size))  # Ensure whole units

            if position_size > 0:
                tp = entry_price + (1.5 * bb_width)
                print(f"""
🌕 MOONSHOT ALERT! 🌕
Entry Price: {entry_price:.2f}
Stop Loss: {sl:.2f} (-{risk_distance:.2f})
Take Profit: {tp:.2f} (+{(tp - entry_price):.2f})
Position Size: {position_size} units
                """)
                self.buy(size=position_size, sl=sl, tp=tp)


# 🛰 Data preprocessing
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
data.columns = [col.strip().lower() for col in data.columns]
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

print("✨ Data cleaned and prepped for lunar launch! 🚀")

# 🚀 Launch backtest
bt = Backtest(data, SqueezeFlowBreakout, cash=1_000_000, commission=0.002)
stats = bt.run()
print("\n🌙 MOON MISSION RESULTS 🌙")
print(stats)
print(stats._strategy)
