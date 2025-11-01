"""
Module phân tích kỹ thuật
"""

import pandas as pd
import numpy as np
from ta import trend, momentum, volatility, volume as ta_volume
from config import TECHNICAL_INDICATORS, SIGNAL_THRESHOLDS

class TechnicalAnalyzer:
    def __init__(self, df):
        """
        Khởi tạo với dataframe chứa dữ liệu giá
        df phải có các cột: open, high, low, close, volume
        """
        self.df = df.copy()
        self.signals = []
        
    def add_all_indicators(self):
        """Thêm tất cả các chỉ số kỹ thuật"""
        self.add_moving_averages()
        self.add_rsi()
        self.add_macd()
        self.add_bollinger_bands()
        self.add_adx()
        self.add_volume_indicators()
        self.add_stochastic()
        return self.df
    
    def add_moving_averages(self):
        """Thêm các đường trung bình động"""
        # Simple Moving Average
        self.df['sma_20'] = self.df['close'].rolling(window=TECHNICAL_INDICATORS['SMA_SHORT']).mean()
        self.df['sma_50'] = self.df['close'].rolling(window=TECHNICAL_INDICATORS['SMA_MEDIUM']).mean()
        self.df['sma_200'] = self.df['close'].rolling(window=TECHNICAL_INDICATORS['SMA_LONG']).mean()
        
        # Exponential Moving Average
        self.df['ema_12'] = self.df['close'].ewm(span=TECHNICAL_INDICATORS['EMA_SHORT'], adjust=False).mean()
        self.df['ema_26'] = self.df['close'].ewm(span=TECHNICAL_INDICATORS['EMA_LONG'], adjust=False).mean()
        
    def add_rsi(self):
        """Thêm chỉ số RSI"""
        rsi_indicator = momentum.RSIIndicator(
            close=self.df['close'], 
            window=TECHNICAL_INDICATORS['RSI_PERIOD']
        )
        self.df['rsi'] = rsi_indicator.rsi()
        
    def add_macd(self):
        """Thêm MACD"""
        macd = trend.MACD(
            close=self.df['close'],
            window_fast=TECHNICAL_INDICATORS['MACD_FAST'],
            window_slow=TECHNICAL_INDICATORS['MACD_SLOW'],
            window_sign=TECHNICAL_INDICATORS['MACD_SIGNAL']
        )
        self.df['macd'] = macd.macd()
        self.df['macd_signal'] = macd.macd_signal()
        self.df['macd_diff'] = macd.macd_diff()
        
    def add_bollinger_bands(self):
        """Thêm Bollinger Bands"""
        bb = volatility.BollingerBands(
            close=self.df['close'],
            window=TECHNICAL_INDICATORS['BB_PERIOD'],
            window_dev=TECHNICAL_INDICATORS['BB_STD']
        )
        self.df['bb_high'] = bb.bollinger_hband()
        self.df['bb_mid'] = bb.bollinger_mavg()
        self.df['bb_low'] = bb.bollinger_lband()
        self.df['bb_width'] = bb.bollinger_wband()
        
    def add_adx(self):
        """Thêm ADX (Average Directional Index)"""
        adx = trend.ADXIndicator(
            high=self.df['high'],
            low=self.df['low'],
            close=self.df['close'],
            window=TECHNICAL_INDICATORS['ADX_PERIOD']
        )
        self.df['adx'] = adx.adx()
        self.df['adx_pos'] = adx.adx_pos()
        self.df['adx_neg'] = adx.adx_neg()
        
    def add_volume_indicators(self):
        """Thêm các chỉ số về khối lượng"""
        self.df['volume_sma'] = self.df['volume'].rolling(window=TECHNICAL_INDICATORS['VOLUME_SMA']).mean()
        self.df['volume_ratio'] = self.df['volume'] / self.df['volume_sma']
        
        # On-Balance Volume
        obv = ta_volume.OnBalanceVolumeIndicator(
            close=self.df['close'],
            volume=self.df['volume']
        )
        self.df['obv'] = obv.on_balance_volume()
        
    def add_stochastic(self):
        """Thêm Stochastic Oscillator"""
        stoch = momentum.StochasticOscillator(
            high=self.df['high'],
            low=self.df['low'],
            close=self.df['close'],
            window=14,
            smooth_window=3
        )
        self.df['stoch_k'] = stoch.stoch()
        self.df['stoch_d'] = stoch.stoch_signal()
        
    def generate_signals(self):
        """Tạo tín hiệu mua/bán dựa trên các chỉ số kỹ thuật"""
        signals = []
        
        if len(self.df) < 2:
            return signals
        
        latest = self.df.iloc[-1]
        prev = self.df.iloc[-2]
        
        # Tín hiệu từ RSI
        if pd.notna(latest['rsi']):
            if latest['rsi'] < SIGNAL_THRESHOLDS['RSI_OVERSOLD']:
                signals.append({
                    'type': 'BUY',
                    'indicator': 'RSI',
                    'strength': 'STRONG',
                    'reason': f'RSI quá bán ({latest["rsi"]:.2f})'
                })
            elif latest['rsi'] > SIGNAL_THRESHOLDS['RSI_OVERBOUGHT']:
                signals.append({
                    'type': 'SELL',
                    'indicator': 'RSI',
                    'strength': 'STRONG',
                    'reason': f'RSI quá mua ({latest["rsi"]:.2f})'
                })
        
        # Tín hiệu từ MACD
        if pd.notna(latest['macd']) and pd.notna(prev['macd']):
            if prev['macd'] < prev['macd_signal'] and latest['macd'] > latest['macd_signal']:
                signals.append({
                    'type': 'BUY',
                    'indicator': 'MACD',
                    'strength': 'MEDIUM',
                    'reason': 'MACD cắt lên đường tín hiệu'
                })
            elif prev['macd'] > prev['macd_signal'] and latest['macd'] < latest['macd_signal']:
                signals.append({
                    'type': 'SELL',
                    'indicator': 'MACD',
                    'strength': 'MEDIUM',
                    'reason': 'MACD cắt xuống đường tín hiệu'
                })
        
        # Tín hiệu từ Moving Average
        if pd.notna(latest['sma_20']) and pd.notna(latest['sma_50']):
            if prev['sma_20'] < prev['sma_50'] and latest['sma_20'] > latest['sma_50']:
                signals.append({
                    'type': 'BUY',
                    'indicator': 'MA',
                    'strength': 'STRONG',
                    'reason': 'Golden Cross: SMA 20 cắt lên SMA 50'
                })
            elif prev['sma_20'] > prev['sma_50'] and latest['sma_20'] < latest['sma_50']:
                signals.append({
                    'type': 'SELL',
                    'indicator': 'MA',
                    'strength': 'STRONG',
                    'reason': 'Death Cross: SMA 20 cắt xuống SMA 50'
                })
        
        # Tín hiệu từ Bollinger Bands
        if pd.notna(latest['bb_low']) and pd.notna(latest['bb_high']):
            if latest['close'] < latest['bb_low']:
                signals.append({
                    'type': 'BUY',
                    'indicator': 'BB',
                    'strength': 'MEDIUM',
                    'reason': 'Giá chạm dải Bollinger dưới'
                })
            elif latest['close'] > latest['bb_high']:
                signals.append({
                    'type': 'SELL',
                    'indicator': 'BB',
                    'strength': 'MEDIUM',
                    'reason': 'Giá chạm dải Bollinger trên'
                })
        
        # Tín hiệu từ Stochastic
        if pd.notna(latest['stoch_k']):
            if latest['stoch_k'] < 20:
                signals.append({
                    'type': 'BUY',
                    'indicator': 'STOCH',
                    'strength': 'MEDIUM',
                    'reason': f'Stochastic quá bán ({latest["stoch_k"]:.2f})'
                })
            elif latest['stoch_k'] > 80:
                signals.append({
                    'type': 'SELL',
                    'indicator': 'STOCH',
                    'strength': 'MEDIUM',
                    'reason': f'Stochastic quá mua ({latest["stoch_k"]:.2f})'
                })
        
        # Tín hiệu từ Volume
        if pd.notna(latest['volume_ratio']):
            if latest['volume_ratio'] > SIGNAL_THRESHOLDS['VOLUME_SPIKE']:
                if latest['close'] > prev['close']:
                    signals.append({
                        'type': 'BUY',
                        'indicator': 'VOLUME',
                        'strength': 'MEDIUM',
                        'reason': f'Khối lượng tăng mạnh ({latest["volume_ratio"]:.2f}x) với giá tăng'
                    })
                else:
                    signals.append({
                        'type': 'SELL',
                        'indicator': 'VOLUME',
                        'strength': 'MEDIUM',
                        'reason': f'Khối lượng tăng mạnh ({latest["volume_ratio"]:.2f}x) với giá giảm'
                    })
        
        self.signals = signals
        return signals
    
    def calculate_score(self):
        """Tính điểm tổng hợp từ các chỉ số kỹ thuật"""
        score = 50  # Điểm trung lập
        
        if len(self.df) < 2:
            return score
        
        latest = self.df.iloc[-1]
        
        # Điểm từ RSI (±10)
        if pd.notna(latest['rsi']):
            if latest['rsi'] < 30:
                score += 10
            elif latest['rsi'] > 70:
                score -= 10
            elif 40 < latest['rsi'] < 60:
                score += 5  # Vùng trung lập tích cực
        
        # Điểm từ MACD (±8)
        if pd.notna(latest['macd']) and pd.notna(latest['macd_signal']):
            if latest['macd'] > latest['macd_signal']:
                score += 8
            else:
                score -= 8
        
        # Điểm từ MA (±12)
        if pd.notna(latest['sma_20']) and pd.notna(latest['sma_50']):
            if latest['close'] > latest['sma_20'] > latest['sma_50']:
                score += 12
            elif latest['close'] < latest['sma_20'] < latest['sma_50']:
                score -= 12
        
        # Điểm từ ADX (±5)
        if pd.notna(latest['adx']):
            if latest['adx'] > SIGNAL_THRESHOLDS['ADX_TREND']:
                if pd.notna(latest['adx_pos']) and pd.notna(latest['adx_neg']):
                    if latest['adx_pos'] > latest['adx_neg']:
                        score += 5
                    else:
                        score -= 5
        
        # Điểm từ Stochastic (±5)
        if pd.notna(latest['stoch_k']):
            if latest['stoch_k'] < 20:
                score += 5
            elif latest['stoch_k'] > 80:
                score -= 5
        
        # Giới hạn điểm trong khoảng 0-100
        score = max(0, min(100, score))
        
        return score
    
    def get_trend(self):
        """Xác định xu hướng thị trường"""
        if len(self.df) < 50:
            return "KHÔNG ĐỦ DỮ LIỆU"
        
        latest = self.df.iloc[-1]
        
        # Xu hướng dựa trên MA
        if pd.notna(latest['sma_20']) and pd.notna(latest['sma_50']):
            if latest['close'] > latest['sma_20'] > latest['sma_50']:
                trend = "TĂNG MẠNH"
            elif latest['close'] > latest['sma_20']:
                trend = "TĂNG"
            elif latest['close'] < latest['sma_20'] < latest['sma_50']:
                trend = "GIẢM MẠNH"
            elif latest['close'] < latest['sma_20']:
                trend = "GIẢM"
            else:
                trend = "SIDEWAY"
        else:
            trend = "KHÔNG XÁC ĐỊNH"
        
        # Xác định sức mạnh xu hướng bằng ADX
        if pd.notna(latest['adx']):
            if latest['adx'] > SIGNAL_THRESHOLDS['ADX_TREND']:
                trend += " (Mạnh)"
            else:
                trend += " (Yếu)"
        
        return trend

