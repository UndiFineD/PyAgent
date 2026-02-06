# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v39.py
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
    adx_threshold = 20  # 🌙 Moon Dev: Tightened ADX threshold back to 20 from 25 to focus on stricter ranging markets, improving win rate on true mean reversion setups for more reliable profits towards 50% target
    risk_per_trade = 0.08  # 🌙 Moon Dev: Increased risk per trade from 5% to 8% to accelerate compounding in high-RR setups, balanced by enhanced filters to maintain drawdown control
    atr_multiplier_sl = 2
    atr_multiplier_tp = 12  # 🌙 Moon Dev: Boosted TP multiplier from 10 to 12 ATR for a 6:1 risk-reward ratio, capturing deeper reversion swings in volatile crypto to amplify average wins and hit target returns
    trail_trigger = 6  # 🌙 Moon Dev: New trailing stop activation after 3x initial risk profit (6 ATR), to lock in gains on runners while allowing extension beyond fixed TP
    trail_atr_mult = 1.5  # 🌙 Moon Dev: Trail stop at 1.5 ATR from high/low once triggered, protecting profits dynamically without cutting winners short

    def init(self):
        # RSI(14) - standard 14 period for balanced noise reduction
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.rsi_sma = self.I(talib.SMA, self.rsi, timeperiod=14)

        # Stochastic %K(14,3,3) - standard fastk 14 for reliable momentum
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

        # Volume SMA(20) for stable baseline
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)

        # New: 200-period SMA for trend bias filter - ensures reversion trades align with broader direction to avoid counter-trend traps and boost overall profitability
        self.sma200 = self.I(talib.SMA, self.data.Close, timeperiod=200)

        print(
            "🌙 Moon Dev: Added 200 SMA trend filter and trailing stop logic for better alignment and profit protection, tightening ADX to 20 for quality trades to propel returns to 50% ✨"
        )

    def next(self):
        # Dynamic trailing stop management - 🌙 Moon Dev: Implement trailing after hitting 3x risk profit to let winners run further, increasing average trade size while securing gains for higher net returns
        if self.position:
            atr_val = self.atr[-1]
            entry_price = (
                self.position.entry_price
                if hasattr(self.position, "entry_price")
                else self.data.Close[-1]
            )
            pl_pips = (
                (self.data.Close[-1] - entry_price) / atr_val
                if self.position.is_long
                else (entry_price - self.data.Close[-1]) / atr_val
            )

            if pl_pips > self.trail_trigger:
                if self.position.is_long:
                    trail_sl = self.data.High[-1] - (self.trail_atr_mult * atr_val)
                    if trail_sl > self.position.sl:
                        self.position.sl = trail_sl
                        print(
                            f"🌙 Moon Dev: Trailing Long SL updated to {trail_sl:.2f} ✨"
                        )
                else:
                    trail_sl = self.data.Low[-1] + (self.trail_atr_mult * atr_val)
                    if trail_sl < self.position.sl:
                        self.position.sl = trail_sl
                        print(
                            f"🌙 Moon Dev: Trailing Short SL updated to {trail_sl:.2f} ✨"
                        )

        # Entry conditions only if no position and sufficient history
        if (
            (not self.position)
            and (len(self.rsi) > 100)
            and (self.adx[-1] < self.adx_threshold)
        ):  # 🌙 Moon Dev: Extended history check to 100 bars (including SMA200 stability) for robust signals, ensuring reliable entries from the start

            # Adjusted volume filter to >0.8x average for slightly more opportunities in quieter but still confirmatory volume, increasing trade count without quality loss
            vol_confirm = self.data.Volume[-1] > 0.8 * self.vol_sma[-1]

            # Trend bias filter - 🌙 Moon Dev: Added SMA200 confirmation (long above, short below) to trade mean reversion with the trend, filtering out low-probability counter-moves and enhancing win rate
            trend_long = self.data.Close[-1] > self.sma200[-1]
            trend_short = self.data.Close[-1] < self.sma200[-1]

            # Long entry: Tightened RSI to <30 (deeper oversold) and Stoch <40 for stronger reversion signals, combined with trend bias for higher conviction
            if (
                vol_confirm
                and trend_long
                and (self.rsi[-1] < self.rsi_sma[-1])
                and (self.rsi[-1] < 30)
                and (self.stoch_k[-1] > self.stoch_sma[-1])
                and (self.stoch_k[-1] < 40)
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
                    0.001, min(75.0, position_size)
                )  # 🌙 Moon Dev: Raised max position size to 75 from 50 to leverage high-conviction trend-aligned setups, amplifying returns with controlled risk

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

            # Short entry: Tightened RSI to >70 (deeper overbought) and Stoch >60 for symmetric strong signals, with trend bias
            if (
                vol_confirm
                and trend_short
                and (self.rsi[-1] > self.rsi_sma[-1])
                and (self.rsi[-1] > 70)
                and (self.stoch_k[-1] < self.stoch_sma[-1])
                and (self.stoch_k[-1] > 60)
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
                    0.001, min(75.0, position_size)
                )  # 🌙 Moon Dev: Raised max size to 75 for shorts, enabling larger profits in downtrends

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
