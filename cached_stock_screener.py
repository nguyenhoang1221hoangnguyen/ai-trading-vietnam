"""
Stock Screener sử dụng cached data
"""

import pandas as pd
import numpy as np
from data_cache import DataCache
from technical_analysis import TechnicalAnalyzer
from trading_signals import TradingSignalGenerator
import time

class CachedStockScreener:
    def __init__(self):
        self.cache = DataCache()
    
    def get_market_comparison_table(self, update_cache=False, max_symbols=100):
        """
        Tạo bảng so sánh toàn diện thị trường
        
        Args:
            update_cache: Có cập nhật cache trước không
            max_symbols: Giới hạn số lượng mã
        """
        if update_cache:
            print("🔄 Updating cache...")
            self.cache.bulk_cache_update(max_symbols=max_symbols)
        
        print("📊 Generating market comparison table...")
        
        # Lấy tổng quan thị trường từ cache
        overview = self.cache.get_market_overview()
        
        if overview.empty:
            print("❌ No cached data found. Please update cache first.")
            return pd.DataFrame()
        
        # Giới hạn số lượng để tránh quá tải
        if len(overview) > max_symbols:
            overview = overview.head(max_symbols)
        
        results = []
        total = len(overview)
        
        for idx, row in overview.iterrows():
            try:
                symbol = row['symbol']
                print(f"[{idx+1}/{total}] Processing {symbol}...")
                
                # Lấy dữ liệu từ cache (1 năm)
                stock_data = self.cache.get_stock_with_indicators(symbol, period_days=365)
                
                if stock_data is None or len(stock_data) < 50:
                    continue
                
                # Phân tích kỹ thuật
                analyzer = TechnicalAnalyzer(stock_data)
                df_with_indicators = analyzer.add_all_indicators()
                
                # Tạo trading signals
                signal_gen = TradingSignalGenerator(df_with_indicators)
                overall_signal = signal_gen.get_overall_signal()
                entry_points = signal_gen.get_entry_points()
                exit_points = signal_gen.get_exit_points()
                risk_reward = signal_gen.get_risk_reward_ratio()
                
                # Tính toán các metrics bổ sung
                latest = df_with_indicators.iloc[-1]
                prev_month = df_with_indicators.iloc[-21] if len(df_with_indicators) >= 21 else df_with_indicators.iloc[0]
                prev_quarter = df_with_indicators.iloc[-63] if len(df_with_indicators) >= 63 else df_with_indicators.iloc[0]
                
                # Performance
                monthly_return = ((latest['close'] - prev_month['close']) / prev_month['close']) * 100
                quarterly_return = ((latest['close'] - prev_quarter['close']) / prev_quarter['close']) * 100
                
                # Volatility (20-day)
                returns = df_with_indicators['close'].pct_change().dropna()
                volatility = returns.tail(20).std() * np.sqrt(252) * 100  # Annualized
                
                # Volume trend
                avg_volume_20 = df_with_indicators['volume'].tail(20).mean()
                current_volume = latest['volume']
                volume_ratio = current_volume / avg_volume_20 if avg_volume_20 > 0 else 1
                
                # Support/Resistance levels
                high_52w = df_with_indicators['high'].tail(252).max() if len(df_with_indicators) >= 252 else df_with_indicators['high'].max()
                low_52w = df_with_indicators['low'].tail(252).min() if len(df_with_indicators) >= 252 else df_with_indicators['low'].min()
                
                # Distance from 52w high/low
                dist_from_high = ((latest['close'] - high_52w) / high_52w) * 100
                dist_from_low = ((latest['close'] - low_52w) / low_52w) * 100
                
                result = {
                    # Basic info
                    'symbol': symbol,
                    'name': row['name'],
                    'exchange': row['exchange'],
                    'current_price': latest['close'],
                    'volume': current_volume,
                    
                    # Performance
                    'monthly_return': monthly_return,
                    'quarterly_return': quarterly_return,
                    'ytd_return': quarterly_return,  # Approximation
                    
                    # Technical indicators
                    'rsi': latest.get('rsi', np.nan),
                    'macd': latest.get('macd', np.nan),
                    'sma_20': latest.get('sma_20', np.nan),
                    'sma_50': latest.get('sma_50', np.nan),
                    'sma_200': latest.get('sma_200', np.nan),
                    'bb_position': self._calculate_bb_position(latest),
                    
                    # Price levels
                    'high_52w': high_52w,
                    'low_52w': low_52w,
                    'dist_from_high': dist_from_high,
                    'dist_from_low': dist_from_low,
                    
                    # Risk metrics
                    'volatility': volatility,
                    'volume_ratio': volume_ratio,
                    
                    # Trading signals
                    'overall_score': overall_signal['overall_score'],
                    'technical_score': overall_signal['technical_score'],
                    'signal': overall_signal['signal'],
                    'entry_points_count': len(entry_points),
                    'exit_points_count': len(exit_points),
                    'risk_reward_ratio': risk_reward['ratio'] if risk_reward else np.nan,
                    
                    # Trend analysis
                    'trend': analyzer.get_trend(),
                    'price_vs_sma20': ((latest['close'] - latest.get('sma_20', latest['close'])) / latest.get('sma_20', latest['close'])) * 100 if pd.notna(latest.get('sma_20')) else 0,
                    'price_vs_sma50': ((latest['close'] - latest.get('sma_50', latest['close'])) / latest.get('sma_50', latest['close'])) * 100 if pd.notna(latest.get('sma_50')) else 0,
                    
                    # Last update
                    'last_update': row['last_update']
                }
                
                results.append(result)
                
            except Exception as e:
                print(f"Error processing {symbol}: {str(e)[:50]}")
                continue
        
        if not results:
            print("❌ No results generated")
            return pd.DataFrame()
        
        df = pd.DataFrame(results)
        
        # Sắp xếp theo overall_score
        df = df.sort_values('overall_score', ascending=False)
        
        print(f"✅ Generated comparison table with {len(df)} stocks")
        return df
    
    def _calculate_bb_position(self, latest_data):
        """Tính vị trí giá so với Bollinger Bands"""
        if pd.isna(latest_data.get('bb_high')) or pd.isna(latest_data.get('bb_low')):
            return np.nan
        
        bb_high = latest_data['bb_high']
        bb_low = latest_data['bb_low']
        close = latest_data['close']
        
        if bb_high == bb_low:
            return 0.5
        
        position = (close - bb_low) / (bb_high - bb_low)
        return position
    
    def filter_by_criteria(self, df, criteria):
        """
        Lọc cổ phiếu theo tiêu chí
        
        Args:
            df: DataFrame từ get_market_comparison_table
            criteria: Dict chứa các tiêu chí lọc
        """
        filtered_df = df.copy()
        
        # Lọc theo điểm số
        if 'min_overall_score' in criteria:
            filtered_df = filtered_df[filtered_df['overall_score'] >= criteria['min_overall_score']]
        
        # Lọc theo RSI
        if 'rsi_range' in criteria:
            rsi_min, rsi_max = criteria['rsi_range']
            filtered_df = filtered_df[
                (filtered_df['rsi'] >= rsi_min) & 
                (filtered_df['rsi'] <= rsi_max)
            ]
        
        # Lọc theo performance
        if 'min_monthly_return' in criteria:
            filtered_df = filtered_df[filtered_df['monthly_return'] >= criteria['min_monthly_return']]
        
        # Lọc theo volume
        if 'min_volume_ratio' in criteria:
            filtered_df = filtered_df[filtered_df['volume_ratio'] >= criteria['min_volume_ratio']]
        
        # Lọc theo trend
        if 'trend_filter' in criteria:
            trends = criteria['trend_filter']
            if isinstance(trends, str):
                trends = [trends]
            filtered_df = filtered_df[filtered_df['trend'].str.contains('|'.join(trends), na=False)]
        
        # Lọc theo signal
        if 'signal_filter' in criteria:
            signals = criteria['signal_filter']
            if isinstance(signals, str):
                signals = [signals]
            filtered_df = filtered_df[filtered_df['signal'].isin(signals)]
        
        return filtered_df
    
    def get_top_performers(self, df, category='overall', top_n=10):
        """
        Lấy top performers theo danh mục
        
        Args:
            df: DataFrame từ get_market_comparison_table
            category: 'overall', 'monthly', 'quarterly', 'technical', 'low_risk'
            top_n: Số lượng top
        """
        if category == 'overall':
            return df.nlargest(top_n, 'overall_score')
        elif category == 'monthly':
            return df.nlargest(top_n, 'monthly_return')
        elif category == 'quarterly':
            return df.nlargest(top_n, 'quarterly_return')
        elif category == 'technical':
            return df.nlargest(top_n, 'technical_score')
        elif category == 'low_risk':
            return df.nsmallest(top_n, 'volatility')
        elif category == 'high_volume':
            return df.nlargest(top_n, 'volume_ratio')
        else:
            return df.head(top_n)
    
    def export_to_excel(self, df, filename='market_analysis.xlsx'):
        """Xuất kết quả ra Excel"""
        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Sheet tổng quan
                df.to_excel(writer, sheet_name='Market Overview', index=False)
                
                # Sheet top performers
                categories = ['overall', 'monthly', 'quarterly', 'technical', 'low_risk']
                for category in categories:
                    top_df = self.get_top_performers(df, category, 20)
                    sheet_name = f'Top {category.title()}'
                    top_df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Sheet filtered
                buy_signals = self.filter_by_criteria(df, {
                    'signal_filter': ['MUA', 'MUA MẠNH'],
                    'min_overall_score': 60
                })
                buy_signals.to_excel(writer, sheet_name='Buy Signals', index=False)
                
            print(f"✅ Exported to {filename}")
            return True
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False
