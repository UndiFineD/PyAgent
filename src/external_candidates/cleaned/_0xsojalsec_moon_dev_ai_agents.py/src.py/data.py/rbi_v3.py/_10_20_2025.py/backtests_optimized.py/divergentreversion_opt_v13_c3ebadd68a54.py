# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v13.py
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
    adx_threshold = 25
    risk_per_trade = 0.01  # 1%
    atr_multiplier_sl = 2
    atr_multiplier_tp = 5  # Increased to 1:2.5 RR for better profit potential while maintaining risk 🌙

    def init(self):
        # RSI(14) - Changed from 20 to standard 14 for more responsive signals
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.rsi_sma = self.I(talib.SMA, self.rsi, timeperiod=14)  # Matched to RSI period for consistency

        # Stochastic %K(14,3,3) - Changed to standard parameters for better reliability
        self.stoch_k, self.stoch_d = self.I(
            talib.STOCH,
            self.data.High,
            self.data.Low,
            self.data.Close,
            fastk_period=14,
            slowk_period=3,
            slowd_period=3,
        )
        self.stoch_sma = self.I(talib.SMA, self.stoch_k, timeperiod=14)  # Matched period

        # ATR(14) for dynamic stops
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)

        # ADX(14) for trend filter - Kept but can allow more trades in mild trends
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14)

        # Volume filter - Added SMA(20) to confirm entries on higher volume for quality setups
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)

        # Trend filter - Added SMA(50) to bias longs above and shorts below for alignment with short-term trend
        self.sma50 = self.I(talib.SMA, self.data.Close, timeperiod=50)

        print("🌙 Moon Dev: Indicators initialized with optimizations: standard params, volume & trend filters ✨")

    def next(self):
        current = self.data.Close[-1]

        # Handle positions: trailing stops first to lock in profits dynamically
        if self.position:
            if self.position.is_long:
                # Trailing stop for long: ratchet SL up to Close - 2*ATR, only if better
                new_sl = current - (self.atr_multiplier_sl * self.atr[-1])
                if new_sl > self.position.sl:
                    self.position.sl = new_sl
                    print(f"🌙 Moon Dev: Trailing Long SL to {new_sl:.2f} 🔒")
            elif self.position.is_short:
                # Trailing stop for short: ratchet SL down to Close + 2*ATR, only if better
                new_sl = current + (self.atr_multiplier_sl * self.atr[-1])
                if new_sl < self.position.sl:
                    self.position.sl = new_sl
                    print(f"🌙 Moon Dev: Trailing Short SL to {new_sl:.2f} 🔒")

            # Signal-based exits for mean reversion
            if self.position.is_long:
                if (self.rsi[-1] > self.rsi_sma[-1]) or (self.stoch_k[-1] < self.stoch_sma[-1]):
                    self.position.close()
                    print(f"🌙 Moon Dev: Long Exit on Reversion Signal at {current:.2f} 🚀")
                    return
            elif self.position.is_short:
                if (self.rsi[-1] < self.rsi_sma[-1]) or (self.stoch_k[-1] > self.stoch_sma[-1]):
                    self.position.close()
                    print(f"🌙 Moon Dev: Short Exit on Reversion Signal at {current:.2f} 🚀")
                    return

        # Entry conditions only if no position
        if (
            not self.position
            and len(self.rsi) > 50
            and self.adx[-1] < self.adx_threshold
            and self.data.Volume[-1] > self.vol_sma[-1]
        ):
            entry_price = current
            atr_val = self.atr[-1]
            equity = self.equity
            risk_amount = equity * self.risk_per_trade
            if atr_val > 0:  # Avoid div by zero
                # Long entry: symmetric divergence in uptrend bias
                if (
                    (entry_price > self.sma50[-1])
                    and (self.rsi[-1] < self.rsi_sma[-1])
                    and (self.stoch_k[-1] > self.stoch_sma[-1])
                ):
                    sl_price = entry_price - (self.atr_multiplier_sl * atr_val)
                    tp_price = entry_price + (self.atr_multiplier_tp * atr_val)
                    risk_distance = entry_price - sl_price

                    position_size = risk_amount / risk_distance

                    if (
                        position_size > 0
                        and not np.isnan(sl_price)
                        and not np.isnan(tp_price)
                        and sl_price < entry_price < tp_price
                    ):
                        self.buy(size=position_size, sl=sl_price, tp=tp_price)
                        print(
                            f"🌙 Moon Dev: Long Entry at {entry_price:.2f}, Size: {position_size:.4f}, SL: {sl_price:.2f}, TP: {tp_price:.2f} ✨"
                        )
                    else:
                        print("🌙 Moon Dev: Invalid Long position size or SL/TP levels, skipping entry ⚠️")
                    return

                # Short entry: symmetric divergence in downtrend bias
                if (
                    (entry_price < self.sma50[-1])
                    and (self.rsi[-1] > self.rsi_sma[-1])
                    and (self.stoch_k[-1] < self.stoch_sma[-1])
                ):
                    sl_price = entry_price + (self.atr_multiplier_sl * atr_val)
                    tp_price = entry_price - (self.atr_multiplier_tp * atr_val)
                    risk_distance = sl_price - entry_price

                    position_size = risk_amount / risk_distance

                    if (
                        position_size > 0
                        and not np.isnan(sl_price)
                        and not np.isnan(tp_price)
                        and tp_price < entry_price < sl_price
                    ):
                        self.sell(size=position_size, sl=sl_price, tp=tp_price)
                        print(
                            f"🌙 Moon Dev: Short Entry at {entry_price:.2f}, Size: {position_size:.4f}, SL: {sl_price:.2f}, TP: {tp_price:.2f} ✨"
                        )
                    else:
                        print("🌙 Moon Dev: Invalid Short position size or SL/TP levels, skipping entry ⚠️")


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
