# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v29.py
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
    adx_threshold = 25  # 🌙 Moon Dev: Loosened ADX threshold from 20 to 25 to include mildly trending markets with reversion potential, increasing trade frequency to boost overall returns while avoiding strong trends
    risk_per_trade = 0.05  # 🌙 Moon Dev: Increased risk per trade from 3% to 5% to accelerate equity compounding towards 50% target, with ATR sizing ensuring controlled exposure per trade
    atr_multiplier_sl = 2
    atr_multiplier_tp = 10  # 🌙 Moon Dev: Increased TP multiplier from 8 to 10 ATR for a 5:1 risk-reward ratio, allowing captures of larger mean reversion moves to significantly enhance profitability

    def init(self):
        # RSI(14) - reverted to standard 14 period from 10 to reduce noise and false signals in volatile crypto, improving signal quality for higher win rate
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.rsi_sma = self.I(
            talib.SMA, self.rsi, timeperiod=14
        )  # 🌙 Moon Dev: Matched SMA to RSI period for accurate crossover signals with less whipsaw

        # Stochastic %K(14,3,3) - reverted to standard fastk 14 from 10 for smoother momentum detection, balancing speed and reliability
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
        )  # 🌙 Moon Dev: Matched SMA to Stoch fastk period for consistent divergence timing

        # ATR(14) for dynamic stops - unchanged for reliable volatility measurement
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # ADX(14) for trend filter - unchanged period for consistency
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # Volume SMA(20) - extended to 20 from 10 for more stable volume baseline, reducing false confirmations in choppy periods
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)

        print(
            "🌙 Moon Dev: Indicators re-tuned to standard periods (RSI/Stoch to 14, Vol to 20) for better signal quality, reducing noise while maintaining responsiveness to drive higher returns ✨"
        )

    def next(self):
        # 🌙 Moon Dev: Removed manual early exit conditions to let winners run fully to TP levels, preventing premature closures on minor pullbacks and improving average trade profitability for target return achievement
        # Now relying solely on SL/TP for exits to maximize reversion capture

        # Entry conditions only if no position and sufficient history
        if (
            (not self.position)
            and (len(self.rsi) > 50)
            and (self.adx[-1] < self.adx_threshold)
        ):  # 🌙 Moon Dev: Increased history check to 50 bars for more stable indicator values, filtering out early unreliable signals

            # Loosened volume filter to >1.0x average for more inclusive confirmation, increasing trade opportunities without diluting quality
            vol_confirm = self.data.Volume[-1] > 1.0 * self.vol_sma[-1]

            # Long entry: RSI oversold (below 35 and SMA), Stoch turning up (above SMA and below 50 for mild oversold) - loosened thresholds for higher frequency while preserving mean reversion bias
            if (
                vol_confirm
                and (self.rsi[-1] < self.rsi_sma[-1])
                and (self.rsi[-1] < 35)
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
                    0.001, min(50.0, position_size)
                )  # 🌙 Moon Dev: Increased max position size from 20 to 50 to amplify returns on high-conviction setups with 1M cash, balanced by risk limits

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

            # Short entry: RSI overbought (above 65 and SMA), Stoch turning down (below SMA and above 50 for mild overbought) - symmetric loosening for balanced trade frequency
            if (
                vol_confirm
                and (self.rsi[-1] > self.rsi_sma[-1])
                and (self.rsi[-1] > 65)
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
                    0.001, min(50.0, position_size)
                )  # 🌙 Moon Dev: Increased max size to 50 for larger short positions, enhancing reversion profit potential

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
