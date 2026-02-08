# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\04_10_2025\backtests\LiquidationReversal_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy
from backtesting.lib import crossover, crossunder

# Load and preprocess data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")

# Clean and format columns 🌙
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


class LiquidationReversal(Strategy):
    def init(self):
        # Volatility and momentum indicators 🌊
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.rsi = self.I(talib.RSI, self.data.Close, 14)

        # Price pattern detection 🕯️
        self.bullish_engulf = self.I(
            talib.CDLENGULFING,
            self.data.Open,
            self.data.High,
            self.data.Low,
            self.data.Close,
        )
        self.hammer = self.I(
            talib.CDLHAMMER,
            self.data.Open,
            self.data.High,
            self.data.Low,
            self.data.Close,
        )

        # Swing detection 🌗
        self.swing_low = self.I(talib.MIN, self.data.Low, 20)

        print("🌙 Lunar indicators activated! Tracking cosmic patterns... 🌌")

    def next(self):
        if self.position:
            return  # Maintain existing position

        # Extract current market conditions 🧮
        entry_price = self.data.Close[-1]
        funding_negative = self.data.fundingrate[-1] < 0
        in_liquidation_zone = self.data.liquidationcluster[-1] == 1
        rsi_oversold = self.rsi[-1] < 30
        bullish_signal = self.bullish_engulf[-1] == 100 or self.hammer[-1] == 100

        # Cosmic entry alignment conditions 🌠
        if all([funding_negative, in_liquidation_zone, rsi_oversold, bullish_signal]):
            # Risk management calculations ⚖️
            sl_price = self.swing_low[-1]
            risk_per_share = entry_price - sl_price

            if risk_per_share <= 0:
                print("🚨 Cosmic anomaly! SL >= entry price. Aborting launch. 🚨")
                return

            # Position sizing calculation 🌕
            risk_capital = self.equity * 0.01  # 1% risk
            position_size = int(round(risk_capital / risk_per_share))

            if position_size <= 0:
                print(f"🌙 Stardust shortage: {position_size} units available. Needs more cosmic dust! 🌌")
                return

            # Execute trade with celestial stops 🌌
            tp_price = entry_price + 1.5 * self.atr[-1]
            self.buy(size=position_size, sl=sl_price, tp=tp_price, tag="LunarReversal")

            print(
                f"🚀🌕 MOONSHOT INITIATED! Entry: {entry_price:.2f} | "
                f"Size: {position_size} | SL: {sl_price:.2f} | TP: {tp_price:.2f}"
            )

    def notify_trade_exit(self, exit_price: float, size: float, is_loss: bool):
        if is_loss:
            print(f"💥 COSMIC COLLISION! Position exited at {exit_price:.2f} (Loss) 🌑")
        else:
            print(f"🎇 STELLAR PROFIT! Harvested {size} units at {exit_price:.2f} 🌠✨")


# Launch backtest 🚀
bt = Backtest(data, LiquidationReversal, cash=1_000_000, commission=0.002)
stats = bt.run()

# Display cosmic performance report 📜
print("\n" + "=" * 50)
print("🌙 MOON DEV BACKTEST RESULTS 🌙")
print("=" * 50)
print(stats)
print("\n✨ STRATEGY PERFORMANCE BREAKDOWN ✨")
print(stats._strategy)
