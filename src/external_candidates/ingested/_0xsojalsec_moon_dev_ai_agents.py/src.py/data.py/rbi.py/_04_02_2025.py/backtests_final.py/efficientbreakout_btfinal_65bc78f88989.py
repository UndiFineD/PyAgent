# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_02_2025\backtests_final\EfficientBreakout_BTFinal.py
import pandas as pd
import pandas_ta as ta
import talib
from backtesting import Backtest, Strategy


class EfficientBreakout(Strategy):
    risk_percent = 0.01  # 1% risk per trade 🌙

    def init(self):
        # Moon Dev Indicator Suite ✨
        self.ker = self.I(ta.efficiency_ratio, self.data.Close, length=10)

        # Bollinger Bands (upper band only needed for entry)
        self.bb_upper = self.I(
            lambda close: talib.BBANDS(close, 20, 2, 2, 0)[0], self.data.Close
        )

        # 20-period SMA for exit
        self.sma20 = self.I(talib.SMA, self.data.Close, timeperiod=20)

        # Chandelier Exit components
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 22)
        self.high_max = self.I(talib.MAX, self.data.High, 22)
        self.chandelier_exit = self.I(
            lambda high, atr: high - 3 * atr, self.high_max, self.atr
        )

        print("🌙✨ Moon Dev Indicator Suite initialized successfully!")

    def next(self):
        current_close = self.data.Close[-1]
        current_low = self.data.Low[-1]

        # Moon Dev Debug Prints 🌕
        # print(f"🌙 KER: {self.ker[-1]:.2f} | Close: {current_close:.2f} | BB_UPPER: {self.bb_upper[-1]:.2f}")

        if not self.position:
            # Entry Condition: KER > 0.8 and Close > Bollinger Upper Band
            if self.ker[-1] > 0.8 and current_close > self.bb_upper[-1]:
                sl_price = self.chandelier_exit[-1]
                risk_per_share = current_close - sl_price

                if risk_per_share > 0:
                    position_size = int(
                        round((self.equity * self.risk_percent) / risk_per_share)
                    )
                    if position_size > 0:
                        self.buy(size=position_size)
                        print(
                            f"🚀🌕 MOON DEV ENTRY: Long {position_size} units at {current_close:.2f}"
                        )
                        print(
                            f"   SL: {sl_price:.2f} | Risk: ${risk_per_share*position_size:.2f} 🌙"
                        )

        else:
            # Exit Conditions
            if current_low <= self.sma20[-1]:
                self.position.close()
                print(
                    f"🌙✨ SMA20 EXIT: {current_close:.2f} | PNL: {self.position.pl:.2f}"
                )
            elif current_low <= self.chandelier_exit[-1]:
                self.position.close()
                print(
                    f"🌙🚨 CHANDELIER STOP: {current_close:.2f} | PNL: {self.position.pl:.2f}"
                )


# Moon Dev Data Loading Protocol 🌙📊
try:
    data = pd.read_csv(
        "BTC-USD-15m.csv",  # Simplified path for portability
        parse_dates=["datetime"],
        index_col="datetime",
    )

    # Clean columns with Moon Dev precision
    data.columns = data.columns.str.strip().str.lower()
    data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
    data = data.rename(
        columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume",
        }
    )

    print("🌙📊 Moon Dev data preprocessing complete!")
    print(data.head(2))

except Exception as e:
    print(f"🌙🚨 MOON DEV DATA ERROR: {str(e)}")
    raise

# Launch Moon Dev Backtest Engine 🚀
try:
    bt = Backtest(data, EfficientBreakout, cash=1_000_000, commission=0.002)
    stats = bt.run()

    print("\n🌕🌕🌕 MOON DEV QUANT REPORT 🌕🌕🌕")
    print(stats)
    print(stats._strategy)

except Exception as e:
    print(f"🌙🚨 MOON DEV BACKTEST ERROR: {str(e)}")
    raise
