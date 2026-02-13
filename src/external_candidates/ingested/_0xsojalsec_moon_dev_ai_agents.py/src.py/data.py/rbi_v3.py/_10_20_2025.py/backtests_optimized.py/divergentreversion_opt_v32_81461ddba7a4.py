# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v32.py
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
    adx_threshold = 30  # 🌙 Moon Dev: Further loosened ADX threshold from 25 to 30 to capture more ranging market opportunities, increasing trade frequency to accelerate towards 50% target while still avoiding strong trends
    risk_per_trade = 0.08  # 🌙 Moon Dev: Increased risk per trade from 5% to 8% for faster equity growth and compounding, balanced by ATR-based sizing and new trend filter to maintain risk control
    atr_multiplier_sl = 2
    atr_multiplier_tp = 12  # 🌙 Moon Dev: Extended TP multiplier from 10 to 12 ATR for improved 6:1 risk-reward ratio, enabling larger profit capture on mean reversion swings to boost overall returns

    def init(self):
        # RSI(14) - standard 14 period for reduced noise and higher quality signals in crypto volatility
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.rsi_sma = self.I(
            talib.SMA, self.rsi, timeperiod=14
        )  # 🌙 Moon Dev: Consistent SMA period matching RSI for reliable crossover detection with minimal whipsaws

        # Stochastic %K(14,3,3) - standard fastk 14 for balanced momentum signals
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
        )  # 🌙 Moon Dev: Aligned SMA to Stoch period for precise timing of momentum shifts

        # ATR(14) for dynamic stops - standard for accurate volatility adjustment
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # ADX(14) for trend filter - standard period for reliable strength measurement
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # Volume SMA(20) - 20 period for stable baseline volume confirmation
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)

        # EMA(200) for trend alignment filter - new addition to ensure pullback trades align with overall trend, improving win rate and risk-adjusted returns by avoiding counter-trend reversion setups
        self.ema200 = self.I(talib.EMA, self.data.Close, timeperiod=200)

        print(
            "🌙 Moon Dev: Added EMA200 trend filter for higher-quality aligned entries; indicators tuned for optimal balance of frequency and reliability to drive returns higher ✨"
        )

    def next(self):
        # 🌙 Moon Dev: Retained reliance on SL/TP exits to fully capture reversion moves, with trend filter enhancing entry quality for better profitability without premature exits

        # Entry conditions only if no position and sufficient history for all indicators including EMA200
        if (
            (not self.position)
            and (len(self.rsi) > 200)
            and (self.adx[-1] < self.adx_threshold)
        ):  # 🌙 Moon Dev: Extended history check to 200 bars to ensure EMA stability, filtering early data for more robust signals

            # Loosened volume filter to >0.8x average for broader confirmation, allowing more trades in varying volume regimes without compromising quality
            vol_confirm = self.data.Volume[-1] > 0.8 * self.vol_sma[-1]

            # Long entry: RSI mildly oversold (below 40 and SMA), Stoch turning up (above SMA and below 60), volume confirm, and price above EMA200 for uptrend pullback bias - adjusted thresholds for increased frequency with trend alignment
            if (
                vol_confirm
                and (self.rsi[-1] < self.rsi_sma[-1])
                and (self.rsi[-1] < 40)
                and (self.stoch_k[-1] > self.stoch_sma[-1])
                and (self.stoch_k[-1] < 60)
                and (self.data.Close[-1] > self.ema200[-1])
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
                )  # 🌙 Moon Dev: Raised max position size from 50 to 100 to leverage high-conviction trend-aligned setups more aggressively, capped for risk control

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
                        "🌙 Moon Dev: Invalid long position size or SL/TP levels, skipping entry ⚠️"
                    )
                return

            # Short entry: RSI mildly overbought (above 60 and SMA), Stoch turning down (below SMA and above 40), volume confirm, and price below EMA200 for downtrend pullback bias - symmetric adjustments for balanced opportunities
            if (
                vol_confirm
                and (self.rsi[-1] > self.rsi_sma[-1])
                and (self.rsi[-1] > 60)
                and (self.stoch_k[-1] < self.stoch_sma[-1])
                and (self.stoch_k[-1] > 40)
                and (self.data.Close[-1] < self.ema200[-1])
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
                )  # 🌙 Moon Dev: Increased max size to 100 for amplified short exposure in downtrends, supporting higher return potential

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
