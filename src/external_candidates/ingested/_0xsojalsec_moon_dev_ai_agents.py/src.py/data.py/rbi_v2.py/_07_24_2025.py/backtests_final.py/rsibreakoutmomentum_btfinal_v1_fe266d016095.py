# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v2\07_24_2025\backtests_final\RsiBreakoutMomentum_BTFinal_v1.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy


class RsiBreakoutMomentum(Strategy):
    rsi_period = 50
    rsi_oversold = 30
    rsi_overbought = 70
    ma_period = 20
    atr_period = 20
    atr_stop_multiplier = 0.2
    risk_per_trade = 0.01
    max_positions = 3
    breakeven_atr_multiple = 2

    def init(self):
        # Clean and prepare data
        data = self.data.df.copy()
        data.columns = data.columns.str.strip().str.lower()
        data = data.drop(
            columns=[col for col in data.columns if "unnamed" in col.lower()]
        )

        # Calculate indicators
        self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_period)
        self.ma = self.I(talib.SMA, self.data.Close, self.ma_period)
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, self.atr_period
        )

        # Track entry conditions
        self.entry_trigger_high = None
        self.active_positions = 0
        self.entry_price = None

    def next(self):
        current_rsi = self.rsi[-1]
        current_close = self.data.Close[-1]
        current_high = self.data.High[-1]

        # Moon Dev debug prints 🌙
        print(
            f"🌙 Current RSI: {current_rsi:.2f} | Close: {current_close:.2f} | Active Positions: {self.active_positions}"
        )

        # Check for new entry conditions
        if self.active_positions < self.max_positions:
            if current_rsi < self.rsi_oversold and pd.notna(current_rsi):
                self.entry_trigger_high = current_high
                print(
                    f"✨ RSI Oversold! Watching for breakout above {self.entry_trigger_high:.2f}"
                )

            if (
                self.entry_trigger_high is not None
                and current_high > self.entry_trigger_high
            ):
                # Calculate position size based on risk
                atr_value = self.atr[-1]
                stop_loss = current_close - (atr_value * self.atr_stop_multiplier)
                risk_amount = self.equity * self.risk_per_trade
                risk_per_share = current_close - stop_loss
                position_size = int(round(risk_amount / risk_per_share))

                if position_size > 0:
                    self.buy(size=position_size)
                    self.entry_price = current_close
                    self.active_positions += 1
                    print(
                        f"🚀 ENTRY LONG | Size: {position_size} | Price: {current_close:.2f} | SL: {stop_loss:.2f}"
                    )
                    self.entry_trigger_high = None

        # Manage open positions
        for trade in self.trades:
            if trade.is_long:
                current_atr = self.atr[-1]
                current_ma = self.ma[-1]

                # Check for exit conditions
                if self.data.Low[-1] <= current_ma:
                    trade.close()
                    self.active_positions -= 1
                    print(
                        f"🌑 EXIT MA Touch | Price: {current_close:.2f} | PnL: {trade.pl:.2f}"
                    )
                elif self.rsi[-1] > self.rsi_overbought:
                    trade.close()
                    self.active_positions -= 1
                    print(
                        f"🌕 EXIT Overbought | Price: {current_close:.2f} | PnL: {trade.pl:.2f}"
                    )
                else:
                    # Trail stop to breakeven after 2x ATR move
                    breakeven_level = self.entry_price + (
                        current_atr * self.breakeven_atr_multiple
                    )
                    if current_close > breakeven_level and trade.sl < self.entry_price:
                        trade.sl = self.entry_price
                        print(f"🛡️ Trail Stop to Breakeven at {self.entry_price:.2f}")


if __name__ == "__main__":
    data = pd.read_csv(
        "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
    )
    data.columns = data.columns.str.strip().str.lower()
    data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])

    # Ensure proper column mapping and datetime index
    data = data.rename(
        columns={
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume",
        }
    )
    data = data.set_index(pd.to_datetime(data["datetime"]))

    # Increase initial cash to handle BTC prices
    bt = Backtest(
        data, RsiBreakoutMomentum, commission=0.002, exclusive_orders=True, cash=100000
    )
    stats = bt.run()
    print(stats)
    print(stats._strategy)
