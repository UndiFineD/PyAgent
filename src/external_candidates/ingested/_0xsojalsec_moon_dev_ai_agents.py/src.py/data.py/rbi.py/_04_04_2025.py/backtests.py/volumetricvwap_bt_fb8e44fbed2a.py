# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_04_2025\backtests\VolumetricVwap_BT.py
# Required imports
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover


class VolumetricVwap(Strategy):
    # Strategy parameters
    short_vwap_window = 20  # 5-min equivalent (adjust based on timeframe)
    long_vwap_window = 80  # 1-hour equivalent
    volume_lookback = 90
    atr_period = 14
    risk_pct = 0.01  # 1% risk per trade

    def init(self):
        # Clean and prepare data
        self.data.df.columns = self.data.df.columns.str.strip().str.lower()
        self.data.df = self.data.df.drop(
            columns=[col for col in self.data.df.columns if "unnamed" in col]
        )

        # Calculate indicators
        typical_price = (self.data.High + self.data.Low + self.data.Close) / 3

        # VWAP calculations
        def calc_vwap(price, volume, window):
            return (price * volume).rolling(window).sum() / volume.rolling(window).sum()

        self.vwap_short = self.I(
            calc_vwap,
            typical_price,
            self.data.Volume,
            self.short_vwap_window,
            name="VWAP_5m",
        )
        self.vwap_long = self.I(
            calc_vwap,
            typical_price,
            self.data.Volume,
            self.long_vwap_window,
            name="VWAP_1h",
        )

        # Volume percentile
        self.volume_pct = self.I(
            lambda: self.data.Volume.rolling(self.volume_lookback).quantile(0.9),
            name="Volume_Pct_90",
        )

        # ATR calculation
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            self.atr_period,
            name="ATR_14",
        )

        print("🌙 Moon Dev Indicators Initialized! ✨")

    def next(self):
        if self.position:
            return  # No pyramiding

        # Get current values
        current_close = self.data.Close[-1]
        current_volume = self.data.Volume[-1]
        volume_pct = self.volume_pct[-1]
        atr_value = self.atr[-1]

        # Entry conditions
        vwap_cross = crossover(self.vwap_short, self.vwap_long)
        volume_trigger = current_volume > volume_pct if volume_pct else False

        if vwap_cross and volume_trigger:
            # Risk management calculations
            stop_loss = current_close - 2 * atr_value
            take_profit = current_close + 1.5 * atr_value

            # Position sizing
            risk_amount = self.equity * self.risk_pct
            risk_per_share = current_close - stop_loss
            position_size = int(round(risk_amount / abs(risk_per_share)))

            if position_size > 0:
                # Execute trade with OCO orders
                self.buy(
                    size=position_size,
                    sl=stop_loss,
                    tp=take_profit,
                    tag="🌙 Moon Dev Entry!",
                )

                print(f"🚀✨ Lunar Launch! Long {position_size} @ {current_close:.2f}")
                print(
                    f"   🌑 Stop Loss: {stop_loss:.2f} | 🌕 Take Profit: {take_profit:.2f}"
                )


# Data preparation
data = pd.read_csv(
    "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv",
    parse_dates=["datetime"],
    index_col="datetime",
)
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

# Run backtest
bt = Backtest(data, VolumetricVwap, cash=1_000_000, commission=0.002)
stats = bt.run()

# Print results
print("\n🌕🌖🌗🌘🌑🌒🌓🌔🌕")
print("Moon Dev Strategy Complete! Full Lunar Report:")
print(stats)
print(stats._strategy)
