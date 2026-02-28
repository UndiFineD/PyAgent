# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_16_2025\backtests\StochasticBreakout_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Data preparation 🌙
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")

# Clean and format columns ✨
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


class StochasticBreakout(Strategy):
    def init(self):
        # Calculate cosmic indicators 🌌
        high = self.data.High.values
        low = self.data.Low.values
        close = self.data.Close.values

        # Stellar Stochastic Oscillator 🌟
        slowk, slowd = talib.STOCH(
            high, low, close, fastk_period=14, slowk_period=3, slowd_period=3
        )
        self.slowk = self.I(pd.Series, slowk, name="Stoch_%K")
        self.slowd = self.I(pd.Series, slowd, name="Stoch_%D")

        # Galactic Swing Levels 🌠
        self.swing_high = self.I(talib.MAX, self.data.High, 20, name="Swing_High")
        self.swing_low = self.I(talib.MIN, self.data.Low, 20, name="Swing_Low")

        # Orbital ATR for risk management 🛰️
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, 14, name="ATR"
        )

    def next(self):
        # Skip if still forming cosmic patterns 🌑
        if len(self.data.Close) < 20 or pd.isna(self.slowk[-1]):
            return

        current_close = self.data.Close[-1]
        stoch_k = self.slowk[-1]
        atr = self.atr[-1]
        sw_high = self.swing_high[-1]
        sw_low = self.swing_low[-1]

        # Moon-powered risk management 🌕
        risk_pct = 0.01  # 1% of lunar treasury
        base_size = 1_000_000 * risk_pct

        if not self.position:
            # Long entry when breaking through the stratosphere 🚀
            if current_close > sw_high and stoch_k > 50:
                sl_price = sw_high - 1.5 * atr
                risk_per_share = current_close - sl_price
                if risk_per_share > 0:
                    position_size = int(round(base_size / risk_per_share))
                    print(
                        f"🌙🚀 LUNAR LIFT-OFF! Buying {position_size} shares at {current_close:.2f}"
                    )
                    self.buy(
                        size=position_size,
                        sl=sl_price,
                        tp=current_close + 3 * risk_per_share,
                    )

            # Short entry during meteor showers ☄️
            elif current_close < sw_low and stoch_k < 50:
                sl_price = sw_low + 1.5 * atr
                risk_per_share = sl_price - current_close
                if risk_per_share > 0:
                    position_size = int(round(base_size / risk_per_share))
                    print(
                        f"🌑💫 COMET DIVE! Shorting {position_size} shares at {current_close:.2f}"
                    )
                    self.sell(
                        size=position_size,
                        sl=sl_price,
                        tp=current_close - 3 * risk_per_share,
                    )


# Launch backtest sequence 🛸
bt = Backtest(data, StochasticBreakout, cash=1_000_000, commission=0.002)
stats = bt.run()

# Print cosmic performance report 🌠
print("\n=== MOON DEV INTERSTELLAR REPORT ===")
print(stats)
print(stats._strategy)
