# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v7.py
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
    risk_per_trade = (
        0.02  # Increased to 2% for higher potential returns while managing risk 🌙
    )
    atr_multiplier_sl = 2
    atr_multiplier_tp = (
        5  # Improved RR to ~1:2.5 for better expectancy in mean reversion setups ✨
    )

    def init(self):
        # RSI(14) - Standardized period for faster, more responsive signals
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.rsi_sma = self.I(talib.SMA, self.rsi, timeperiod=14)

        # Stochastic %K(14,3,3) - Standardized parameters for better reliability
        self.stoch_k, self.stoch_d = self.I(
            talib.STOCH,
            self.data.High,
            self.data.Low,
            self.data.Close,
            fastk_period=14,
            slowk_period=3,
            slowd_period=3,
        )
        self.stoch_sma = self.I(talib.SMA, self.stoch_k, timeperiod=14)

        # ATR(14) for dynamic stops
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # ADX(14) for trend filter
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # Volume SMA for quality filter - Avoid low volume signals to improve entry quality
        self.volume_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)

        print("🌙 Moon Dev: Indicators initialized with optimizations ✨")

    def next(self):
        # Handle exits first for any open position
        if self.position:
            if self.position.is_long:
                # Close long on opposite reversion signal (RSI oversold or Stoch overbought relative to SMAs)
                if (self.rsi[-1] > self.rsi_sma[-1]) or (
                    self.stoch_k[-1] < self.stoch_sma[-1]
                ):
                    self.position.close()
                    print(
                        f"🌙 Moon Dev: Long Exit on Reversion Signal at {self.data.Close[-1]:.2f} 🚀"
                    )
                return
            elif self.position.is_short:
                # Close short on opposite reversion signal (RSI overbought or Stoch oversold relative to SMAs)
                if (self.rsi[-1] < self.rsi_sma[-1]) or (
                    self.stoch_k[-1] > self.stoch_sma[-1]
                ):
                    self.position.close()
                    print(
                        f"🌙 Moon Dev: Short Exit on Reversion Signal at {self.data.Close[-1]:.2f} 🚀"
                    )
                return

        # Entry conditions only if no position and sufficient history
        if (
            (not self.position)
            and (len(self.rsi) > 20)
            and (self.adx[-1] < self.adx_threshold)
            and (self.data.Volume[-1] > self.volume_sma[-1])
        ):
            entry_price = self.data.Close[-1]
            atr_val = self.atr[-1]
            if np.isnan(atr_val) or atr_val == 0:
                return

            # Long entry: RSI oversold + Stoch overbought divergence for bullish reversion
            if (self.rsi[-1] < self.rsi_sma[-1]) and (
                self.stoch_k[-1] > self.stoch_sma[-1]
            ):
                sl_price = entry_price - (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price + (self.atr_multiplier_tp * atr_val)
                risk_distance = entry_price - sl_price

                # Position sizing: risk fixed % of equity, allow float for precise sizing
                equity = self.equity
                risk_amount = equity * self.risk_per_trade
                position_size = risk_amount / risk_distance if risk_distance > 0 else 0

                # Validate for long
                if (
                    position_size > 0
                    and not np.isnan(sl_price)
                    and not np.isnan(tp_price)
                    and sl_price < entry_price < tp_price
                ):
                    self.buy(
                        size=position_size, sl=sl_price, tp=tp_price
                    )  # Market entry, removed limit for immediate fill
                    print(
                        f"🌙 Moon Dev: Long Entry at {entry_price:.2f}, Size: {position_size:.4f}, SL: {sl_price:.2f}, TP: {tp_price:.2f} ✨"
                    )
                else:
                    print(
                        "🌙 Moon Dev: Invalid long position size or SL/TP levels, skipping entry ⚠️"
                    )
                return

            # Short entry: RSI overbought + Stoch oversold divergence for bearish reversion
            if (self.rsi[-1] > self.rsi_sma[-1]) and (
                self.stoch_k[-1] < self.stoch_sma[-1]
            ):
                sl_price = entry_price + (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price - (self.atr_multiplier_tp * atr_val)
                risk_distance = sl_price - entry_price

                # Position sizing: risk fixed % of equity, allow float for precise sizing
                equity = self.equity
                risk_amount = equity * self.risk_per_trade
                position_size = risk_amount / risk_distance if risk_distance > 0 else 0

                # Validate for short
                if (
                    position_size > 0
                    and not np.isnan(sl_price)
                    and not np.isnan(tp_price)
                    and tp_price < entry_price < sl_price
                ):
                    self.sell(
                        size=position_size, sl=sl_price, tp=tp_price
                    )  # Market entry, removed limit for immediate fill
                    print(
                        f"🌙 Moon Dev: Short Entry at {entry_price:.2f}, Size: {position_size:.4f}, SL: {sl_price:.2f}, TP: {tp_price:.2f} ✨"
                    )
                else:
                    print(
                        "🌙 Moon Dev: Invalid short position size or SL/TP levels, skipping entry ⚠️"
                    )


# Run backtest
bt = Backtest(
    df,
    DivergentReversion,
    cash=1000000,
    commission=0.002,
    exclusive_orders=True,
    trade_on_close=True,
)

print("🌙 Moon Dev: Running optimized backtest... 🚀")
stats = bt.run()
print(stats)
