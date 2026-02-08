# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v28.py
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
    adx_threshold = 25  # 🌙 Moon Dev: Increased ADX threshold from 20 to 25 to include slightly trending markets with reversion potential, boosting trade frequency and exposure to more opportunities for higher cumulative returns
    risk_per_trade = 0.04  # 🌙 Moon Dev: Raised risk per trade from 3% to 4% to compound gains faster towards 50% target, while ATR sizing ensures drawdowns remain controlled in volatile crypto
    atr_multiplier_sl = 2
    atr_multiplier_tp = 10  # 🌙 Moon Dev: Extended TP multiplier from 8 to 10 ATR for a stronger 5:1 RR, capturing larger mean reversion swings to amplify profits on high-quality setups
    trailing_atr_mult = 1.5  # 🌙 Moon Dev: New trailing stop parameter at 1.5 ATR to lock in gains dynamically, allowing winners to run further while protecting against reversals

    def init(self):
        # RSI(8) - shortened from 10 to 8 for ultra-responsive overextension detection, enabling earlier entries in fast-moving crypto for better timing and return potential
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=8)
        self.rsi_sma = self.I(
            talib.SMA, self.rsi, timeperiod=8
        )  # 🌙 Moon Dev: Matched SMA to RSI period for sharper crossover signals, improving precision in reversion trades

        # Stochastic %K(8,3,3) - further shortened fastk from 10 to 8 for accelerated momentum detection, balancing speed with noise reduction for more frequent valid signals
        self.stoch_k, _ = self.I(
            talib.STOCH,
            self.data.High,
            self.data.Low,
            self.data.Close,
            fastk_period=8,
            slowk_period=3,
            slowd_period=3,
        )
        self.stoch_sma = self.I(
            talib.SMA, self.stoch_k, timeperiod=8
        )  # 🌙 Moon Dev: Adjusted SMA to 8 periods matching Stoch for synchronized divergence, enhancing entry quality and win rate

        # ATR(14) for dynamic stops - kept standard for robust volatility adaptation
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)

        # ADX(14) for trend filter - standard period for reliable ranging detection
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14)

        # Volume SMA(8) - shortened from 10 to 8 to sync with faster indicators, providing quicker volume surge confirmation for higher conviction entries
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=8)

        print(
            "🌙 Moon Dev: Indicators initialized with aggressive tuning (RSI/Stoch/Vol to 8 periods) for rapid signals, combined with trailing stops to maximize returns in dynamic markets ✨"
        )

    def next(self):
        # 🌙 Moon Dev: Implemented dynamic trailing stops for longs/shorts to trail SL behind price by trailing_atr_mult * ATR once profitable, letting winners extend towards higher TP while securing gains; widened manual exit thresholds to 80/20 to reduce premature closes
        if self.position.is_long:
            # Update trailing stop for long: if current price > entry + 2*ATR (initial buffer), trail SL to max(current SL, close - trailing_atr_mult*ATR)
            if self.position.pl > 0:  # Only trail if in profit
                current_atr = self.atr[-1]
                trail_sl = self.data.Close[-1] - (self.trailing_atr_mult * current_atr)
                self.position.sl = max(self.position.sl, trail_sl) if self.position.sl else trail_sl

            # Long exit on extreme overbought reversion: RSI >80 crossing down OR Stoch <20 crossing up, holding longer for bigger moves
            if (self.rsi[-1] > 80 and self.rsi[-1] < self.rsi_sma[-1]) or (
                self.stoch_k[-1] < 20 and self.stoch_k[-1] > self.stoch_sma[-1]
            ):
                self.position.close()
                print(f"🌙 Moon Dev: Long Exit on Extreme Reversion Signal at {self.data.Close[-1]:.2f} 🚀")
            return

        if self.position.is_short:
            # Update trailing stop for short: if current price < entry - 2*ATR, trail SL to min(current SL, close + trailing_atr_mult*ATR)
            if self.position.pl > 0:  # Only trail if in profit
                current_atr = self.atr[-1]
                trail_sl = self.data.Close[-1] + (self.trailing_atr_mult * current_atr)
                self.position.sl = min(self.position.sl, trail_sl) if self.position.sl else trail_sl

            # Short exit on extreme oversold reversion: RSI <20 crossing up OR Stoch >80 crossing down
            if (self.rsi[-1] < 20 and self.rsi[-1] > self.rsi_sma[-1]) or (
                self.stoch_k[-1] > 80 and self.stoch_k[-1] < self.stoch_sma[-1]
            ):
                self.position.close()
                print(f"🌙 Moon Dev: Short Exit on Extreme Reversion Signal at {self.data.Close[-1]:.2f} 🚀")
            return

        # 🌙 Moon Dev: Deepened entry thresholds to 20/80 from 30/70 for ultra-extreme oversold/overbought conditions, ensuring only high-probability reversions; further loosened volume to 1.1x for increased trade volume without diluting quality, driving towards 50% target
        # Entry conditions only if no position and sufficient history
        if (not self.position) and (len(self.rsi) > 20) and (self.adx[-1] < self.adx_threshold):
            # Relaxed volume filter to 1.1x average for more inclusive momentum confirmation, allowing additional quality trades
            vol_confirm = self.data.Volume[-1] > 1.1 * self.vol_sma[-1]

            # Long entry: RSI extremely oversold (<20 and below SMA), Stoch turning up (> SMA) - deeper threshold for superior win rate and larger reversions
            if (
                vol_confirm
                and (self.rsi[-1] < self.rsi_sma[-1])
                and (self.rsi[-1] < 20)
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
                    0.001, min(25.0, position_size)
                )  # 🌙 Moon Dev: Expanded max size from 20.0 to 25.0 to leverage stronger setups more aggressively, scaling returns with controlled risk

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

            # Short entry: RSI extremely overbought (>80 and above SMA), Stoch turning down (< SMA)
            if (
                vol_confirm
                and (self.rsi[-1] > self.rsi_sma[-1])
                and (self.rsi[-1] > 80)
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
                    0.001, min(25.0, position_size)
                )  # 🌙 Moon Dev: Symmetric max size increase to 25.0 for shorts, enabling larger reversion profits

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
