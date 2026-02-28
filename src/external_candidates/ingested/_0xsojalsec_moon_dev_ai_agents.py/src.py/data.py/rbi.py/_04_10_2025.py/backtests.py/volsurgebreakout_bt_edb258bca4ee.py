# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_10_2025\backtests\VolSurgeBreakout_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


class VolSurgeBreakout(Strategy):
    risk_percent = 0.01  # 1% risk per trade

    def init(self):
        # Calculate indicators with Moon Dev precision 🌙
        self.lower_band = self.I(
            lambda x: talib.BBANDS(x, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)[2],
            self.data.Close,
        )
        self.volume_sma = self.I(talib.SMA, self.data.Volume, 20)
        self.sar = self.I(
            talib.SAR, self.data.High, self.data.Low, acceleration=0.02, maximum=0.2
        )

        print("🌙 MOON DEV INIT: Indicators locked and loaded! ✨")

    def next(self):
        price = self.data.Close[-1]

        # MOON DEV ENTRY LOGIC 🌙🚀
        if not self.position and len(self.data.Close) >= 3:
            # Volatility compression check
            in_compression = all(
                c <= lb for c, lb in zip(self.data.Close[-3:], self.lower_band[-3:])
            )

            # Volume surge detection
            volume_spike = self.data.Volume[-1] > 1.25 * self.volume_sma[-1]

            # Breakout trigger
            consolidation_high = max(self.data.High[-3:])
            breakout_trigger = self.data.High[-1] > consolidation_high

            if in_compression and volume_spike and breakout_trigger:
                # Moon-sized risk management 🌕
                entry_price = self.data.Close[-1]
                stop_loss = entry_price * 0.98
                risk_amount = self.equity * self.risk_percent
                position_size = int(round(risk_amount / (entry_price - stop_loss)))

                if position_size > 0:
                    self.buy(size=position_size, sl=stop_loss, tag="MOON_ENTRY")
                    print(
                        f"🌙🚀 MOON BLASTOFF! Long {position_size} @ ${entry_price:.2f} | Stop: ${stop_loss:.2f}"
                    )

        # MOON DEV EXIT LOGIC 🌙✨
        if self.position:
            current_sar = self.sar[-1]
            current_lower = self.lower_band[-1]

            # Parabolic SAR trend reversal
            if current_sar < price:
                self.position.close()
                print(f"🌙💫 SAR REVERSE! Closing @ ${price:.2f}")

            # Lower band re-entry protection
            elif price < current_lower:
                self.position.close()
                print(f"🌙🛑 BAND DEFENSE! Closing @ ${price:.2f}")


# MOON DATA PREP 🌙🔧
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
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

# LAUNCH MOON MISSION 🌙🚀
bt = Backtest(data, VolSurgeBreakout, cash=1_000_000, commission=0.002)
stats = bt.run()
print("\n🌕🌖🌗🌘🌑🌒🌓🌔🌕")
print("MOON DEV BACKTEST COMPLETE! FULL STATS:")
print(stats)
print(stats._strategy)
