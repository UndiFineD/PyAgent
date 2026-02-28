# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_14_2025\AI_BACKTEST_RESULTS\BandStochFusion_AI3.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class BandStochFusion(Strategy):
    risk_pct = 0.01  # 1% risk per trade
    bb_period = 20
    stoch_period = 14
    swing_window = 20

    def init(self):
        # Bollinger Bands Calculation
        def bb_upper(close):
            upper, _, _ = talib.BBANDS(close, timeperiod=self.bb_period, nbdevup=2)
            return upper

        self.upper = self.I(bb_upper, self.data.Close)

        def bb_middle(close):
            _, middle, _ = talib.BBANDS(close, timeperiod=self.bb_period)
            return middle

        self.middle = self.I(bb_middle, self.data.Close)

        def bb_lower(close):
            _, _, lower = talib.BBANDS(close, timeperiod=self.bb_period, nbdevdn=2)
            return lower

        self.lower = self.I(bb_lower, self.data.Close)

        # Stochastic Oscillator
        def stoch_k(high, low, close):
            k, _ = talib.STOCH(
                high,
                low,
                close,
                fastk_period=self.stoch_period,
                slowk_period=3,
                slowd_period=3,
            )
            return k

        self.stoch_k = self.I(stoch_k, self.data.High, self.data.Low, self.data.Close)

        def stoch_d(high, low, close):
            _, d = talib.STOCH(
                high,
                low,
                close,
                fastk_period=self.stoch_period,
                slowk_period=3,
                slowd_period=3,
            )
            return d

        self.stoch_d = self.I(stoch_d, self.data.High, self.data.Low, self.data.Close)

        # Swing High/Low for Stops
        self.swing_high = self.I(
            talib.MAX, self.data.High, timeperiod=self.swing_window
        )
        self.swing_low = self.I(talib.MIN, self.data.Low, timeperiod=self.swing_window)

        print("🌙✨ Lunar Indicators Activated! Ready for Cosmic Trading! 🚀")

    def next(self):
        price = self.data.Close[-1]

        # Moon Dev progress tracker
        if len(self.data) % 500 == 0:
            print(f"🌙 Processing Bar {len(self.data)} | Price: {price:.2f}")

        # Long Exit Conditions
        if self.position.is_long:
            if self.data.High[-1] >= self.middle[-1] or (
                self.stoch_k[-2] > 80 and self.stoch_k[-1] <= 80
            ):
                print(f"🌗 Closing LONG at {price:.2f} (Middle Band/Stoch Exit)")
                self.position.close()

        # Short Exit Conditions
        elif self.position.is_short:
            if self.data.Low[-1] <= self.middle[-1] or (
                self.stoch_k[-2] < 20 and self.stoch_k[-1] >= 20
            ):
                print(f"🌘 Closing SHORT at {price:.2f} (Middle Band/Stoch Exit)")
                self.position.close()

        # Entry Signals Only When Flat
        if not self.position:
            # Long Entry Logic
            long_cond = (
                self.data.Low[-1] <= self.lower[-1]
                and self.stoch_k[-1] < 20
                and (
                    self.stoch_k[-2] < self.stoch_d[-2]
                    and self.stoch_k[-1] > self.stoch_d[-1]
                )
            )

            if long_cond:
                sl = min(self.swing_low[-1], self.lower[-1])
                risk_amount = self.risk_pct * self.equity
                risk_per_share = price - sl

                if risk_per_share > 0:
                    position_size = int(round(risk_amount / risk_per_share))

                    if position_size > 0:
                        self.buy(size=position_size, sl=sl)
                        print(
                            f"\n🌕 LUNAR LONG ENTRY! 🚀"
                            f"\nEntry: {price:.2f}"
                            f"\nSize: {position_size} units"
                            f"\nStop Loss: {sl:.2f}\n"
                        )

            # Short Entry Logic
            short_cond = (
                self.data.High[-1] >= self.upper[-1]
                and self.stoch_k[-1] > 80
                and (
                    self.stoch_k[-2] > self.stoch_d[-2]
                    and self.stoch_k[-1] < self.stoch_d[-1]
                )
            )

            if short_cond:
                sl = max(self.swing_high[-1], self.upper[-1])
                risk_amount = self.risk_pct * self.equity
                risk_per_share = sl - price

                if risk_per_share > 0:
                    position_size = int(round(risk_amount / risk_per_share))

                    if position_size > 0:
                        self.sell(size=position_size, sl=sl)
                        print(
                            f"\n🌑 LUNAR SHORT ENTRY! 📉"
                            f"\nEntry: {price:.2f}"
                            f"\nSize: {position_size} units"
                            f"\nStop Loss: {sl:.2f}\n"
                        )


# Data preparation
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

# Launch moon mission 🚀
bt = Backtest(data, BandStochFusion, cash=1_000_000)
stats = bt.run()

print("\n🌕🌖🌗🌘🌑🌒🌓🌔 MOON DEV BANDSTOCH FUSION REPORT 🌔🌓🌒🌑🌘🌗🌖🌕")
print(stats)
print(stats._strategy)
print("\nLunar Mission Complete! 🌙🧀")
