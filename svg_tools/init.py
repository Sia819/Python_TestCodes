#!/usr/bin/env python3
"""
SVG 변환 도구 초기화 스크립트
다른 세션에서 /Init 명령으로 실행 가능
"""

import os
import sys

def init_svg_tools():
    """SVG 변환 도구 환경 초기화"""
    print("SVG 변환 도구 초기화 중...")
    print("=" * 50)
    
    # 필요한 파일들이 있는지 확인
    required_files = [
        'svg_tools.py',
        'README_SVG_TOOLS.md'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("⚠️  다음 파일들이 없습니다:")
        for file in missing_files:
            print(f"   - {file}")
        print("\n필요한 파일들을 생성하거나 복사해주세요.")
        return False
    
    print("✅ 필수 파일 확인 완료")
    
    # SVG 파일 확인
    svg_files = [f for f in os.listdir('.') if f.endswith('.svg')]
    if svg_files:
        print(f"\n📁 발견된 SVG 파일: {len(svg_files)}개")
        for svg in svg_files[:5]:  # 최대 5개만 표시
            print(f"   - {svg}")
        if len(svg_files) > 5:
            print(f"   ... 외 {len(svg_files) - 5}개")
    else:
        print("\n📁 SVG 파일이 없습니다.")
    
    # 사용 가능한 명령어 안내
    print("\n🛠️  사용 가능한 명령어:")
    print("   python3 svg_tools.py      - 대화형 도구 실행")
    print("   python3 resize_svg.py     - SVG 크기 조정")
    print("   python3 scale_symbol.py   - 심볼 확대 및 중앙 정렬")
    print("   python3 reverse_svg_path.py - 패스 방향 변환")
    
    print("\n📖 자세한 사용법은 README_SVG_TOOLS.md를 참조하세요.")
    
    # 빠른 시작 옵션
    print("\n🚀 빠른 시작:")
    print("1. 전체 변환 프로세스 실행 (Icon.svg -> 1000x1000 -> 850x850 심볼)")
    print("2. 대화형 도구 실행")
    print("3. README 보기")
    print("4. 종료")
    
    choice = input("\n선택 (1-4): ")
    
    if choice == '1':
        if os.path.exists('Icon.svg'):
            print("\n전체 변환 프로세스를 시작합니다...")
            os.system('python3 svg_tools.py')
            # 자동으로 옵션 4 선택
            import subprocess
            subprocess.run(['python3', 'svg_tools.py'], input='4\n', text=True)
        else:
            print("Icon.svg 파일을 찾을 수 없습니다.")
    
    elif choice == '2':
        os.system('python3 svg_tools.py')
    
    elif choice == '3':
        if os.path.exists('README_SVG_TOOLS.md'):
            with open('README_SVG_TOOLS.md', 'r', encoding='utf-8') as f:
                print(f.read())
        else:
            print("README 파일을 찾을 수 없습니다.")
    
    print("\n✅ SVG 변환 도구 초기화 완료!")
    return True

if __name__ == "__main__":
    init_svg_tools()