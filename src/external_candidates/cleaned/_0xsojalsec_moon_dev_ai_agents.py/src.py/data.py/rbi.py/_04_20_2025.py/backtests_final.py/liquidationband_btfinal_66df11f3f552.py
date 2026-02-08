# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_20_2025\backtests_final\LiquidationBand_BTFinal.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class LiquidationBand(Strategy):
    bbw_threshold = 0.5
    risk_percent = 0.01
    cluster_buffer = 0.01

    def init(self):
        close = self.data.Close
        high = self.data.High
        low = self.data.Low

        # Bollinger Bands components
        self.middle_band = self.I(talib.SMA, close, timeperiod=20, name="Middle Band")
        std_dev = self.I(talib.STDDEV, close, timeperiod=20, nbdev=1, name="StdDev")
        self.upper_band = self.I(lambda: self.middle_band + 2 * std_dev, name="Upper Band")
        self.lower_band = self.I(lambda: self.middle_band - 2 * std_dev, name="Lower Band")
        self.bbw = self.I(lambda: (self.upper_band - self.lower_band) / self.middle_band, name="BBW")

        # Liquidation clusters (swing high/low)
        self.swing_high = self.I(talib.MAX, high, timeperiod=20, name="Swing High")
        self.swing_low = self.I(talib.MIN, low, timeperiod=20, name="Swing Low")

        # Volume analysis
        self.volume_ma = self.I(talib.SMA, self.data.Volume, timeperiod=20, name="Volume MA")

    def next(self):
        if len(self.data) < 20:
            return

        current_close = self.data.Close[-1]
        current_bbw = self.bbw[-1]
        bullish_cluster = self.swing_low[-1]
        bearish_cluster = self.swing_high[-1]

        # Entry Logic
        if not self.position:
            # Long Entry Conditions
            if (
                current_bbw < self.bbw_threshold
                and current_close <= bullish_cluster * (1 + self.cluster_buffer)
                and current_close >= bullish_cluster * (1 - self.cluster_buffer)
            ):
                stop_loss = bullish_cluster * (1 - self.cluster_buffer)
                risk_per_trade = current_close - stop_loss
                if risk_per_trade > 0:
                    size = int(round((self.equity * self.risk_percent) / risk_per_trade))
                    self.buy(size=size, sl=stop_loss, tag="🌙 LONG ENTRY")
                    print(
                        f"🌙 MOON DEV LONG SIGNAL! 🚀 | Price: {current_close:.2f} | Cluster: {bullish_cluster:.2f} | Size: {size}"
                    )

            # Short Entry Conditions
            elif (
                current_bbw < self.bbw_threshold
                and current_close <= bearish_cluster * (1 + self.cluster_buffer)
                and current_close >= bearish_cluster * (1 - self.cluster_buffer)
            ):
                stop_loss = bearish_cluster * (1 + self.cluster_buffer)
                risk_per_trade = stop_loss - current_close
                if risk_per_trade > 0:
                    size = int(round((self.equity * self.risk_percent) / risk_per_trade))
                    self.sell(size=size, sl=stop_loss, tag="🌙 SHORT ENTRY")
                    print(
                        f"🌙 MOON DEV SHORT SIGNAL! 🚨 | Price: {current_close:.2f} | Cluster: {bearish_cluster:.2f} | Size: {size}"
                    )

        # Exit Logic
        if self.position:
            # Volume Surge Exit
            current_volume = self.data.Volume[-1]
            if current_volume > 2 * self.volume_ma[-1]:
                if (self.position.is_long and current_close < self.data.Close[-2]) or (
                    self.position.is_short and current_close > self.data.Close[-2]
                ):
                    self.position.close()
                    print(
                        f"🌙 VOLUME SURGE EXIT! {'📉' if self.position.is_long else '📈'} | Price: {current_close:.2f}"
                    )

            # Mid-Band Exit
            if (self.position.is_long and current_close < self.middle_band[-1]) or (
                self.position.is_short and current_close > self.middle_band[-1]
            ):
                self.position.close()
                print(f"🌙 MID-BAND EXIT! 🎯 | Price: {current_close:.2f}")


# Data handling
data_path = "/Users/md/Dropbox/dev/github"
