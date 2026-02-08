# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v23.py
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
    adx_threshold = 20  # 🌙 Moon Dev: Further loosened ADX threshold to 20 from 25 to capture more ranging market opportunities, increasing trade frequency for higher potential returns while still filtering strong trends
    risk_per_trade = 0.03  # 🌙 Moon Dev: Increased risk per trade from 2% to 3% to accelerate equity growth towards target, balanced with ATR-based sizing to control drawdowns
    atr_multiplier_sl = 2
    atr_multiplier_tp = 8  # 🌙 Moon Dev: Boosted TP multiplier from 7 to 8 ATR for enhanced 4:1 RR, allowing deeper reversion captures to significantly improve profitability on winning trades

    def init(self):
        # RSI(10) - shortened further from 14 to 10 for even faster response to overextensions, improving entry timing in volatile crypto markets
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=10)
        self.rsi_sma = self.I(
            talib.SMA, self.rsi, timeperiod=10
        )  # 🌙 Moon Dev: Kept SMA matched to RSI period for precise crossover detection

        # Stochastic %K(10,3,3) - shortened fastk from 14 to 10 for quicker momentum shifts while keeping slow periods standard to reduce noise
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
        )  # 🌙 Moon Dev: Shortened SMA from 10 to match Stoch fastk for faster divergence signals, enhancing sensitivity without excessive false positives

        # ATR(14) for dynamic stops - unchanged for reliable volatility measurement
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)

        # ADX(14) for trend filter - unchanged period for consistency
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14)

        # Volume SMA(10) - shortened from 14 to 10 to align with faster indicators, providing more timely volume confirmation
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=10)

        print(
            "🌙 Moon Dev: Indicators initialized with further tuned periods (RSI/Stoch/Vol to 10) for quicker signals and enhanced volume filter to boost trade quality and frequency ✨"
        )

    def next(self):
        # 🌙 Moon Dev: Tightened exit thresholds to 70/30 extremes from 65/35 to hold positions longer through minor pullbacks, letting winners run towards higher TP for better returns
        if self.position.is_long:
            # Long exit only on very strong overbought reversion: RSI deeply overbought crossing down OR Stoch deeply oversold crossing up
            if (self.rsi[-1] > 70 and self.rsi[-1] < self.rsi_sma[-1]) or (
                self.stoch_k[-1] < 30 and self.stoch_k[-1] > self.stoch_sma[-1]
            ):
                self.position.close()
                print(f"🌙 Moon Dev: Long Exit on Strong Reversion Signal at {self.data.Close[-1]:.2f} 🚀")
            return

        if self.position.is_short:
            # Short exit only on very strong oversold reversion: RSI deeply oversold crossing up OR Stoch deeply overbought crossing down
            if (self.rsi[-1] < 30 and self.rsi[-1] > self.rsi_sma[-1]) or (
                self.stoch_k[-1] > 70 and self.stoch_k[-1] < self.stoch_sma[-1]
            ):
                self.position.close()
                print(f"🌙 Moon Dev: Short Exit on Strong Reversion Signal at {self.data.Close[-1]:.2f} 🚀")
            return

        # 🌙 Moon Dev: Tightened RSI thresholds to 30/70 from 35/65 for stronger mean reversion setups, reducing false entries; loosened volume to 1.2x for more opportunities without sacrificing quality
        # Entry conditions only if no position and sufficient history
        if (not self.position) and (len(self.rsi) > 20) and (self.adx[-1] < self.adx_threshold):
            # Enhanced volume filter: lowered to 1.2x average volume for broader confirmation while maintaining momentum filter
            vol_confirm = self.data.Volume[-1] > 1.2 * self.vol_sma[-1]

            # Long entry: RSI deeply oversold (below SMA and <30), Stoch turning up (above SMA) - stronger divergence with tightened threshold for higher win rate
            if (
                vol_confirm
                and (self.rsi[-1] < self.rsi_sma[-1])
                and (self.rsi[-1] < 30)
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
                    0.001, min(20.0, position_size)
                )  # 🌙 Moon Dev: Increased max size from 10.0 to 20.0 to support larger positions on high-conviction setups, amplifying returns with 1M cash base

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

            # Short entry: RSI deeply overbought (above SMA and >70), Stoch turning down (below SMA) - stronger divergence with tightened threshold for higher win rate
            if (
                vol_confirm
                and (self.rsi[-1] > self.rsi_sma[-1])
                and (self.rsi[-1] > 70)
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
                    0.001, min(20.0, position_size)
                )  # 🌙 Moon Dev: Increased max size from 10.0 to 20.0 for symmetric larger short positions to maximize reversion gains

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
