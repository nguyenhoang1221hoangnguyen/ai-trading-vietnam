"""
Module tìm điểm mua/bán
"""

import pandas as pd
import numpy as np
from technical_analysis import TechnicalAnalyzer
from fundamental_analysis import FundamentalAnalyzer
from config import SCORING_WEIGHTS

class TradingSignalGenerator:
    def __init__(self, stock_data, financial_data=None, ratios_data=None):
        """
        Khởi tạo với dữ liệu giá và dữ liệu tài chính
        """
        self.stock_data = stock_data
        self.financial_data = financial_data
        self.ratios_data = ratios_data
        
        # Khởi tạo các analyzer
        self.technical_analyzer = TechnicalAnalyzer(stock_data)
        # QUAN TRỌNG: Cập nhật stock_data với các chỉ báo kỹ thuật
        self.stock_data = self.technical_analyzer.add_all_indicators()
        
        if financial_data is not None and ratios_data is not None:
            self.fundamental_analyzer = FundamentalAnalyzer(financial_data, ratios_data)
        else:
            self.fundamental_analyzer = None
    
    def get_overall_signal(self):
        """Lấy tín hiệu tổng hợp"""
        # Tính điểm kỹ thuật
        technical_score = self.technical_analyzer.calculate_score()
        
        # Tính điểm cơ bản
        if self.fundamental_analyzer:
            fundamental_score = self.fundamental_analyzer.calculate_score()
        else:
            fundamental_score = 50  # Trung lập nếu không có dữ liệu
        
        # Tính điểm tổng hợp
        overall_score = (
            technical_score * SCORING_WEIGHTS['TECHNICAL'] + 
            fundamental_score * SCORING_WEIGHTS['FUNDAMENTAL']
        )
        
        # Xác định tín hiệu
        if overall_score >= 70:
            signal = 'MUA MẠNH'
            color = '🟢'
        elif overall_score >= 60:
            signal = 'MUA'
            color = '🟢'
        elif overall_score >= 45:
            signal = 'GIỮ'
            color = '🟡'
        elif overall_score >= 35:
            signal = 'BÁN'
            color = '🔴'
        else:
            signal = 'BÁN MẠNH'
            color = '🔴'
        
        return {
            'signal': signal,
            'color': color,
            'overall_score': overall_score,
            'technical_score': technical_score,
            'fundamental_score': fundamental_score
        }
    
    def get_entry_points(self):
        """Xác định các điểm vào lệnh (entry points)"""
        entry_points = []
        
        if len(self.stock_data) < 2:
            return entry_points
        
        latest = self.stock_data.iloc[-1]
        current_price = latest['close']
        
        # Không cần debug nữa
        
        # Điểm mua dựa trên support - chỉ khi giá hiện tại GẦN hoặc DƯỚI support
        if 'bb_low' in self.stock_data.columns and pd.notna(latest['bb_low']):
            bb_low = latest['bb_low']
            if current_price <= bb_low * 1.02:  # Trong vòng 2% của BB lower
                entry_points.append({
                    'type': 'MUA',
                    'price': bb_low,
                    'reason': f'Support Bollinger Band dưới ({bb_low*1000:,.0f} VNĐ)'
                })
        
        if 'sma_20' in self.stock_data.columns and pd.notna(latest['sma_20']):
            sma_20 = latest['sma_20']
            if current_price <= sma_20 * 1.03:  # Trong vòng 3% của SMA 20
                entry_points.append({
                    'type': 'MUA',
                    'price': sma_20,
                    'reason': f'Support SMA 20 ({sma_20*1000:,.0f} VNĐ)'
                })
        
        if 'sma_50' in self.stock_data.columns and pd.notna(latest['sma_50']):
            sma_50 = latest['sma_50']
            if current_price <= sma_50 * 1.05:  # Trong vòng 5% của SMA 50
                entry_points.append({
                    'type': 'MUA',
                    'price': sma_50,
                    'reason': f'Support SMA 50 ({sma_50*1000:,.0f} VNĐ)'
                })
        
        # Thêm điểm mua dựa trên RSI quá bán
        if 'rsi' in self.stock_data.columns and pd.notna(latest['rsi']):
            rsi = latest['rsi']
            if rsi < 30:
                entry_points.append({
                    'type': 'MUA',
                    'price': current_price,
                    'reason': f'RSI quá bán ({rsi:.1f}) - Cơ hội mua'
                })
        
        # Thêm điểm mua dựa trên Stochastic quá bán
        if 'stoch_k' in self.stock_data.columns and pd.notna(latest['stoch_k']):
            stoch_k = latest['stoch_k']
            if stoch_k < 20:
                entry_points.append({
                    'type': 'MUA',
                    'price': current_price,
                    'reason': f'Stochastic quá bán ({stoch_k:.1f}) - Tín hiệu mua'
                })
        
        return entry_points
    
    def get_exit_points(self):
        """Xác định các điểm thoát lệnh (exit points)"""
        exit_points = []
        
        if len(self.stock_data) < 2:
            return exit_points
        
        latest = self.stock_data.iloc[-1]
        current_price = latest['close']
        
        # Điểm chốt lời (take profit) - Bollinger Band trên
        if 'bb_high' in self.stock_data.columns and pd.notna(latest['bb_high']):
            bb_high = latest['bb_high']
            profit_pct = ((bb_high - current_price) / current_price) * 100
            if profit_pct > 0:  # Chỉ hiển thị nếu có lợi nhuận
                exit_points.append({
                    'type': 'CHỐT LỜI',
                    'price': bb_high,
                    'profit_pct': profit_pct,
                    'reason': f'Resistance Bollinger Band trên (+{profit_pct:.1f}%)'
                })
        
        # Điểm chốt lời theo RSI quá mua
        if 'rsi' in self.stock_data.columns and pd.notna(latest['rsi']):
            rsi = latest['rsi']
            if rsi > 70:
                exit_points.append({
                    'type': 'CHỐT LỜI',
                    'price': current_price,
                    'profit_pct': 0,
                    'reason': f'RSI quá mua ({rsi:.1f}) - Nên chốt lời'
                })
        
        # Điểm chốt lời theo Stochastic quá mua
        if 'stoch_k' in self.stock_data.columns and pd.notna(latest['stoch_k']):
            stoch_k = latest['stoch_k']
            if stoch_k > 80:
                exit_points.append({
                    'type': 'CHỐT LỜI',
                    'price': current_price,
                    'profit_pct': 0,
                    'reason': f'Stochastic quá mua ({stoch_k:.1f}) - Tín hiệu bán'
                })
        
        # Điểm cắt lỗ (stop loss) - 3% dưới SMA 20
        if 'sma_20' in self.stock_data.columns and pd.notna(latest['sma_20']):
            sma_20 = latest['sma_20']
            stop_loss_price = sma_20 * 0.97
            loss_pct = ((stop_loss_price - current_price) / current_price) * 100
            exit_points.append({
                'type': 'CẮT LỖ',
                'price': stop_loss_price,
                'loss_pct': loss_pct,
                'reason': f'Stop Loss: 3% dưới SMA 20 ({loss_pct:.1f}%)'
            })
        
        # Điểm cắt lỗ dự phòng - 5% dưới giá hiện tại
        emergency_stop = current_price * 0.95
        emergency_loss_pct = -5.0
        exit_points.append({
            'type': 'CẮT LỖ',
            'price': emergency_stop,
            'loss_pct': emergency_loss_pct,
            'reason': f'Stop Loss khẩn cấp: -5% ({emergency_stop*1000:,.0f} VNĐ)'
        })
        
        return exit_points
    
    def get_risk_reward_ratio(self):
        """Tính tỷ lệ rủi ro/lợi nhuận"""
        entry_points = self.get_entry_points()
        exit_points = self.get_exit_points()
        
        if not entry_points or not exit_points:
            return None
        
        latest = self.stock_data.iloc[-1]
        current_price = latest['close']
        
        # Tìm điểm chốt lời và cắt lỗ
        take_profit = None
        stop_loss = None
        
        for point in exit_points:
            if point['type'] == 'CHỐT LỜI' and take_profit is None:
                take_profit = point['price']
            elif point['type'] == 'CẮT LỖ' and stop_loss is None:
                stop_loss = point['price']
        
        if take_profit and stop_loss:
            potential_profit = take_profit - current_price
            potential_loss = current_price - stop_loss
            
            if potential_loss > 0:
                risk_reward = potential_profit / potential_loss
                return {
                    'ratio': risk_reward,
                    'potential_profit': potential_profit,
                    'potential_loss': potential_loss,
                    'take_profit': take_profit,
                    'stop_loss': stop_loss
                }
        
        return None
    
    def get_recommendation(self):
        """Đưa ra khuyến nghị đầu tư chi tiết"""
        overall_signal = self.get_overall_signal()
        technical_signals = self.technical_analyzer.generate_signals()
        trend = self.technical_analyzer.get_trend()
        
        recommendation = {
            'signal': overall_signal,
            'trend': trend,
            'technical_signals': technical_signals,
            'entry_points': self.get_entry_points(),
            'exit_points': self.get_exit_points(),
            'risk_reward': self.get_risk_reward_ratio()
        }
        
        # Thêm phân tích cơ bản nếu có
        if self.fundamental_analyzer:
            recommendation['fundamental'] = {
                'valuation': self.fundamental_analyzer.get_valuation_analysis(),
                'profitability': self.fundamental_analyzer.get_profitability_analysis(),
                'financial_health': self.fundamental_analyzer.get_financial_health(),
                'growth': self.fundamental_analyzer.get_growth_analysis()
            }
        
        return recommendation
    
    def get_investment_timeframe(self):
        """Xác định khung thời gian đầu tư phù hợp"""
        overall_signal = self.get_overall_signal()
        trend = self.technical_analyzer.get_trend()
        
        timeframes = []
        
        # Ngắn hạn: dựa vào tín hiệu kỹ thuật
        if overall_signal['technical_score'] >= 65:
            timeframes.append('NGẮN HẠN (1-3 tháng)')
        
        # Trung hạn: cần có cả tín hiệu kỹ thuật và xu hướng tốt
        if overall_signal['technical_score'] >= 60 and 'TĂNG' in trend:
            timeframes.append('TRUNG HẠN (3-12 tháng)')
        
        # Dài hạn: cần có cơ bản tốt
        if self.fundamental_analyzer:
            fund_score = overall_signal['fundamental_score']
            if fund_score >= 60 and overall_signal['technical_score'] >= 55:
                timeframes.append('DÀI HẠN (> 1 năm)')
        
        return timeframes if timeframes else ['KHÔNG PHÙ HỢP']

