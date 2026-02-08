# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\MoonMomentumBreakout_AI2.py
import numpy as np
import pandas as pd
from backtesting import Backtest, Strategy

# Data preprocessing
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data.rename(
    columns={
        "datetime": "Date",
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    },
    inplace=True,
)
data["Date"] = pd.to_datetime(data["Date"])
data.set_index("Date", inplace=True)


class MoonMomentumBreakout(Strategy):
    risk_pct = 0.02
    lookback = 50
    momentum_threshold = 0.05
    atr_period = 14
    stop_loss_atr = 2.0
    take_profit_atr = 6.0

    def init(self):
        # 🌙 Moon Dev Momentum Setup
        close = pd.Series(self.data.Close)
        high = pd.Series(self.data.High)
        low = pd.Series(self.data.Low)
        volume = pd.Series(self.data.Volume)

        # Momentum indicators
        self.sma_fast = self.I(lambda: close.rolling(10).mean())
        self.sma_slow = self.I(lambda: close.rolling(30).mean())

        # Breakout levels
        self.high_breakout = self.I(lambda: high.rolling(self.lookback).max())
        self.low_breakout = self.I(lambda: low.rolling(self.lookback).min())

        # ATR for volatility-based stops
        tr1 = high - low
        tr2 = (high - close.shift(1)).abs()
        tr3 = (low - close.shift(1)).abs()
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        self.atr = self.I(lambda: tr.rolling(self.atr_period).mean())

        # Volume momentum
        self.volume_sma = self.I(lambda: volume.rolling(20).mean())

        # Price momentum
        momentum_vals = []
        for i in range(len(close)):
            if i < 20:
                momentum_vals.append(0)
            else:
                current_price = close.iloc[i]
                past_price = close.iloc[i - 20]
                momentum = (current_price - past_price) / past_price if past_price > 0 else 0
                momentum_vals.append(momentum)

        self.momentum = self.I(lambda: pd.Series(momentum_vals, index=close.index))

        print("🌙✨ Moon Momentum Breakout Strategy Activated! 🚀")

    def next(self):
        if len(self.data) < self.lookback + 20:
            return

        price = self.data.Close[-1]
        volume = self.data.Volume[-1]

        # Safe indicator access
        atr_val = self.atr[-1] if not np.isnan(self.atr[-1]) else 100
        momentum_val = self.momentum[-1] if not np.isnan(self.momentum[-1]) else 0
        high_break = self.high_breakout[-1] if not np.isnan(self.high_breakout[-1]) else price
        sma_fast = self.sma_fast[-1] if not np.isnan(self.sma_fast[-1]) else price
        sma_slow = self.sma_slow[-1] if not np.isnan(self.sma_slow[-1]) else price
        volume_sma = self.volume_sma[-1] if not np.isnan(self.volume_sma[-1]) else volume

        # 🚀 Long Entry: Breakout with Strong Momentum
        if not self.position and atr_val > 0:
            # Conditions for long entry
            breakout_condition = price > high_break * 0.999
            momentum_condition = momentum_val > self.momentum_threshold
            trend_condition = sma_fast > sma_slow
            volume_condition = volume > volume_sma * 1.2

            if breakout_condition and momentum_condition and trend_condition and volume_condition:
                # Risk management
                stop_loss = price - self.stop_loss_atr * atr_val
                take_profit = price + self.take_profit_atr * atr_val
                risk_amount = self.equity * self.risk_pct
                risk_per_share = price - stop_loss

                if risk_per_share > 0:
                    position_size = int(round(risk_amount / risk_per_share))

                    if position_size > 0:
                        self.buy(size=position_size, sl=stop_loss, tp=take_profit)
                        print(
                            f"🌙🚀 MOON BREAKOUT! Long {position_size} @ {price:.2f} | "
                            f"SL: {stop_loss:.2f} | TP: {take_profit:.2f} | Momentum: {momentum_val:.3f}"
                        )

        # 📈 Exit conditions - trend reversal
        elif self.position and self.position.is_long:
            # Exit on momentum reversal or SMA cross
            if momentum_val < -0.02 or sma_fast < sma_slow * 0.995:
                self.position.close()
                print(f"🌑 MOON RETREAT! Closing long @ {price:.2f} | Momentum: {momentum_val:.3f}")


# 🌙🚀 Moon Dev Backtest Execution
print("🌙🚀 Starting Moon Momentum Breakout Backtest...")
bt = Backtest(data, MoonMomentumBreakout, cash=1000000, commission=0.002)
stats = bt.run()
print("\n" + "=" * 60)
print("🌙✨ MOON MOMENTUM BREAKOUT STRATEGY RESULTS ✨🌙")
print("=" * 60)
print(stats)
print("\n🚀 Strategy Details:")
print(stats._strategy)
print("=" * 60)
