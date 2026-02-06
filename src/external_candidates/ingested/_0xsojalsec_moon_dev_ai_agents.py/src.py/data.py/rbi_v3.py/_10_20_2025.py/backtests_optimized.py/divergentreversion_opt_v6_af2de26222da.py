# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v6.py
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
    adx_threshold = 20  # Optimized: Lowered from 25 to focus on stronger ranging conditions for better signal quality
    risk_per_trade = 0.015  # Optimized: Increased from 0.01 to 1.5% for higher exposure and potential returns while maintaining risk control
    atr_multiplier_sl = 2
    atr_multiplier_tp = 5  # Optimized: Increased from 4 to 5 for improved 1:2.5 RR to capture larger reversions and boost returns

    def init(self):
        # RSI(14) - Optimized: Changed from 20 to standard 14 for more responsive signals
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.rsi_sma = self.I(
            talib.SMA, self.rsi, timeperiod=14
        )  # Optimized: Matched SMA period to RSI for consistency

        # Stochastic slow %K(14,3,3) - Optimized: Changed from fast(8,1,1) to standard slow stochastic for smoother, less noisy signals
        self.stoch_k, _ = self.I(
            talib.STOCH,
            self.data.High,
            self.data.Low,
            self.data.Close,
            fastk_period=14,
            slowk_period=3,
            slowd_period=3,
        )
        self.stoch_sma = self.I(
            talib.SMA, self.stoch_k, timeperiod=14
        )  # Optimized: Matched SMA period to stochastic

        # ATR(14) for dynamic stops
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # ADX(14) for trend filter
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # Volume SMA(14) - New: Added for volume confirmation to filter out low-quality, low-conviction setups
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=14)

        print("🌙 Moon Dev: Indicators initialized ✨")

    def next(self):
        # Optimized: Added comprehensive exit logic for both long and short positions based on reversion signals
        # Check for exit first if in position
        if self.position:
            if self.position.is_long:
                if (self.rsi[-1] > self.rsi_sma[-1]) or (
                    self.stoch_k[-1] < self.stoch_sma[-1]
                ):
                    self.position.close()
                    print(
                        f"🌙 Moon Dev: Long Exit on Reversion Signal at {self.data.Close[-1]:.2f} 🚀"
                    )
                return
            elif self.position.is_short:
                if (self.rsi[-1] < self.rsi_sma[-1]) or (
                    self.stoch_k[-1] > self.stoch_sma[-1]
                ):
                    self.position.close()
                    print(
                        f"🌙 Moon Dev: Short Exit on Reversion Signal at {self.data.Close[-1]:.2f} 🚀"
                    )
                return

        # Entry conditions only if no position - Optimized: Added symmetric long entries to capture upside reversions in BTC's bullish bias
        # Updated: len check to 14 to match indicator periods
        if (
            (not self.position)
            and (len(self.rsi) > 14)
            and (self.adx[-1] < self.adx_threshold)
            and (self.data.Volume[-1] > self.vol_sma[-1])
        ):

            entry_price = self.data.Close[-1]
            atr_val = self.atr[-1]

            # Long entry: RSI oversold relative to SMA, Stoch overbought relative to SMA (divergence for upside reversion)
            if (self.rsi[-1] < self.rsi_sma[-1]) and (
                self.stoch_k[-1] > self.stoch_sma[-1]
            ):
                sl_price = entry_price - (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price + (self.atr_multiplier_tp * atr_val)
                risk_distance = entry_price - sl_price

                # Optimized: Switched to fractional position sizing for precise risk management (size as fraction of equity)
                # Formula ensures exact risk_per_trade % exposure based on stop distance
                if (
                    not np.isnan(sl_price)
                    and not np.isnan(tp_price)
                    and sl_price < entry_price < tp_price
                ):
                    size = self.risk_per_trade * entry_price / risk_distance
                    if size > 1.0:
                        size = 1.0
                    self.buy(
                        size=size, sl=sl_price, tp=tp_price
                    )  # Optimized: Removed limit for market entry at next open to avoid fill issues
                    print(
                        f"🌙 Moon Dev: Long Entry at {entry_price:.2f}, Size: {size:.4f}, SL: {sl_price:.2f}, TP: {tp_price:.2f} ✨"
                    )
                else:
                    print("🌙 Moon Dev: Invalid Long SL/TP levels, skipping entry ⚠️")
                return  # Only one direction per bar

            # Short entry: RSI overbought relative to SMA, Stoch oversold relative to SMA (divergence for downside reversion)
            if (self.rsi[-1] > self.rsi_sma[-1]) and (
                self.stoch_k[-1] < self.stoch_sma[-1]
            ):
                sl_price = entry_price + (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price - (self.atr_multiplier_tp * atr_val)
                risk_distance = sl_price - entry_price

                if (
                    not np.isnan(sl_price)
                    and not np.isnan(tp_price)
                    and tp_price < entry_price < sl_price
                ):
                    size = self.risk_per_trade * entry_price / risk_distance
                    if size > 1.0:
                        size = 1.0
                    self.sell(
                        size=size, sl=sl_price, tp=tp_price
                    )  # Optimized: Removed limit for market entry at next open
                    print(
                        f"🌙 Moon Dev: Short Entry at {entry_price:.2f}, Size: {size:.4f}, SL: {sl_price:.2f}, TP: {tp_price:.2f} ✨"
                    )
                else:
                    print("🌙 Moon Dev: Invalid Short SL/TP levels, skipping entry ⚠️")


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
