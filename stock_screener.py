"""
Module tìm kiếm mã chứng khoán tiềm năng
"""

import pandas as pd
import numpy as np
import time
from data_fetcher import DataFetcher
from trading_signals import TradingSignalGenerator
import streamlit as st

class StockScreener:
    def __init__(self):
        self.data_fetcher = DataFetcher()
    
    def _normalize_stocks_dataframe(self, df):
        """Chuẩn hóa DataFrame từ all_stocks"""
        if df is None or df.empty:
            return df
        
        # Chuẩn hóa tên cột
        if 'organ_name' in df.columns and 'organName' not in df.columns:
            df['organName'] = df['organ_name']
        
        # Thêm cột exchange nếu không có (mặc định HOSE)
        if 'exchange' not in df.columns:
            df['exchange'] = 'HOSE'
        
        return df
    
    def scan_market(self, investment_type='SHORT_TERM', top_n=20, progress_callback=None):
        """
        Quét thị trường tìm các cổ phiếu tiềm năng
        
        Args:
            investment_type: Loại đầu tư (SHORT_TERM, MEDIUM_TERM, LONG_TERM)
            top_n: Số lượng cổ phiếu trả về
            progress_callback: Callback để cập nhật tiến trình
        """
        # Lấy danh sách tất cả cổ phiếu
        all_stocks = self.data_fetcher.get_all_stocks()
        
        if all_stocks is None or all_stocks.empty:
            return []
        
        # Chuẩn hóa DataFrame
        all_stocks = self._normalize_stocks_dataframe(all_stocks)
        
        # Lọc chỉ lấy cổ phiếu trên HOSE và HNX (nếu có cột exchange)
        if 'exchange' in all_stocks.columns:
            all_stocks = all_stocks[all_stocks['exchange'].isin(['HOSE', 'HNX'])]
        
        results = []
        # Giới hạn số lượng để tránh timeout
        total = min(len(all_stocks), 50)  # Giảm xuống 50 mã để tránh timeout
        print(f"Scanning {total} stocks out of {len(all_stocks)} total stocks")
        
        for idx, row in all_stocks.head(total).iterrows():
            try:
                symbol = row['symbol']
                
                if progress_callback:
                    progress_callback(idx + 1, total, symbol)
                
                # Xác định period dựa vào loại đầu tư
                if investment_type == 'SHORT_TERM':
                    period = '3M'
                elif investment_type == 'MEDIUM_TERM':
                    period = '1Y'
                else:  # LONG_TERM
                    period = '3Y'
                
                # Lấy dữ liệu với retry mechanism
                stock_data = None
                max_retries = 2
                for retry in range(max_retries):
                    try:
                        stock_data = self.data_fetcher.get_stock_data(symbol, period=period)
                        if stock_data is not None and len(stock_data) >= 20:
                            break
                        time.sleep(0.3)  # Đợi giữa các retry
                    except Exception as e:
                        if retry < max_retries - 1:
                            time.sleep(0.5)  # Đợi lâu hơn trước retry
                        continue
                
                # Delay để tránh rate limit
                time.sleep(0.3)
                
                if stock_data is None or len(stock_data) < 20:
                    continue
                
                # Lấy dữ liệu tài chính (chỉ cho trung và dài hạn)
                financial_data = None
                ratios_data = None
                
                if investment_type in ['MEDIUM_TERM', 'LONG_TERM']:
                    ratios_data = self.data_fetcher.get_financial_ratios(symbol)
                
                # Phân tích
                signal_gen = TradingSignalGenerator(stock_data, financial_data, ratios_data)
                overall_signal = signal_gen.get_overall_signal()
                timeframes = signal_gen.get_investment_timeframe()
                
                # Kiểm tra phù hợp với loại đầu tư
                is_suitable = False
                if investment_type == 'SHORT_TERM' and 'NGẮN HẠN' in ' '.join(timeframes):
                    is_suitable = True
                elif investment_type == 'MEDIUM_TERM' and 'TRUNG HẠN' in ' '.join(timeframes):
                    is_suitable = True
                elif investment_type == 'LONG_TERM' and 'DÀI HẠN' in ' '.join(timeframes):
                    is_suitable = True
                
                if is_suitable and overall_signal['overall_score'] >= 55:
                    latest_price = stock_data.iloc[-1]['close']
                    
                    results.append({
                        'symbol': symbol,
                        'name': row.get('organName', symbol),
                        'exchange': row.get('exchange', ''),
                        'price': latest_price,
                        'overall_score': overall_signal['overall_score'],
                        'technical_score': overall_signal['technical_score'],
                        'fundamental_score': overall_signal['fundamental_score'],
                        'signal': overall_signal['signal'],
                        'timeframes': timeframes
                    })
                
            except Exception as e:
                continue
        
        # Sắp xếp theo điểm số
        results = sorted(results, key=lambda x: x['overall_score'], reverse=True)
        
        return results[:top_n]
    
    def filter_by_technical_criteria(self, criteria):
        """
        Lọc cổ phiếu theo tiêu chí kỹ thuật
        
        criteria: dict chứa các tiêu chí
        - rsi_range: tuple (min, max)
        - trend: str ('TĂNG', 'GIẢM', 'SIDEWAY')
        - volume_spike: bool
        """
        all_stocks = self.data_fetcher.get_all_stocks()
        
        if all_stocks is None or all_stocks.empty:
            return []
        
        all_stocks = self._normalize_stocks_dataframe(all_stocks)
        
        # Lọc chỉ lấy cổ phiếu trên HOSE và HNX (nếu có cột exchange)
        if 'exchange' in all_stocks.columns:
            all_stocks = all_stocks[all_stocks['exchange'].isin(['HOSE', 'HNX'])]
        
        results = []
        
        for idx, row in all_stocks.head(50).iterrows():
            try:
                symbol = row['symbol']
                try:
                    stock_data = self.data_fetcher.get_stock_data(symbol, period='3M')
                except Exception:
                    continue
                
                if stock_data is None or len(stock_data) < 20:
                    continue
                
                from technical_analysis import TechnicalAnalyzer
                analyzer = TechnicalAnalyzer(stock_data)
                analyzer.add_all_indicators()
                
                latest = analyzer.df.iloc[-1]
                
                # Kiểm tra các tiêu chí
                match = True
                
                # RSI
                if 'rsi_range' in criteria and pd.notna(latest['rsi']):
                    rsi_min, rsi_max = criteria['rsi_range']
                    if not (rsi_min <= latest['rsi'] <= rsi_max):
                        match = False
                
                # Trend
                if 'trend' in criteria:
                    trend = analyzer.get_trend()
                    if criteria['trend'] not in trend:
                        match = False
                
                # Volume spike
                if 'volume_spike' in criteria and criteria['volume_spike']:
                    if pd.notna(latest['volume_ratio']):
                        if latest['volume_ratio'] < 1.5:
                            match = False
                
                if match:
                    results.append({
                        'symbol': symbol,
                        'name': row.get('organName', symbol),
                        'price': latest['close'],
                        'rsi': latest.get('rsi', None),
                        'trend': analyzer.get_trend(),
                        'volume_ratio': latest.get('volume_ratio', None)
                    })
                
            except Exception as e:
                continue
        
        return results
    
    def find_breakout_stocks(self):
        """Tìm cổ phiếu đang breakout"""
        all_stocks = self.data_fetcher.get_all_stocks()
        
        if all_stocks is None or all_stocks.empty:
            return []
        
        all_stocks = self._normalize_stocks_dataframe(all_stocks)
        
        # Lọc chỉ lấy cổ phiếu trên HOSE và HNX (nếu có cột exchange)
        if 'exchange' in all_stocks.columns:
            all_stocks = all_stocks[all_stocks['exchange'].isin(['HOSE', 'HNX'])]
        
        results = []
        
        for idx, row in all_stocks.head(50).iterrows():
            try:
                symbol = row['symbol']
                try:
                    stock_data = self.data_fetcher.get_stock_data(symbol, period='6M')
                except Exception:
                    continue
                
                if stock_data is None or len(stock_data) < 100:
                    continue
                
                from technical_analysis import TechnicalAnalyzer
                analyzer = TechnicalAnalyzer(stock_data)
                analyzer.add_all_indicators()
                
                latest = analyzer.df.iloc[-1]
                prev = analyzer.df.iloc[-2]
                
                # Điều kiện breakout:
                # 1. Giá vượt qua SMA 50
                # 2. Volume tăng mạnh
                # 3. RSI > 50 nhưng chưa quá mua
                
                is_breakout = False
                
                if pd.notna(latest['sma_50']) and pd.notna(latest['volume_ratio']):
                    price_breakout = prev['close'] < prev['sma_50'] and latest['close'] > latest['sma_50']
                    volume_surge = latest['volume_ratio'] > 1.5
                    rsi_ok = pd.notna(latest['rsi']) and 50 < latest['rsi'] < 70
                    
                    if price_breakout and volume_surge and rsi_ok:
                        is_breakout = True
                
                if is_breakout:
                    results.append({
                        'symbol': symbol,
                        'name': row.get('organName', symbol),
                        'price': latest['close'],
                        'sma_50': latest['sma_50'],
                        'volume_ratio': latest['volume_ratio'],
                        'rsi': latest['rsi']
                    })
                
            except Exception as e:
                continue
        
        return results
    
    def find_oversold_stocks(self):
        """Tìm cổ phiếu quá bán (cơ hội mua vào)"""
        all_stocks = self.data_fetcher.get_all_stocks()
        
        if all_stocks is None or all_stocks.empty:
            return []
        
        all_stocks = self._normalize_stocks_dataframe(all_stocks)
        
        # Lọc chỉ lấy cổ phiếu trên HOSE và HNX (nếu có cột exchange)
        if 'exchange' in all_stocks.columns:
            all_stocks = all_stocks[all_stocks['exchange'].isin(['HOSE', 'HNX'])]
        
        results = []
        
        for idx, row in all_stocks.head(50).iterrows():
            try:
                symbol = row['symbol']
                try:
                    stock_data = self.data_fetcher.get_stock_data(symbol, period='3M')
                except Exception:
                    continue
                
                if stock_data is None or len(stock_data) < 20:
                    continue
                
                from technical_analysis import TechnicalAnalyzer
                analyzer = TechnicalAnalyzer(stock_data)
                analyzer.add_all_indicators()
                
                latest = analyzer.df.iloc[-1]
                
                # Điều kiện quá bán:
                # RSI < 30 hoặc giá chạm Bollinger Band dưới
                is_oversold = False
                
                if pd.notna(latest['rsi']) and latest['rsi'] < 30:
                    is_oversold = True
                
                if pd.notna(latest['bb_low']) and latest['close'] <= latest['bb_low']:
                    is_oversold = True
                
                if is_oversold:
                    results.append({
                        'symbol': symbol,
                        'name': row.get('organName', symbol),
                        'price': latest['close'],
                        'rsi': latest.get('rsi', None),
                        'bb_position': 'Chạm dải dưới' if pd.notna(latest['bb_low']) and latest['close'] <= latest['bb_low'] else 'RSI quá bán'
                    })
                
            except Exception as e:
                continue
        
        return results

