# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi\03_28_2025\backtests_package\DynamicTrendSync_PKG.py
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Clean and prepare data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
data = pd.read_csv(data_path, parse_dates=["datetime"], index_col="datetime")
data.columns = data.columns.str.strip().str.lower()
data = data.drop(columns=[col for col in data.columns if "unnamed" in col.lower()])
data = data.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }
)


class DynamicTrendSync(Strategy):
    risk_pct = 0.01  # 1% risk per trade
    atr_multiplier = 2

    def init(self):
        self.ema50 = self.I(talib.EMA, self.data.Close, timeperiod=50, name="EMA50 🌙")
        self.ema200 = self.I(talib.EMA, self.data.Close, timeperiod=200, name="EMA200 🌕")
        self.adx = self.I(
            talib.ADX,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=14,
            name="ADX 📈",
        )
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14, name="RSI 📉")
        self.atr = self.I(
            talib.ATR,
            self.data.High,
            self.data.Low,
            self.data.Close,
            timeperiod=14,
            name="ATR ⚡",
        )

    def next(self):
        price = self.data.Close[-1]

        # Moon Dev Debug Dashboard
        # print(f"🌙✨ {self.data.index[-1]} | Price: {price:.2f} | EMA50: {self.ema50[-1]:.2f} | EMA200: {self.ema200[-1]:.2f}")

        if not self.position:
            # Entry Logic 🌟
            bullish_cross = self.ema50[-2] < self.ema200[-2] and self.ema50[-1] > self.ema200[-1]
            if bullish_cross and self.adx[-1] > 25 and self.adx[-1] > self.adx[-2]:
                risk_amount = self.equity * self.risk_pct
                atr_value = self.atr[-1]
                est_entry = self.data.Close[-1]  # Estimate entry at next open
                sl_price = est_entry - (self.atr_multiplier * atr_value)

                if sl_price <= 0:
                    print(f"🌙💥 Invalid SL: {sl_price:.2f} - Trade Canceled")
                    return

                risk_per_share = est_entry - sl_price
                if risk_per_share <= 0:
                    print(f"🌙💥 Risk/Share: {risk_per_share:.2f} - Trade Canceled")
                    return

                position_size = int(round(risk_amount / risk_per_share))

                if position_size > 0:
                    self.buy(size=position_size, sl=sl_price)
                    print(
                        f"🚀🌙 MOON DEV LONG ENTRY ✨ | Size: {position_size} | Est.Entry: {est_entry:.2f} | SL: {sl_price:.2f} | RSI: {self.rsi[-1]:.1f}"
                    )

        else:
            # Exit Logic 🛑
            exit_rsi = self.rsi[-2] > 70 and self.rsi[-1] <= 70
            exit_ema = self.ema50[-2] > self.ema200[-2] and self.ema50[-1] < self.ema200[-1]

            if exit_rsi or exit_ema:
                self.position.close()
                reason = "RSI <70 🔻" if exit_rsi else "EMA Cross 🔀"
                print(
                    f"🌙✨ PROFIT CAPTURED | {reason} | Exit Price: {price:.2f} | P/L: {self.position.pl_pct:.1f}% 🌟"
                )


# Execute backtest with Moon Dev settings 🌕
bt = Backtest(data, DynamicTrendSync, cash=1_000_000, commission=0.002)
stats = bt.run()
print(stats)
print(stats._strategy)
