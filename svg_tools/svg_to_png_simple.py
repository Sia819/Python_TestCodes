#!/usr/bin/env python3
"""
SVG를 PNG로 변환하는 간단한 도구
웹 서비스 또는 base64 인코딩 사용
"""

import os
import sys
import base64
import json

def svg_to_png_data_uri(svg_path, output_path=None, size=1000):
    """SVG를 읽어서 PNG 변환을 위한 HTML 생성"""
    if not os.path.exists(svg_path):
        print(f"SVG 파일을 찾을 수 없습니다: {svg_path}")
        return False
    
    if output_path is None:
        output_path = svg_path.replace('.svg', '.png')
    
    # SVG 파일 읽기
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()
    
    # HTML 파일 생성 (Canvas를 사용한 변환)
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>SVG to PNG Converter</title>
</head>
<body>
    <h2>SVG to PNG 변환 도구</h2>
    <p>1. 아래 이미지를 우클릭하여 "이미지로 저장"을 선택하세요.</p>
    <p>2. 파일명: {os.path.basename(output_path)}</p>
    
    <div id="container" style="border: 1px solid #ccc; display: inline-block;">
        <!-- Original SVG (hidden) -->
        <div id="svg-container" style="display: none;">
            {svg_content}
        </div>
        
        <!-- Canvas for PNG -->
        <canvas id="canvas" width="{size}" height="{size}"></canvas>
    </div>
    
    <br><br>
    <button onclick="downloadPNG()">PNG로 다운로드</button>
    
    <script>
        window.onload = function() {{
            const svgElement = document.querySelector('#svg-container svg');
            const canvas = document.getElementById('canvas');
            const ctx = canvas.getContext('2d');
            
            // SVG를 문자열로 변환
            const svgString = new XMLSerializer().serializeToString(svgElement);
            
            // SVG를 data URL로 변환
            const svgBlob = new Blob([svgString], {{type: 'image/svg+xml;charset=utf-8'}});
            const url = URL.createObjectURL(svgBlob);
            
            // Image 객체 생성
            const img = new Image();
            img.onload = function() {{
                ctx.drawImage(img, 0, 0, {size}, {size});
                URL.revokeObjectURL(url);
            }};
            img.src = url;
        }};
        
        function downloadPNG() {{
            const canvas = document.getElementById('canvas');
            const link = document.createElement('a');
            link.download = '{os.path.basename(output_path)}';
            link.href = canvas.toDataURL();
            link.click();
        }}
    </script>
</body>
</html>"""
    
    # HTML 파일 저장
    html_path = output_path.replace('.png', '_converter.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 변환 도구가 생성되었습니다: {html_path}")
    print(f"브라우저에서 열어 PNG로 저장하세요.")
    
    # 추가로 변환 명령 스크립트 생성
    create_conversion_script(svg_path, output_path, size)
    
    return True

def create_conversion_script(svg_path, png_path, size):
    """다양한 변환 명령어를 포함한 스크립트 생성"""
    script_content = f"""#!/bin/bash
# SVG to PNG 변환 스크립트
# 생성된 파일: {os.path.basename(png_path)}

echo "SVG to PNG 변환 옵션:"
echo "====================="

# 옵션 1: CairoSVG (Python)
echo "1. CairoSVG 사용:"
echo "   pip install cairosvg"
echo "   python3 -c 'import cairosvg; cairosvg.svg2png(url=\"{svg_path}\", write_to=\"{png_path}\", output_width={size}, output_height={size})'"
echo ""

# 옵션 2: Inkscape
echo "2. Inkscape 사용:"
echo "   inkscape {svg_path} --export-type=png --export-filename={png_path} --export-width={size} --export-height={size}"
echo ""

# 옵션 3: ImageMagick
echo "3. ImageMagick 사용:"
echo "   convert -density 300 -resize {size}x{size} {svg_path} {png_path}"
echo ""

# 옵션 4: rsvg-convert (librsvg)
echo "4. rsvg-convert 사용:"
echo "   rsvg-convert -w {size} -h {size} {svg_path} -o {png_path}"
echo ""

# 옵션 5: Chrome/Chromium headless
echo "5. Chrome Headless 사용:"
echo "   google-chrome --headless --disable-gpu --screenshot={png_path} --window-size={size},{size} {svg_path}"
echo ""

echo "위 명령어 중 하나를 선택하여 실행하세요."
"""
    
    script_path = png_path.replace('.png', '_convert.sh')
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    os.chmod(script_path, 0o755)
    print(f"✅ 변환 스크립트가 생성되었습니다: {script_path}")

def main():
    """메인 함수"""
    if len(sys.argv) > 1:
        svg_file = sys.argv[1]
    else:
        svg_file = '../Images/Icon_1000x1000_profile.svg'
    
    output_file = svg_file.replace('.svg', '.png')
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    size = 1000
    if len(sys.argv) > 3:
        size = int(sys.argv[3])
    
    print(f"SVG 파일: {svg_file}")
    print(f"출력 PNG: {output_file}")
    print(f"크기: {size}x{size}")
    print("")
    
    svg_to_png_data_uri(svg_file, output_file, size)

if __name__ == "__main__":
    main()