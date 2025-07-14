#!/usr/bin/env python3
"""
SVG 파일을 HTML로 표시하는 뷰어 생성
"""

import os
import sys

def create_svg_viewer(svg_files, output_html="svg_viewer.html"):
    """여러 SVG 파일을 비교할 수 있는 HTML 뷰어 생성"""
    
    # SVG 파일들 읽기
    svg_contents = []
    for svg_file in svg_files:
        if os.path.exists(svg_file):
            with open(svg_file, 'r', encoding='utf-8') as f:
                content = f.read()
                svg_contents.append({
                    'filename': os.path.basename(svg_file),
                    'path': svg_file,
                    'content': content
                })
        else:
            print(f"파일을 찾을 수 없습니다: {svg_file}")
    
    if not svg_contents:
        print("표시할 SVG 파일이 없습니다.")
        return False
    
    # HTML 생성
    html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SVG Viewer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f0f0f0;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .svg-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .svg-item {
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .svg-title {
            font-weight: bold;
            margin-bottom: 10px;
            text-align: center;
            color: #333;
        }
        .svg-container {
            border: 1px solid #ddd;
            border-radius: 4px;
            overflow: hidden;
            position: relative;
            background: #fafafa;
        }
        .svg-container svg {
            display: block;
            width: 100%;
            height: auto;
        }
        .circle-overlay {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 98%;
            height: 98%;
            border: 2px dashed #ff0000;
            border-radius: 50%;
            pointer-events: none;
            display: none;
        }
        .show-circle .circle-overlay {
            display: block;
        }
        .controls {
            margin-top: 10px;
            text-align: center;
        }
        .controls button {
            padding: 5px 15px;
            margin: 0 5px;
            cursor: pointer;
            border: 1px solid #ddd;
            border-radius: 4px;
            background: white;
        }
        .controls button:hover {
            background: #f0f0f0;
        }
        .info {
            margin-top: 10px;
            font-size: 12px;
            color: #666;
            text-align: center;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        .compare-mode {
            text-align: center;
            margin: 20px 0;
        }
        .compare-mode label {
            margin-right: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>SVG Viewer</h1>
        
        <div class="compare-mode">
            <label>
                <input type="checkbox" id="showCircles" onchange="toggleCircles()">
                원형 프로필 가이드 표시
            </label>
            <label>
                배경색: 
                <select id="bgColor" onchange="changeBgColor()">
                    <option value="#fafafa">밝은 회색</option>
                    <option value="#ffffff">흰색</option>
                    <option value="#000000">검은색</option>
                    <option value="#1a1a1a">어두운 회색</option>
                    <option value="#13aefe">파란색</option>
                </select>
            </label>
        </div>
        
        <div class="svg-grid">
"""
    
    # 각 SVG 아이템 추가
    for i, svg_data in enumerate(svg_contents):
        html_content += f"""
            <div class="svg-item">
                <div class="svg-title">{svg_data['filename']}</div>
                <div class="svg-container" id="container-{i}">
                    {svg_data['content']}
                    <div class="circle-overlay"></div>
                </div>
                <div class="controls">
                    <button onclick="downloadSVG({i})">SVG 다운로드</button>
                    <button onclick="downloadPNG({i})">PNG 다운로드</button>
                </div>
                <div class="info">{svg_data['path']}</div>
            </div>
"""
    
    html_content += """
        </div>
    </div>
    
    <script>
        // SVG 데이터 저장
        const svgData = """ + str([{
            'filename': d['filename'],
            'content': d['content'].replace('\n', '\\n').replace('"', '\\"')
        } for d in svg_contents]) + """;
        
        function toggleCircles() {
            const containers = document.querySelectorAll('.svg-container');
            const showCircles = document.getElementById('showCircles').checked;
            
            containers.forEach(container => {
                if (showCircles) {
                    container.classList.add('show-circle');
                } else {
                    container.classList.remove('show-circle');
                }
            });
        }
        
        function changeBgColor() {
            const color = document.getElementById('bgColor').value;
            const containers = document.querySelectorAll('.svg-container');
            
            containers.forEach(container => {
                container.style.backgroundColor = color;
            });
        }
        
        function downloadSVG(index) {
            const data = svgData[index];
            const blob = new Blob([data.content], {type: 'image/svg+xml'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = data.filename;
            a.click();
            URL.revokeObjectURL(url);
        }
        
        function downloadPNG(index) {
            const container = document.getElementById(`container-${index}`);
            const svg = container.querySelector('svg');
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            // SVG 크기 가져오기
            const box = svg.viewBox.baseVal;
            canvas.width = box.width || 1000;
            canvas.height = box.height || 1000;
            
            // SVG를 문자열로 변환
            const svgString = new XMLSerializer().serializeToString(svg);
            const svgBlob = new Blob([svgString], {type: 'image/svg+xml;charset=utf-8'});
            const url = URL.createObjectURL(svgBlob);
            
            const img = new Image();
            img.onload = function() {
                ctx.drawImage(img, 0, 0);
                URL.revokeObjectURL(url);
                
                canvas.toBlob(function(blob) {
                    const pngUrl = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = pngUrl;
                    a.download = svgData[index].filename.replace('.svg', '.png');
                    a.click();
                    URL.revokeObjectURL(pngUrl);
                });
            };
            img.src = url;
        }
    </script>
</body>
</html>
"""
    
    # HTML 파일 저장
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ SVG 뷰어가 생성되었습니다: {output_html}")
    print(f"   표시된 파일 수: {len(svg_contents)}개")
    return True

def main():
    # 기본 SVG 파일 목록
    default_files = [
        '../Images/Icon_1000x1000_profile.svg',
        '../Images/Icon_WithoutTail_1000x1000_profile.svg',
        '../Images/Icon_WithoutTail_1000x1000_profile2.svg'
    ]
    
    # 명령줄 인수가 있으면 사용, 없으면 기본값
    if len(sys.argv) > 1:
        svg_files = sys.argv[1:]
    else:
        svg_files = default_files
    
    # 실제 존재하는 파일만 필터링
    existing_files = [f for f in svg_files if os.path.exists(f)]
    
    if not existing_files:
        print("표시할 SVG 파일이 없습니다.")
        print("사용법: python svg_viewer.py [svg파일1] [svg파일2] ...")
        return
    
    output_html = '../svg_viewer.html'
    create_svg_viewer(existing_files, output_html)

if __name__ == "__main__":
    main()