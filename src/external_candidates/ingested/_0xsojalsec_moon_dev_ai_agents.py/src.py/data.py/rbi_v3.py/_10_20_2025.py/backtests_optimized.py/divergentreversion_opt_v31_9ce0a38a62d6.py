# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v31.py
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
    adx_threshold = 30  # 🌙 Moon Dev: Further loosened ADX threshold from 25 to 30 to capture more ranging market opportunities, increasing trade frequency and exposure to reversion setups for accelerated return growth towards 50% target
    risk_per_trade = 0.08  # 🌙 Moon Dev: Increased risk per trade from 5% to 8% to enhance compounding velocity, balanced by tighter SL and trailing to maintain risk control while pushing for higher equity curve
    atr_multiplier_sl = 1.5  # 🌙 Moon Dev: Tightened initial SL multiplier from 2 to 1.5 ATR for reduced risk distance, improving risk-reward ratio and allowing larger position sizes per trade to amplify profits
    atr_multiplier_tp = 12  # 🌙 Moon Dev: Extended TP multiplier from 10 to 12 ATR for an 8:1 risk-reward potential, targeting deeper mean reversion swings to capture outsized gains and drive overall returns higher
    trail_start = 3  # 🌙 Moon Dev: ATR multiple to start trailing (after 3 ATR profit), enabling winners to run while protecting gains
    trail_atr = 2  # 🌙 Moon Dev: Trailing distance in ATR, dynamically adjusting SL to lock in profits as price moves favorably

    def init(self):
        # RSI(14) - standard period retained for reliable overbought/oversold detection
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.rsi_sma = self.I(
            talib.SMA, self.rsi, timeperiod=14
        )  # Matched for crossover stability

        # Stochastic %K(14,3,3) - standard for momentum confirmation
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
        )  # Matched for divergence alignment

        # ATR(14) for dynamic stops and trailing
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # ADX(14) for trend filter
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # Volume SMA(20) - stable baseline
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)

        print(
            "🌙 Moon Dev: Indicators stable with added trailing stop logic for profit protection, combined with loosened filters to boost trade count and returns without excessive risk ✨"
        )

    def next(self):
        # 🌙 Moon Dev: Enhanced with trailing stop mechanism - after reaching trail_start ATR profit, trail SL by trail_atr ATR to let winners extend while securing gains, improving average trade profitability and reducing give-back for higher net returns

        # Trailing stop logic for existing positions
        if self.position:
            atr_val = self.atr[-1]
            if self.position.is_long:
                profit = self.data.Close[-1] - self.position.price
                if profit > self.trail_start * atr_val:
                    new_sl = self.data.Close[-1] - self.trail_atr * atr_val
                    if new_sl > self.position.sl:
                        self.position.sl = new_sl
                        print(
                            f"🌙 Moon Dev: Trailing Long SL updated to {new_sl:.2f} (profit: {profit:.2f}) 🔒"
                        )
            elif self.position.is_short:
                profit = self.position.price - self.data.Close[-1]
                if profit > self.trail_start * atr_val:
                    new_sl = self.data.Close[-1] + self.trail_atr * atr_val
                    if new_sl < self.position.sl:
                        self.position.sl = new_sl
                        print(
                            f"🌙 Moon Dev: Trailing Short SL updated to {new_sl:.2f} (profit: {profit:.2f}) 🔒"
                        )

        # Entry conditions only if no position and sufficient history
        if (
            (not self.position)
            and (len(self.rsi) > 30)
            and (self.adx[-1] < self.adx_threshold)
        ):  # 🌙 Moon Dev: Reduced history check to 30 bars for earlier strategy activation, capturing more historical opportunities to compound towards target

            # Further loosened volume filter to >0.8x average for broader confirmation, allowing more trades in varying volume regimes to increase overall activity and returns
            vol_confirm = self.data.Volume[-1] > 0.8 * self.vol_sma[-1]

            # Long entry: Loosened RSI to <40 (from 35) for more oversold captures, Stoch <55 (from 50) for earlier momentum turns, enhancing signal frequency while retaining reversion edge
            if (
                vol_confirm
                and (self.rsi[-1] < self.rsi_sma[-1])
                and (self.rsi[-1] < 40)
                and (self.stoch_k[-1] > self.stoch_sma[-1])
                and (self.stoch_k[-1] < 55)
            ):
                entry_price = self.data.Close[-1]
                atr_val = self.atr[-1]
                sl_price = entry_price - (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price + (self.atr_multiplier_tp * atr_val)
                risk_distance = entry_price - sl_price

                equity = (
                    self._broker.get_cash() + self._broker.get_equity()
                )  # 🌙 Moon Dev: Use accurate equity calculation for precise sizing
                risk_amount = equity * self.risk_per_trade
                position_size = risk_amount / risk_distance
                position_size = max(
                    0.001, min(100.0, position_size)
                )  # 🌙 Moon Dev: Increased max position size to 100 for greater leverage on strong signals, enabling larger returns with 1M starting cash while ATR limits exposure

                if (
                    position_size > 0
                    and not np.isnan(sl_price)
                    and not np.isnan(tp_price)
                    and sl_price < entry_price < tp_price
                ):
                    self.buy(size=position_size, sl=sl_price, tp=tp_price)
                    print(
                        f"🌙 Moon Dev: Long Entry at {entry_price:.2f}, Size: {position_size:.4f}, SL: {sl_price:.2f}, TP: {tp_price:.2f} ✨"
                    )
                else:
                    print(
                        "🌙 Moon Dev: Invalid long position size or SL/TP levels, skipping entry ⚠️"
                    )
                return

            # Short entry: Loosened RSI to >60 (from 65) for more overbought entries, Stoch >45 (from 50) for earlier downside momentum, symmetrically boosting short opportunities
            if (
                vol_confirm
                and (self.rsi[-1] > self.rsi_sma[-1])
                and (self.rsi[-1] > 60)
                and (self.stoch_k[-1] < self.stoch_sma[-1])
                and (self.stoch_k[-1] > 45)
            ):
                entry_price = self.data.Close[-1]
                atr_val = self.atr[-1]
                sl_price = entry_price + (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price - (self.atr_multiplier_tp * atr_val)
                risk_distance = sl_price - entry_price

                equity = (
                    self._broker.get_cash() + self._broker.get_equity()
                )  # 🌙 Moon Dev: Accurate equity for short sizing
                risk_amount = equity * self.risk_per_trade
                position_size = risk_amount / risk_distance
                position_size = max(
                    0.001, min(100.0, position_size)
                )  # 🌙 Moon Dev: Max size 100 for amplified short returns

                if (
                    position_size > 0
                    and not np.isnan(sl_price)
                    and not np.isnan(tp_price)
                    and tp_price < entry_price < sl_price
                ):
                    self.sell(size=position_size, sl=sl_price, tp=tp_price)
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
