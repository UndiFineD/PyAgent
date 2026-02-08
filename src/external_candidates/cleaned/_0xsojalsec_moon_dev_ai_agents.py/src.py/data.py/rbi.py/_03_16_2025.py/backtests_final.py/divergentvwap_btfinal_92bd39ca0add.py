# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_16_2025\backtests_final\DivergentVwap_BTFinal.py
import pandas as pd
import pandas_ta as pta
import talib
from backtesting import Backtest, Strategy


class DivergentVwap(Strategy):
    risk_pct = 0.01  # 1% risk per trade
    trailing_stop = 0.01  # 1% trailing stop
    stoch_period = 14
    rsi_period = 14

    def init(self):
        # Calculate indicators with Moon Dev precision 🌙
        self.stoch_k = self.I(
            lambda: talib.STOCH(
                self.data.High,
                self.data.Low,
                self.data.Close,
                fastk_period=self.stoch_period,
                slowk_period=3,
                slowk_matype=0,
                slowd_period=3,
                slowd_matype=0,
            )[0]
        )

        self.stoch_d = self.I(
            lambda: talib.STOCH(
                self.data.High,
                self.data.Low,
                self.data.Close,
                fastk_period=self.stoch_period,
                slowk_period=3,
                slowk_matype=0,
                slowd_period=3,
                slowd_matype=0,
            )[1]
        )

        self.vwap = self.I(
            lambda: pta.vwap(
                high=self.data.High,
                low=self.data.Low,
                close=self.data.Close,
                volume=self.data.Volume,
            )
        )

        self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_period)
        self.swing_low = self.I(talib.MIN, self.data.Low, 20)

    def next(self):
        # Moon Dev's Galactic Entry Logic 🌌
        if not self.position and len(self.data) > 20:
            stoch_oversold = self.stoch_k[-1] < 20
            price_divergence = self.data.Low[-1] < self.data.Low[-2] and self.stoch_k[-1] > self.stoch_k[-2]
            vwap_bullish = self.vwap[-1] > self.vwap[-2]

            if stoch_oversold and price_divergence and vwap_bullish:
                # Calculate cosmic position size 🌠
                entry_price = self.data.Close[-1]
                sl_price = min(self.swing_low[-1], entry_price * 0.98)
                risk_amount = self.risk_pct * self.equity
                position_size = int(round(risk_amount / (entry_price - sl_price)))

                if position_size > 0:
                    self.buy(size=position_size, sl=sl_price, tp=None)
                    print(f"🌙✨🚀 MOON DEV LONG: {position_size} units @ {entry_price:.2f} | SL {sl_price:.2f}")

        # Moon Dev's Stellar Exit Strategy 🌠
        elif self.position and self.rsi[-1] >= 70:
            self.position.close()
            print(f"🌙✨🔻 MOON DEV EXIT: RSI {self.rsi[-1]:.2f} @ {self.data.Close[-1]:.2f}")


# Load and prepare cosmic data 🌌
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
data["datetime"] = pd.to_datetime(data["datetime"])
data.set_index("datetime", inplace=True)

# Launch Moon Dev's Backtest Rocket 🚀
bt = Backtest(data, DivergentVwap, cash=1_000_000, commission=0.002)
stats = bt.run()
print("\n🌕🌖🌗🌘🌑🌒🌓🌔🌕")
print("MOON DEV BACKTEST RESULTS:")
print(stats)
print(stats._strategy)
