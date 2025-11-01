#!/usr/bin/env python3
"""
Script để chuyển đổi giữa Demo Mode và Real Data Mode
"""

import os
import sys
import argparse

def set_demo_mode(enable=True):
    """Bật/tắt demo mode"""
    if enable:
        os.environ['FORCE_DEMO_MODE'] = 'true'
        print("✅ Demo Mode được BẬT")
        print("   - Ứng dụng sẽ sử dụng dữ liệu mẫu")
        print("   - Không cần kết nối API thực tế")
        print("   - Phù hợp để demo hoặc test")
    else:
        os.environ['FORCE_DEMO_MODE'] = 'false'
        print("✅ Real Data Mode được BẬT")
        print("   - Ứng dụng sẽ sử dụng dữ liệu thật từ vnstock API")
        print("   - Cần kết nối internet ổn định")
        print("   - Dữ liệu cập nhật theo thời gian thực")

def get_current_mode():
    """Kiểm tra mode hiện tại"""
    demo_mode = os.getenv('FORCE_DEMO_MODE', 'false').lower() == 'true'
    if demo_mode:
        return "Demo Mode"
    else:
        return "Real Data Mode"

def main():
    parser = argparse.ArgumentParser(description='Chuyển đổi giữa Demo Mode và Real Data Mode')
    parser.add_argument('--mode', choices=['demo', 'real'], 
                       help='Chọn mode: demo (dữ liệu mẫu) hoặc real (dữ liệu thật)')
    parser.add_argument('--status', action='store_true', 
                       help='Hiển thị trạng thái hiện tại')
    
    args = parser.parse_args()
    
    if args.status:
        current_mode = get_current_mode()
        print(f"📊 Trạng thái hiện tại: {current_mode}")
        return
    
    if args.mode == 'demo':
        set_demo_mode(True)
    elif args.mode == 'real':
        set_demo_mode(False)
    else:
        # Interactive mode
        print("🔧 AI Trading - Mode Switcher")
        print("=" * 40)
        print(f"Trạng thái hiện tại: {get_current_mode()}")
        print()
        print("Chọn mode:")
        print("1. Demo Mode (dữ liệu mẫu)")
        print("2. Real Data Mode (dữ liệu thật)")
        print("3. Hiển thị trạng thái")
        print("0. Thoát")
        
        while True:
            try:
                choice = input("\nNhập lựa chọn (0-3): ").strip()
                
                if choice == '1':
                    set_demo_mode(True)
                    break
                elif choice == '2':
                    set_demo_mode(False)
                    break
                elif choice == '3':
                    print(f"Trạng thái hiện tại: {get_current_mode()}")
                elif choice == '0':
                    print("👋 Thoát chương trình")
                    break
                else:
                    print("❌ Lựa chọn không hợp lệ. Vui lòng nhập 0-3.")
                    
            except KeyboardInterrupt:
                print("\n👋 Thoát chương trình")
                break
            except Exception as e:
                print(f"❌ Lỗi: {e}")

if __name__ == "__main__":
    main()
