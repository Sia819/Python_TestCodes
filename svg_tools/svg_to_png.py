#!/usr/bin/env python3
"""
SVG를 PNG로 변환하는 도구
cairosvg 또는 Pillow + svglib 사용
"""

import os
import sys
import subprocess

def check_and_install_libraries():
    """필요한 라이브러리 확인 및 설치"""
    libraries = {
        'cairosvg': 'cairosvg',
        'PIL': 'pillow',
        'svglib': 'svglib',
        'reportlab': 'reportlab'
    }
    
    missing = []
    for lib, pip_name in libraries.items():
        try:
            __import__(lib)
        except ImportError:
            missing.append(pip_name)
    
    if missing:
        print("필요한 라이브러리가 설치되어 있지 않습니다.")
        print(f"다음 명령어로 설치하세요: pip install {' '.join(missing)}")
        return False
    return True

def convert_with_cairosvg(svg_path, png_path, width=None, height=None):
    """CairoSVG를 사용한 변환"""
    try:
        import cairosvg
        print("CairoSVG를 사용하여 변환 중...")
        cairosvg.svg2png(
            url=svg_path, 
            write_to=png_path,
            output_width=width,
            output_height=height
        )
        return True
    except Exception as e:
        print(f"CairoSVG 변환 실패: {e}")
        return False

def convert_with_svglib(svg_path, png_path, width=None, height=None):
    """svglib + reportlab + Pillow를 사용한 변환"""
    try:
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPM
        from PIL import Image
        
        print("svglib를 사용하여 변환 중...")
        drawing = svg2rlg(svg_path)
        renderPM.drawToFile(drawing, png_path, fmt="PNG")
        
        # 크기 조정이 필요한 경우
        if width or height:
            img = Image.open(png_path)
            if width and height:
                img = img.resize((width, height), Image.Resampling.LANCZOS)
            img.save(png_path)
        
        return True
    except Exception as e:
        print(f"svglib 변환 실패: {e}")
        return False

def convert_with_inkscape(svg_path, png_path, width=None, height=None):
    """Inkscape 명령줄 도구를 사용한 변환"""
    try:
        print("Inkscape를 사용하여 변환 중...")
        cmd = ['inkscape', svg_path, '--export-type=png', f'--export-filename={png_path}']
        
        if width:
            cmd.extend(['--export-width', str(width)])
        if height:
            cmd.extend(['--export-height', str(height)])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            print(f"Inkscape 변환 실패: {result.stderr}")
            return False
    except FileNotFoundError:
        print("Inkscape가 설치되어 있지 않습니다.")
        return False

def convert_with_imagemagick(svg_path, png_path, width=None, height=None):
    """ImageMagick을 사용한 변환"""
    try:
        print("ImageMagick을 사용하여 변환 중...")
        cmd = ['convert']
        
        if width and height:
            cmd.extend(['-density', '300', '-resize', f'{width}x{height}'])
        
        cmd.extend([svg_path, png_path])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            print(f"ImageMagick 변환 실패: {result.stderr}")
            return False
    except FileNotFoundError:
        print("ImageMagick이 설치되어 있지 않습니다.")
        return False

def svg_to_png(svg_path, png_path=None, width=None, height=None):
    """SVG를 PNG로 변환 (여러 방법 시도)"""
    if not os.path.exists(svg_path):
        print(f"SVG 파일을 찾을 수 없습니다: {svg_path}")
        return False
    
    if png_path is None:
        png_path = svg_path.replace('.svg', '.png')
    
    print(f"변환 중: {svg_path} -> {png_path}")
    
    # Python 라이브러리 방법 시도
    if check_and_install_libraries():
        # CairoSVG 시도
        if convert_with_cairosvg(svg_path, png_path, width, height):
            print(f"✅ 변환 성공: {png_path}")
            return True
        
        # svglib 시도
        if convert_with_svglib(svg_path, png_path, width, height):
            print(f"✅ 변환 성공: {png_path}")
            return True
    
    # 외부 프로그램 시도
    if convert_with_inkscape(svg_path, png_path, width, height):
        print(f"✅ 변환 성공: {png_path}")
        return True
    
    if convert_with_imagemagick(svg_path, png_path, width, height):
        print(f"✅ 변환 성공: {png_path}")
        return True
    
    print("\n❌ 변환 실패. 다음 중 하나를 설치하세요:")
    print("1. Python 라이브러리: pip install cairosvg")
    print("2. Inkscape: https://inkscape.org/")
    print("3. ImageMagick: https://imagemagick.org/")
    
    return False

def main():
    """메인 함수"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SVG를 PNG로 변환')
    parser.add_argument('svg_file', nargs='?', default='../Images/Icon_1000x1000_profile.svg',
                        help='변환할 SVG 파일 경로')
    parser.add_argument('-o', '--output', help='출력 PNG 파일 경로')
    parser.add_argument('-w', '--width', type=int, help='출력 너비')
    parser.add_argument('--height', type=int, help='출력 높이')
    parser.add_argument('-s', '--size', type=int, help='정사각형 크기 (너비와 높이 동일)')
    
    args = parser.parse_args()
    
    # 크기 설정
    width = args.width
    height = args.height
    if args.size:
        width = height = args.size
    
    # 변환 실행
    success = svg_to_png(args.svg_file, args.output, width, height)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()