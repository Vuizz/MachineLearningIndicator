# Import necessary libraries and load data
import pandas as pd
from ta.volatility import BollingerBands
from ta.momentum import RSIIndicator, StochasticOscillator, WilliamsRIndicator, ROCIndicator, RelativeVigorIndexIndicator, UltimateOscillator
from ta.trend import MACD, AverageTrueRange, IchimokuIndicator, AroonIndicator
from ta.volume import OnBalanceVolumeIndicator, ChaikinMoneyFlowIndicator
from ta.others import UlcerIndex, ChoppinessIndicator, DetrendedPriceOscillator
import yfinance as yf

df = yf.download("BTC-USD", start="2016-01-01", end="2022-03-23")

# Add Bollinger Bands, RSI, OBV, Fib levels, and MACD
bb = BollingerBands(close=df['Close'], window=20, window_dev=2)
df['bb_upperband'] = bb.bollinger_hband()
df['bb_lowerband'] = bb.bollinger_lband()

rsi = RSIIndicator(close=df['Close'], window=14)
df['rsi'] = rsi.rsi()

obv = OnBalanceVolumeIndicator(close=df['Close'], volume=df['Volume'])
df['obv'] = obv.on_balance_volume()

fib38 = (df['High'].max() - df['Low'].min()) * 0.382
df['fib_23.6'] = df['Close'] - fib38
df['fib_38.2'] = df['Close'] + fib38

fib62 = (df['High'].max() - df['Low'].min()) * 0.618
df['fib_61.8'] = df['Close'] - fib62

macd = MACD(close=df['Close'], window_slow=26, window_fast=12)
df['macd'] = macd.macd()

# Add Stochastic Oscillator, ATR, RSI Divergence, Chaikin Money Flow
sto = StochasticOscillator(high=df['High'], low=df['Low'], close=df['Close'], window=14, smooth_window=3)
df['sto'] = sto.stoch()

atr = AverageTrueRange(high=df['High'], low=df['Low'], close=df['Close'], window=14)
df['atr'] = atr.average_true_range()

rsi_div = RSIIndicator(close=df['Close'], window=14)
df['rsi_div'] = rsi_div.rsi_divergence()

cmf = ChaikinMoneyFlowIndicator(high=df['High'], low=df['Low'], close=df['Close'], volume=df['Volume'], window=20)
df['cmf'] = cmf.chaikin_money_flow()

# Add Ulcer Index, Choppiness Index, Detrended Price Oscillator, Aroon Oscillator, Ultimate Oscillator
ui = UlcerIndex(close=df['Close'], window=14)
df['ui'] = ui.ulcer_index()

ci = ChoppinessIndicator(high=df['High'], low=df['Low'], close=df['Close'], window=14)
df['ci'] = ci.choppiness()

dpo = DetrendedPriceOscillator(close=df['Close'], window=14)
df['dpo'] = dpo.detrended_price_oscillator()

aroon = AroonIndicator(close=df['Close'], window=14)
df['aroonosc'] = aroon.aroon_indicator()

aroonosc = AroonOscillator(high=df['High'], low=df['Low'], window=25) 
df['AROONOSC'] = aroonosc.aroon_oscillator()

ultosc = UltimateOscillator(high=df['High'], low=df['Low'], close=df['Close'], window1=7, window2=14, window3=28) 
df['ULTOSC'] = ultosc.ultimate_oscillator()


 # Select relevant features 
features = ['Close', 'bb_upperband', 'bb_lowerband', 'rsi', 'obv', 'fib_23.6', 'fib_38.2', 'fib_61.8', 'macd', 'sto', 'atr', 'rsi_div', 'cmf', 'UI', 'CI', 'DPO', 'AROONOSC', 'ULTOSC'] 
df = df[features]
