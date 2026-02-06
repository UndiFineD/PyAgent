# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_28_2025\backtests\VortexSurge_BT.py
import pandas as pd
import pandas_ta as pta
import talib
from backtesting import Backtest, Strategy

# Data Preparation
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")

# Clean and format columns
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


class VortexSurge(Strategy):
    def init(self):
        # Calculate indicators
        high = self.data.High
        low = self.data.Low
        close = self.data.Close

        # Vortex Indicator (VI+, VI-)
        vi_plus, vi_minus = pta.vortex(high=high, low=low, close=close, length=14)
        self.vi_plus = self.I(lambda: vi_plus, name="VI_PLUS")
        self.vi_minus = self.I(lambda: vi_minus, name="VI_MINUS")

        # Volume SMA
        self.vol_sma = self.I(talib.SMA, self.data.Volume, 20)

        # ATR for exit conditions
        self.atr = self.I(talib.ATR, high, low, close, 14)

        print("🌙 Moon Dev Indicators Ready! Vortex Surge Activated 🚀")

    def next(self):
        # Skip early bars where indicators are NaN
        if len(self.data) < 20:
            return

        # Get current values
        vi_plus = self.vi_plus[-1]
        vi_plus_prev = self.vi_plus[-2]
        vi_minus = self.vi_minus[-1]
        vi_minus_prev = self.vi_minus[-2]

        volume = self.data.Volume[-1]
        vol_sma = self.vol_sma[-1]
        atr = self.atr[-1]

        # Entry condition
        if not self.position:
            if (
                (vi_plus > vi_minus)
                and (vi_plus_prev <= vi_minus_prev)
                and (volume > vol_sma)
            ):
                # Risk management
                risk_pct = 0.01  # 1% risk per trade
                equity = self.equity
                risk_amount = equity * risk_pct

                if atr == 0:
                    return

                position_size = risk_amount / atr
                position_size = int(round(position_size))

                if position_size > 0:
                    self.buy(
                        size=position_size,
                        tag={"entry_price": self.data.Close[-1], "atr": atr},
                    )
                    print(
                        f"🚀 MOON DEV ENTRY! Size: {position_size} @ {self.data.Close[-1]:.2f} 🌙 TP: {self.data.Close[-1] + 1.5*atr:.2f}"
                    )

        # Exit conditions
        elif self.position:
            entry_price = self.position.tag["entry_price"]
            atr_entry = self.position.tag["atr"]

            # VI reversal exit
            vi_reversal = (vi_plus < vi_minus) and (vi_plus_prev >= vi_minus_prev)

            # ATR profit target (1.5x)
            tp_price = entry_price + 1.5 * atr_entry
            tp_hit = self.data.High[-1] >= tp_price

            if vi_reversal or tp_hit:
                self.position.close()
                reason = "VI Reversal" if vi_reversal else "Profit Target"
                print(f"🌙 MOON DEV EXIT! {reason} @ {self.data.Close[-1]:.2f} ✨")


# Run backtest
bt = Backtest(data, VortexSurge, cash=1_000_000, commission=0.002)
stats = bt.run()

print("\n🌕🌖🌗🌘🌑🌒🌓🌔🌕")
print("MOON DEV BACKTEST COMPLETE!")
print("FULL STRATEGY STATS:")
print(stats)
print(stats._strategy)
print("TO THE MOON! 🚀🚀🚀")
