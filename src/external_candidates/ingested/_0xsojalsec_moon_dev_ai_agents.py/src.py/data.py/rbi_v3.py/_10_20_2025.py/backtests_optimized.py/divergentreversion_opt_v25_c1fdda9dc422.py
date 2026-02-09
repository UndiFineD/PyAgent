# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v25.py
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
    adx_threshold = 25  # 🌙 Moon Dev: Increased ADX threshold from 20 to 25 to include mildly trending markets as ranging opportunities, boosting trade frequency and cumulative returns towards 50% target while maintaining trend avoidance
    risk_per_trade = 0.04  # 🌙 Moon Dev: Raised risk per trade from 3% to 4% for accelerated equity growth and compounding, paired with robust ATR sizing to keep drawdowns manageable under 20%
    atr_multiplier_sl = 2
    atr_multiplier_tp = 10  # 🌙 Moon Dev: Elevated TP multiplier from 8 to 10 ATR for a stronger ~5:1 risk-reward ratio, enabling capture of extended mean reversions in crypto volatility to amplify winning trade profits significantly

    def init(self):
        # RSI(10) - kept at 10 for fast response to overextensions, balancing sensitivity and noise in 15m BTC data
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=10)
        self.rsi_sma = self.I(
            talib.SMA, self.rsi, timeperiod=10
        )  # 🌙 Moon Dev: Matched SMA to RSI period for accurate crossover signals in reversion setups

        # Stochastic %K(5,3,3) - shortened fastk from 10 to 5 for ultra-quick momentum detection, increasing signal frequency while slow periods filter noise
        self.stoch_k, _ = self.I(
            talib.STOCH,
            self.data.High,
            self.data.Low,
            self.data.Close,
            fastk_period=5,
            slowk_period=3,
            slowd_period=3,
        )
        self.stoch_sma = self.I(
            talib.SMA, self.stoch_k, timeperiod=5
        )  # 🌙 Moon Dev: Shortened SMA to 5 matching fastk for rapid divergence capture, enhancing entry timing without over-trading

        # ATR(14) for dynamic stops - standard period for consistent volatility adaptation
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # ADX(14) for trend filter - standard for reliable ranging detection
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # Volume SMA(5) - shortened from 10 to 5 for quicker volume spike confirmation, aligning with faster oscillators to increase trade opportunities
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=5)

        print(
            "🌙 Moon Dev: Indicators optimized with shorter Stoch/Vol periods (5) for faster signals, maintained RSI at 10, and ADX at 25 threshold to elevate trade frequency and quality for 50% return goal ✨"
        )

    def next(self):
        # 🌙 Moon Dev: Further tightened exit thresholds to 75/25 extremes from 70/30 to allow positions to run longer through noise, maximizing profits on strong reversions before counter-signals trigger
        if self.position.is_long:
            # Long exit on extreme overbought reversion: RSI deeply overbought crossing down OR Stoch deeply oversold crossing up
            if (self.rsi[-1] > 75 and self.rsi[-1] < self.rsi_sma[-1]) or (
                self.stoch_k[-1] < 25 and self.stoch_k[-1] > self.stoch_sma[-1]
            ):
                self.position.close()
                print(
                    f"🌙 Moon Dev: Long Exit on Extreme Reversion Signal at {self.data.Close[-1]:.2f} 🚀"
                )
            return

        if self.position.is_short:
            # Short exit on extreme oversold reversion: RSI deeply oversold crossing up OR Stoch deeply overbought crossing down
            if (self.rsi[-1] < 25 and self.rsi[-1] > self.rsi_sma[-1]) or (
                self.stoch_k[-1] > 75 and self.stoch_k[-1] < self.stoch_sma[-1]
            ):
                self.position.close()
                print(
                    f"🌙 Moon Dev: Short Exit on Extreme Reversion Signal at {self.data.Close[-1]:.2f} 🚀"
                )
            return

        # 🌙 Moon Dev: Loosened RSI thresholds to 35/65 from 30/70 for more frequent yet still quality mean reversion entries; volume filter to 1.0x SMA for broader opportunity capture without diluting momentum; increased history check to 50 bars for robust signal confirmation
        # Entry conditions only if no position and sufficient history
        if (
            (not self.position)
            and (len(self.rsi) > 50)
            and (self.adx[-1] < self.adx_threshold)
        ):

            # Loosened volume filter to 1.0x average for increased trade frequency while ensuring baseline activity
            vol_confirm = self.data.Volume[-1] > 1.0 * self.vol_sma[-1]

            # Long entry: RSI oversold (below SMA and <35), Stoch turning up (above SMA) - balanced divergence for higher frequency with solid win potential
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
                    0.001, min(50.0, position_size)
                )  # 🌙 Moon Dev: Expanded max size from 20.0 to 50.0 to leverage high-conviction signals more aggressively with 1M cash, scaling returns in favorable setups

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

            # Short entry: RSI overbought (above SMA and >65), Stoch turning down (below SMA) - balanced divergence for higher frequency with solid win potential
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
                    0.001, min(50.0, position_size)
                )  # 🌙 Moon Dev: Expanded max size to 50.0 for symmetric aggressive short scaling, maximizing downside reversion profits

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
