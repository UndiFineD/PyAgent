# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v2\07_24_2025\backtests_package\VolatilityDivergence_PKG.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class VolatilityDivergence(Strategy):
    rsi_period = 14
    atr_period = 14
    vix_lookback = 5
    risk_per_trade = 0.01
    vix_threshold = 20

    def init(self):
        # Clean and prepare data
        self.data.df.columns = self.data.df.columns.str.strip().str.lower()
        self.data.df = self.data.df.drop(columns=[col for col in self.data.df.columns if "unnamed" in col.lower()])

        # Calculate indicators
        close = self.data.Close
        high = self.data.High
        low = self.data.Low

        self.rsi = self.I(talib.RSI, close, self.rsi_period)
        self.atr = self.I(talib.ATR, high, low, close, self.atr_period)
        self.vix = self.I(talib.SMA, self.data.df["vix"], timeperiod=3) if "vix" in self.data.df.columns else None

        # Track previous values for divergence detection
        self.prev_low = None
        self.prev_rsi = None
        self.divergence_confirmed = False

    def next(self):
        if len(self.data.Close) < max(self.rsi_period, self.atr_period) + 5:
            return

        current_low = self.data.Low[-1]
        current_rsi = self.rsi[-1]

        # Moon Dev debug prints 🌙
        print(f"🌙 Current Price: {self.data.Close[-1]:.2f} | RSI: {current_rsi:.2f} | ATR: {self.atr[-1]:.2f}")

        # Check for bullish divergence (price lower low, RSI higher low)
        if self.prev_low is not None and self.prev_rsi is not None:
            if current_low < self.prev_low and current_rsi > self.prev_rsi:
                print(f"✨ Bullish divergence detected! Price LL at {current_low:.2f}, RSI HL at {current_rsi:.2f}")
                self.divergence_confirmed = True

        # Check VIX rising condition
        vix_rising = False
        if self.vix is not None and len(self.vix) >= self.vix_lookback:
            vix_rising = all(self.vix[-i] > self.vix[-i - 1] for i in range(1, min(5, len(self.vix))))
            print(f"📈 VIX {'rising' if vix_rising else 'not rising'} | Current: {self.vix[-1]:.2f}")

        # Entry conditions
        if (
            not self.position
            and self.divergence_confirmed
            and vix_rising
            and (self.vix is None or self.vix[-1] > self.vix_threshold)
        ):
            # Calculate position size based on ATR risk
            atr_value = self.atr[-1]
            stop_loss = self.data.Low[-1] - atr_value
            risk_amount = self.equity * self.risk_per_trade
            position_size = risk_amount / (self.data.Close[-1] - stop_loss)
            position_size = int(round(position_size))

            print(
                f"🚀 ENTRY SIGNAL | Size: {position_size} | SL: {stop_loss:.2f} | TP1: {self.data.Close[-1] + 2 * atr_value:.2f} | TP2: {self.data.Close[-1] + 3 * atr_value:.2f}"
            )

            # Enter trade with initial stop loss
            self.buy(size=position_size, sl=stop_loss)
            self.divergence_confirmed = False

        # Exit conditions
        elif self.position:
            entry_price = self.position.entry_price
            atr_value = self.atr[-1]

            # First profit target (2x ATR)
            if not self.position.is_short and self.data.Close[-1] >= entry_price + 2 * atr_value:
                if self.position.size > 1:  # Partial exit
                    exit_size = int(round(self.position.size / 2))
                    print(f"🌕 Partial profit taken at 2x ATR ({entry_price + 2 * atr_value:.2f}) | Size: {exit_size}")
                    self.position.close(exit_size)

            # Second profit target (3x ATR)
            if not self.position.is_short and self.data.Close[-1] >= entry_price + 3 * atr_value:
                print(f"🌖 Full profit taken at 3x ATR ({entry_price + 3 * atr_value:.2f})")
                self.position.close()

            # Update trailing stop (1x ATR below current low)
            new_sl = self.data.Low[-1] - atr_value
            if new_sl > self.position.sl:
                self.position.sl = new_sl
                print(f"🛡️ Trailing SL updated to {new_sl:.2f}")

        # Update previous values
        self.prev_low = current_low
        self.prev_rsi = current_rsi


# Load and prepare data
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

# Ensure proper column mapping
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)

# Run backtest
bt = Backtest(data, VolatilityDivergence, commission=0.002, exclusive_orders=True)
stats = bt.run()
print(stats)
print(stats._strategy)
