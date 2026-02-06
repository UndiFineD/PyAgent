# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_05_2025\backtests\ElderReversion_BT.py
import pandas as pd
import pandas_ta as pd_ta
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


class ElderReversion(Strategy):
    def init(self):
        # Calculate Bollinger Bands
        self.bb_upper, self.bb_middle, self.bb_lower = self.I(
            talib.BBANDS,
            self.data.Close,
            timeperiod=20,
            nbdevup=2,
            nbdevdn=2,
            matype=0,
            name=["BB_Upper", "BB_Middle", "BB_Lower"],
        )

        # Calculate Elder Force Index
        self.efi = self.I(
            pd_ta.force_index,
            close=self.data.Close,
            volume=self.data.Volume,
            length=1,
            name="EFI",
        )
        self.efi_signal = self.I(talib.EMA, self.efi, timeperiod=13, name="EFI_Signal")

        # Calculate ADX
        self.adx = self.I(
            talib.ADX,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=14,
            name="ADX",
        )

        # Calculate ATR for risk management
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=14,
            name="ATR",
        )

        print("🌙 Moon Dev Indicators Activated! ✨")

    def next(self):
        # Moon Dev progress tracker
        if len(self.data) % 100 == 0:
            print(
                f"🌕 Scanning Bar {len(self.data)} | Close: {self.data.Close[-1]:.2f} | ADX: {self.adx[-1]:.2f}"
            )

        # Entry Strategy
        if not self.position:
            entry_conditions = [
                self.data.Close[-1] < self.bb_lower[-1],  # Price below lower BB
                crossover(self.efi, self.efi_signal),  # EFI cross above signal
                self.adx[-1] < 25,  # Low trend strength
            ]

            if all(entry_conditions):
                # Risk management calculations
                entry_price = self.data.Close[-1]
                stop_loss = entry_price - 1.5 * self.atr[-1]
                risk_per_share = entry_price - stop_loss

                if risk_per_share <= 0:
                    print("⚠️ Invalid SL! Trade aborted.")
                    return

                # Position sizing with Moon Dev safety
                risk_percent = 0.01  # 1% equity risk
                risk_amount = self.equity * risk_percent
                position_size = int(round(risk_amount / risk_per_share))

                if position_size > 0:
                    take_profit = self.bb_middle[-1]
                    self.buy(size=position_size, sl=stop_loss, tp=take_profit)
                    print(
                        f"🚀 LONG {position_size} @ {entry_price:.2f} | SL: {stop_loss:.2f} 🌙"
                    )

        # Exit Strategy
        else:
            if crossover(self.efi_signal, self.efi):  # EFI cross below signal
                self.position.close()
                print(
                    f"🌑 Exit Signal @ {self.data.Close[-1]:.2f} | Profit: {self.position.pl_pct:.2%} ✨"
                )


# Data preparation
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)

# Clean and format data
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

# Launch Moon Dev Backtest
bt = Backtest(data, ElderReversion, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
