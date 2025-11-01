"""
Module quản lý cache dữ liệu chứng khoán
"""

import os
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import time
from data_fetcher import DataFetcher

class DataCache:
    def __init__(self, cache_dir="data_cache"):
        """
        Khởi tạo cache manager
        
        Args:
            cache_dir: Thư mục lưu cache
        """
        self.cache_dir = cache_dir
        self.db_path = os.path.join(cache_dir, "stock_data.db")
        self.data_fetcher = DataFetcher()
        
        # Tạo thư mục cache nếu chưa có
        os.makedirs(cache_dir, exist_ok=True)
        
        # Khởi tạo database
        self._init_database()
    
    def _init_database(self):
        """Khởi tạo database SQLite"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Bảng lưu dữ liệu giá
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_price (
                symbol TEXT,
                date TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                PRIMARY KEY (symbol, date)
            )
        ''')
        
        # Bảng lưu thông tin cổ phiếu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_info (
                symbol TEXT PRIMARY KEY,
                name TEXT,
                exchange TEXT,
                listing_date TEXT,
                last_update TEXT,
                status TEXT
            )
        ''')
        
        # Bảng lưu chỉ số kỹ thuật
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS technical_indicators (
                symbol TEXT,
                date TEXT,
                sma_20 REAL,
                sma_50 REAL,
                sma_200 REAL,
                rsi REAL,
                macd REAL,
                macd_signal REAL,
                bb_high REAL,
                bb_low REAL,
                adx REAL,
                stoch_k REAL,
                PRIMARY KEY (symbol, date)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_all_symbols(self):
        """Lấy danh sách tất cả mã chứng khoán"""
        try:
            all_stocks = self.data_fetcher.get_all_stocks()
            if all_stocks is not None and not all_stocks.empty:
                return all_stocks
        except Exception as e:
            print(f"Error getting symbols: {e}")
        
        # Fallback: lấy từ database
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query("SELECT DISTINCT symbol FROM stock_info", conn)
        conn.close()
        return df
    
    def update_stock_info(self, symbols_df):
        """Cập nhật thông tin cơ bản các mã cổ phiếu"""
        conn = sqlite3.connect(self.db_path)
        
        for _, row in symbols_df.iterrows():
            symbol = row['symbol']
            name = row.get('organName', row.get('organ_name', symbol))
            exchange = row.get('exchange', 'HOSE')
            
            # Insert hoặc update
            conn.execute('''
                INSERT OR REPLACE INTO stock_info 
                (symbol, name, exchange, last_update, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (symbol, name, exchange, datetime.now().isoformat(), 'active'))
        
        conn.commit()
        conn.close()
        print(f"Updated info for {len(symbols_df)} stocks")
    
    def get_cached_data(self, symbol, start_date=None, end_date=None):
        """
        Lấy dữ liệu từ cache
        
        Args:
            symbol: Mã chứng khoán
            start_date: Ngày bắt đầu (YYYY-MM-DD)
            end_date: Ngày kết thúc (YYYY-MM-DD)
        """
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT * FROM stock_price WHERE symbol = ?"
        params = [symbol]
        
        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        
        query += " ORDER BY date"
        
        df = pd.read_sql_query(query, conn, params=params, parse_dates=['date'])
        conn.close()
        
        if not df.empty:
            df.set_index('date', inplace=True)
        
        return df
    
    def get_last_date(self, symbol):
        """Lấy ngày dữ liệu cuối cùng của mã cổ phiếu"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT MAX(date) FROM stock_price WHERE symbol = ?", 
            (symbol,)
        )
        result = cursor.fetchone()[0]
        conn.close()
        
        if result:
            return datetime.fromisoformat(result).date()
        return None
    
    def cache_stock_data(self, symbol, force_full_update=False):
        """
        Cache dữ liệu một mã cổ phiếu
        
        Args:
            symbol: Mã chứng khoán
            force_full_update: Có cập nhật toàn bộ dữ liệu không
        """
        try:
            # Xác định khoảng thời gian cần lấy
            if force_full_update:
                # Lấy từ 5 năm trước
                start_date = (datetime.now() - timedelta(days=5*365)).strftime('%Y-%m-%d')
                print(f"Full update {symbol} from {start_date}")
            else:
                # Lấy từ ngày cuối cùng có dữ liệu
                last_date = self.get_last_date(symbol)
                if last_date:
                    start_date = (last_date + timedelta(days=1)).strftime('%Y-%m-%d')
                    if start_date >= datetime.now().strftime('%Y-%m-%d'):
                        print(f"{symbol} is up to date")
                        return True
                else:
                    # Chưa có dữ liệu, lấy 2 năm
                    start_date = (datetime.now() - timedelta(days=2*365)).strftime('%Y-%m-%d')
                
                print(f"Incremental update {symbol} from {start_date}")
            
            # Lấy dữ liệu từ API
            end_date = datetime.now().strftime('%Y-%m-%d')
            stock_data = self.data_fetcher.get_stock_data(
                symbol, 
                period='MAX',  # Lấy tối đa
                start_date=start_date,
                end_date=end_date
            )
            
            if stock_data is None or stock_data.empty:
                print(f"No data for {symbol}")
                return False
            
            # Lưu vào database
            conn = sqlite3.connect(self.db_path)
            
            # Chuẩn bị dữ liệu
            stock_data_copy = stock_data.copy()
            stock_data_copy['symbol'] = symbol
            stock_data_copy['date'] = stock_data_copy.index.strftime('%Y-%m-%d')
            
            # Lưu dữ liệu giá
            stock_data_copy[['symbol', 'date', 'open', 'high', 'low', 'close', 'volume']].to_sql(
                'stock_price', conn, if_exists='append', index=False
            )
            
            conn.commit()
            conn.close()
            
            print(f"Cached {len(stock_data)} records for {symbol}")
            return True
            
        except Exception as e:
            print(f"Error caching {symbol}: {str(e)[:100]}")
            return False
    
    def bulk_cache_update(self, symbols_list=None, max_symbols=None, progress_callback=None):
        """
        Cập nhật cache hàng loạt
        
        Args:
            symbols_list: Danh sách mã cần cập nhật (None = tất cả)
            max_symbols: Giới hạn số lượng mã
            progress_callback: Callback báo tiến trình
        """
        if symbols_list is None:
            # Lấy tất cả mã từ thị trường
            all_stocks = self.get_all_symbols()
            if all_stocks.empty:
                print("No symbols found")
                return
            
            # Cập nhật thông tin cơ bản
            self.update_stock_info(all_stocks)
            
            symbols_list = all_stocks['symbol'].tolist()
        
        if max_symbols:
            symbols_list = symbols_list[:max_symbols]
        
        total = len(symbols_list)
        success_count = 0
        
        print(f"Starting bulk cache update for {total} symbols...")
        
        for idx, symbol in enumerate(symbols_list):
            try:
                if progress_callback:
                    progress_callback(idx + 1, total, f"Caching {symbol}...")
                
                success = self.cache_stock_data(symbol)
                if success:
                    success_count += 1
                
                # Delay để tránh rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error processing {symbol}: {e}")
                continue
        
        print(f"Bulk cache completed: {success_count}/{total} successful")
        return success_count
    
    def get_market_overview(self):
        """Tạo bảng tổng quan thị trường"""
        conn = sqlite3.connect(self.db_path)
        
        # Lấy dữ liệu mới nhất của tất cả mã
        query = '''
            SELECT 
                si.symbol,
                si.name,
                si.exchange,
                sp.close as current_price,
                sp.volume,
                sp.date as last_update
            FROM stock_info si
            LEFT JOIN (
                SELECT symbol, close, volume, date,
                       ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY date DESC) as rn
                FROM stock_price
            ) sp ON si.symbol = sp.symbol AND sp.rn = 1
            WHERE sp.close IS NOT NULL
            ORDER BY si.exchange, si.symbol
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df
    
    def get_stock_with_indicators(self, symbol, period_days=365):
        """
        Lấy dữ liệu cổ phiếu kèm chỉ báo kỹ thuật
        
        Args:
            symbol: Mã cổ phiếu
            period_days: Số ngày lấy dữ liệu
        """
        start_date = (datetime.now() - timedelta(days=period_days)).strftime('%Y-%m-%d')
        
        # Lấy dữ liệu từ cache
        df = self.get_cached_data(symbol, start_date=start_date)
        
        if df.empty:
            print(f"No cached data for {symbol}, fetching from API...")
            # Fallback: lấy từ API
            df = self.data_fetcher.get_stock_data(symbol, f"{period_days}D")
            if df is not None and not df.empty:
                # Cache lại
                self.cache_stock_data(symbol)
        
        return df
    
    def cleanup_old_data(self, days_to_keep=1095):  # 3 năm
        """Xóa dữ liệu cũ để tiết kiệm dung lượng"""
        cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).strftime('%Y-%m-%d')
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM stock_price WHERE date < ?", (cutoff_date,))
        cursor.execute("DELETE FROM technical_indicators WHERE date < ?", (cutoff_date,))
        
        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()
        
        print(f"Cleaned up {deleted_count} old records before {cutoff_date}")
        return deleted_count
    
    def get_cache_stats(self):
        """Thống kê cache"""
        conn = sqlite3.connect(self.db_path)
        
        stats = {}
        
        # Số lượng mã cổ phiếu
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(DISTINCT symbol) FROM stock_price")
        stats['total_symbols'] = cursor.fetchone()[0]
        
        # Tổng số records
        cursor.execute("SELECT COUNT(*) FROM stock_price")
        stats['total_records'] = cursor.fetchone()[0]
        
        # Ngày cũ nhất và mới nhất
        cursor.execute("SELECT MIN(date), MAX(date) FROM stock_price")
        result = cursor.fetchone()
        stats['date_range'] = f"{result[0]} to {result[1]}"
        
        # Kích thước database
        stats['db_size_mb'] = round(os.path.getsize(self.db_path) / (1024*1024), 2)
        
        conn.close()
        
        return stats

