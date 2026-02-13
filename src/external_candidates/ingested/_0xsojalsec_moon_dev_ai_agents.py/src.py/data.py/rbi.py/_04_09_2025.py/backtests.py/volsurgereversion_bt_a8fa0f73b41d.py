# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_09_2025\backtests\VolSurgeReversion_BT.py
# 🌙 Moon Dev Backtest AI Generated Code 🚀
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# =====================
# DATA PREPARATION 🌍
# =====================
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path)

# Clean and format columns 🌙
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


# =====================
# VOLSURGE STRATEGY ⚡
# =====================
class VolSurgeReversion(Strategy):
    bb_period = 2880  # 30 days in 15m intervals (30*24*4)
    rsi_period = 14
    vol_multiplier = 2
    risk_pct = 0.02  # 2% risk per trade
    swing_window = 20  # Swing low period

    def init(self):
        # 🌙 Calculate Indicators with TA-Lib
        self.upper_band, self.middle_band, self.lower_band = self.I(
            talib.BBANDS,
            self.data.Close,
            timeperiod=self.bb_period,
            nbdevup=2,
            nbdevdn=2,
            matype=0,
        )

        # 🌊 Volume Surge Indicator
        self.vol_ma = self.I(talib.SMA, self.data.Volume, self.bb_period)

        # 📈 RSI for Exit Signals
        self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_period)

        # 🏔 Swing Low Detection
        self.swing_low = self.I(talib.MIN, self.data.Low, self.swing_window)

    def next(self):
        # Wait for indicators to warm up 🌙
        if len(self.data) < self.bb_period:
            return

        # 🌙 Current Market Conditions
        price = self.data.Close[-1]
        lower_band = self.lower_band[-1]
        volume = self.data.Volume[-1]
        vol_ma = self.vol_ma[-1]
        swing_low = self.swing_low[-1]
        rsi = self.rsi[-1]

        # 🚀 ENTRY LOGIC: Price breach + Volume Surge
        if (
            not self.position
            and price < lower_band
            and volume > self.vol_multiplier * vol_ma
        ):

            # 🌙 Risk Management Calculations
            risk_amount = self.risk_pct * self.equity
            stop_loss = swing_low
            risk_per_share = price - stop_loss

            if risk_per_share > 0:
                position_size = int(round(risk_amount / risk_per_share))
                if position_size > 0:
                    self.buy(size=position_size, sl=stop_loss)
                    print(
                        f"🚀 MOON DEV LONG ENTRY 🌙 | Size: {position_size:,} | Entry: {price:.2f} | SL: {stop_loss:.2f}"
                    )

        # 🎯 EXIT LOGIC: RSI Cross 50
        if self.position.is_long and crossover(self.rsi, 50):
            self.position.close()
            print(
                f"🌙 RSI EXIT SIGNAL ✨ | Close: {price:.2f} | P&L: {self.position.pl:.2f}"
            )


# =====================
# BACKTEST EXECUTION ⚡
# =====================
bt = Backtest(data, VolSurgeReversion, cash=1e6, margin=1.0, trade_on_close=True)
stats = bt.run()

# 🌙 Print Full Statistics
print("\n" + "=" * 50)
print("MOON DEV BACKTEST REPORT 🌕✨")
print("=" * 50)
print(stats)
print(stats._strategy)
print("=" * 50 + "\n")
print("🌙 Backtest Complete! May your trades be lunar-powered! 🚀")
