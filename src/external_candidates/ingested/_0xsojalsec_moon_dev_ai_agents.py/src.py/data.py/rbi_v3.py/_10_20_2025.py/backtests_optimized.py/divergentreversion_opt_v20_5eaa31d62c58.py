# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v20.py
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
    adx_threshold = (
        20  # 🌙 Moon Dev: Kept ADX threshold at 20 for ranging market filter
    )
    risk_per_trade = 0.01  # 1% risk maintained for good risk management
    atr_multiplier_sl = 2
    atr_multiplier_tp = 6  # 🌙 Moon Dev: Kept TP multiplier at 6 for 1:3 RR to balance capture and realism
    atr_multiplier_trail = (
        1.5  # 🌙 Moon Dev: Added trailing multiplier for dynamic SL adjustment
    )
    trail_activation_atr = 1  # 🌙 Moon Dev: Activate trailing after 1 ATR profit

    def init(self):
        # 🌙 Moon Dev: Tuned RSI to standard 14 period for better sensitivity in mean reversion
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)

        # 🌙 Moon Dev: Changed Stochastic to standard 14,3,3 for smoother, more reliable oversold/overbought signals
        self.stoch_k, self.stoch_d = self.I(
            talib.STOCH,
            self.data.High,
            self.data.Low,
            self.data.Close,
            fastk_period=14,
            slowk_period=3,
            slowd_period=3,
        )

        # ATR(14) for dynamic stops - unchanged
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # ADX(14) for trend filter - unchanged period
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # 🌙 Moon Dev: Kept volume SMA filter to confirm entries on higher volume for better quality signals
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)

        # 🌙 Moon Dev: Added Bollinger Bands for entry filter to catch stronger reversion at band extremes
        self.bb_upper, self.bb_mid, self.bb_lower = self.I(
            talib.BBANDS, self.data.Close, timeperiod=20, nbdevup=2, nbdevdn=2
        )

        print(
            "🌙 Moon Dev: Indicators initialized with BB filter and tuned oscillators ✨"
        )

    def next(self):
        # 🌙 Moon Dev: First, handle trailing stops for existing positions to lock profits and let winners run
        if self.position:
            atr_val = self.atr[-1]
            entry_price = self.position.price
            current_price = self.data.Close[-1]

            if self.position.is_long:
                profit_dist = current_price - entry_price
                if profit_dist > (self.trail_activation_atr * atr_val):
                    new_sl = current_price - (self.atr_multiplier_trail * atr_val)
                    if new_sl > self.position.sl:
                        self.position.sl = new_sl
                        print(
                            f"🌙 Moon Dev: Trailed Long SL to {new_sl:.2f} at {current_price:.2f} 🔒"
                        )

            elif self.position.is_short:
                profit_dist = entry_price - current_price
                if profit_dist > (self.trail_activation_atr * atr_val):
                    new_sl = current_price + (self.atr_multiplier_trail * atr_val)
                    if new_sl < self.position.sl:
                        self.position.sl = new_sl
                        print(
                            f"🌙 Moon Dev: Trailed Short SL to {new_sl:.2f} at {current_price:.2f} 🔒"
                        )
            return  # Exit after handling trailing to avoid new entries while positioned

        # 🌙 Moon Dev: Removed early signal-based exits to rely on SL/TP/trailing for larger profit capture
        # Entry conditions only if no position and sufficient history
        if (
            (not self.position)
            and (len(self.rsi) > 20)
            and (self.adx[-1] < self.adx_threshold)
        ):

            # Volume filter for all entries
            vol_confirm = self.data.Volume[-1] > self.vol_sma[-1]

            # 🌙 Moon Dev: Improved to standard mean reversion: both oscillators oversold for long, with BB lower touch for quality filter
            # This replaces divergent logic with aligned oversold for higher win rate in ranging markets
            if (
                vol_confirm
                and (self.rsi[-1] < 30)
                and (self.stoch_d[-1] < 20)
                and (self.data.Close[-1] < self.bb_lower[-1])
            ):
                entry_price = self.data.Close[-1]
                atr_val = self.atr[-1]
                sl_price = entry_price - (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price + (self.atr_multiplier_tp * atr_val)
                risk_distance = entry_price - sl_price

                equity = (
                    self._broker._cash
                )  # 🌙 Moon Dev: Use broker cash for accurate equity in sizing
                risk_amount = equity * self.risk_per_trade
                position_size = risk_amount / risk_distance
                position_size = max(
                    0.001, min(10.0, position_size)
                )  # 🌙 Moon Dev: Increased max size cap to 10 BTC for higher return potential while risk-controlled

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

            # Short entry: both overbought with BB upper touch
            if (
                vol_confirm
                and (self.rsi[-1] > 70)
                and (self.stoch_d[-1] > 80)
                and (self.data.Close[-1] > self.bb_upper[-1])
            ):
                entry_price = self.data.Close[-1]
                atr_val = self.atr[-1]
                sl_price = entry_price + (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price - (self.atr_multiplier_tp * atr_val)
                risk_distance = sl_price - entry_price

                equity = (
                    self._broker._cash
                )  # 🌙 Moon Dev: Use broker cash for accurate equity in sizing
                risk_amount = equity * self.risk_per_trade
                position_size = risk_amount / risk_distance
                position_size = max(
                    0.001, min(10.0, position_size)
                )  # 🌙 Moon Dev: Increased max size cap to 10 BTC for higher return potential while risk-controlled

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
