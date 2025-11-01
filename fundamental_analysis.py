"""
Module phân tích cơ bản
"""

import pandas as pd
import numpy as np

class FundamentalAnalyzer:
    def __init__(self, financial_data, ratios_data):
        """
        Khởi tạo với dữ liệu tài chính và chỉ số
        """
        self.financial_data = financial_data
        self.ratios_data = ratios_data
        
    def calculate_score(self):
        """Tính điểm phân tích cơ bản (0-100)"""
        score = 50  # Điểm cơ bản
        
        if self.ratios_data is None or self.ratios_data.empty:
            return score
        
        try:
            # Lấy dữ liệu mới nhất
            latest = self.ratios_data.iloc[0] if len(self.ratios_data) > 0 else None
            
            if latest is None:
                return score
            
            # P/E Ratio (±10 điểm)
            if 'pe' in latest.index and pd.notna(latest['pe']):
                pe = float(latest['pe'])
                if 0 < pe < 15:
                    score += 10  # P/E thấp, tốt
                elif 15 <= pe < 25:
                    score += 5   # P/E trung bình
                elif pe >= 40:
                    score -= 10  # P/E quá cao
            
            # P/B Ratio (±8 điểm)
            if 'pb' in latest.index and pd.notna(latest['pb']):
                pb = float(latest['pb'])
                if 0 < pb < 1.5:
                    score += 8
                elif 1.5 <= pb < 3:
                    score += 4
                elif pb >= 5:
                    score -= 8
            
            # ROE (±10 điểm)
            if 'roe' in latest.index and pd.notna(latest['roe']):
                roe = float(latest['roe'])
                if roe > 20:
                    score += 10
                elif roe > 15:
                    score += 7
                elif roe > 10:
                    score += 4
                elif roe < 5:
                    score -= 10
            
            # ROA (±7 điểm)
            if 'roa' in latest.index and pd.notna(latest['roa']):
                roa = float(latest['roa'])
                if roa > 10:
                    score += 7
                elif roa > 5:
                    score += 4
                elif roa < 2:
                    score -= 7
            
            # Debt to Equity (±8 điểm)
            if 'debtToEquity' in latest.index and pd.notna(latest['debtToEquity']):
                de = float(latest['debtToEquity'])
                if de < 0.5:
                    score += 8
                elif de < 1:
                    score += 4
                elif de > 2:
                    score -= 8
            
            # EPS Growth (±7 điểm)
            if 'epsGrowth' in latest.index and pd.notna(latest['epsGrowth']):
                eps_growth = float(latest['epsGrowth'])
                if eps_growth > 20:
                    score += 7
                elif eps_growth > 10:
                    score += 4
                elif eps_growth < 0:
                    score -= 7
            
        except Exception as e:
            print(f"Lỗi khi tính điểm cơ bản: {str(e)}")
        
        # Giới hạn điểm trong khoảng 0-100
        score = max(0, min(100, score))
        return score
    
    def get_valuation_analysis(self):
        """Phân tích định giá"""
        analysis = {
            'valuation': 'TRUNG LẬP',
            'details': []
        }
        
        if self.ratios_data is None or self.ratios_data.empty:
            return analysis
        
        try:
            latest = self.ratios_data.iloc[0]
            
            # Phân tích P/E
            if 'pe' in latest.index and pd.notna(latest['pe']):
                pe = float(latest['pe'])
                if 0 < pe < 15:
                    analysis['details'].append(f"✅ P/E = {pe:.2f} (Định giá hấp dẫn)")
                elif 15 <= pe < 25:
                    analysis['details'].append(f"➖ P/E = {pe:.2f} (Định giá hợp lý)")
                elif pe >= 25:
                    analysis['details'].append(f"⚠️ P/E = {pe:.2f} (Định giá cao)")
            
            # Phân tích P/B
            if 'pb' in latest.index and pd.notna(latest['pb']):
                pb = float(latest['pb'])
                if 0 < pb < 1:
                    analysis['details'].append(f"✅ P/B = {pb:.2f} (Giá rẻ so với giá trị sổ sách)")
                elif 1 <= pb < 3:
                    analysis['details'].append(f"➖ P/B = {pb:.2f} (Hợp lý)")
                elif pb >= 3:
                    analysis['details'].append(f"⚠️ P/B = {pb:.2f} (Cao)")
            
            # Xác định định giá tổng thể
            score = self.calculate_score()
            if score > 65:
                analysis['valuation'] = 'HẤP DẪN'
            elif score < 40:
                analysis['valuation'] = 'ĐẮT'
            
        except Exception as e:
            print(f"Lỗi phân tích định giá: {str(e)}")
        
        return analysis
    
    def get_profitability_analysis(self):
        """Phân tích khả năng sinh lời"""
        analysis = {
            'profitability': 'TRUNG LẬP',
            'details': []
        }
        
        if self.ratios_data is None or self.ratios_data.empty:
            return analysis
        
        try:
            latest = self.ratios_data.iloc[0]
            
            # ROE
            if 'roe' in latest.index and pd.notna(latest['roe']):
                roe = float(latest['roe'])
                if roe > 15:
                    analysis['details'].append(f"✅ ROE = {roe:.2f}% (Tốt)")
                elif roe > 10:
                    analysis['details'].append(f"➖ ROE = {roe:.2f}% (Trung bình)")
                else:
                    analysis['details'].append(f"⚠️ ROE = {roe:.2f}% (Thấp)")
            
            # ROA
            if 'roa' in latest.index and pd.notna(latest['roa']):
                roa = float(latest['roa'])
                if roa > 5:
                    analysis['details'].append(f"✅ ROA = {roa:.2f}% (Tốt)")
                elif roa > 2:
                    analysis['details'].append(f"➖ ROA = {roa:.2f}% (Trung bình)")
                else:
                    analysis['details'].append(f"⚠️ ROA = {roa:.2f}% (Thấp)")
            
            # Profit Margin
            if 'profitMargin' in latest.index and pd.notna(latest['profitMargin']):
                margin = float(latest['profitMargin'])
                if margin > 10:
                    analysis['details'].append(f"✅ Biên lợi nhuận = {margin:.2f}% (Tốt)")
                elif margin > 5:
                    analysis['details'].append(f"➖ Biên lợi nhuận = {margin:.2f}% (Trung bình)")
                else:
                    analysis['details'].append(f"⚠️ Biên lợi nhuận = {margin:.2f}% (Thấp)")
            
            # Xác định khả năng sinh lời
            score = self.calculate_score()
            if score > 65:
                analysis['profitability'] = 'TỐT'
            elif score < 40:
                analysis['profitability'] = 'YẾU'
            
        except Exception as e:
            print(f"Lỗi phân tích sinh lời: {str(e)}")
        
        return analysis
    
    def get_financial_health(self):
        """Đánh giá sức khỏe tài chính"""
        health = {
            'status': 'TRUNG LẬP',
            'details': []
        }
        
        if self.ratios_data is None or self.ratios_data.empty:
            return health
        
        try:
            latest = self.ratios_data.iloc[0]
            
            # Debt to Equity
            if 'debtToEquity' in latest.index and pd.notna(latest['debtToEquity']):
                de = float(latest['debtToEquity'])
                if de < 0.5:
                    health['details'].append(f"✅ Nợ/Vốn CSH = {de:.2f} (Thấp, tốt)")
                elif de < 1:
                    health['details'].append(f"➖ Nợ/Vốn CSH = {de:.2f} (Trung bình)")
                else:
                    health['details'].append(f"⚠️ Nợ/Vốn CSH = {de:.2f} (Cao)")
            
            # Current Ratio
            if 'currentRatio' in latest.index and pd.notna(latest['currentRatio']):
                cr = float(latest['currentRatio'])
                if cr > 2:
                    health['details'].append(f"✅ Thanh khoản hiện hành = {cr:.2f} (Tốt)")
                elif cr > 1:
                    health['details'].append(f"➖ Thanh khoản hiện hành = {cr:.2f} (Chấp nhận được)")
                else:
                    health['details'].append(f"⚠️ Thanh khoản hiện hành = {cr:.2f} (Yếu)")
            
            # Quick Ratio
            if 'quickRatio' in latest.index and pd.notna(latest['quickRatio']):
                qr = float(latest['quickRatio'])
                if qr > 1:
                    health['details'].append(f"✅ Thanh khoản nhanh = {qr:.2f} (Tốt)")
                else:
                    health['details'].append(f"⚠️ Thanh khoản nhanh = {qr:.2f} (Cần cải thiện)")
            
            # Xác định sức khỏe tài chính
            good_indicators = sum(1 for detail in health['details'] if detail.startswith('✅'))
            bad_indicators = sum(1 for detail in health['details'] if detail.startswith('⚠️'))
            
            if good_indicators > bad_indicators:
                health['status'] = 'TỐT'
            elif bad_indicators > good_indicators:
                health['status'] = 'YẾU'
            
        except Exception as e:
            print(f"Lỗi đánh giá sức khỏe tài chính: {str(e)}")
        
        return health
    
    def get_growth_analysis(self):
        """Phân tích tăng trưởng"""
        growth = {
            'trend': 'ỔN ĐỊNH',
            'details': []
        }
        
        if self.ratios_data is None or len(self.ratios_data) < 2:
            return growth
        
        try:
            latest = self.ratios_data.iloc[0]
            
            # EPS Growth
            if 'epsGrowth' in latest.index and pd.notna(latest['epsGrowth']):
                eps_growth = float(latest['epsGrowth'])
                if eps_growth > 20:
                    growth['details'].append(f"✅ Tăng trưởng EPS = {eps_growth:.2f}% (Cao)")
                elif eps_growth > 0:
                    growth['details'].append(f"➖ Tăng trưởng EPS = {eps_growth:.2f}% (Dương)")
                else:
                    growth['details'].append(f"⚠️ Tăng trưởng EPS = {eps_growth:.2f}% (Âm)")
            
            # Revenue Growth
            if 'revenueGrowth' in latest.index and pd.notna(latest['revenueGrowth']):
                rev_growth = float(latest['revenueGrowth'])
                if rev_growth > 15:
                    growth['details'].append(f"✅ Tăng trưởng doanh thu = {rev_growth:.2f}% (Cao)")
                elif rev_growth > 0:
                    growth['details'].append(f"➖ Tăng trưởng doanh thu = {rev_growth:.2f}% (Dương)")
                else:
                    growth['details'].append(f"⚠️ Tăng trưởng doanh thu = {rev_growth:.2f}% (Âm)")
            
            # Xác định xu hướng tăng trưởng
            positive_growth = sum(1 for detail in growth['details'] if 'Cao' in detail or 'Dương' in detail)
            negative_growth = sum(1 for detail in growth['details'] if 'Âm' in detail)
            
            if positive_growth > 0 and negative_growth == 0:
                growth['trend'] = 'TĂNG TRƯỞNG'
            elif negative_growth > positive_growth:
                growth['trend'] = 'SUY GIẢM'
            
        except Exception as e:
            print(f"Lỗi phân tích tăng trưởng: {str(e)}")
        
        return growth

