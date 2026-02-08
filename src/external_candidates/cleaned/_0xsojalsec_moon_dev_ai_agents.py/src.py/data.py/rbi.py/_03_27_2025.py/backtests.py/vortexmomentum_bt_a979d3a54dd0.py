# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_27_2025\backtests\VortexMomentum_BT.py
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


# Moon Dev Data Preparation Ritual 🌙
def prepare_data(path):
    data = pd.read_csv(path)
    # Cleanse column names
    data.columns = data.columns.str.strip().str.lower()
    # Banish unnamed columns
    data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
    # Proper column mapping
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


class VortexMomentum(Strategy):
    risk_per_trade = 0.01  # 1% of equity at risk

    def init(self):
        # Moon Dev Indicator Conjuring ✨
        high, low, close = self.data.High, self.data.Low, self.data.Close

        # Vortex Magic
        vortex = ta.vortex(high=high, low=low, close=close, length=14)
        self.vi_plus = self.I(lambda: vortex["VIp"], name="VI+")
        self.vi_minus = self.I(lambda: vortex["VIm"], name="VI-")

        # Momentum Sorcery
        self.cmo = self.I(talib.CMO, close, timeperiod=14, name="CMO")

        # Risk Protection Spells 🛡️
        self.atr = self.I(talib.ATR, high, low, close, timeperiod=14, name="ATR")

        print("🌕 Moon Dev Strategy Activated: Vortex & CMO Spells Ready")

    def next(self):
        # Moon Dev Trading Logic Constellation 🌌
        price = self.data.Close[-1]

        if not self.position:
            # Long Entry Constellation
            if crossover(self.vi_plus, self.vi_minus) and self.cmo[-1] > 50:
                # Risk Management Alchemy 🧪
                atr_val = self.atr[-1]
                stop_price = price - 1.5 * atr_val
                risk_amount = self.risk_per_trade * self.equity
                risk_per_share = price - stop_price

                if risk_per_share <= 0:
                    print("🌑 Moon Dev Warning: Negative Risk Detected!")
                    return

                position_size = int(round(risk_amount / risk_per_share))

                if position_size > 0:
                    self.buy(
                        size=position_size,
                        sl=stop_price,
                        tag=f"🚀 Moon Launch: {price:.2f}",
                    )
                    print(f"🚀 BUY SIGNAL: {price:.2f} | Size: {position_size}")

        else:
            # Exit Constellation 🌠
            exit_cond1 = crossover(self.vi_minus, self.vi_plus)
            exit_cond2 = self.cmo[-1] < 30

            if exit_cond1 or exit_cond2:
                self.position.close()
                print(f"🌙 SELL SIGNAL: {price:.2f} | CMO: {self.cmo[-1]:.2f}")


# Moon Dev Backtest Ritual 🔮
if __name__ == "__main__":
    DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
    data = prepare_data(DATA_PATH)

    bt = Backtest(data, VortexMomentum, cash=1_000_000, commission=0.002, exclusive_orders=True)

    stats = bt.run()
    print("\n🌕🌖🌗🌘🌑🌒🌓🌔🌕")
    print("MOON DEV BACKTEST RESULTS:")
    print(stats)
    print(stats._strategy)
