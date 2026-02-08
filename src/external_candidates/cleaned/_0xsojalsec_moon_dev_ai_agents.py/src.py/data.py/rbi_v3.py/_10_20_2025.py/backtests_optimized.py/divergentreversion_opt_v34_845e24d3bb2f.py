# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v34.py
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
    adx_threshold = 28  # 🌙 Moon Dev: Adjusted ADX threshold from 25 to 28 to capture slightly more ranging market opportunities, increasing trade frequency realistically without entering strong trends, aiding higher compounded returns towards 50% target
    risk_per_trade = 0.06  # 🌙 Moon Dev: Increased risk per trade from 5% to 6% for accelerated compounding while keeping drawdowns manageable, combined with improved sizing for balanced risk to achieve target return
    atr_multiplier_sl = 2
    atr_multiplier_tp = 11  # 🌙 Moon Dev: Fine-tuned TP multiplier from 10 to 11 ATR for a ~5.5:1 risk-reward ratio, allowing deeper mean reversion captures to boost average profitability per trade without over-optimization

    def init(self):
        # RSI(14) - standard 14 period for reduced noise in crypto volatility, enhancing signal reliability
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.rsi_sma = self.I(
            talib.SMA, self.rsi, timeperiod=14
        )  # 🌙 Moon Dev: Consistent SMA period matching RSI for precise crossover detection with minimal whipsaws

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
        )  # 🌙 Moon Dev: Aligned SMA to Stoch period for better divergence synchronization

        # ATR(14) for dynamic stops - standard for volatility adaptation
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)

        # ADX(14) for trend filter - standard period
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14)

        # Volume SMA(20) - stable baseline for confirmation
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)

        # EMA(50) for counter-trend filter - 🌙 Moon Dev: Added 50-period EMA to confirm mean reversion setups against the intermediate trend, improving entry quality by focusing on pullbacks for higher win rate and returns
        self.ema50 = self.I(talib.EMA, self.data.Close, timeperiod=50)

        print(
            "🌙 Moon Dev: Added EMA50 counter-trend filter and fine-tuned parameters for enhanced signal quality and frequency, driving realistic path to 50% target return ✨"
        )

    def next(self):
        # 🌙 Moon Dev: Retained no manual early exits to maximize reversion moves, now enhanced with dynamic trailing for profit protection to improve overall expectancy and reduce risk of giving back gains
        # Trailing stop logic added for longs/shorts to lock in profits after 2x ATR gain, moving SL to breakeven + 0.5 ATR for better risk-adjusted returns

        if self.position:
            atr_val = self.atr[-1]
            if self.position.is_long:
                profit = self.data.Close[-1] - self.position.entry_price
                if profit > 2 * atr_val:
                    new_sl = max(self.position.sl, self.position.entry_price + 0.5 * atr_val)
                    self.position.sl = new_sl
            elif self.position.is_short:
                profit = self.position.entry_price - self.data.Close[-1]
                if profit > 2 * atr_val:
                    new_sl = min(self.position.sl, self.position.entry_price - 0.5 * atr_val)
                    self.position.sl = new_sl

        # Entry conditions only if no position and sufficient history
        if (
            (not self.position) and (len(self.rsi) > 70) and (self.adx[-1] < self.adx_threshold)
        ):  # 🌙 Moon Dev: Extended history check to 70 bars for even more stable indicators, ensuring reliable signals from backtest start while filtering noise
            # Adjusted volume filter to >0.95x average for slightly more inclusive confirmation, boosting trade opportunities realistically
            vol_confirm = self.data.Volume[-1] > 0.95 * self.vol_sma[-1]

            # Long entry: Loosened RSI to <38 (from 35) and Stoch <52 (from 50) for higher frequency of quality oversold reversion setups, plus EMA counter-trend filter
            if (
                vol_confirm
                and (self.rsi[-1] < self.rsi_sma[-1])
                and (self.rsi[-1] < 38)
                and (self.stoch_k[-1] > self.stoch_sma[-1])
                and (self.stoch_k[-1] < 52)
                and (self.data.Close[-1] < self.ema50[-1])
            ):
                entry_price = self.data.Close[-1]
                atr_val = self.atr[-1]
                sl_price = entry_price - (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price + (self.atr_multiplier_tp * atr_val)
                risk_distance = entry_price - sl_price

                equity = self._broker.getcash()  # 🌙 Moon Dev: Use broker cash for accurate available equity in sizing
                risk_amount = equity * self.risk_per_trade
                position_size = risk_amount / risk_distance
                # 🌙 Moon Dev: Added realistic cash-based cap to prevent overexposure beyond available equity (spot trading assumption), improving risk management; removed arbitrary max 50 for dynamic scaling as equity grows
                max_affordable = (equity * 0.95) / entry_price
                position_size = max(0.001, min(position_size, max_affordable))

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

            # Short entry: Symmetric adjustments - RSI >62 (from 65), Stoch >48 (from 50), with EMA counter-trend filter for balanced overbought reversion
            if (
                vol_confirm
                and (self.rsi[-1] > self.rsi_sma[-1])
                and (self.rsi[-1] > 62)
                and (self.stoch_k[-1] < self.stoch_sma[-1])
                and (self.stoch_k[-1] > 48)
                and (self.data.Close[-1] > self.ema50[-1])
            ):
                entry_price = self.data.Close[-1]
                atr_val = self.atr[-1]
                sl_price = entry_price + (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price - (self.atr_multiplier_tp * atr_val)
                risk_distance = sl_price - entry_price

                equity = self._broker.getcash()  # 🌙 Moon Dev: Consistent cash usage for short sizing accuracy
                risk_amount = equity * self.risk_per_trade
                position_size = risk_amount / risk_distance
                max_affordable = (equity * 0.95) / entry_price
                position_size = max(0.001, min(position_size, max_affordable))

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
