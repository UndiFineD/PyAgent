# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v21.py
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
    adx_threshold = 25  # 🌙 Moon Dev: Loosened ADX threshold to 25 for more trading opportunities while still filtering weak trends
    risk_per_trade = 0.02  # 🌙 Moon Dev: Increased risk per trade to 2% to amplify returns with controlled exposure
    atr_multiplier_sl = 2
    atr_multiplier_tp = 6  # 🌙 Moon Dev: Maintained 1:3 RR for favorable risk-reward to capture reversion moves

    def init(self):
        # RSI(14) - shortened period from 20 to 14 for faster, more responsive mean reversion signals
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.rsi_sma = self.I(talib.SMA, self.rsi, timeperiod=14)

        # Stochastic %K(5,3,3) - adjusted to faster settings for quicker signals in 15m timeframe
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
        )  # 🌙 Moon Dev: Shortened SMA to 5 for faster momentum detection

        # ATR(14) for dynamic stops - unchanged for consistent volatility measure
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # ADX(14) for trend filter - unchanged period
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # 🌙 Moon Dev: Kept volume SMA filter but strengthened confirmation in next() for higher quality entries
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)

        print(
            "🌙 Moon Dev: Indicators initialized with faster periods and volume filter for improved signal quality ✨"
        )

    def next(self):
        # 🌙 Moon Dev: Enhanced exit and trailing logic for better profit capture and risk management
        if self.position.is_long:
            # Long exit on reversion: either indicator recovers from oversold
            if (self.rsi[-1] > self.rsi_sma[-1]) or (
                self.stoch_k[-1] > self.stoch_sma[-1]
            ):
                self.position.close()
                print(
                    f"🌙 Moon Dev: Long Exit on Reversion Signal at {self.data.Close[-1]:.2f} 🚀"
                )

            # 🌙 Moon Dev: Added trailing stop after 2 ATR profit to lock in gains and allow larger moves
            price_profit = self.data.Close[-1] - self.position.entry_price
            if price_profit > 2 * self.atr[-1]:
                trail_sl = self.data.Close[-1] - 2 * self.atr[-1]
                if hasattr(self.position, "sl") and (
                    self.position.sl is None or trail_sl > self.position.sl
                ):
                    self.position.sl = trail_sl
                    print(
                        f"🌙 Moon Dev: Long SL trailed to {trail_sl:.2f} for profit protection 🌙"
                    )
            return

        if self.position.is_short:
            # Short exit on reversion: either indicator recovers from overbought
            if (self.rsi[-1] < self.rsi_sma[-1]) or (
                self.stoch_k[-1] < self.stoch_sma[-1]
            ):
                self.position.close()
                print(
                    f"🌙 Moon Dev: Short Exit on Reversion Signal at {self.data.Close[-1]:.2f} 🚀"
                )

            # 🌙 Moon Dev: Added trailing stop after 2 ATR profit to lock in gains on downside moves
            price_profit = self.position.entry_price - self.data.Close[-1]
            if price_profit > 2 * self.atr[-1]:
                trail_sl = self.data.Close[-1] + 2 * self.atr[-1]
                if hasattr(self.position, "sl") and (
                    self.position.sl is None or trail_sl < self.position.sl
                ):
                    self.position.sl = trail_sl
                    print(
                        f"🌙 Moon Dev: Short SL trailed to {trail_sl:.2f} for profit protection 🌙"
                    )
            return

        # 🌙 Moon Dev: Switched to pure mean reversion entries (both indicators oversold/overbought) for stronger, aligned signals instead of divergence
        # Entry conditions only if no position and sufficient history
        if (
            (not self.position)
            and (len(self.rsi) > 25)
            and (self.adx[-1] < self.adx_threshold)
        ):

            # Strengthened volume filter to >1.5x SMA for higher conviction entries and better risk management
            vol_confirm = self.data.Volume[-1] > 1.5 * self.vol_sma[-1]

            # Long entry: Both RSI and Stoch oversold (below their SMAs) for pure mean reversion bounce
            if (
                vol_confirm
                and (self.rsi[-1] < self.rsi_sma[-1])
                and (self.stoch_k[-1] < self.stoch_sma[-1])
            ):
                entry_price = self.data.Close[-1]
                atr_val = self.atr[-1]
                sl_price = entry_price - (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price + (self.atr_multiplier_tp * atr_val)
                risk_distance = entry_price - sl_price

                equity = (
                    self._broker._cash
                )  # 🌙 Moon Dev: Use broker cash for accurate equity in position sizing
                risk_amount = equity * self.risk_per_trade
                position_size = risk_amount / risk_distance
                position_size = max(
                    0.001, position_size
                )  # 🌙 Moon Dev: Removed upper cap to allow full risk-based sizing for higher returns without overexposure (backtest caps by cash)

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

            # Short entry: Both RSI and Stoch overbought (above their SMAs) for pure mean reversion drop
            if (
                vol_confirm
                and (self.rsi[-1] > self.rsi_sma[-1])
                and (self.stoch_k[-1] > self.stoch_sma[-1])
            ):
                entry_price = self.data.Close[-1]
                atr_val = self.atr[-1]
                sl_price = entry_price + (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price - (self.atr_multiplier_tp * atr_val)
                risk_distance = sl_price - entry_price

                equity = (
                    self._broker._cash
                )  # 🌙 Moon Dev: Use broker cash for accurate equity in position sizing
                risk_amount = equity * self.risk_per_trade
                position_size = risk_amount / risk_distance
                position_size = max(
                    0.001, position_size
                )  # 🌙 Moon Dev: Removed upper cap to allow full risk-based sizing for higher returns

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
