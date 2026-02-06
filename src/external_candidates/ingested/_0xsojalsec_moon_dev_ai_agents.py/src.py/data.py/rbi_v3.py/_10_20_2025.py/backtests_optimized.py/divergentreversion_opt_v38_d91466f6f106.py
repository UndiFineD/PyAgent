# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v38.py
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
    adx_threshold = 20  # 🌙 Moon Dev: Tightened ADX threshold back to 20 from 25 to focus on even lower trend environments, improving mean reversion success rate and filtering out emerging trends for higher quality trades towards 50% target
    risk_per_trade = 0.08  # 🌙 Moon Dev: Increased risk per trade to 8% from 5% to accelerate compounding on winning trades, balanced by enhanced filters and trailing stops to maintain drawdown control while pushing for target returns
    atr_multiplier_sl = 1.5  # 🌙 Moon Dev: Reduced SL multiplier to 1.5 ATR from 2 for tighter stops, reducing risk exposure per trade and allowing larger position sizes to amplify returns without increasing overall portfolio risk
    atr_multiplier_tp = 12  # 🌙 Moon Dev: Extended TP to 12 ATR from 10 for an 8:1 RR ratio, capturing deeper reversion swings in crypto volatility to boost average profit per trade significantly
    trailing_activation = 4  # ATR levels to activate trailing stop
    trailing_offset = 1  # ATR offset for trailing SL

    def init(self):
        # RSI(14) - kept at 14 for balanced noise reduction, but added divergence check potential via tighter crossovers
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.rsi_sma = self.I(talib.SMA, self.rsi, timeperiod=14)

        # Stochastic %K(14,3,3) - standard for reliable momentum turns
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

        # Volume SMA(20) - stable baseline
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)

        # 🌙 Moon Dev: Added 200-period SMA as a higher timeframe trend filter to confirm overall direction, only taking longs above it and shorts below to align with macro trend and avoid counter-trend traps, enhancing win rate for target returns
        self.sma200 = self.I(talib.SMA, self.data.Close, timeperiod=200)

        # 🌙 Moon Dev: Added Bollinger Bands (20,2) as complementary reversion indicator to confirm overextensions, tightening entry quality by requiring price touch of outer bands for stronger mean reversion setups ✨

        self.bb_upper, self.bb_middle, self.bb_lower = self.I(
            talib.BBANDS, self.data.Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
        )

        print(
            "🌙 Moon Dev: Enhanced with SMA200 trend filter and BBands for multi-indicator confirmation, plus trailing stop params for better exit management to drive returns to 50% while controlling risk ✨"
        )

    def next(self):
        # 🌙 Moon Dev: Implemented trailing stop logic for positions: activates after 4 ATR profit, trails SL at 1 ATR behind high/low to lock in gains on extended moves, letting winners run longer without giving back profits, key to hitting high return targets
        if self.position:
            atr_val = self.atr[-1]
            if self.position.is_long:
                unrealized_pnl = self.data.Close[-1] - self.position.entry_price
                profit_atr = unrealized_pnl / atr_val
                if profit_atr > self.trailing_activation:
                    new_sl = self.data.High[-1] - (
                        self.trailing_offset * atr_val
                    )  # Trail from recent high
                    if new_sl > self.position.sl:
                        self.position.sl = new_sl
                        print(
                            f"🌙 Moon Dev: Trailing SL updated for long to {new_sl:.2f} 🚀"
                        )
            else:  # short
                unrealized_pnl = self.position.entry_price - self.data.Close[-1]
                profit_atr = unrealized_pnl / atr_val
                if profit_atr > self.trailing_activation:
                    new_sl = self.data.Low[-1] + (
                        self.trailing_offset * atr_val
                    )  # Trail from recent low
                    if new_sl < self.position.sl:
                        self.position.sl = new_sl
                        print(
                            f"🌙 Moon Dev: Trailing SL updated for short to {new_sl:.2f} 🚀"
                        )

        # Entry conditions only if no position and sufficient history
        if (not self.position) and (
            len(self.rsi) > 100
        ):  # 🌙 Moon Dev: Extended history check to 100 bars (including SMA200) for fully stable indicators, ensuring reliable signals from the start
            vol_confirm = (
                self.data.Volume[-1] > 1.2 * self.vol_sma[-1]
            )  # 🌙 Moon Dev: Tightened volume filter to >1.2x SMA from 1.0x for higher conviction entries, filtering low-volume noise to improve trade quality and win rate

            # 🌙 Moon Dev: Added BB touch and trend filter: for long, price near lower BB and above SMA200; for short, near upper BB and below SMA200 - this multi-TF confirmation reduces false signals in ranging markets, boosting overall profitability
            bb_long_confirm = (
                self.data.Close[-1] <= self.bb_lower[-1] * 1.01
            )  # Within 1% of lower band
            bb_short_confirm = (
                self.data.Close[-1] >= self.bb_upper[-1] * 0.99
            )  # Within 1% of upper band
            trend_long = self.data.Close[-1] > self.sma200[-1]
            trend_short = self.data.Close[-1] < self.sma200[-1]

            if (
                (self.adx[-1] < self.adx_threshold)
                and vol_confirm
                and trend_long
                and bb_long_confirm
            ):
                # Long entry: Tightened RSI to <30 from 35 for deeper oversold, Stoch <45 from 50 for stronger turn
                if (
                    (self.rsi[-1] < self.rsi_sma[-1])
                    and (self.rsi[-1] < 30)
                    and (self.stoch_k[-1] > self.stoch_sma[-1])
                    and (self.stoch_k[-1] < 45)
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
                    )  # 🌙 Moon Dev: Further increased max size to 100 from 50 with tighter SL and filters, allowing larger bets on confirmed setups to compound towards 50% faster

                    if (
                        position_size > 0
                        and not np.isnan(sl_price)
                        and not np.isnan(tp_price)
                        and sl_price < entry_price < tp_price
                    ):
                        self.buy(
                            size=position_size,
                            limit=entry_price,
                            sl=sl_price,
                            tp=tp_price,
                        )
                        print(
                            f"🌙 Moon Dev: Long Entry at {entry_price:.2f}, Size: {position_size:.4f}, SL: {sl_price:.2f}, TP: {tp_price:.2f} ✨"
                        )
                    else:
                        print(
                            "🌙 Moon Dev: Invalid long position size or SL/TP levels, skipping entry ⚠️"
                        )
                    return

            if (
                (self.adx[-1] < self.adx_threshold)
                and vol_confirm
                and trend_short
                and bb_short_confirm
            ):
                # Short entry: Tightened RSI to >70 from 65, Stoch >55 from 50
                if (
                    (self.rsi[-1] > self.rsi_sma[-1])
                    and (self.rsi[-1] > 70)
                    and (self.stoch_k[-1] < self.stoch_sma[-1])
                    and (self.stoch_k[-1] > 55)
                ):
                    entry_price = self.data.Close[-1]
                    atr_val = self.atr[-1]
                    sl_price = entry_price + (self.atr_multiplier_sl * atr_val)
                    tp_price = entry_price - (self.atr_multiplier_tp * atr_val)
                    risk_distance = sl_price - entry_price

                    equity = self.equity
                    risk_amount = equity * self.risk_per_trade
                    position_size = risk_amount / risk_distance
                    position_size = max(0.001, min(100.0, position_size))

                    if (
                        position_size > 0
                        and not np.isnan(sl_price)
                        and not np.isnan(tp_price)
                        and tp_price < entry_price < sl_price
                    ):
                        self.sell(
                            size=position_size,
                            limit=entry_price,
                            sl=sl_price,
                            tp=tp_price,
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
