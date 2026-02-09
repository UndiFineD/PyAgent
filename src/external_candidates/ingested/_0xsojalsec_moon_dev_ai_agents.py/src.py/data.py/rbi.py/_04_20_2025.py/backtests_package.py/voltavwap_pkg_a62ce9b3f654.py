# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_20_2025\backtests_package\VoltaVwap_PKG.py
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy


class VoltaVwap(Strategy):
    def init(self):
        self.vwap = self.I(
            ta.vwap,
            self.data.High,
            self.data.Low,
            self.data.Close,
            self.data.Volume,
            length=20,
            name="VWAP 🌊",
        )
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=14,
            name="ATR 🌡️",
        )
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14, name="RSI 💹")

    def next(self):
        current_close = self.data.Close[-1]
        current_rsi = self.rsi[-1]
        prev_rsi = self.rsi[-2] if len(self.rsi) > 1 else 50

        current_vwap = self.vwap[-1]
        current_atr = self.atr[-1]
        upper_band = current_vwap + 2 * current_atr
        lower_band = current_vwap - 2 * current_atr

        # Moon Dev Debug Prints 🌙
        print(
            f"🌙 Moon Dev Indicators >> VWAP: {current_vwap:.2f}, ATR: {current_atr:.2f}, Upper: {upper_band:.2f}, Lower: {lower_band:.2f}, RSI: {current_rsi:.2f}"
        )

        # Entry Logic
        if not self.position:
            risk_percent = 0.01
            risk_amount = self.equity * risk_percent

            # Long Entry 🚀
            if current_close > upper_band and current_rsi > 40:
                risk_per_share = current_close - lower_band
                if risk_per_share > 0:
                    position_size = int(round(risk_amount / risk_per_share))
                    self.buy(size=position_size)
                    print(
                        f"🚀 Moon Dev LONG Entry! Size: {position_size} @ {current_close:.2f}, SL: {lower_band:.2f}"
                    )

            # Short Entry 🐻
            elif current_close < lower_band and current_rsi < 60:
                risk_per_share = upper_band - current_close
                if risk_per_share > 0:
                    position_size = int(round(risk_amount / risk_per_share))
                    self.sell(size=position_size)
                    print(
                        f"🐻 Moon Dev SHORT Entry! Size: {position_size} @ {current_close:.2f}, SL: {upper_band:.2f}"
                    )

        # Exit Logic
        else:
            # Long Exits
            if self.position.is_long:
                if current_rsi < 60 and prev_rsi >= 60:
                    self.position.close()
                    print(f"💰 Moon Dev LONG Exit: RSI Cross <60 @ {current_close:.2f}")

                if self.data.Low[-1] <= lower_band:
                    self.position.close()
                    print(f"🌧️ Moon Dev LONG Stop Loss @ {current_close:.2f}")

            # Short Exits
            elif self.position.is_short:
                if current_rsi > 40 and prev_rsi <= 40:
                    self.position.close()
                    print(
                        f"💰 Moon Dev SHORT Exit: RSI Cross >40 @ {current_close:.2f}"
                    )

                if self.data.High[-1] >= upper_band:
                    self.position.close()
                    print(f"🌧️ Moon Dev SHORT Stop Loss @ {current_close:.2f}")


# Data Handling 🌐
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=["datetime"],
    index_col="datetime",
)
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)

# Run Backtest ⚡
bt = Backtest(data, VoltaVwap, cash=1_000_000)
stats = bt.run()
print(stats)
print(stats._strategy)
