# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v35.py
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
    adx_threshold = 30  # 🌙 Moon Dev: Loosened ADX threshold from 25 to 30 to capture more ranging market opportunities, increasing trade frequency and exposure to mean reversion setups for accelerated return growth towards 50% target
    risk_per_trade = 0.08  # 🌙 Moon Dev: Increased risk per trade from 5% to 8% to enhance compounding effects on winning trades, balanced by volatility-based sizing to maintain risk control while pushing for higher overall returns
    atr_multiplier_sl = 1.5  # 🌙 Moon Dev: Tightened SL multiplier from 2 to 1.5 ATR for quicker invalidation of weak signals, improving capital efficiency and allowing more trades to reach profitable TP levels
    atr_multiplier_tp = 12  # 🌙 Moon Dev: Extended TP multiplier from 10 to 12 ATR for an 8:1 risk-reward ratio, enabling capture of deeper mean reversion swings in volatile crypto markets to boost profitability per trade

    def init(self):
        # RSI(14) - standard period for reliable overbought/oversold detection
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.rsi_sma = self.I(talib.SMA, self.rsi, timeperiod=14)

        # Stochastic %K(14,3,3) - standard for momentum turns
        self.stoch_k, _ = self.I(
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

        # Volume SMA(20) for confirmation
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)

        # EMA(50) for trend bias filter - 🌙 Moon Dev: Added 50-period EMA to ensure mean reversion trades align with the intermediate trend (longs above EMA, shorts below), improving win rate by avoiding counter-trend setups and enhancing return potential in favorable regimes

        self.ema50 = self.I(talib.EMA, self.data.Close, timeperiod=50)

        print(
            "🌙 Moon Dev: Added EMA50 trend filter for directional bias in reversion trades; tightened SL/TP for better RR; overall tuning to increase frequency and quality for 50% target ✨"
        )

    def next(self):
        # Dynamic trailing stop implementation - 🌙 Moon Dev: Added trailing stop logic after 3 ATR profit to lock in gains and let winners run beyond fixed TP, reducing premature exits and capturing larger moves to significantly improve average returns while preserving risk management

        if self.trades:
            last_trade = self.trades[-1]
            atr_val = self.atr[-1]

            if last_trade.is_long:
                profit = self.data.Close[-1] - last_trade.entry_price
                if profit > 3 * atr_val:
                    trail_sl = self.data.Close[-1] - self.atr_multiplier_sl * atr_val
                    last_trade.sl = max(last_trade.sl, trail_sl)
            elif last_trade.is_short:
                profit = last_trade.entry_price - self.data.Close[-1]
                if profit > 3 * atr_val:
                    trail_sl = self.data.Close[-1] + self.atr_multiplier_sl * atr_val
                    last_trade.sl = min(last_trade.sl, trail_sl)

        # Entry conditions only if no position and sufficient history
        if (
            (not self.position)
            and (len(self.rsi) > 100)
            and (self.adx[-1] < self.adx_threshold)
        ):  # 🌙 Moon Dev: Extended history check to 100 bars to ensure stable EMA50 values, filtering early noise for higher-quality signals

            # Loosened volume filter to >0.8x average for broader inclusion of volume-confirmed setups, increasing trade opportunities to drive higher cumulative returns
            vol_confirm = self.data.Volume[-1] > 0.8 * self.vol_sma[-1]

            # Trend bias filter using EMA50
            above_trend = self.data.Close[-1] > self.ema50[-1]
            below_trend = self.data.Close[-1] < self.ema50[-1]

            # Long entry: Tightened RSI to <30 for stronger oversold, Stoch turning up from <50; added trend bias for longs above EMA50
            if (
                vol_confirm
                and above_trend
                and (self.rsi[-1] < self.rsi_sma[-1])
                and (self.rsi[-1] < 30)
                and (self.stoch_k[-1] > self.stoch_sma[-1])
                and (self.stoch_k[-1] < 50)
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
                )  # 🌙 Moon Dev: Increased max position size from 50 to 100 to leverage high-conviction trend-aligned setups, amplifying returns while ATR limits exposure

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

            # Short entry: Tightened RSI to >70 for stronger overbought, Stoch turning down from >50; added trend bias for shorts below EMA50
            if (
                vol_confirm
                and below_trend
                and (self.rsi[-1] > self.rsi_sma[-1])
                and (self.rsi[-1] > 70)
                and (self.stoch_k[-1] < self.stoch_sma[-1])
                and (self.stoch_k[-1] > 50)
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
                )  # 🌙 Moon Dev: Increased max size to 100 for amplified short exposure in downtrends, enhancing reversion profits

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
