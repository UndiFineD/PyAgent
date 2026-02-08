# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v4.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
df = pd.read_csv(data_path)

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# Drop any unnamed columns
df = df.drop(columns=[col for col in df.columns if "unnamed" in col.lower()])

# Set datetime as index
df = df.set_index(pd.to_datetime(df["datetime"]))

# Rename columns properly
df.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    },
    inplace=True,
)

# Sort index to ensure chronological order
df = df.sort_index()

# Ensure required columns
print("🌙 Moon Dev: Data loaded and cleaned. Shape:", df.shape)
print("Columns:", df.columns.tolist())


class DivergentReversion(Strategy):
    adx_threshold = 20  # 🌙 Moon Dev: Tightened ADX threshold from 25 to 20 for more selective ranging market entries, reducing whipsaws
    risk_per_trade = (
        0.015  # 🌙 Moon Dev: Increased risk per trade from 1% to 1.5% to amplify returns while keeping risk controlled
    )
    atr_multiplier_sl = 2
    atr_multiplier_tp = 6  # 🌙 Moon Dev: Extended TP multiplier from 4 to 6 for 1:3 RR, allowing winners to run further for higher returns

    def init(self):
        # RSI(20)
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=20)
        self.rsi_sma = self.I(talib.SMA, self.rsi, timeperiod=20)

        # Stochastic %K(8)
        self.stoch_k, _ = self.I(
            talib.STOCH,
            self.data.High,
            self.data.Low,
            self.data.Close,
            fastk_period=8,
            slowk_period=1,
            slowd_period=1,
        )
        self.stoch_sma = self.I(talib.SMA, self.stoch_k, timeperiod=20)

        # ATR(14) for dynamic stops
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)

        # ADX(14) for trend filter
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14)

        # Volume SMA for quality filter
        self.vol_sma = self.I(
            talib.SMA, self.data.Volume, timeperiod=20
        )  # 🌙 Moon Dev: Added volume SMA filter to enter only on above-average volume for stronger signals

        print("🌙 Moon Dev: Indicators initialized ✨")

    def next(self):
        # 🌙 Moon Dev: Removed signal-based exits to rely solely on SL/TP, preventing premature closure of winners and improving return potential
        # Check for exit first if in position (commented out signal exits for optimization)
        # if self.position.is_long:
        #     if (self.rsi[-1] > self.rsi_sma[-1]) or (self.stoch_k[-1] < self.stoch_sma[-1]):
        #         self.position.close()
        #         print(f"🌙 Moon Dev: Long Exit on Reversion Signal at {self.data.Close[-1]:.2f} 🚀")
        #     return
        #
        # if self.position.is_short:
        #     if (self.rsi[-1] < self.rsi_sma[-1]) or (self.stoch_k[-1] > self.stoch_sma[-1]):
        #         self.position.close()
        #         print(f"🌙 Moon Dev: Short Exit on Reversion Signal at {self.data.Close[-1]:.2f} 🚀")
        #     return

        # Entry conditions (only if no position)
        if not self.position and len(self.rsi) > 20 and self.adx[-1] < self.adx_threshold:
            entry_price = self.data.Close[-1]
            atr_val = self.atr[-1]
            vol_condition = (
                self.data.Volume[-1] > self.vol_sma[-1]
            )  # 🌙 Moon Dev: Added volume filter for higher-quality entries with conviction

            if vol_condition:
                # Long entry: symmetric divergence (RSI bearish, Stoch bullish) for reversion up
                if (self.rsi[-1] < self.rsi_sma[-1]) and (self.stoch_k[-1] > self.stoch_sma[-1]):
                    sl_price = entry_price - (self.atr_multiplier_sl * atr_val)
                    tp_price = entry_price + (self.atr_multiplier_tp * atr_val)
                    risk_distance = entry_price - sl_price

                    # Position sizing: risk fixed % of equity, use float for precise sizing
                    equity = (
                        self._broker.get_cash() + self._broker.get_equity() - self._broker.get_cash()
                    )  # Approximate equity
                    risk_amount = equity * self.risk_per_trade
                    position_size = (
                        risk_amount / risk_distance
                    )  # 🌙 Moon Dev: Use float sizing for precision, no int rounding to avoid under/over-sizing

                    # Check if size and SL/TP levels are valid for long
                    if (
                        position_size > 0
                        and not np.isnan(sl_price)
                        and not np.isnan(tp_price)
                        and sl_price < entry_price < tp_price
                    ):
                        self.buy(
                            size=position_size,
                            limit=entry_price,
                            sl=sl_price,
                            tp=tp_price,
                        )
                        print(
                            f"🌙 Moon Dev: Long Entry at {entry_price:.2f}, Size: {position_size:.4f}, SL: {sl_price:.2f}, TP: {tp_price:.2f} ✨"
                        )
                    else:
                        print("🌙 Moon Dev: Invalid position size or SL/TP levels for long, skipping entry ⚠️")

                # Short entry: original divergence (RSI bullish, Stoch bearish) for reversion down
                elif (self.rsi[-1] > self.rsi_sma[-1]) and (self.stoch_k[-1] < self.stoch_sma[-1]):
                    sl_price = entry_price + (self.atr_multiplier_sl * atr_val)
                    tp_price = entry_price - (self.atr_multiplier_tp * atr_val)
                    risk_distance = sl_price - entry_price

                    # Position sizing: risk fixed % of equity, use float for precise sizing
                    equity = (
                        self._broker.get_cash() + self._broker.get_equity() - self._broker.get_cash()
                    )  # Approximate equity
                    risk_amount = equity * self.risk_per_trade
                    position_size = (
                        risk_amount / risk_distance
                    )  # 🌙 Moon Dev: Use float sizing for precision, no int rounding to avoid under/over-sizing

                    # Check if size and SL/TP levels are valid for short
                    if (
                        position_size > 0
                        and not np.isnan(sl_price)
                        and not np.isnan(tp_price)
                        and tp_price < entry_price < sl_price
                    ):
                        self.sell(
                            size=position_size,
                            limit=entry_price,
                            sl=sl_price,
                            tp=tp_price,
                        )
                        print(
                            f"🌙 Moon Dev: Short Entry at {entry_price:.2f}, Size: {position_size:.4f}, SL: {sl_price:.2f}, TP: {tp_price:.2f} ✨"
                        )
                    else:
                        print("🌙 Moon Dev: Invalid position size or SL/TP levels for short, skipping entry ⚠️")


# Run backtest
bt = Backtest(
    df,
    DivergentReversion,
    cash=1000000,
    commission=0.002,
    exclusive_orders=True,
    trade_on_close=True,
)

print("🌙 Moon Dev: Running backtest... 🚀")
stats = bt.run()
print(stats)
