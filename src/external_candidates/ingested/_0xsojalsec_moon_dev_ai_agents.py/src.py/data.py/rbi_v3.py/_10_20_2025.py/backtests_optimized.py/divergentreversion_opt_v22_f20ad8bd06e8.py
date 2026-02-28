# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v22.py
import numpy as np
import pandas as pd
import talib
from backtesting import Backtest, Strategy

# Load data
data_path = "/Users/md/Dropbox/dev/github/moon-dev-ai-agents-for-trading/src/data/rbi/BTC-USD-15m.csv"
df = pd.read_csv(data_path)

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# Drop any unnamed columns
df = df.drop(columns=[col for col in df.columns if "unnamed" in col.lower()])

# Set datetime as index
df = df.set_index(pd.to_datetime(df["datetime"]))

# Rename columns properly
df.rename(
    columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    },
    inplace=True,
)

# Sort index to ensure chronological order
df = df.sort_index()

# Ensure required columns
print("🌙 Moon Dev: Data loaded and cleaned. Shape:", df.shape)
print("Columns:", df.columns.tolist())


class DivergentReversion(Strategy):
    adx_threshold = 25  # 🌙 Moon Dev: Loosened ADX threshold back to 25 from 20 to allow more trades in mildly trending/ranging markets while maintaining filter
    risk_per_trade = 0.02  # 🌙 Moon Dev: Increased risk per trade from 1% to 2% to amplify returns while still conservative for risk management
    atr_multiplier_sl = 2
    atr_multiplier_tp = 7  # 🌙 Moon Dev: Increased TP multiplier from 6 to 7 for improved 1:3.5 RR to capture larger reversions and boost overall profitability

    def init(self):
        # RSI(14) - shortened period from 20 to 14 for faster, more responsive mean reversion signals
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.rsi_sma = self.I(
            talib.SMA, self.rsi, timeperiod=14
        )  # 🌙 Moon Dev: Matched SMA period to RSI for tighter alignment

        # Stochastic %K(14,3,3) - changed to standard periods from (8,1,1) for smoother, less noisy signals while retaining sensitivity
        self.stoch_k, _ = self.I(
            talib.STOCH,
            self.data.High,
            self.data.Low,
            self.data.Close,
            fastk_period=14,
            slowk_period=3,
            slowd_period=3,
        )
        self.stoch_sma = self.I(
            talib.SMA, self.stoch_k, timeperiod=10
        )  # 🌙 Moon Dev: Shortened SMA from 20 to 10 for quicker divergence detection without excessive whipsaws

        # ATR(14) for dynamic stops - unchanged for consistency
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # ADX(14) for trend filter - unchanged period
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # Volume SMA(14) - shortened to match other indicators for more current volume confirmation
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=14)

        print(
            "🌙 Moon Dev: Indicators initialized with tuned periods and volume filter for enhanced signal quality ✨"
        )

    def next(self):
        # 🌙 Moon Dev: Stricter exit logic to avoid premature closes, only trigger on strong opposite extremes to let winners run longer
        if self.position.is_long:
            # Long exit only on strong overbought reversion: RSI overbought crossing down OR Stoch oversold crossing up
            if (self.rsi[-1] > 65 and self.rsi[-1] < self.rsi_sma[-1]) or (
                self.stoch_k[-1] < 35 and self.stoch_k[-1] > self.stoch_sma[-1]
            ):
                self.position.close()
                print(
                    f"🌙 Moon Dev: Long Exit on Strong Reversion Signal at {self.data.Close[-1]:.2f} 🚀"
                )
            return

        if self.position.is_short:
            # Short exit only on strong oversold reversion: RSI oversold crossing up OR Stoch overbought crossing down
            if (self.rsi[-1] < 35 and self.rsi[-1] > self.rsi_sma[-1]) or (
                self.stoch_k[-1] > 65 and self.stoch_k[-1] < self.stoch_sma[-1]
            ):
                self.position.close()
                print(
                    f"🌙 Moon Dev: Short Exit on Strong Reversion Signal at {self.data.Close[-1]:.2f} 🚀"
                )
            return

        # 🌙 Moon Dev: Retained symmetric entries but added absolute RSI thresholds for higher quality oversold/overbought setups to filter weak signals
        # Entry conditions only if no position and sufficient history
        if (
            (not self.position)
            and (len(self.rsi) > 20)
            and (self.adx[-1] < self.adx_threshold)
        ):

            # Enhanced volume filter: require 1.5x average volume for stronger confirmation of move
            vol_confirm = self.data.Volume[-1] > 1.5 * self.vol_sma[-1]

            # Long entry: RSI oversold (below SMA and <35), Stoch turning up (above SMA) - improved divergence with threshold filter
            if (
                vol_confirm
                and (self.rsi[-1] < self.rsi_sma[-1])
                and (self.rsi[-1] < 35)
                and (self.stoch_k[-1] > self.stoch_sma[-1])
            ):
                entry_price = self.data.Close[-1]
                atr_val = self.atr[-1]
                sl_price = entry_price - (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price + (self.atr_multiplier_tp * atr_val)
                risk_distance = entry_price - sl_price

                equity = self.equity
                risk_amount = equity * self.risk_per_trade
                position_size = risk_amount / risk_distance
                position_size = max(
                    0.001, min(10.0, position_size)
                )  # 🌙 Moon Dev: Increased max size from 1.0 to 10.0 to allow larger positions with 1M cash, enabling higher returns on good setups

                if (
                    position_size > 0
                    and not np.isnan(sl_price)
                    and not np.isnan(tp_price)
                    and sl_price < entry_price < tp_price
                ):
                    self.buy(
                        size=position_size, limit=entry_price, sl=sl_price, tp=tp_price
                    )
                    print(
                        f"🌙 Moon Dev: Long Entry at {entry_price:.2f}, Size: {position_size:.4f}, SL: {sl_price:.2f}, TP: {tp_price:.2f} ✨"
                    )
                else:
                    print(
                        "🌙 Moon Dev: Invalid long position size or SL/TP levels, skipping entry ⚠️"
                    )
                return

            # Short entry: RSI overbought (above SMA and >65), Stoch turning down (below SMA) - improved divergence with threshold filter
            if (
                vol_confirm
                and (self.rsi[-1] > self.rsi_sma[-1])
                and (self.rsi[-1] > 65)
                and (self.stoch_k[-1] < self.stoch_sma[-1])
            ):
                entry_price = self.data.Close[-1]
                atr_val = self.atr[-1]
                sl_price = entry_price + (self.atr_multiplier_sl * atr_val)
                tp_price = entry_price - (self.atr_multiplier_tp * atr_val)
                risk_distance = sl_price - entry_price

                equity = self.equity
                risk_amount = equity * self.risk_per_trade
                position_size = risk_amount / risk_distance
                position_size = max(
                    0.001, min(10.0, position_size)
                )  # 🌙 Moon Dev: Increased max size from 1.0 to 10.0 for symmetric larger short positions

                if (
                    position_size > 0
                    and not np.isnan(sl_price)
                    and not np.isnan(tp_price)
                    and tp_price < entry_price < sl_price
                ):
                    self.sell(
                        size=position_size, limit=entry_price, sl=sl_price, tp=tp_price
                    )
                    print(
                        f"🌙 Moon Dev: Short Entry at {entry_price:.2f}, Size: {position_size:.4f}, SL: {sl_price:.2f}, TP: {tp_price:.2f} ✨"
                    )
                else:
                    print(
                        "🌙 Moon Dev: Invalid short position size or SL/TP levels, skipping entry ⚠️"
                    )


# Run backtest
bt = Backtest(
    df,
    DivergentReversion,
    cash=1000000,
    commission=0.002,
    exclusive_orders=True,
    trade_on_close=True,
)

print("🌙 Moon Dev: Running backtest... 🚀")
stats = bt.run()
print(stats)
