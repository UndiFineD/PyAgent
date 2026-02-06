# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_07_2025\backtests\VolBackVwap_BT.py
# -*- coding: utf-8 -*-
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


# Moon Dev Data Preparation Ritual 🌙✨
def prepare_data(path):
    # Load cosmic data
    data = pd.read_csv(path)

    # Cleanse column names
    data.columns = data.columns.str.strip().str.lower()

    # Banish unnamed columns
    data = data.drop(columns=[col for col in data.columns if "unnamed" in col])

    # Align with celestial coordinate system
    data = data.rename(
        columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume",
        }
    )

    # Convert to temporal dimension
    data["datetime"] = pd.to_datetime(data["datetime"])
    data = data.set_index("datetime")

    return data


# Moon Dev's VolBackVwap Strategy 🌙🚀
class VolBackVwap(Strategy):
    risk_per_trade = 0.01  # 1% of cosmic stardust

    def init(self):
        # Celestial Indicator Conjuration
        self.vwap = self.I(
            ta.vwap,
            high=self.data.High,
            low=self.data.Low,
            close=self.data.Close,
            volume=self.data.Volume,
            anchor="D",
            name="VWAP",
        )

        self.volume_ma = self.I(talib.SMA, self.data.Volume, 20, name="VolMA20")
        self.upper_bb, _, _ = self.I(
            talib.BBANDS,
            self.data.Close,
            timeperiod=20,
            nbdevup=2,
            nbdevdn=2,
            matype=0,
            name="BBANDS",
        )

        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, 14, name="ATR14"
        )

    def next(self):
        # Wait for cosmic alignment
        if len(self.data) < 20:
            return

        # Stellar Entry Conditions 🌌
        vwap_breakout = crossover(self.data.Close, self.vwap)[-1]
        volume_surge = self.data.Volume[-1] > self.volume_ma[-1]
        vix_backwardation = self.data["vix1"][-1] > self.data["vix2"][-1]

        # Moon Dev's Cosmic Entry Signal 🌙🚀
        if not self.position and all([vwap_breakout, volume_surge, vix_backwardation]):
            entry_price = self.data.Close[-1]
            atr_value = self.atr[-1]

            # Quantum Risk Calculations
            stop_loss = entry_price - 1.5 * atr_value
            risk_amount = self.equity * self.risk_per_trade
            position_size = risk_amount / (entry_price - stop_loss)
            position_size = int(round(position_size))

            if position_size > 0:
                self.buy(
                    size=position_size, sl=stop_loss, tag="Moon Dev Cosmic Entry 🌙✨"
                )
                print(
                    f"🌙🚀 MOON DEV ALERT: Buying {position_size} units at {entry_price:.2f}"
                )
                print(f"    Cosmic Shield Activated: Stop Loss at {stop_loss:.2f} 🛡️")

        # Stellar Exit Conditions 🌠
        if self.position.is_long and self.data.Close[-1] >= self.upper_bb[-1]:
            self.position.close()
            print(
                f"🌙💫 MOON DEV EXIT: Upper Bollinger Band reached at {self.data.Close[-1]:.2f}"
            )


# Initiate Moon Dev's Cosmic Backtest 🌙✨
if __name__ == "__main__":
    # Path to celestial data
    data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"

    # Summon cosmic data
    cosmic_data = prepare_data(data_path)

    # Activate Moon Dev's Backtest Engine
    bt = Backtest(cosmic_data, VolBackVwap, cash=1_000_000, exclusive_orders=True)

    # Execute celestial simulation
    stats = bt.run()

    # Decrypt cosmic performance metrics
    print("\n🌙🚀🌙🚀 MOON DEV BACKTEST RESULTS 🌙🚀🌙🚀")
    print(stats)
    print("\n🌌 Cosmic Strategy Details:")
    print(stats._strategy)
