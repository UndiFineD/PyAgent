# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v26.py
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
    adx_threshold = 25  # 🌙 Moon Dev: Loosened ADX threshold back to 25 from 20 to include slightly stronger trends where mean reversion can still occur, increasing trade opportunities and overall return potential without excessive trend-following risk
    risk_per_trade = 0.04  # 🌙 Moon Dev: Increased risk per trade from 3% to 4% to accelerate compounding towards 50% target, paired with tighter stops to maintain drawdown control under 20%
    atr_multiplier_sl = 1.5  # 🌙 Moon Dev: Tightened SL multiplier from 2 to 1.5 ATR for reduced risk distance, improving effective RR to ~1:6.67 and allowing larger position sizes per risk unit for higher returns
    atr_multiplier_tp = 10  # 🌙 Moon Dev: Extended TP multiplier from 8 to 10 ATR to capture deeper mean reversion moves in volatile BTC, targeting larger winners to push total return past 50% while relying on filters for quality setups

    def init(self):
        # RSI(14) - reverted to standard 14 period from 10 for more reliable overextension signals, reducing whipsaws in choppy 15m crypto data while maintaining responsiveness
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.rsi_sma = self.I(
            talib.SMA, self.rsi, timeperiod=14
        )  # 🌙 Moon Dev: Matched SMA to RSI period for accurate crossover timing, enhancing signal reliability

        # Stochastic %K(14,3,3) - reverted to standard fastk=14 from 10 for smoother momentum detection, minimizing false signals in ranging markets
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
        )  # 🌙 Moon Dev: Matched SMA to Stoch fastk period for consistent divergence capture, improving entry precision

        # ATR(10) - shortened from 14 to 10 for faster adaptation to short-term volatility spikes in 15m BTC, enabling tighter dynamic stops/TP for better risk-adjusted returns
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=10)

        # ADX(14) for trend filter - kept standard period for robust trend strength measurement
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14)

        # Volume SMA(14) - extended to 14 from 10 to align with standard indicators, providing stable volume baseline for confirmation
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=14)

        # Bollinger Bands (20,2) - added as complementary mean reversion filter to confirm price extremes, tightening entries to high-probability bounces for higher win rate and returns
        self.bb_upper, self.bb_middle, self.bb_lower = self.I(
            talib.BBANDS, self.data.Close, timeperiod=20, nbdevup=2, nbdevdn=2
        )

        print(
            "🌙 Moon Dev: Indicators initialized with optimized periods (RSI/Stoch/Vol/ATR to 14/10) and added BB(20,2) for enhanced reversion confirmation, boosting signal quality and trade frequency towards 50% target ✨"
        )

    def next(self):
        # 🌙 Moon Dev: Further loosened exit thresholds to 75/25 extremes from 70/30 to allow positions to run longer towards ambitious TP levels, maximizing profit capture on strong reversion trades
        if self.position.is_long:
            # Long exit on extreme overbought reversion: RSI deeply overbought crossing down OR Stoch deeply oversold crossing up, but only at looser levels to let winners breathe
            if (self.rsi[-1] > 75 and self.rsi[-1] < self.rsi_sma[-1]) or (
                self.stoch_k[-1] < 25 and self.stoch_k[-1] > self.stoch_sma[-1]
            ):
                self.position.close()
                print(f"🌙 Moon Dev: Long Exit on Strong Reversion Signal at {self.data.Close[-1]:.2f} 🚀")
            return

        if self.position.is_short:
            # Short exit on extreme oversold reversion: RSI deeply oversold crossing up OR Stoch deeply overbought crossing down, loosened for extended holds
            if (self.rsi[-1] < 25 and self.rsi[-1] > self.rsi_sma[-1]) or (
                self.stoch_k[-1] > 75 and self.stoch_k[-1] < self.stoch_sma[-1]
            ):
                self.position.close()
                print(f"🌙 Moon Dev: Short Exit on Strong Reversion Signal at {self.data.Close[-1]:.2f} 🚀")
            return

        # 🌙 Moon Dev: Loosened RSI thresholds to 25/75 from 30/70 for more frequent high-quality entries in volatile conditions; further lowered volume filter to 1.0x for increased opportunities; added BB touch confirmation to avoid low-conviction setups, balancing frequency and win rate for 50% return push
        # Entry conditions only if no position and sufficient history
        if (not self.position) and (len(self.rsi) > 20) and (self.adx[-1] < self.adx_threshold):
            # Loosened volume filter to exactly average volume for broader participation while still ensuring activity
            vol_confirm = self.data.Volume[-1] > 1.0 * self.vol_sma[-1]

            # Long entry: RSI oversold (below SMA and <25), Stoch turning up (above SMA), and price at lower BB for strong reversion setup
            if (
                vol_confirm
                and (self.rsi[-1] < self.rsi_sma[-1])
                and (self.rsi[-1] < 25)
                and (self.stoch_k[-1] > self.stoch_sma[-1])
                and (self.data.Close[-1] < self.bb_lower[-1])
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
                )  # 🌙 Moon Dev: Raised max size from 20.0 to 25.0 to leverage high-conviction BB-confirmed setups, amplifying returns with controlled risk

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

            # Short entry: RSI overbought (above SMA and >75), Stoch turning down (below SMA), and price at upper BB for strong reversion setup
            if (
                vol_confirm
                and (self.rsi[-1] > self.rsi_sma[-1])
                and (self.rsi[-1] > 75)
                and (self.stoch_k[-1] < self.stoch_sma[-1])
                and (self.data.Close[-1] > self.bb_upper[-1])
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
                )  # 🌙 Moon Dev: Raised max size to 25.0 for symmetric BB-enhanced short positions, driving higher reversion profits

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
