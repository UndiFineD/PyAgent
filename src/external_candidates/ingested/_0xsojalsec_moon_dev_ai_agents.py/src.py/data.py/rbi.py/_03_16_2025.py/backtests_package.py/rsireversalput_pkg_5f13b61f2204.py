# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_16_2025\backtests_package\RSIReversalPut_PKG.py
# 🌙 Moon Dev's RSI Reversal Put Backtest 🌙
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# 🚀 Data Preparation with Moon Dev Standards 🚀
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)

# Cleanse and align cosmic energies ✨
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

# Proper column capitalization for universal harmony
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

# Temporal alignment ⏳
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)


class RSIReversalPut(Strategy):
    risk_percentage = 0.01  # 1% cosmic risk allocation 🌌
    take_profit_pct = 0.10  # 10% stellar profit target 🌠
    stop_loss_pct = 0.02  # 2% planetary protection shield 🛡️

    def init(self):
        # 🌗 Calculate RSI and its lunar minimum phase
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.min_rsi = self.I(talib.MIN, self.rsi, timeperiod=672)  # 1 week of 15m bars

    def next(self):
        # 🌑 Check for cosmic oversold conditions
        if not self.position and self.min_rsi[-1] <= 30:
            # 🪐 Calculate position size with quantum precision
            entry_price = self.data.Close[-1]
            stop_loss_price = entry_price * (1 + self.stop_loss_pct)
            take_profit_price = entry_price * (1 - self.take_profit_pct)
            risk_per_share = stop_loss_price - entry_price

            if risk_per_share > 0:
                position_size = int(
                    round((self.equity * self.risk_percentage) / risk_per_share)
                )
                if position_size > 0:
                    # 🌘 Execute short position with celestial orders
                    self.sell(
                        size=position_size,
                        sl=stop_loss_price,
                        tp=take_profit_price,
                        tag="RSI Reversal Put",
                    )

    def notify_order(self, order):
        # 🌕 Order execution notifications
        if order.status == order.Completed:
            direction = "SELL" if order.is_sell else "BUY"
            emoji = "🌙" if order.is_sell else "✨"
            print(
                f"{emoji} Cosmic {direction} Order Executed at {order.executed_price:.2f} "
                f"Size: {abs(order.size)} {emoji}"
            )

    def notify_trade(self, trade):
        # 🌟 Trade closure celebrations
        if trade.is_closed:
            profit_pct = trade.profit_pct * 100
            print(f"🌠✨ Trade Closed! Celestial Profit: {profit_pct:.2f}% ✨🌠")


# 🚀 Launch Backtest with 1M Moon Dust 🚀
bt = Backtest(data, RSIReversalPut, cash=1_000_000, margin=1.0, trade_on_close=True)
stats = bt.run()

# 🌙 Print Universal Performance Metrics 🌙
print("\n" + "=" * 50)
print("🌌 Moon Dev's Cosmic Performance Report 🌌")
print("=" * 50 + "\n")
print(stats)
print("\n" + "=" * 50)
print("🌠 Strategy Quantum Parameters 🌠")
print("=" * 50)
print(stats._strategy)
