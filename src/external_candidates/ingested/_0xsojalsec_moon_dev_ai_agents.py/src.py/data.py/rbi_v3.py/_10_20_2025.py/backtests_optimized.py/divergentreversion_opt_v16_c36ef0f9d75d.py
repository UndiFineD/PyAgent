# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v16.py
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
    # 🌙 Moon Dev Optimization: Tightened parameters for faster signals and better alignment
    rsi_period = 14  # Changed from 20 to standard 14 for quicker response
    stoch_fast = 5  # Faster stochastic for 15m timeframe (was 8)
    sma_period = 5  # Shorter SMA on indicators for recent overbought/oversold (was 20)
    adx_threshold = 20  # Tightened from 25 to focus on stronger ranging markets
    risk_per_trade = 0.015  # Increased slightly from 1% to 1.5% for higher exposure while managing risk
    atr_multiplier_sl = 1.5  # Tightened SL from 2 to 1.5 ATR for better risk control
    atr_multiplier_tp = 4.5  # Improved RR to 1:3 (from 1:2) for higher reward potential
    trend_exit_adx = 30  # New: Exit on strong trend to avoid whipsaws
    min_position_size = 0.001  # Minimum size to avoid micro trades
    volume_multiplier = (
        1.2  # New: Volume filter - only trade on 20% above average volume
    )

    def init(self):
        # RSI with optimized period
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=self.rsi_period)
        self.rsi_sma = self.I(talib.SMA, self.rsi, timeperiod=self.sma_period)

        # Stochastic with faster parameters and standard slowk/d
        self.stoch_k, _ = self.I(
            talib.STOCH,
            self.data.High,
            self.data.Low,
            self.data.Close,
            fastk_period=self.stoch_fast,
            slowk_period=3,
            slowd_period=3,
        )
        self.stoch_sma = self.I(talib.SMA, self.stoch_k, timeperiod=self.sma_period)

        # ATR(14) for dynamic stops - unchanged but used more efficiently
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # ADX(14) for trend filter - tightened threshold
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # New: Volume SMA for quality filter to avoid low-volume fakeouts
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)

        print("🌙 Moon Dev: Indicators initialized with optimizations ✨")

    def next(self):
        # 🌙 Moon Dev Optimization: New trend-based exit to protect profits in breakouts
        if self.position and self.adx[-1] > self.trend_exit_adx:
            self.position.close()
            print(
                f"🌙 Moon Dev: Exit on trend strength (ADX > {self.trend_exit_adx}) at {self.data.Close[-1]:.2f} 🚀"
            )
            return

        # 🌙 Moon Dev Optimization: Improved reversion exits - wait for both indicators to align on oversold/overbought
        # This holds positions longer until full mean reversion, improving win rate
        if self.position.is_long:
            if (
                self.rsi[-1] > self.rsi_sma[-1]
                and self.stoch_k[-1] > self.stoch_sma[-1]
            ):
                self.position.close()
                print(
                    f"🌙 Moon Dev: Long Exit on Overbought Reversion Signal at {self.data.Close[-1]:.2f} 🚀"
                )
                return
        elif self.position.is_short:
            if (
                self.rsi[-1] < self.rsi_sma[-1]
                and self.stoch_k[-1] < self.stoch_sma[-1]
            ):
                self.position.close()
                print(
                    f"🌙 Moon Dev: Short Exit on Oversold Reversion Signal at {self.data.Close[-1]:.2f} 🚀"
                )
                return

        # Entry conditions only if no position and sufficient history
        if (not self.position) and (
            len(self.rsi) > 30
        ):  # Increased from 20 for full indicator warmup
            current_volume = self.data.Volume[-1]
            avg_volume = self.vol_sma[-1]
            volume_filter = current_volume > (
                avg_volume * self.volume_multiplier
            )  # New filter for high-conviction setups
            adx_filter = (
                self.adx[-1] < self.adx_threshold
            )  # Ranging market confirmation

            entry_price = self.data.Close[-1]
            atr_val = self.atr[-1]

            if np.isnan(atr_val) or not volume_filter or not adx_filter:
                return

            # 🌙 Moon Dev Optimization: Fixed entry signals to aligned overbought/oversold (both indicators agree)
            # Previously divergent/mixed - now both high for short, both low for long for true mean reversion
            # Added long entries for balance (BTC has up bias, shorts alone lose)

            # Long entry: Both indicators oversold in ranging market with volume
            if (self.rsi[-1] < self.rsi_sma[-1]) and (
                self.stoch_k[-1] < self.stoch_sma[-1]
            ):
                sl_price = entry_price - (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price + (self.atr_multiplier_tp * atr_val)
                risk_distance = entry_price - sl_price

                equity = self.equity
                risk_amount = equity * self.risk_per_trade
                position_size = risk_amount / risk_distance  # Float for fractional BTC

                # Valid checks and min size
                if (
                    position_size >= self.min_position_size
                    and not np.isnan(sl_price)
                    and not np.isnan(tp_price)
                    and sl_price < entry_price < tp_price
                ):
                    self.buy(size=position_size, sl=sl_price, tp=tp_price)
                    print(
                        f"🌙 Moon Dev: Long Entry at {entry_price:.2f}, Size: {position_size:.4f}, SL: {sl_price:.2f}, TP: {tp_price:.2f} ✨"
                    )
                else:
                    print(
                        "🌙 Moon Dev: Invalid long position size or SL/TP levels, skipping entry ⚠️"
                    )

            # Short entry: Both indicators overbought in ranging market with volume
            elif (self.rsi[-1] > self.rsi_sma[-1]) and (
                self.stoch_k[-1] > self.stoch_sma[-1]
            ):
                sl_price = entry_price + (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price - (self.atr_multiplier_tp * atr_val)
                risk_distance = sl_price - entry_price

                equity = self.equity
                risk_amount = equity * self.risk_per_trade
                position_size = risk_amount / risk_distance  # Float for fractional BTC

                # Valid checks and min size
                if (
                    position_size >= self.min_position_size
                    and not np.isnan(sl_price)
                    and not np.isnan(tp_price)
                    and tp_price < entry_price < sl_price
                ):
                    self.sell(size=position_size, sl=sl_price, tp=tp_price)
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
