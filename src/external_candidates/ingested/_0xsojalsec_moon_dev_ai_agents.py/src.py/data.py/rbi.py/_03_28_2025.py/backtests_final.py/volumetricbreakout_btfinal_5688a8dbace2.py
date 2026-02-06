# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_28_2025\backtests_final\VolumetricBreakout_BTFinal.py
# 🌙 Moon Dev's Volumetric Breakout Backtest 🌙
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


class VolumetricBreakout(Strategy):
    risk_per_trade = 0.01  # 1% of equity per trade

    def init(self):
        # 🌈 Indicator Calculations
        # Bollinger Bands (Upper, Middle, Lower)
        def upper_bb(close):
            upper, _, _ = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)
            return upper

        self.upper_band = self.I(upper_bb, self.data.Close)

        # Volume 90th Percentile (20-period)
        self.volume_pct = self.I(
            lambda x: ta.percentile(x, length=20, percentile=90), self.data.Volume
        )

        # RSI for exits
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)

        # Swing Low for stop calculation
        self.swing_low = self.I(talib.MIN, self.data.Low, timeperiod=20)

        # ATR for position sizing
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        print("🌙 Indicators initialized! Ready for cosmic analysis ✨")

    def next(self):
        price = self.data.Close[-1]
        upper = self.upper_band[-1]
        volume = self.data.Volume[-1]
        vol_pct = self.volume_pct[-1]

        # 🚀 Entry Logic
        if not self.position and price > upper and volume > vol_pct:
            # Calculate dynamic stop loss
            entry_price = price
            swing_low_val = self.swing_low[-1]
            price_stop = entry_price * 0.99  # 1% stop
            final_stop = max(swing_low_val, price_stop)

            risk_per_share = entry_price - final_stop
            if risk_per_share <= 0:
                print(
                    f"🌙 Invalid stop {final_stop:.2f} for entry {entry_price:.2f} ✖️"
                )
                return

            # Calculate position size (round to whole units)
            risk_amount = self.equity * self.risk_per_trade
            position_size = int(round(risk_amount / risk_per_share))

            if position_size > 0:
                self.buy(size=position_size, sl=final_stop)
                print(
                    f"🚀 BLASTOFF! Long {position_size} units @ {entry_price:.2f} | Stop: {final_stop:.2f} 🌕"
                )

        # 🌌 Exit Logic
        if self.position:
            rsi_value = self.rsi[-1]
            if crossover(self.rsi, 70) or price < self.upper_band[-1]:
                self.position.close()
                print(
                    f"🌙 RETURN TO BASE | Exit @ {price:.2f} | RSI: {rsi_value:.1f} 🎯"
                )


# 📡 Data Processing
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path)

# 🧹 Clean data according to cosmic standards
data.columns = [col.strip().lower() for col in data.columns]
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

# 🚀 Launch Backtest
bt = Backtest(data, VolumetricBreakout, cash=1_000_000, commission=0.002)
stats = bt.run()

# 🌕 Display Cosmic Performance
print("\n🌙🌕🌖🌗🌘🌑🌒🌓🌔🌙")
print("MOON DEV TRADING REPORT:")
print(stats)
print("To the moon and beyond! 🚀✨")
