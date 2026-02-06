# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_16_2025\backtests\HarmonicBreakoutFilter_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

# Clean and prepare data
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
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
data["DateTime"] = pd.to_datetime(data["datetime"])
data.set_index("DateTime", inplace=True)


class HarmonicBreakoutFilter(Strategy):
    swing_period = 20
    volume_ma_period = 50
    risk_pct = 0.01
    rr_ratio = 2

    def init(self):
        # Core indicators
        self.swing_high = self.I(
            talib.MAX, self.data.High, self.swing_period, name="🌙 Swing High"
        )
        self.swing_low = self.I(
            talib.MIN, self.data.Low, self.swing_period, name="🌙 Swing Low"
        )
        self.vol_ma = self.I(
            talib.SMA, self.data.Volume, self.volume_ma_period, name="🌙 Volume MA"
        )
        self.bullish_engulf = self.I(
            talib.CDLENGULFING,
            self.data.Open,
            self.data.High,
            self.data.Low,
            self.data.Close,
            name="✨ Engulfing",
        )

    def next(self):
        if not self.position:
            current_high = self.swing_high[-1]
            current_low = self.swing_low[-1]

            # Calculate Fibonacci levels
            fib_618 = current_low + 0.618 * (current_high - current_low)

            # Entry conditions
            price_action_cond = (
                self.data.Close[-1] > current_high and self.data.Low[-2] < fib_618
            )
            volume_cond = self.data.Volume[-1] > self.vol_ma[-1]
            pattern_cond = self.bullish_engulf[-1] > 0

            if price_action_cond and volume_cond and pattern_cond:
                # Risk management calculations
                entry_price = self.data.Close[-1]
                stop_loss = current_low
                risk_per_share = entry_price - stop_loss

                if risk_per_share > 0:
                    risk_amount = self.equity * self.risk_pct
                    position_size = int(round(risk_amount / risk_per_share))

                    if position_size > 0:
                        take_profit = entry_price + self.rr_ratio * risk_per_share
                        print(
                            f"🌙✨🚀 MOON DEV ALERT: LONG Entry {entry_price:.2f} | "
                            f"SL: {stop_loss:.2f} | TP: {take_profit:.2f} | "
                            f"Size: {position_size} contracts"
                        )

                        self.buy(size=position_size, sl=stop_loss, tp=take_profit)

    def notify_trade(self, trade):
        if trade.is_closed:
            emoji = "🚀🌕" if trade.pl > 0 else "💥🌑"
            print(
                f"🌙 Trade Closed: {trade.direction} {trade.size} | "
                f"P&L: ${trade.pl:.2f} | ROI: {trade.pl_pct:.2%} {emoji}"
            )


# Execute backtest
bt = Backtest(data, HarmonicBreakoutFilter, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
