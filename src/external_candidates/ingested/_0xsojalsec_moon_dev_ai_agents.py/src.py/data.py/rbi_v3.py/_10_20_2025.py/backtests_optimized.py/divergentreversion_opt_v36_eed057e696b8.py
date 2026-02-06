# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v36.py
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
    adx_threshold = 28  # 🌙 Moon Dev: Further loosened ADX threshold to 28 from 25 to capture more ranging market opportunities, increasing trade frequency and exposure to reversion setups for accelerated return growth towards 50% target
    risk_per_trade = 0.08  # 🌙 Moon Dev: Increased risk per trade to 8% from 5% to enhance compounding velocity, balanced by improved entry filters and trailing stops to maintain risk control while pushing for higher overall returns
    atr_multiplier_sl = 1.8  # 🌙 Moon Dev: Slightly tightened SL multiplier to 1.8 ATR from 2 to reduce risk distance, allowing larger position sizes for the same risk % and improving capital efficiency
    atr_multiplier_tp = 12  # 🌙 Moon Dev: Extended TP multiplier to 12 ATR from 10 for a ~6.7:1 risk-reward ratio, enabling capture of deeper mean reversion swings to boost average profit per trade significantly

    def init(self):
        # RSI(14) - standard period maintained for reliable overbought/oversold detection
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.rsi_sma = self.I(talib.SMA, self.rsi, timeperiod=14)

        # Stochastic %K(14,3,3) - standard parameters for balanced momentum signals
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

        # ATR(14) for dynamic stops and sizing
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # ADX(14) for trend filter to avoid strong trends
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # Volume SMA(20) for confirmation
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)

        # Bollinger Bands (20,2) for additional reversion filter - 🌙 Moon Dev: Added BB to confirm extreme deviations, tightening entries to high-quality mean reversion setups at band touches, improving win rate and signal selectivity without reducing frequency too much
        self.bb_upper, self.bb_middle, self.bb_lower = self.I(
            talib.BBANDS, self.data.Close, timeperiod=20, nbdevup=2, nbdevdn=2
        )

        # 50-period EMA for mild trend bias filter - 🌙 Moon Dev: Added EMA filter to favor longs above EMA and shorts below in ranging markets, adding a subtle directional bias to enhance profitability in mildly trending ranges while preserving reversion core
        self.ema_50 = self.I(talib.EMA, self.data.Close, timeperiod=50)

        print(
            "🌙 Moon Dev: Enhanced indicators with BB for reversion confirmation and 50 EMA for trend bias, refining entry quality to drive higher win rates and returns ✨"
        )

    def next(self):
        # Trailing stop logic for longs - 🌙 Moon Dev: Implemented trailing stop after 3% profit: trail SL to current close - 2 ATR, allowing winners to run further beyond fixed TP in strong reversions, potentially increasing average returns while protecting gains
        if self.position and self.position.is_long:
            entry_price = self.position.entry_price
            current_price = self.data.Close[-1]
            profit_pct = (current_price - entry_price) / entry_price
            if profit_pct > 0.03:  # Trail after 3% profit
                trail_sl = current_price - (2 * self.atr[-1])
                if trail_sl > self.position.sl:
                    self.position.sl = trail_sl
                    print(
                        f"🌙 Moon Dev: Trailing SL updated for long to {trail_sl:.2f} at profit {profit_pct*100:.2f}% 🚀"
                    )

        # Trailing stop logic for shorts - symmetric implementation
        if self.position and self.position.is_short:
            entry_price = self.position.entry_price
            current_price = self.data.Close[-1]
            profit_pct = (entry_price - current_price) / entry_price
            if profit_pct > 0.03:  # Trail after 3% profit
                trail_sl = current_price + (2 * self.atr[-1])
                if trail_sl < self.position.sl:
                    self.position.sl = trail_sl
                    print(
                        f"🌙 Moon Dev: Trailing SL updated for short to {trail_sl:.2f} at profit {profit_pct*100:.2f}% 🚀"
                    )

        # Entry conditions only if no position and sufficient history
        if (
            (not self.position)
            and (len(self.rsi) > 100)
            and (self.adx[-1] < self.adx_threshold)
        ):  # 🌙 Moon Dev: Extended history check to 100 bars for even more stable signals, ensuring robust indicator calculations in early data

            # Adjusted volume filter to >0.9x average for slightly more inclusive confirmation, balancing quality and opportunity to increase trade count
            vol_confirm = self.data.Volume[-1] > 0.9 * self.vol_sma[-1]

            # Trend bias filter using EMA
            ema_bias_long = self.data.Close[-1] > self.ema_50[-1]
            ema_bias_short = self.data.Close[-1] < self.ema_50[-1]

            # Long entry: Tightened RSI to <32 (from 35) for stronger oversold, Stoch <45 (from 50) for better timing, plus BB lower touch and EMA bias
            if (
                vol_confirm
                and ema_bias_long
                and (self.rsi[-1] < self.rsi_sma[-1])
                and (self.rsi[-1] < 32)
                and (self.stoch_k[-1] > self.stoch_sma[-1])
                and (self.stoch_k[-1] < 45)
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
                    0.001, min(200.0, position_size)
                )  # 🌙 Moon Dev: Increased max position size to 200 from 50 to leverage high-conviction filtered setups more aggressively, amplifying returns with controlled risk via tighter SL and filters

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

            # Short entry: Symmetric tightening - RSI >68 (from 65), Stoch >55 (from 50), BB upper touch, EMA bias
            if (
                vol_confirm
                and ema_bias_short
                and (self.rsi[-1] > self.rsi_sma[-1])
                and (self.rsi[-1] > 68)
                and (self.stoch_k[-1] < self.stoch_sma[-1])
                and (self.stoch_k[-1] > 55)
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
                    0.001, min(200.0, position_size)
                )  # 🌙 Moon Dev: Increased max size to 200 for amplified short exposure on filtered setups

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
