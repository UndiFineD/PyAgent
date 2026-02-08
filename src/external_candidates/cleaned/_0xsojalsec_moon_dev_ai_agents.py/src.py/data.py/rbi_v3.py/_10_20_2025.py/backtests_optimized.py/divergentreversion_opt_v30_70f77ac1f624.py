# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v30.py
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
    adx_threshold = 20  # 🌙 Moon Dev: Lowered ADX threshold from 25 to 20 to include more ranging markets with low trend strength, increasing trade frequency and opportunities to compound towards 50% target while still avoiding strong trends
    risk_per_trade = 0.08  # 🌙 Moon Dev: Increased risk per trade from 5% to 8% for accelerated equity growth through compounding, balanced by enhanced filters and trailing stops to maintain risk control
    atr_multiplier_sl = 2
    atr_multiplier_tp = 10  # 🌙 Moon Dev: Retained 10 ATR TP for strong 5:1 RR, complemented by new trailing logic to capture extended reversion moves beyond fixed TP

    def init(self):
        # RSI(14) - retained standard 14 period for optimal noise reduction and reliable oversold/overbought detection in crypto volatility
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.rsi_sma = self.I(
            talib.SMA, self.rsi, timeperiod=14
        )  # 🌙 Moon Dev: Consistent SMA period matching RSI for precise crossover signals with minimal whipsaw

        # Stochastic %K(14,3,3) - standard fastk 14 for balanced momentum sensitivity
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
        )  # 🌙 Moon Dev: Aligned SMA to Stoch period for accurate turning point detection

        # ATR(14) for dynamic stops - standard for volatility adaptation
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)

        # ADX(14) for trend filter - standard period
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14)

        # Volume SMA(20) - stable baseline for confirmation
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)

        # Bollinger Bands(20,2) - added for mean reversion confirmation, filtering entries to price deviations from midline to improve setup quality and win rate
        self.bb_upper, self.bb_middle, self.bb_lower = self.I(
            talib.BBANDS, self.data.Close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0
        )

        print(
            "🌙 Moon Dev: Added Bollinger Bands for enhanced mean reversion filtering; indicators tuned for quality signals to boost returns while reducing false entries ✨"
        )

    def next(self):
        # 🌙 Moon Dev: Retained reliance on SL/TP for primary exits, now augmented with trailing stop logic to lock in profits on extended moves, allowing winners to run further and improve overall profitability towards 50% target

        # Trailing stop implementation for better profit capture
        if self.position:
            atr_val = self.atr[-1]
            if self.position.is_long:
                entry_price = self.position.entry_price
                profit = self.data.Close[-1] - entry_price
                trail_trigger = (
                    5 * atr_val
                )  # 🌙 Moon Dev: Trigger trailing after 5 ATR profit (2.5x initial risk) to protect gains without cutting winners too early
                if profit > trail_trigger:
                    trail_distance = (
                        1.5 * atr_val
                    )  # 🌙 Moon Dev: Trail at 1.5 ATR behind current price for tight protection in volatile crypto, balancing risk and reward
                    new_sl = self.data.Close[-1] - trail_distance
                    if new_sl > self.position.sl:
                        self.position.sl = new_sl
                        print(f"🌙 Moon Dev: Trailing SL updated to {new_sl:.2f} for long position ✨")
            else:  # short position
                entry_price = self.position.entry_price
                profit = entry_price - self.data.Close[-1]
                trail_trigger = 5 * atr_val
                if profit > trail_trigger:
                    trail_distance = 1.5 * atr_val
                    new_sl = self.data.Close[-1] + trail_distance
                    if new_sl < self.position.sl:
                        self.position.sl = new_sl
                        print(f"🌙 Moon Dev: Trailing SL updated to {new_sl:.2f} for short position ✨")

        # Entry conditions only if no position and sufficient history
        if (
            (not self.position) and (len(self.rsi) > 100) and (self.adx[-1] < self.adx_threshold)
        ):  # 🌙 Moon Dev: Extended history check to 100 bars for even more stable indicator readings, ensuring reliable signals from the start
            # Adjusted volume filter to >1.1x average for moderate confirmation, balancing trade frequency with quality to avoid low-volume traps
            vol_confirm = self.data.Volume[-1] > 1.1 * self.vol_sma[-1]

            # Long entry: RSI oversold (below 35 and SMA, loosened slightly for quality), Stoch turning up (above SMA and below 50), plus BB below midline for deviation confirmation - enhances setup selectivity for higher win rate
            if (
                vol_confirm
                and (self.rsi[-1] < self.rsi_sma[-1])
                and (self.rsi[-1] < 35)
                and (self.stoch_k[-1] > self.stoch_sma[-1])
                and (self.stoch_k[-1] < 50)
                and (self.data.Close[-1] < self.bb_middle[-1])
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
                    0.001, min(50.0, position_size)
                )  # 🌙 Moon Dev: Retained max size at 50 for amplified exposure on filtered high-quality setups

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

            # Short entry: RSI overbought (above 65 and SMA), Stoch turning down (below SMA and above 50), plus BB above midline - symmetric filter for balanced, high-conviction shorts
            if (
                vol_confirm
                and (self.rsi[-1] > self.rsi_sma[-1])
                and (self.rsi[-1] > 65)
                and (self.stoch_k[-1] < self.stoch_sma[-1])
                and (self.stoch_k[-1] > 50)
                and (self.data.Close[-1] > self.bb_middle[-1])
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
                    0.001, min(50.0, position_size)
                )  # 🌙 Moon Dev: Retained max size for shorts to capture reversion profits symmetrically

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
