# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_15_2025\backtests\PatternReversal_BT.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy


# Moon Dev Data Preparation 🌙✨
def prepare_data(filepath):
    data = pd.read_csv(filepath)
    # Clean column names
    data.columns = data.columns.str.strip().str.lower()
    # Drop unnamed columns
    data = data.drop(columns=[col for col in data.columns if "unnamed" in col])
    # Proper column mapping
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
    return data


# Moon Dev PatternReversal Strategy 🚀📈
class PatternReversal(Strategy):
    neckline = None
    head_low = None

    def init(self):
        # Moon Dev Indicators 🌙📊
        self.atr = self.I(talib.ATR, self.data.High, self.data.Low, self.data.Close, 14)
        self.rsi = self.I(talib.RSI, self.data.Close, 14)
        self.swing_high = self.I(talib.MAX, self.data.High, 20)
        self.swing_low = self.I(talib.MIN, self.data.Low, 20)

    def next(self):
        # Pattern Detection Logic 🕵️♂️
        if len(self.data) < 100:
            return

        # Find potential head (lowest low in last 50 periods)
        min_idx = self.data.Low.iloc[-50:].argmin()
        head_idx = len(self.data) - 50 + min_idx
        self.head_low = self.data.Low.iloc[head_idx]

        # Find shoulders and neckline 🌙📉
        left_shoulder = self.find_shoulder(head_idx, -1)
        right_shoulder = self.find_shoulder(head_idx, 1)

        if left_shoulder and right_shoulder:
            # Calculate neckline from swing highs
            neck_start = self.swing_high[left_shoulder]
            neck_end = self.swing_high[right_shoulder]
            self.neckline = max(neck_start, neck_end)

            # Entry Conditions 🌙🚀
            if (
                self.data.Close[-1] > self.neckline
                and self.rsi[-1] > 50
                and self.data.Volume[-1] > self.data.Volume[-20:].mean()
            ):

                # Risk Management 🛡️
                atr_value = self.atr[-1]
                stop_loss = self.neckline - 2 * atr_value
                risk_amount = 0.01 * self.equity  # 1% risk

                # Moon Dev Position Sizing 🌙🧮
                risk_per_share = self.data.Close[-1] - stop_loss
                if risk_per_share > 0:
                    position_size = int(round(risk_amount / risk_per_share))
                    self.buy(size=position_size, sl=stop_loss)
                    print(f"🌙🚀 MOON DEV ENTRY at {self.data.Close[-1]:.2f}")
                    print(
                        f"Size: {position_size} | SL: {stop_loss:.2f} | TP: {self.neckline + (self.neckline - self.head_low):.2f}"
                    )

    def find_shoulder(self, head_idx, direction):
        # Shoulder detection logic 👥
        step = -1 if direction == -1 else 1
        for i in range(head_idx + direction, head_idx + (direction * 50), step):
            if 0 < i < len(self.data):
                if self.data.Low[i] > self.head_low:
                    return i
        return None


# Moon Dev Backtest Execution 🌙💻
if __name__ == "__main__":
    data = prepare_data(
        "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
    )
    bt = Backtest(data, PatternReversal, cash=1_000_000)
    stats = bt.run()
    print("\n🌙✨ MOON DEV FINAL STATS ✨🌙")
    print(stats)
    print(stats._strategy)
