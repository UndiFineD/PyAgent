# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_16_2025\backtests_final\VoltaicConvergence_BTFinal.py
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy

# Load and clean data
print("🌙✨ Initializing Moon Dev Data Loader...")
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

# Format columns for backtesting
print("🌙✨ Formatting Moon Dev Data Structure...")
data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
        "datetime": "Date",
    },
    inplace=True,
)

data["Date"] = pd.to_datetime(data["Date"])
data.set_index("Date", inplace=True)


class VoltaicConvergence(Strategy):
    def init(self):
        print("🌙✨ Initializing Moon Dev Indicators...")
        # Volatility indicators
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=14,
            name="ATR",
        )
        self.recent_high = self.I(
            talib.MAX, self.data.High, timeperiod=20, name="Recent High"
        )

        # Momentum indicators
        self.ema20 = self.I(talib.EMA, self.data.Close, timeperiod=20, name="EMA20")
        kst = ta.kst(self.data.Close, roc1=10, roc2=15, roc3=20, roc4=30)
        self.I(lambda: kst.iloc[:, 0], name="KST")  # Main KST line

        # Trade tracking
        self.entry_atr = None
        self.entry_price = None

    def next(self):
        price = self.data.Close[-1]

        if not self.position:
            # Entry conditions
            atr_val = self.atr[-1]
            kst_val = self.data["KST"][-1]
            high_zone = self.recent_high[-1] * 0.99

            if (price >= high_zone) and (atr_val < kst_val):
                # Risk management calculations
                risk_amount = self.equity * 0.01
                risk_distance = atr_val * 1.5
                position_size = risk_amount / risk_distance
                position_size = int(
                    round(position_size)
                )  # Ensure whole number of units

                if position_size > 0:
                    self.entry_atr = atr_val
                    self.entry_price = price
                    stop_loss = price - risk_distance
                    self.buy(size=position_size, sl=stop_loss)
                    print(
                        f"🌙✨🚀 MOON DEV ENTRY: {price:.2f} | ATR: {atr_val:.2f} | Size: {position_size} | SL: {stop_loss:.2f} ✨"
                    )
        else:
            # Exit conditions
            current_atr = self.atr[-1]
            ema_val = self.ema20[-1]

            # Take profit condition
            if current_atr >= self.entry_atr * 2:
                self.position.close()
                print(
                    f"🎯🌕 MOON DEV TP: ATR doubled to {current_atr:.2f} | Profit: {self.position.pl:.2f} 🌙"
                )

            # Trend reversal exit
            elif price < ema_val:
                self.position.close()
                print(
                    f"📉🌙 MOON DEV EXIT: Price below EMA20 ({ema_val:.2f}) | P/L: {self.position.pl:.2f} ✨"
                )


# Execute backtest
print("🌙✨ Launching Moon Dev Backtest Engine...")
bt = Backtest(data, VoltaicConvergence, cash=1_000_000, commission=0.002)
stats = bt.run()

# Print full results
print("\n🌙🌙🌙 MOON DEV BACKTEST RESULTS 🌙🌙🌙")
print(stats)
print("\n🔍 STRATEGY DETAILS:")
print(stats._strategy)
print("🌙✨ Moon Dev Backtest Complete! ✨🌙")
