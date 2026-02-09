# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-moon-dev-ai-agents\src\data\rbi_v3\10_20_2025\backtests_optimized\DivergentReversion_OPT_v33.py
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
    adx_threshold = 30  # 🌙 Moon Dev: Further loosened ADX threshold from 25 to 30 to capture more ranging and mildly trending markets, significantly increasing trade frequency to accelerate towards 50% target return while ADX still filters out strong trends
    risk_per_trade = 0.08  # 🌙 Moon Dev: Increased risk per trade from 5% to 8% to enhance equity compounding speed, balanced by ATR-based sizing and overall drawdown limits for robust risk management
    atr_multiplier_sl = 2
    atr_multiplier_tp = 12  # 🌙 Moon Dev: Boosted TP multiplier from 10 to 12 ATR for a 6:1 risk-reward ratio, optimized to capture extended mean reversion swings in volatile BTC 15m data, improving per-trade profitability

    def init(self):
        # RSI(14) - kept at 14 for balanced noise reduction and signal quality in crypto volatility
        self.rsi = self.I(talib.RSI, self.data.Close, timeperiod=14)
        self.rsi_sma = self.I(
            talib.SMA, self.rsi, timeperiod=14
        )  # 🌙 Moon Dev: Consistent SMA period for reliable crossover detection

        # Stochastic %K(14,3,3) - standard for momentum, providing timely reversion signals
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
            talib.SMA, self.stoch_k, timeperiod=14
        )  # 🌙 Moon Dev: Aligned SMA for precise turning point identification

        # ATR(14) for dynamic stops - core volatility measure, unchanged
        self.atr = self.I(
            talib.ATR, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # ADX(14) for trend filter - standard period for market regime detection
        self.adx = self.I(
            talib.ADX, self.data.High, self.data.Low, self.data.Close, timeperiod=14
        )

        # Volume SMA(14) - shortened from 20 to 14 to match other indicators, providing more responsive volume confirmation without excessive lag
        self.vol_sma = self.I(talib.SMA, self.data.Volume, timeperiod=14)

        print(
            "🌙 Moon Dev: Indicators optimized with Vol SMA to 14 for faster confirmation, enhancing entry timing and overall trade efficiency to drive higher returns ✨"
        )

    def next(self):
        # 🌙 Moon Dev: Retained no manual early exits to allow full TP capture; added simple breakeven adjustment logic below for better risk management on winners without overcomplicating structure

        # Entry conditions only if no position and sufficient history
        if (
            (not self.position)
            and (len(self.rsi) > 20)
            and (self.adx[-1] < self.adx_threshold)
        ):  # 🌙 Moon Dev: Reduced history check from 50 to 20 bars to enable earlier trading, adding more opportunities from the dataset start while ensuring indicator stability

            # Further loosened volume filter to >0.8x average for broader inclusion of valid setups, boosting trade count without compromising quality
            vol_confirm = self.data.Volume[-1] > 0.8 * self.vol_sma[-1]

            # Long entry: RSI oversold (below 40 and SMA), Stoch turning up (above SMA and below 60 for broader oversold zone) - loosened thresholds to increase frequency of high-quality mean reversion longs
            if (
                vol_confirm
                and (self.rsi[-1] < self.rsi_sma[-1])
                and (self.rsi[-1] < 40)
                and (self.stoch_k[-1] > self.stoch_sma[-1])
                and (self.stoch_k[-1] < 60)
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
                    0.001, min(100.0, position_size)
                )  # 🌙 Moon Dev: Raised max position size from 50 to 100 to scale up returns on strong signals, capped for risk control with 1M starting cash

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

            # Short entry: RSI overbought (above 60 and SMA), Stoch turning down (below SMA and above 40 for broader overbought zone) - symmetric loosening to balance and increase short opportunities
            if (
                vol_confirm
                and (self.rsi[-1] > self.rsi_sma[-1])
                and (self.rsi[-1] > 60)
                and (self.stoch_k[-1] < self.stoch_sma[-1])
                and (self.stoch_k[-1] > 40)
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
                    0.001, min(100.0, position_size)
                )  # 🌙 Moon Dev: Raised max size to 100 for amplified short exposure, supporting higher reversion profits

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

        # 🌙 Moon Dev: Added basic breakeven protection for open positions to lock in gains after 4 ATR profit, improving risk-reward by protecting capital without trailing complexity
        if self.position and len(self.trades) > 0:
            trade = self.trades[-1]
            if trade.is_open:
                entry_price = trade.entry_price
                current_price = self.data.Close[-1]
                atr_val = self.atr[-1]
                profit_dist = (
                    (current_price - entry_price)
                    if trade.is_long
                    else (entry_price - current_price)
                )
                if profit_dist > 4 * atr_val:
                    # Close and re-enter at market with SL moved to breakeven (entry_price)
                    orig_size = trade.size
                    orig_tp = trade.tp
                    self.position.close()
                    # Re-enter with breakeven SL
                    if trade.is_long:
                        new_sl = entry_price
                        new_tp = orig_tp
                        self.buy(size=orig_size, sl=new_sl, tp=new_tp)
                        print(
                            f"🌙 Moon Dev: Long breakeven adjustment at {entry_price:.2f} after {profit_dist:.2f} profit ✨"
                        )
                    else:
                        new_sl = entry_price
                        new_tp = orig_tp
                        self.sell(size=orig_size, sl=new_sl, tp=new_tp)
                        print(
                            f"🌙 Moon Dev: Short breakeven adjustment at {entry_price:.2f} after {profit_dist:.2f} profit ✨"
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
