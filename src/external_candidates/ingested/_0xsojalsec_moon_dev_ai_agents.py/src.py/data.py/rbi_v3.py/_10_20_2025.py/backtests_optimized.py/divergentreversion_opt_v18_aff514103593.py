# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v18.py
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
    adx_threshold = 20  # 🌙 Moon Dev: Tightened ADX threshold from 25 to 20 for stricter ranging market filter to avoid weak trends
    risk_per_trade = 0.01  # 1% risk per trade, maintained for solid risk management
    atr_multiplier_sl = 2  # Stop loss multiplier
    atr_multiplier_tp = 6  # 🌙 Moon Dev: Increased TP multiplier from 4 to 6 for 1:3 RR to boost returns on winning trades while keeping risk fixed

    def init(self):
        # RSI(14) - 🌙 Moon Dev: Changed from 20 to 14 for faster response to overbought/oversold conditions
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.rsi_sma = self.I(
            talib.SMA, self.rsi, timeperiod=14
        )  # 🌙 Moon Dev: Shortened SMA period to 14 for better alignment with RSI

        # Stochastic %K(14,3,3) - 🌙 Moon Dev: Updated to standard Stochastic parameters for more reliable momentum signals
        self.stoch_k, self.stoch_d = self.I(
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
        )  # 🌙 Moon Dev: SMA of %K for divergence detection, shortened period

        # ATR(14) for dynamic stops - unchanged, solid for volatility adjustment
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # ADX(14) for trend filter
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # Volume SMA for filter - 🌙 Moon Dev: Added volume confirmation to avoid low-volume false signals, improving entry quality
        self.volume_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)

        print("🌙 Moon Dev: Indicators initialized with optimizations ✨")

    def next(self):
        # 🌙 Moon Dev: Check exits first for any open position
        if self.position:
            if self.position.is_long:
                # Long exit on reversion: RSI crosses above SMA or Stoch %K crosses below SMA
                if (self.rsi[-1] > self.rsi_sma[-1]) or (
                    self.stoch_k[-1] < self.stoch_sma[-1]
                ):
                    self.position.close()
                    print(
                        f"🌙 Moon Dev: Long Exit on Reversion Signal at {self.data.Close[-1]:.2f} 🚀"
                    )
                return
            elif self.position.is_short:
                # Short exit on reversion: RSI crosses below SMA or Stoch %K crosses above SMA
                if (self.rsi[-1] < self.rsi_sma[-1]) or (
                    self.stoch_k[-1] > self.stoch_sma[-1]
                ):
                    self.position.close()
                    print(
                        f"🌙 Moon Dev: Short Exit on Reversion Signal at {self.data.Close[-1]:.2f} 🚀"
                    )
                return

        # 🌙 Moon Dev: Entry conditions only if no position and sufficient history
        if (
            (not self.position)
            and (len(self.rsi) > 20)
            and (self.adx[-1] < self.adx_threshold)
            and (self.data.Volume[-1] > self.volume_sma[-1])
        ):
            entry_price = self.data.Close[-1]
            atr_val = self.atr[-1]
            if np.isnan(atr_val) or atr_val == 0:
                return  # Skip if invalid ATR

            # Long entry: Bullish divergence - RSI oversold (< SMA) and Stoch momentum rising (> SMA)
            if (self.rsi[-1] < self.rsi_sma[-1]) and (
                self.stoch_k[-1] > self.stoch_sma[-1]
            ):
                sl_price = entry_price - (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price + (self.atr_multiplier_tp * atr_val)
                risk_distance = entry_price - sl_price

                # Position sizing: risk 1% of equity - 🌙 Moon Dev: Allow fractional sizes for precise risk control (no int rounding)
                equity = self.equity
                risk_amount = equity * self.risk_per_trade
                position_size = risk_amount / risk_distance  # Float for fractional BTC

                # Check validity for long
                if (
                    position_size > 0
                    and not np.isnan(sl_price)
                    and not np.isnan(tp_price)
                    and sl_price < entry_price < tp_price
                ):
                    self.buy(
                        size=position_size, sl=sl_price, tp=tp_price
                    )  # 🌙 Moon Dev: Removed limit for market entry at close
                    print(
                        f"🌙 Moon Dev: Long Entry at {entry_price:.2f}, Size: {position_size:.4f}, SL: {sl_price:.2f}, TP: {tp_price:.2f} ✨"
                    )
                else:
                    print(
                        "🌙 Moon Dev: Invalid long position size or SL/TP levels, skipping entry ⚠️"
                    )
                return

            # Short entry: Bearish divergence - RSI overbought (> SMA) and Stoch momentum falling (< SMA)
            if (self.rsi[-1] > self.rsi_sma[-1]) and (
                self.stoch_k[-1] < self.stoch_sma[-1]
            ):
                sl_price = entry_price + (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price - (self.atr_multiplier_tp * atr_val)
                risk_distance = sl_price - entry_price

                # Position sizing: risk 1% of equity
                equity = self.equity
                risk_amount = equity * self.risk_per_trade
                position_size = risk_amount / risk_distance  # Float for fractional BTC

                # Check validity for short
                if (
                    position_size > 0
                    and not np.isnan(sl_price)
                    and not np.isnan(tp_price)
                    and tp_price < entry_price < sl_price
                ):
                    self.sell(
                        size=position_size, sl=sl_price, tp=tp_price
                    )  # 🌙 Moon Dev: Removed limit for market entry at close
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

print("🌙 Moon Dev: Running backtest... 🚀")
stats = bt.run()
print(stats)
