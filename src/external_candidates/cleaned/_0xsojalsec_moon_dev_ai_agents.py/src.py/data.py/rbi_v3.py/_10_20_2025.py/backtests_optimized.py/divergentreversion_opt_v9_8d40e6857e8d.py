# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v9.py
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
    adx_threshold = (
        20  # 🌙 Moon Dev: Tightened ADX threshold from 25 to 20 for stricter ranging market filter to avoid weak trends
    )
    risk_per_trade = 0.015  # 🌙 Moon Dev: Increased risk per trade from 1% to 1.5% to allow higher exposure and target 50% returns while maintaining risk management
    atr_multiplier_sl = 1.5  # 🌙 Moon Dev: Reduced SL multiplier from 2 to 1.5 for tighter stops to improve win rate
    atr_multiplier_tp = (
        4.5  # 🌙 Moon Dev: Increased TP multiplier from 4 to 4.5 for 1:3 RR (from 1:2) to boost returns on winners
    )

    def init(self):
        # RSI(14) - 🌙 Moon Dev: Changed period from 20 to 14 (standard) for more responsive signals
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)

        # Stochastic %K(14,3,3) - 🌙 Moon Dev: Changed to standard Stochastic parameters for better overbought/oversold detection
        self.stoch_k, _ = self.I(
            talib.STOCH,
            self.data.High,
            self.data.Low,
            self.data.Close,
            fastk_period=14,
            slowk_period=3,
            slowd_period=3,
        )

        # Volume SMA(20) - 🌙 Moon Dev: Added volume filter to confirm entries only on above-average volume for higher quality setups
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)

        # ATR(14) for dynamic stops
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)

        # ADX(14) for trend filter
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14)

        # 🌙 Moon Dev: Removed RSI and Stoch SMAs as we're using absolute levels for tighter, more reliable entry/exit signals (e.g., RSI >70 for overbought)
        print("🌙 Moon Dev: Indicators initialized with optimizations for better signal quality ✨")

    def next(self):
        # Check for exits first
        if self.position.is_short:
            # 🌙 Moon Dev: Exit short on mean reversion to neutral levels (RSI <50 or Stoch >50) for improved timing
            if (self.rsi[-1] < 50) or (self.stoch_k[-1] > 50):
                self.position.close()
                print(f"🌙 Moon Dev: Short Exit on Reversion Signal at {self.data.Close[-1]:.2f} 🚀")
            return

        if self.position.is_long:
            # 🌙 Moon Dev: Exit long on mean reversion to neutral levels (RSI >50 or Stoch <50) symmetrically
            if (self.rsi[-1] > 50) or (self.stoch_k[-1] < 50):
                self.position.close()
                print(f"🌙 Moon Dev: Long Exit on Reversion Signal at {self.data.Close[-1]:.2f} 🚀")
            return

        # Entry conditions (only if no position) - 🌙 Moon Dev: Added symmetric long entries and absolute thresholds (RSI 70/30, Stoch 50 crossover) for divergence detection; added volume > SMA for confirmation
        if (
            (not self.position)
            and (len(self.rsi) > 20)
            and (self.adx[-1] < self.adx_threshold)
            and (self.data.Volume[-1] > self.vol_sma[-1])
        ):
            entry_price = self.data.Close[-1]
            atr_val = self.atr[-1]

            # Short entry: RSI overbought (>70) with Stoch not overbought (<50) for bearish divergence in ranging market
            if (self.rsi[-1] > 70) and (self.stoch_k[-1] < 50):
                sl_price = entry_price + (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price - (self.atr_multiplier_tp * atr_val)
                risk_distance = sl_price - entry_price

                # Position sizing: risk fixed % of equity - 🌙 Moon Dev: Use float for fractional BTC positions (no int rounding) for precise risk management
                equity = self.equity
                risk_amount = equity * self.risk_per_trade
                position_size = risk_amount / risk_distance

                # Check validity - added min size for practicality
                if (
                    position_size >= 0.001
                    and not np.isnan(sl_price)
                    and not np.isnan(tp_price)
                    and tp_price < entry_price < sl_price
                ):
                    self.sell(size=position_size, limit=entry_price, sl=sl_price, tp=tp_price)
                    print(
                        f"🌙 Moon Dev: Short Entry at {entry_price:.2f}, Size: {position_size:.4f}, SL: {sl_price:.2f}, TP: {tp_price:.2f} ✨"
                    )
                else:
                    print("🌙 Moon Dev: Invalid short position size or SL/TP levels, skipping entry ⚠️")
                return

            # Long entry: RSI oversold (<30) with Stoch not oversold (>50) for bullish divergence in ranging market
            if (self.rsi[-1] < 30) and (self.stoch_k[-1] > 50):
                sl_price = entry_price - (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price + (self.atr_multiplier_tp * atr_val)
                risk_distance = entry_price - sl_price

                equity = self.equity
                risk_amount = equity * self.risk_per_trade
                position_size = risk_amount / risk_distance

                # Check validity
                if (
                    position_size >= 0.001
                    and not np.isnan(sl_price)
                    and not np.isnan(tp_price)
                    and sl_price < entry_price < tp_price
                ):
                    self.buy(size=position_size, limit=entry_price, sl=sl_price, tp=tp_price)
                    print(
                        f"🌙 Moon Dev: Long Entry at {entry_price:.2f}, Size: {position_size:.4f}, SL: {sl_price:.2f}, TP: {tp_price:.2f} ✨"
                    )
                else:
                    print("🌙 Moon Dev: Invalid long position size or SL/TP levels, skipping entry ⚠️")


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
