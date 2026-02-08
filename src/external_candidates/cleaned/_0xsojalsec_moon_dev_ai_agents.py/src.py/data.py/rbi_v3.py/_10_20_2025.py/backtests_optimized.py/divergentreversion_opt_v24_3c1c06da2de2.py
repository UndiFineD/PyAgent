# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v24.py
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
    adx_threshold = 25  # 🌙 Moon Dev: Loosened ADX threshold to 25 from 20 to include more mild trending/ranging markets, increasing trade frequency for higher overall returns while still avoiding strong trends
    risk_per_trade = 0.05  # 🌙 Moon Dev: Increased risk per trade to 5% from 3% to accelerate equity compounding towards 50% target, with ATR sizing ensuring controlled exposure per setup
    atr_multiplier_sl = 2
    atr_multiplier_tp = 10  # 🌙 Moon Dev: Increased TP multiplier to 10 ATR from 8 for a 5:1 risk-reward ratio, allowing captures of deeper mean reversions to boost profitability on high-quality trades

    def init(self):
        # RSI(10) - kept at 10 for fast response to overextensions in volatile crypto, balancing sensitivity and noise
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=10)
        self.rsi_sma = self.I(
            talib.SMA, self.rsi, timeperiod=10
        )  # 🌙 Moon Dev: Maintained matched SMA for accurate crossover signals in reversion setups

        # Stochastic %K(10,3,3) - kept fastk at 10 for quick momentum detection
        self.stoch_k, _ = self.I(
            talib.STOCH,
            self.data.High,
            self.data.Low,
            self.data.Close,
            fastk_period=10,
            slowk_period=3,
            slowd_period=3,
        )
        self.stoch_sma = self.I(
            talib.SMA, self.stoch_k, timeperiod=10
        )  # 🌙 Moon Dev: Kept SMA at 10 for consistent fast divergence detection, improving entry/exit timing

        # ATR(14) for dynamic stops - standard period for robust volatility adaptation
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)

        # ADX(14) for trend filter - standard for reliable ranging market identification
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14)

        # Volume SMA(10) - kept short for timely confirmation aligned with other indicators
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=10)

        print(
            "🌙 Moon Dev: Indicators initialized with optimized parameters for faster signals and volume alignment to enhance trade frequency and quality towards target returns ✨"
        )

    def next(self):
        # 🌙 Moon Dev: Fixed Stochastic exit conditions for logical symmetry - now properly closes long on bearish overbought crossovers and short on bullish oversold crossovers, eliminating bug that prematurely closed winning trades and significantly boosting realized profits
        # Further adjusted exit thresholds to 75/25 extremes to hold positions longer through noise, allowing more reversion capture for higher returns
        if self.position.is_long:
            # Long exit on strong bearish reversion: RSI overbought crossing down OR Stoch overbought crossing down
            if (self.rsi[-1] > 75 and self.rsi[-1] < self.rsi_sma[-1]) or (
                self.stoch_k[-1] > 75 and self.stoch_k[-1] < self.stoch_sma[-1]
            ):
                self.position.close()
                print(f"🌙 Moon Dev: Long Exit on Strong Bearish Reversion Signal at {self.data.Close[-1]:.2f} 🚀")
            return

        if self.position.is_short:
            # Short exit on strong bullish reversion: RSI oversold crossing up OR Stoch oversold crossing up
            if (self.rsi[-1] < 25 and self.rsi[-1] > self.rsi_sma[-1]) or (
                self.stoch_k[-1] < 25 and self.stoch_k[-1] > self.stoch_sma[-1]
            ):
                self.position.close()
                print(f"🌙 Moon Dev: Short Exit on Strong Bullish Reversion Signal at {self.data.Close[-1]:.2f} 🚀")
            return

        # 🌙 Moon Dev: Loosened RSI entry thresholds to 35/65 from 30/70 for more frequent high-conviction setups without entering too early; volume filter to >=1.0x SMA for broader participation while confirming activity, increasing trade count to drive returns higher
        # Entry conditions only if no position and sufficient history
        if (not self.position) and (len(self.rsi) > 20) and (self.adx[-1] < self.adx_threshold):
            # Volume filter: >= average for inclusive momentum confirmation, reducing missed opportunities
            vol_confirm = self.data.Volume[-1] >= 1.0 * self.vol_sma[-1]

            # Long entry: RSI oversold (below SMA and <35), Stoch turning up (above SMA) - balanced for quality and frequency
            if (
                vol_confirm
                and (self.rsi[-1] < self.rsi_sma[-1])
                and (self.rsi[-1] < 35)
                and (self.stoch_k[-1] > self.stoch_sma[-1])
            ):
                entry_price = self.data.Close[-1]
                atr_val = self.atr[-1]
                sl_price = entry_price - (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price + (self.atr_multiplier_tp * atr_val)
                risk_distance = entry_price - sl_price

                equity = self.equity
                risk_amount = equity * self.risk_per_trade
                position_size = risk_amount / risk_distance
                position_size = max(
                    0.001, min(100.0, position_size)
                )  # 🌙 Moon Dev: Raised max size to 100.0 from 20.0 to enable larger positions on strong signals, amplifying returns with controlled risk on 1M base

                if (
                    position_size > 0
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
                return

            # Short entry: RSI overbought (above SMA and >65), Stoch turning down (below SMA) - balanced for quality and frequency
            if (
                vol_confirm
                and (self.rsi[-1] > self.rsi_sma[-1])
                and (self.rsi[-1] > 65)
                and (self.stoch_k[-1] < self.stoch_sma[-1])
            ):
                entry_price = self.data.Close[-1]
                atr_val = self.atr[-1]
                sl_price = entry_price + (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price - (self.atr_multiplier_tp * atr_val)
                risk_distance = sl_price - entry_price

                equity = self.equity
                risk_amount = equity * self.risk_per_trade
                position_size = risk_amount / risk_distance
                position_size = max(
                    0.001, min(100.0, position_size)
                )  # 🌙 Moon Dev: Raised max size to 100.0 for symmetric aggressive shorts, maximizing reversion profits

                if (
                    position_size > 0
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
