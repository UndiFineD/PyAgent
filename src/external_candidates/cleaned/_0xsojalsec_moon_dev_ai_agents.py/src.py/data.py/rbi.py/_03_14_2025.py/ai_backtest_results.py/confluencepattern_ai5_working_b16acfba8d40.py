# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\ConfluencePattern_AI5_working.py
# 🌙 Moon Dev's ConfluencePattern Backtest - AI5 Implementation
import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy

# Data Preparation
print("🌙 Loading BTC-USD 15m data for ConfluencePattern strategy...")
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    },
    inplace=True,
)
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)

print(f"🚀 Data loaded: {len(data)} bars from {data.index[0]} to {data.index[-1]}")


def ema(series, period):
    if isinstance(series, np.ndarray):
        series = pd.Series(series)
    return series.ewm(span=period).mean().values


def rsi(series, period=14):
    if isinstance(series, np.ndarray):
        series = pd.Series(series)
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return (100 - (100 / (1 + rs))).values


def macd(series, fast=12, slow=26, signal=9):
    if isinstance(series, np.ndarray):
        series = pd.Series(series)
    ema_fast = series.ewm(span=fast).mean()
    ema_slow = series.ewm(span=slow).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal).mean()
    histogram = macd_line - signal_line
    return macd_line.values, signal_line.values, histogram.values


def sma(series, period):
    if isinstance(series, np.ndarray):
        series = pd.Series(series)
    return series.rolling(period).mean().values


def rolling_max(series, period):
    if isinstance(series, np.ndarray):
        series = pd.Series(series)
    return series.rolling(period).max().values


def rolling_min(series, period):
    if isinstance(series, np.ndarray):
        series = pd.Series(series)
    return series.rolling(period).min().values


class ConfluencePattern(Strategy):
    risk_per_trade = 0.01  # 1% risk per trade

    def init(self):
        # 🌙 Calculate indicators using custom functions
        self.ema50 = self.I(ema, self.data.Close, 50)
        self.ema200 = self.I(ema, self.data.Close, 200)
        self.rsi = self.I(rsi, self.data.Close, 14)
        self.macd_line, self.macd_signal, self.macd_hist = self.I(macd, self.data.Close, 12, 26, 9)
        self.volume_sma = self.I(sma, self.data.Volume, 20)
        self.swing_high = self.I(rolling_max, self.data.High, 20)
        self.swing_low = self.I(rolling_min, self.data.Low, 20)

        print("🌙✨ Moon Dev ConfluencePattern Indicators Initialized!")
        print("EMA(50, 200), RSI(14), MACD(12,26,9)")
        print("Volume SMA(20), Swing High/Low(20)")

    def next(self):
        # Ensure we have enough data
        if len(self.ema200) < 200:
            return

        current_close = self.data.Close[-1]
        current_volume = self.data.Volume[-1]

        # 🌙 Get indicator values
        ema50 = self.ema50[-1]
        ema200 = self.ema200[-1]
        rsi_val = self.rsi[-1]
        macd_hist = self.macd_hist[-1]
        volume_sma = self.volume_sma[-1]
        swing_high = self.swing_high[-1]
        swing_low = self.swing_low[-1]

        # Check for valid indicator values
        if (
            np.isnan(ema50)
            or np.isnan(ema200)
            or np.isnan(rsi_val)
            or np.isnan(macd_hist)
            or np.isnan(volume_sma)
            or np.isnan(swing_high)
            or np.isnan(swing_low)
        ):
            return

        # 🌙 Moon Dev Risk Management Parameters
        risk_amount = self.risk_per_trade * self.equity

        if not self.position:
            # 🌙✨ Long Entry Conditions - ALL must be true for confluence
            long_conditions = [
                current_close > ema50,
                current_close > ema200,
                rsi_val > 50,
                macd_hist > 0,
                current_volume > volume_sma,
                current_close > swing_high,
            ]

            # 🌙✨ Short Entry Conditions - ALL must be true for confluence
            short_conditions = [
                current_close < ema50,
                current_close < ema200,
                rsi_val < 50,
                macd_hist < 0,
                current_volume > volume_sma,
                current_close < swing_low,
            ]

            if all(long_conditions):
                # 🌙 Calculate long position size
                entry_price = current_close
                stop_loss = swing_low
                risk_per_share = entry_price - stop_loss

                if risk_per_share > 0:
                    position_size = int(round(risk_amount / risk_per_share))
                    take_profit = entry_price + 2 * risk_per_share

                    if position_size > 0:
                        self.buy(size=position_size, sl=stop_loss, tp=take_profit)
                        print(f"🌙🚀✨ BULLISH CONFLUENCE! Long {position_size} shares")
                        print(f"Entry: {entry_price:.2f}, SL: {stop_loss:.2f}, TP: {take_profit:.2f}")

            elif all(short_conditions):
                # 🌙 Calculate short position size
                entry_price = current_close
                stop_loss = swing_high
                risk_per_share = stop_loss - entry_price

                if risk_per_share > 0:
                    position_size = int(round(risk_amount / risk_per_share))
                    take_profit = entry_price - 2 * risk_per_share

                    if position_size > 0:
                        self.sell(size=position_size, sl=stop_loss, tp=take_profit)
                        print(f"🌙📉✨ BEARISH CONFLUENCE! Short {position_size} shares")
                        print(f"Entry: {entry_price:.2f}, SL: {stop_loss:.2f}, TP: {take_profit:.2f}")


# 🌙✨ Launch Backtest
print("🚀 Launching ConfluencePattern backtest with $1,000,000 portfolio...")
bt = Backtest(data, ConfluencePattern, cash=1_000_000, commission=0.002)
stats = bt.run()

print("\n" + "=" * 60)
print("🌙 MOON DEV CONFLUENCEPATTERN STRATEGY RESULTS 🌙")
print("=" * 60)
print(stats)
print("\n🔍 Strategy Details:")
print(stats._strategy)
print("=" * 60)
