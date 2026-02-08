# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v5.py
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
    adx_threshold = 25  # Kept as is for ranging market filter
    risk_per_trade = 0.015  # Increased from 1% to 1.5% for higher exposure while maintaining risk
    atr_multiplier_sl = 1.5  # Tightened SL from 2 to 1.5 ATR for better risk control
    atr_multiplier_tp = 4.5  # Increased TP from 4 to 4.5 ATR for improved 1:3 RR to boost returns

    def init(self):
        # RSI(20)
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=20)
        self.rsi_sma = self.I(talib.SMA, self.rsi, timeperiod=20)

        # Stochastic %K(8)
        self.stoch_k, _ = self.I(
            talib.STOCH,
            self.data.High,
            self.data.Low,
            self.data.Close,
            fastk_period=8,
            slowk_period=1,
            slowd_period=1,
        )
        self.stoch_sma = self.I(talib.SMA, self.stoch_k, timeperiod=20)

        # ATR(14) for dynamic stops
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14)

        # ADX(14) for trend filter
        self.adx = self.I(talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14)

        # Volume SMA for entry filter to avoid low-quality signals
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=20)

        print("🌙 Moon Dev: Indicators initialized ✨")

    def next(self):
        # 🌙 Moon Dev Optimization: Check for exits first if in position (symmetric for long/short)
        if self.position.is_long:
            # Exit long on first sign of mean reversion upward (RSI or Stoch rising above SMA)
            if (self.rsi[-1] > self.rsi_sma[-1]) or (self.stoch_k[-1] > self.stoch_sma[-1]):
                self.position.close()
                print(f"🌙 Moon Dev: Long Exit on Reversion Signal at {self.data.Close[-1]:.2f} 🚀")
            return

        elif self.position.is_short:
            # Exit short on first sign of mean reversion downward (RSI or Stoch falling below SMA)
            if (self.rsi[-1] < self.rsi_sma[-1]) or (self.stoch_k[-1] < self.stoch_sma[-1]):
                self.position.close()
                print(f"🌙 Moon Dev: Short Exit on Reversion Signal at {self.data.Close[-1]:.2f} 🚀")
            return

        # 🌙 Moon Dev Optimization: Entry conditions only if no position (added long side for bull market capture)
        if (not self.position) and (len(self.rsi) > 20) and (self.adx[-1] < self.adx_threshold):
            # Volume filter for higher quality setups
            if self.data.Volume[-1] <= self.vol_sma[-1]:
                return  # Skip low volume entries

            entry_price = self.data.Close[-1]
            atr_val = self.atr[-1]

            # Long entry: Both indicators oversold relative to their SMAs (mean reversion up)
            if (self.rsi[-1] < self.rsi_sma[-1]) and (self.stoch_k[-1] < self.stoch_sma[-1]):
                sl_price = entry_price - (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price + (self.atr_multiplier_tp * atr_val)
                risk_distance = entry_price - sl_price

                # Position sizing: risk defined % of equity (allow fractions for precision)
                equity = self._broker.get_cash() + self.position.pl  # Use current equity
                risk_amount = equity * self.risk_per_trade
                position_size = risk_amount / risk_distance

                # Check validity
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

            # Short entry: Both indicators overbought relative to their SMAs (fixed Stoch condition from < to >; mean reversion down)
            if (self.rsi[-1] > self.rsi_sma[-1]) and (self.stoch_k[-1] > self.stoch_sma[-1]):
                sl_price = entry_price + (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price - (self.atr_multiplier_tp * atr_val)
                risk_distance = sl_price - entry_price

                # Position sizing: risk defined % of equity (allow fractions for precision)
                equity = self._broker.get_cash() + self.position.pl  # Use current equity
                risk_amount = equity * self.risk_per_trade
                position_size = risk_amount / risk_distance

                # Check validity
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
