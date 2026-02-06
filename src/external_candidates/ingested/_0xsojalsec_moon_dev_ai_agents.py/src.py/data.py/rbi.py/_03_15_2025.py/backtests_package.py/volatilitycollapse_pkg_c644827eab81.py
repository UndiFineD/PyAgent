# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_15_2025\backtests_package\VolatilityCollapse_PKG.py
# 🌙 MOON DEV BACKTESTING IMPLEMENTATION FOR VOLATILITYCOLLAPSE STRATEGY

import pandas as pd
import talib
from backtesting import Backtest, Strategy

# 🚀 DATA PREPARATION WITH MOON DEV SANITIZATION
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
)

# Clean and format columns according to Moon Dev standards 🌙
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
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


class VolatilityCollapse(Strategy):
    # 🌗 STRATEGY PARAMETERS
    atr_period = 14
    donchian_period = 20
    volume_ma_period = 20
    risk_per_trade = 0.01  # 1% risk per trade

    def init(self):
        # 🌌 INDICATOR CALCULATION USING TALIB
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=self.atr_period,
        )
        self.donchian_upper = self.I(
            talib.MAX, self.data.High, timeperiod=self.donchian_period
        )
        self.donchian_lower = self.I(
            talib.MIN, self.data.Low, timeperiod=self.donchian_period
        )
        self.volume_ma = self.I(
            talib.SMA, self.data.Volume, timeperiod=self.volume_ma_period
        )

        # 🌠 Calculate inverse volatility (normalized)
        self.inverse_vol = self.I(lambda x: 100 / x, self.atr)

    def next(self):
        # 🌕 MOON DEV TRADING LOGIC
        price = self.data.Close[-1]
        current_vol = self.inverse_vol[-1]
        current_volume = self.data.Volume[-1]
        volume_ma = self.volume_ma[-1]

        # 🌑 VOLATILITY COLLAPSE CONDITIONS
        volatility_cond = current_vol > 2.0  # Inverse volatility threshold
        volume_cond = current_volume < 0.5 * volume_ma  # Volume collapse
        long_break = price > self.donchian_upper[-1]  # Breakout up
        short_break = price < self.donchian_lower[-1]  # Breakout down

        # 💰 RISK MANAGEMENT CALCULATIONS
        atr_value = self.atr[-1]
        stop_pct = atr_value * 1.5
        tp_pct = atr_value * 3

        if not self.position:
            # 🌙 LONG ENTRY SIGNAL
            if volatility_cond and volume_cond and long_break:
                risk_amount = self.risk_per_trade * self.equity
                stop_loss = price - stop_pct
                risk_per_share = price - stop_loss
                position_size = int(round(risk_amount / risk_per_share))

                if position_size > 0:
                    self.buy(size=position_size, sl=stop_loss, tp=price + tp_pct)
                    print(
                        f"🌕✨ MOON DEV LONG SIGNAL! Entry: {price:.2f}, Size: {position_size} BTC, Risk: {risk_per_share:.2f} USD"
                    )

            # 🌑 SHORT ENTRY SIGNAL
            elif volatility_cond and volume_cond and short_break:
                risk_amount = self.risk_per_trade * self.equity
                stop_loss = price + stop_pct
                risk_per_share = stop_loss - price
                position_size = int(round(risk_amount / risk_per_share))

                if position_size > 0:
                    self.sell(size=position_size, sl=stop_loss, tp=price - tp_pct)
                    print(
                        f"🌑✨ MOON DEV SHORT SIGNAL! Entry: {price:.2f}, Size: {position_size} BTC, Risk: {risk_per_share:.2f} USD"
                    )


# 🚀 BACKTEST EXECUTION WITH MOON DEV SETTINGS
bt = Backtest(data, VolatilityCollapse)
