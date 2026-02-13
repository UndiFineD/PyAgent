# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v14.py
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
        25  # Kept at 25 for ranging market filter, realistic for avoiding trends
    )
    risk_per_trade = 0.01  # 1% risk maintained for good risk management
    atr_multiplier_sl = 2
    atr_multiplier_tp = 5  # Increased to 5x ATR for 1:2.5 RR to improve returns while keeping risk controlled 🌙

    def init(self):
        # RSI(14) - Adjusted to standard period for better responsiveness without curve fitting
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.rsi_sma = self.I(talib.SMA, self.rsi, timeperiod=14)

        # Stochastic %K(14,3,3) - Changed to standard parameters for more reliable momentum signals
        self.stoch_k, self.stoch_d = self.I(
            talib.STOCH,
            self.data.High,
            self.data.Low,
            self.data.Close,
            fastk_period=14,
            slowk_period=3,
            slowd_period=3,
        )
        self.stoch_sma = self.I(talib.SMA, self.stoch_k, timeperiod=20)

        # ATR(14) for dynamic stops
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # ADX(14) for trend filter
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # Volume SMA(20) - Added for quality filter: only trade on above-average volume to avoid low-liquidity setups ✨
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)

        print("🌙 Moon Dev: Indicators initialized with optimizations ✨")

    def next(self):
        # Check for exits first if in position - Kept signal-based exits but symmetric for long/short to capture reversions timely
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

        # Entry conditions only if no position, sufficient history, low ADX (ranging), and volume filter
        if (
            (not self.position)
            and (len(self.rsi) > 20)
            and (self.adx[-1] < self.adx_threshold)
            and (self.data.Volume[-1] > self.vol_sma[-1])
        ):

            entry_price = self.data.Close[-1]
            atr_val = self.atr[-1]

            # Long entry: RSI oversold, Stoch overbought (divergent reversion up) - Added symmetric longs to capture bull moves in BTC for higher returns 🌙
            if (self.rsi[-1] < self.rsi_sma[-1]) and (
                self.stoch_k[-1] > self.stoch_sma[-1]
            ):
                sl_price = entry_price - (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price + (self.atr_multiplier_tp * atr_val)
                risk_distance = entry_price - sl_price

                # Position sizing: risk 1% of equity - Changed to float for precise fractional sizing in crypto
                equity = self.equity
                risk_amount = equity * self.risk_per_trade
                position_size = (
                    risk_amount / risk_distance
                )  # Float for better precision

                # Check if size and SL/TP levels are valid for long
                if (
                    position_size > 0
                    and not np.isnan(sl_price)
                    and not np.isnan(tp_price)
                    and sl_price < entry_price < tp_price
                ):
                    self.buy(
                        size=position_size, limit=entry_price, sl=sl_price, tp=tp_price
                    )
                    print(
                        f"🌙 Moon Dev: Long Entry at {entry_price:.2f}, Size: {position_size:.4f}, SL: {sl_price:.2f}, TP: {tp_price:.2f} ✨"
                    )
                else:
                    print(
                        "🌙 Moon Dev: Invalid position size or SL/TP levels for long, skipping entry ⚠️"
                    )
                return

            # Short entry: RSI overbought, Stoch oversold (divergent reversion down) - Original logic preserved
            if (self.rsi[-1] > self.rsi_sma[-1]) and (
                self.stoch_k[-1] < self.stoch_sma[-1]
            ):
                sl_price = entry_price + (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price - (self.atr_multiplier_tp * atr_val)
                risk_distance = sl_price - entry_price

                # Position sizing: risk 1% of equity - Float for precision
                equity = self.equity
                risk_amount = equity * self.risk_per_trade
                position_size = (
                    risk_amount / risk_distance
                )  # Float for better precision

                # Check if size and SL/TP levels are valid for short
                if (
                    position_size > 0
                    and not np.isnan(sl_price)
                    and not np.isnan(tp_price)
                    and tp_price < entry_price < sl_price
                ):
                    self.sell(
                        size=position_size, limit=entry_price, sl=sl_price, tp=tp_price
                    )
                    print(
                        f"🌙 Moon Dev: Short Entry at {entry_price:.2f}, Size: {position_size:.4f}, SL: {sl_price:.2f}, TP: {tp_price:.2f} ✨"
                    )
                else:
                    print(
                        "🌙 Moon Dev: Invalid position size or SL/TP levels for short, skipping entry ⚠️"
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
