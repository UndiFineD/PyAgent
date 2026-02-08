# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_16_2025\backtests\BandVwapSync_BT.py
# 🌙 Moon Dev's BandVwapSync Backtest Implementation 🚀
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


class BandVwapSync(Strategy):
    risk_per_trade = 0.02  # 2% risk per trade 🌙

    def init(self):
        # 🌗 Bollinger Bands (20,2) with TA-Lib
        self.I(
            talib.BBANDS,
            self.data.Close,
            timeperiod=20,
            nbdevup=2,
            nbdevdn=2,
            name=["BB_upper", "BB_middle", "BB_lower"],
        )

        # 🌀 Volume-Weighted Average Price (20-period)
        self.I(
            ta.vwap,
            self.data.High,
            self.data.Low,
            self.data.Close,
            self.data.Volume,
            length=20,
            name="VWAP_20",
        )

        # 📈 5-period MA of VWAP
        self.I(talib.SMA, self.data.VWAP_20, timeperiod=5, name="VWAP_MA_5")

    def next(self):
        # Wait for sufficient data 🌊
        if len(self.data) < 20:
            return

        # 🛑 Current indicator values
        price_low = self.data.Low[-1]
        bb_lower = self.data.BB_lower[-1]
        vwap = self.data.VWAP_20[-1]
        prev_vwap = self.data.VWAP_20[-2] if len(self.data.VWAP_20) > 1 else vwap

        # 🌙 Entry Logic: Band touch + VWAP momentum
        if not self.position:
            if price_low <= bb_lower and vwap > prev_vwap:
                # 🛡️ Risk Management Calculations
                entry_price = self.data.Close[-1]
                bb_upper = self.data.BB_upper[-1]
                bandwidth = bb_upper - bb_lower
                stop_loss = bb_lower - (bandwidth * 0.5)

                risk_amount = self.equity * self.risk_per_trade
                risk_per_share = entry_price - stop_loss

                if risk_per_share > 0:
                    position_size = int(round(risk_amount / risk_per_share))
                    if position_size > 0:
                        self.buy(size=position_size, sl=stop_loss)
                        print(
                            f"🌙 MOON DEV ALERT: LONG @ {entry_price:.2f} ✨ | Size: {position_size} | SL: {stop_loss:.2f} 🚀"
                        )

        # 💼 Exit Logic
        else:
            # 📉 VWAP trend reversal exit
            if crossover(self.data.VWAP_MA_5, self.data.VWAP_20):
                self.position.close()
                print("🌙 VWAP Trend Reversal - Closing Position! 🏁")

            # 🎯 Upper band profit taking
            if self.data.High[-1] >= self.data.BB_upper[-1]:
                self.position.close()
                print("🚀 Upper Band Reached - Profit Harvest! 🌕")

            # 🛡️ Trailing stop to breakeven
            if self.data.High[-1] >= self.data.BB_middle[-1] and self.position.sl < self.position.entry_price:
                self.position.sl = self.position.entry_price
                print("🌙 Trail Stop Activated - Breakeven Secured! 🛡️")


# 🧹 Data Cleaning Ritual
data = pd.read_csv("/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv")
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
data["DateTime"] = pd.to_datetime(data["datetime"])
data = data.set_index("DateTime").sort_index()

# 🌙 Launch Backtest
bt = Backtest(data, BandVwapSync, cash=1_000_000, commission=0.002)
stats = bt.run()
print("\n🌕🌖🌗🌘🌑 MOON DEV BACKTEST RESULTS 🌑🌒🌓🌔🌕")
print(stats)
print(stats._strategy)
