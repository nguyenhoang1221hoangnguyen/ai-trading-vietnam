# 📈 AI Trading - Ứng dụng hỗ trợ đầu tư chứng khoán Việt Nam

Ứng dụng phân tích chứng khoán thông minh sử dụng AI và Machine Learning để hỗ trợ nhà đầu tư ra quyết định đầu tư tốt hơn trên thị trường chứng khoán Việt Nam.

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎯 Tính năng chính

### 1. Phân tích mã chứng khoán chi tiết
- ✅ **Phân tích kỹ thuật** với hơn 10 chỉ báo chuyên nghiệp
- ✅ **Phân tích cơ bản** về tài chính doanh nghiệp
- ✅ **Tín hiệu mua/bán** tự động dựa trên thuật toán AI
- ✅ **Xác định điểm vào/thoát lệnh** tối ưu
- ✅ **Tính toán Risk/Reward Ratio**
- ✅ **Biểu đồ nến tương tác** với đầy đủ chỉ báo kỹ thuật

### 2. 🌍 Quét toàn bộ thị trường (TÍNH NĂNG MỚI!)
- 🖥️ **Quét qua giao diện web**: Không cần terminal, tất cả qua UI thân thiện
- 📊 **Quét 1700+ mã**: Toàn bộ thị trường Việt Nam (HOSE, HNX, UPCOM)
- ⏱️ **Tiến độ real-time**: Progress bar, logs, metrics thành công/thất bại
- ⚙️ **Cài đặt linh hoạt**: Batch size, delay, số lượng mã tùy chỉnh
- 💾 **Cache thông minh**: Lưu trữ dữ liệu, tránh tải lại không cần thiết
- 🎯 **Lọc theo tiêu chí kỹ thuật** tùy chỉnh
- 🚀 **Tìm cổ phiếu breakout** (đột phá)
- 📉 **Tìm cổ phiếu quá bán** (oversold)

### 3. 📈 Market Overview - Tổng quan thị trường
- 🔍 **Market Scanner**: Quét và phân tích hàng trăm mã trong vài giây
- 🏆 **Top Performers**: Xếp hạng theo nhiều tiêu chí (tổng thể, tháng, quý, kỹ thuật)
- 📊 **Market Analysis**: Lọc thông minh với bộ lọc đa tiêu chí
- 📁 **Export Excel**: Xuất dữ liệu để phân tích offline
- ⚙️ **Cache Management**: Quản lý dữ liệu thông minh

### 4. Hỗ trợ đa khung thời gian đầu tư
- 📅 **Ngắn hạn** (1-3 tháng): Dựa vào tín hiệu kỹ thuật
- 📆 **Trung hạn** (3-12 tháng): Kết hợp kỹ thuật và xu hướng
- 📅 **Dài hạn** (> 1 năm): Tập trung vào cơ bản doanh nghiệp

## 📊 Chỉ số kỹ thuật

Ứng dụng sử dụng các chỉ số kỹ thuật phổ biến và hiệu quả:

- **RSI** (Relative Strength Index): Đo lường động lượng và xác định vùng quá mua/quá bán
- **MACD** (Moving Average Convergence Divergence): Xác định xu hướng và điểm đảo chiều
- **Bollinger Bands**: Đo biến động và xác định support/resistance động
- **Moving Averages**: SMA 20, 50, 200 cho xu hướng ngắn/trung/dài hạn
- **ADX** (Average Directional Index): Đo sức mạnh xu hướng
- **Stochastic Oscillator**: Xác định động lượng giá
- **Volume Analysis**: Phân tích khối lượng giao dịch

## 💼 Phân tích cơ bản

Đánh giá sức khỏe tài chính doanh nghiệp:

- **P/E Ratio**: Định giá so với thu nhập
- **P/B Ratio**: Định giá so với giá trị sổ sách
- **ROE**: Lợi nhuận trên vốn chủ sở hữu
- **ROA**: Lợi nhuận trên tổng tài sản
- **Debt to Equity**: Tỷ lệ nợ
- **Profit Margin**: Biên lợi nhuận
- **EPS Growth**: Tăng trưởng lợi nhuận

## 🚀 Cài đặt

### Yêu cầu hệ thống
- Python 3.8 trở lên
- pip hoặc conda
- Kết nối Internet

### Các bước cài đặt

1. **Clone repository hoặc tải xuống mã nguồn**

```bash
git clone https://github.com/yourusername/ai-trading.git
cd ai-trading
```

2. **Cài đặt các thư viện cần thiết**

```bash
pip install -r requirements.txt
```

3. **Chạy ứng dụng**

```bash
streamlit run app.py
```

4. **Mở trình duyệt**

Ứng dụng sẽ tự động mở tại: `http://localhost:8501`

## 📖 Hướng dẫn sử dụng

### 1. Phân tích mã chứng khoán

1. Chọn **"📊 Phân tích mã CK"** từ menu bên trái
2. Nhập mã chứng khoán (ví dụ: VNM, FPT, VIC)
3. Chọn khung thời gian phân tích (1M, 3M, 6M, 1Y, 3Y, 5Y)
4. Nhấn **"🔍 Phân tích"**
5. Xem kết quả phân tích chi tiết:
   - Thông tin công ty
   - Tín hiệu đầu tư tổng hợp
   - Xu hướng và khung thời gian phù hợp
   - Tín hiệu kỹ thuật chi tiết
   - Điểm vào/thoát lệnh
   - Tỷ lệ Risk/Reward
   - Phân tích cơ bản
   - Biểu đồ kỹ thuật tương tác

### 2. 🌍 Quét toàn bộ thị trường (TÍNH NĂNG MỚI!)

#### Market Overview - Tổng quan thị trường
1. Chọn **"📈 Tổng quan thị trường"** từ menu chính
2. Sử dụng 4 tab chính:

**🔍 Market Scanner**
- Quét nhanh 50-200 mã chứng khoán
- Hiển thị kết quả trong vài giây
- Xem tổng quan điểm số và tín hiệu

**🏆 Top Performers**  
- Xem top cổ phiếu theo nhiều tiêu chí:
  - Tổng thể (Overall)
  - Tăng trưởng tháng (Monthly)
  - Tăng trưởng quý (Quarterly)
  - Điểm kỹ thuật (Technical)
  - Rủi ro thấp (Low Risk)
  - Khối lượng cao (High Volume)

**📊 Market Analysis**
- Lọc thông minh với bộ lọc đa tiêu chí:
  - Điểm tối thiểu
  - Tín hiệu (MUA MẠNH, MUA, GIỮ, BÁN, BÁN MẠNH)
  - RSI Range (20-80)
  - Tỷ lệ khối lượng
  - Tăng trưởng tháng
  - Xu hướng
- Export Excel kết quả lọc hoặc toàn bộ dữ liệu

**⚙️ Cache Management**
- **Quét toàn bộ thị trường qua giao diện**:
  1. Cài đặt batch size (10-50 mã)
  2. Cài đặt delay (5-30 giây)
  3. Chọn số batch tối đa
  4. Nhấn **"🚀 Bắt đầu quét toàn bộ thị trường"**
  5. Theo dõi tiến độ real-time
  6. Có thể dừng bất kỳ lúc nào

### 3. Tìm kiếm cổ phiếu tiềm năng (Phương pháp cũ)

#### Quét thị trường
1. Chọn **"🔎 Tìm kiếm CK tiềm năng"**
2. Tab **"🎯 Quét thị trường"**
3. Chọn loại đầu tư: Ngắn hạn / Trung hạn / Dài hạn
4. Chọn số lượng cổ phiếu muốn tìm
5. Nhấn **"🚀 Bắt đầu quét"**
6. Xem danh sách cổ phiếu được đề xuất

#### Lọc theo tiêu chí
1. Tab **"📊 Lọc theo tiêu chí"**
2. Thiết lập các tiêu chí:
   - Khoảng RSI
   - Xu hướng
   - Khối lượng tăng đột biến
3. Nhấn **"🔍 Lọc"**

#### Tìm cổ phiếu đặc biệt
1. Tab **"🚀 Cổ phiếu đặc biệt"**
2. Chọn:
   - **Breakout**: Cổ phiếu đang đột phá
   - **Quá bán**: Cơ hội mua vào

## 🏗️ Cấu trúc dự án

```
ai-trading/
├── app.py                      # File chính - giao diện Streamlit
├── config.py                   # Cấu hình chỉ số và thông số
├── data_fetcher.py            # Module lấy dữ liệu từ vnstock
├── technical_analysis.py      # Module phân tích kỹ thuật
├── fundamental_analysis.py    # Module phân tích cơ bản
├── trading_signals.py         # Module tạo tín hiệu mua/bán
├── stock_screener.py          # Module quét và lọc cổ phiếu (cũ)
├── data_cache.py              # Module cache dữ liệu SQLite (MỚI)
├── cached_stock_screener.py   # Module quét thị trường với cache (MỚI)
├── cache_manager.py           # Script quản lý cache terminal (MỚI)
├── gradual_update.py          # Script cập nhật dần dần thị trường (MỚI)
├── requirements.txt           # Danh sách thư viện
└── README.md                  # Tài liệu hướng dẫn
```

## 🔧 Công nghệ sử dụng

- **Python 3.8+**: Ngôn ngữ lập trình chính
- **Streamlit**: Framework xây dựng giao diện web
- **vnstock3**: Thư viện lấy dữ liệu thị trường Việt Nam
- **Pandas**: Xử lý và phân tích dữ liệu
- **NumPy**: Tính toán số học
- **TA-Lib (ta)**: Các chỉ báo kỹ thuật
- **Plotly**: Biểu đồ tương tác
- **SciPy**: Tính toán khoa học

## ⚠️ Lưu ý quan trọng

1. **Không phải lời khuyên đầu tư**: Ứng dụng này chỉ là công cụ hỗ trợ phân tích, không phải lời khuyên đầu tư tài chính. Bạn cần tự nghiên cứu và đánh giá rủi ro.

2. **Dữ liệu có độ trễ**: Dữ liệu từ vnstock có thể có độ trễ vài phút so với thời gian thực.

3. **Rủi ro thị trường**: Thị trường chứng khoán có rủi ro cao. Chỉ đầu tư số tiền bạn có thể chấp nhận mất.

4. **Kết hợp nhiều yếu tố**: Nên kết hợp phân tích kỹ thuật, phân tích cơ bản và tin tức thị trường để đưa ra quyết định tốt nhất.

5. **Backtest**: Luôn kiểm tra lại chiến lược với dữ liệu lịch sử trước khi áp dụng thực tế.

## 💡 Tips sử dụng hiệu quả

1. **Đầu tư ngắn hạn**: Tập trung vào tín hiệu kỹ thuật và khối lượng giao dịch
2. **Đầu tư trung hạn**: Kết hợp tín hiệu kỹ thuật và xu hướng thị trường
3. **Đầu tư dài hạn**: Ưu tiên phân tích cơ bản và chọn công ty có nền tảng vững chắc
4. **Risk Management**: Luôn đặt lệnh cắt lỗ (stop loss) để bảo vệ vốn
5. **Diversification**: Đa dạng hóa danh mục để giảm rủi ro
6. **Patience**: Kiên nhẫn chờ đợi tín hiệu phù hợp trước khi vào lệnh

## 🐛 Báo lỗi và đóng góp

Nếu bạn phát hiện lỗi hoặc muốn đóng góp cải thiện ứng dụng:

1. Mở issue trên GitHub
2. Tạo pull request với mô tả chi tiết
3. Liên hệ qua email: your.email@example.com

## 📝 Changelog

### Version 1.0.0 (2025-11-01)
- ✅ Phát hành phiên bản đầu tiên
- ✅ Phân tích kỹ thuật đầy đủ
- ✅ Phân tích cơ bản
- ✅ Tìm kiếm cổ phiếu tiềm năng
- ✅ Giao diện người dùng đẹp mắt

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết.

## 🙏 Cảm ơn

- [vnstock3](https://github.com/thinh-vu/vnstock) - Thư viện dữ liệu chứng khoán Việt Nam
- [Streamlit](https://streamlit.io/) - Framework giao diện web
- [TA-Lib](https://github.com/mrjbq7/ta-lib) - Thư viện phân tích kỹ thuật

---

**Chúc bạn đầu tư thành công! 🚀📈**

*Lưu ý: Hãy luôn đầu tư có trách nhiệm và chỉ sử dụng số tiền bạn có thể chấp nhận mất.*

