# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_28_2025\backtests_package\VortexEmergence_PKG.py
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy


# Moon Dev Data Preparation Ritual 🌙✨
def prepare_data(path):
    data = pd.read_csv(path)
    # Cleanse column names
    data.columns = data.columns.str.strip().str.lower()
    # Banish unnamed columns
    data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
    # Align cosmic energies with proper column names
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
    # Set temporal index
    data["datetime"] = pd.to_datetime(data["datetime"])
    data.set_index("datetime", inplace=True)
    return data


# Cosmic Path Configuration 🌌
DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class VortexEmergence(Strategy):
    risk_per_trade = 0.01  # 1% risk per trade 🌕

    def init(self):
        # Calculate Celestial Indicators 🌠
        self.vi_plus, self.vi_minus = self.I(
            lambda: ta.vortex(self.data.High, self.data.Low, self.data.Close, length=14),
            name=["VI+", "VI-"],
        )

        # Choppiness Index Calculation 🌊
        self.choppiness = self.I(
            lambda: ta.chop(self.data.High, self.data.Low, self.data.Close, length=14),
            name="CHOP",
        )

        # ATR for Stellar Stop Loss Calculation 🔭
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=14,
            name="ATR",
        )

        print("🌙 Lunar Indicators Activated! Vortex Matrix Initialized ✨")

    def next(self):
        price = self.data.Close[-1]

        # Cosmic Entry Signal 🌟
        if not self.position:
            # Replaced crossover with direct comparison
            if (self.vi_plus[-2] < self.vi_minus[-2] and self.vi_plus[-1] > self.vi_minus[-1]) and (
                self.choppiness[-1] < 35
            ):
                # Starlight Position Sizing Calculation 🌠
                atr_value = self.atr[-1]
                stop_price = price - 1.5 * atr_value
                risk_per_share = price - stop_price

                if risk_per_share > 0:
                    position_size = int(round((self.equity * self.risk_per_trade) / risk_per_share))
                    if position_size > 0:
                        self.buy(size=position_size, sl=stop_price)
                        print(
                            f"🚀🌙 LUNAR LIFTOFF! Entry: {price:.2f} | Size: {position_size} | Cosmic Stop: {stop_price:.2f}"
                        )

        # Galactic Exit Protocol 🌌
        else:
            if self.choppiness[-1] > 65:
                self.position.close()
                print(f"✨🌙 STARLIGHT RETREAT! Exit: {price:.2f} | Profit: {self.position.pl:.2f}")


# Execute Celestial Backtest 🌕
if __name__ == "__main__":
    # Load and purify cosmic data 🌠
    cosmic_data = prepare_data(DATA_PATH)

    # Initialize Stellar Backtest 🌟
    bt = Backtest(
        cosmic_data,
        VortexEmergence,
        cash=1_000_000,
        commission=0.002,
        exclusive_orders=True,
    )

    # Launch Moon Mission 🌕
    stats = bt.run()

    # Reveal Cosmic Truths 📜
    print("\n🌌🌙 FINAL MISSION REPORT 🌌🌙")
    print(stats)
    print("\n🔭 STRATEGY ARTIFACTS 🔭")
    print(stats._strategy)
