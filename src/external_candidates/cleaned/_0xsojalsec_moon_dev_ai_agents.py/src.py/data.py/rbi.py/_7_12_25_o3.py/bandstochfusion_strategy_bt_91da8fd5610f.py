# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\7_12_25_o3\BandStochFusion_strategy_bt.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# 🌙 Moon Dev BandStochFusion strategy – BB + Stochastic oscillator combo 🎯

DATA_PATH = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"


class BandStochFusionStrategy(Strategy):
    def init(self):
        print("🌙 Moon Dev initializing BandStochFusion indicators… 🚀")
        # Bollinger Bands
        self.bb_upper, self.bb_middle, self.bb_lower = (
            self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[0], self.data.Close),
            self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[1], self.data.Close),
            self.I(lambda c: talib.BBANDS(c, 20, 2, 2)[2], self.data.Close),
        )
        # Stochastic Oscillator (%K, %D)
        self.stoch_k = self.I(
            lambda h, l, c: talib.STOCH(h, l, c, 14, 3, 0, 3, 0)[0],
            self.data.High,
            self.data.Low,
            self.data.Close,
        )
        self.stoch_d = self.I(
            lambda h, l, c: talib.STOCH(h, l, c, 14, 3, 0, 3, 0)[1],
            self.data.High,
            self.data.Low,
            self.data.Close,
        )
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)

    def next(self):
        price = self.data.Close[-1]
        atr_val = self.atr[-1]
        k = self.stoch_k[-1]
        d = self.stoch_d[-1]
        upper_band = self.bb_upper[-1]
        lower_band = self.bb_lower[-1]
        middle_band = self.bb_middle[-1]

        # Manage existing position
        if self.position:
            if self.position.is_long:
                # Exit when price touches MB or Stoch leaves overbought
                if price >= middle_band or k > 80:
                    print("🌙 Moon Dev BandStochFusion exiting LONG ✨")
                    self.position.close()
            else:  # short
                if price <= middle_band or k < 20:
                    print("🌙 Moon Dev BandStochFusion exiting SHORT ✨")
                    self.position.close()
            return

        # Long setup: price below lower band & stoch oversold with bullish cross
        if price <= lower_band and k < 20 and k > d:
            sl = price - 1.5 * atr_val
            tp = middle_band
            self._enter("buy", sl, tp)
            return

        # Short setup: price above upper band & stoch overbought with bearish cross
        if price >= upper_band and k > 80 and k < d:
            sl = price + 1.5 * atr_val
            tp = middle_band
            self._enter("sell", sl, tp)

    def _enter(self, side: str, sl: float, tp: float):
        risk_per_unit = abs(self.data.Close[-1] - sl)
        if risk_per_unit <= 0:
            return
        size = int(round((self.equity * 0.01) / risk_per_unit))
        if size <= 0:
            return
        print(f"🌙 Moon Dev {side.upper()} BandStochFusion entry! size={size} 🚀")
        if side == "buy":
            self.buy(size=size, sl=sl, tp=tp)
        else:
            self.sell(size=size, sl=sl, tp=tp)


if __name__ == "__main__":
    print("🌙 Moon Dev loading BTC-USD for BandStochFusion… 📈")
    data = pd.read_csv(DATA_PATH, parse_dates=["datetime"], index_col="datetime")
    data.columns = data.columns.str.strip().str.title()
    data = data.rename(
        columns={
            "Open": "Open",
            "High": "High",
            "Low": "Low",
            "Close": "Close",
            "Volume": "Volume",
        }
    )
    bt = Backtest(
        data,
        BandStochFusionStrategy,
        cash=1_000_000,
        margin=1,
        commission=0.001,
    )
    stats = bt.run()
    print("🌙 Moon Dev BandStochFusion backtest done! ✨\n", stats)
