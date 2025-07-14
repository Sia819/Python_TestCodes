#!/usr/bin/env python3
"""
Images 폴더의 모든 이미지를 실제 이미지로 표시하는 갤러리 HTML 생성
SVG는 img 태그로 로드하여 표시
"""

import os
import glob
import base64
from pathlib import Path

def get_image_src(image_path, base_dir):
    """이미지 경로를 적절한 src로 변환"""
    ext = os.path.splitext(image_path)[1].lower()
    
    if ext == '.svg':
        # SVG는 HTML 파일 위치에서의 상대 경로로 변환
        rel_path = os.path.relpath(image_path, base_dir).replace('\\', '/')
        return rel_path
    else:
        # 다른 이미지는 base64로 인코딩
        try:
            with open(image_path, 'rb') as f:
                data = f.read()
                mime_map = {
                    '.png': 'image/png',
                    '.jpg': 'image/jpeg',
                    '.jpeg': 'image/jpeg',
                    '.gif': 'image/gif',
                    '.webp': 'image/webp'
                }
                mime_type = mime_map.get(ext, 'image/png')
                b64 = base64.b64encode(data).decode('utf-8')
                return f'data:{mime_type};base64,{b64}'
        except Exception as e:
            print(f"Error reading {image_path}: {e}")
            return None

def create_image_gallery_with_preview():
    """이미지 갤러리 HTML 생성 (모든 이미지를 img 태그로)"""
    
    # Images 폴더 경로
    # 현재 스크립트 위치에서 상대 경로 계산
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(os.path.dirname(script_dir), 'Images')
    
    if not os.path.exists(images_dir):
        print(f"Images 폴더를 찾을 수 없습니다: {images_dir}")
        # 대체 경로 시도
        images_dir = os.path.join(script_dir, '..', 'Images')
        if not os.path.exists(images_dir):
            print(f"대체 경로도 실패: {images_dir}")
            return False
    
    # 지원하는 이미지 확장자
    extensions = ['*.svg', '*.png', '*.jpg', '*.jpeg', '*.gif', '*.webp']
    
    # 모든 이미지 파일 찾기
    all_images = []
    for ext in extensions:
        pattern = os.path.join(images_dir, ext)
        files = glob.glob(pattern)
        all_images.extend(files)
    
    # 파일명으로 정렬
    all_images.sort(key=lambda x: os.path.basename(x).lower())
    
    if not all_images:
        print("Images 폴더에 이미지 파일이 없습니다.")
        return False
    
    print(f"찾은 이미지 파일: {len(all_images)}개")
    
    # 출력 경로 먼저 설정
    output_path = os.path.join(os.path.dirname(script_dir), 'image_gallery.html')
    output_dir = os.path.dirname(output_path)
    
    # HTML 생성
    html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Gallery - All Images</title>
    <style>
        * {
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            margin: 0 0 10px 0;
            color: #333;
        }
        .stats {
            color: #666;
            font-size: 14px;
        }
        .controls {
            text-align: center;
            margin-bottom: 20px;
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .controls label {
            margin: 0 15px;
            cursor: pointer;
        }
        .controls select {
            margin: 0 5px;
            padding: 5px 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .view-mode {
            display: inline-block;
            margin-left: 20px;
        }
        .view-btn {
            padding: 5px 15px;
            margin: 0 3px;
            border: 1px solid #ddd;
            background: white;
            border-radius: 5px;
            cursor: pointer;
        }
        .view-btn.active {
            background: #13aefe;
            color: white;
            border-color: #13aefe;
        }
        .gallery {
            display: grid;
            gap: 20px;
        }
        .gallery.grid-view {
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        }
        .gallery.list-view {
            grid-template-columns: 1fr;
        }
        .image-item {
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .image-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }
        .gallery.list-view .image-item {
            display: flex;
            align-items: center;
        }
        .image-frame {
            position: relative;
            background: #fafafa;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }
        .gallery.grid-view .image-frame {
            height: 300px;
        }
        .gallery.list-view .image-frame {
            width: 200px;
            height: 200px;
            flex-shrink: 0;
        }
        .image-frame img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }
        .circle-guide {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 90%;
            height: 90%;
            border: 2px dashed #ff0000;
            border-radius: 50%;
            pointer-events: none;
            display: none;
        }
        .show-circles .circle-guide {
            display: block;
        }
        .image-info {
            padding: 15px;
        }
        .gallery.list-view .image-info {
            flex: 1;
        }
        .image-title {
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
            word-break: break-all;
        }
        .image-meta {
            font-size: 12px;
            color: #666;
            margin-bottom: 10px;
        }
        .image-path {
            font-size: 11px;
            color: #999;
            font-family: monospace;
            margin-bottom: 10px;
        }
        .image-actions {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        .gallery.list-view .image-actions {
            justify-content: flex-start;
        }
        .btn {
            padding: 6px 12px;
            border: 1px solid #ddd;
            background: white;
            border-radius: 5px;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.3s;
            white-space: nowrap;
        }
        .btn:hover {
            background: #f0f0f0;
        }
        .btn-primary {
            background: #13aefe;
            color: white;
            border-color: #13aefe;
        }
        .btn-primary:hover {
            background: #0099e0;
        }
        .btn-success {
            background: #4caf50;
            color: white;
            border-color: #4caf50;
        }
        .btn-success:hover {
            background: #45a049;
        }
        .loading {
            color: #666;
            font-style: italic;
        }
        .error {
            color: #d32f2f;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Image Gallery</h1>
        <div class="stats">Images 폴더 - 총 """ + str(len(all_images)) + """개 파일</div>
    </div>
    
    <div class="controls">
        <label>
            <input type="checkbox" id="showCircles" onchange="toggleCircles()">
            원형 가이드 표시
        </label>
        <label>
            배경색: 
            <select id="bgColor" onchange="changeBgColor()">
                <option value="#fafafa">밝은 회색</option>
                <option value="#ffffff">흰색</option>
                <option value="#000000">검은색</option>
                <option value="#1a1a1a">어두운 회색</option>
                <option value="#13aefe">파란색</option>
                <option value="#e8f5e9">연한 초록</option>
                <option value="#fff3e0">연한 주황</option>
            </select>
        </label>
        <div class="view-mode">
            보기 모드:
            <button class="view-btn active" onclick="setViewMode('grid')">격자</button>
            <button class="view-btn" onclick="setViewMode('list')">목록</button>
        </div>
    </div>
    
    <div class="gallery grid-view" id="gallery">
"""
    
    # 각 이미지 아이템 추가
    for i, image_path in enumerate(all_images):
        filename = os.path.basename(image_path)
        ext = os.path.splitext(filename)[1].lower()[1:]  # 확장자 (점 제외)
        file_size = os.path.getsize(image_path) / 1024  # KB
        
        # 이미지 src 가져오기
        img_src = get_image_src(image_path, output_dir)
        rel_path = os.path.relpath(image_path, output_dir).replace('\\', '/')
        
        html_content += f"""
        <div class="image-item" data-index="{i}">
            <div class="image-frame" id="frame-{i}">
                <img src="{img_src}" alt="{filename}" loading="lazy" 
                     onerror="handleImageError({i})"
                     onload="handleImageLoad({i})">
                <div class="circle-guide"></div>
            </div>
            <div class="image-info">
                <div class="image-title">{filename}</div>
                <div class="image-meta">{ext.upper()} • {file_size:.1f} KB</div>
                <div class="image-path">{rel_path}</div>
                <div class="image-actions">
                    <button class="btn" onclick="openInNewTab({i})">새 탭에서 열기</button>
                    <button class="btn btn-primary" onclick="downloadOriginal({i})">원본 다운로드</button>
                    <button class="btn btn-success" onclick="downloadAsPNG({i})">PNG로 저장</button>
                </div>
            </div>
        </div>
"""
    
    html_content += """
    </div>
    
    <script>
        // 이미지 데이터
        const imageData = """ + str([{
            'filename': os.path.basename(img),
            'path': os.path.relpath(img, os.path.dirname(output_path)).replace('\\', '/'),
            'ext': os.path.splitext(img)[1].lower()[1:],
            'src': get_image_src(img, os.path.dirname(output_path))
        } for img in all_images]) + """;
        
        function toggleCircles() {
            const gallery = document.getElementById('gallery');
            const showCircles = document.getElementById('showCircles').checked;
            
            if (showCircles) {
                gallery.classList.add('show-circles');
            } else {
                gallery.classList.remove('show-circles');
            }
        }
        
        function changeBgColor() {
            const color = document.getElementById('bgColor').value;
            const frames = document.querySelectorAll('.image-frame');
            
            frames.forEach(frame => {
                frame.style.backgroundColor = color;
            });
        }
        
        function setViewMode(mode) {
            const gallery = document.getElementById('gallery');
            const buttons = document.querySelectorAll('.view-btn');
            
            // 버튼 상태 업데이트
            buttons.forEach(btn => {
                btn.classList.remove('active');
                if (btn.textContent.includes(mode === 'grid' ? '격자' : '목록')) {
                    btn.classList.add('active');
                }
            });
            
            // 갤러리 모드 변경
            gallery.classList.remove('grid-view', 'list-view');
            gallery.classList.add(mode + '-view');
        }
        
        function handleImageError(index) {
            const frame = document.getElementById(`frame-${index}`);
            frame.innerHTML = '<div class="error">이미지를 로드할 수 없습니다</div>';
        }
        
        function handleImageLoad(index) {
            // 이미지 로드 완료
        }
        
        function openInNewTab(index) {
            const data = imageData[index];
            window.open(data.path, '_blank');
        }
        
        function downloadOriginal(index) {
            const data = imageData[index];
            const a = document.createElement('a');
            a.href = data.path;
            a.download = data.filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }
        
        function downloadAsPNG(index) {
            const data = imageData[index];
            const img = document.querySelector(`#frame-${index} img`);
            
            // Canvas 생성
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            // SVG의 경우 원본 크기 확인
            if (data.ext === 'svg') {
                // SVG 파일에서 viewBox 또는 width/height 추출
                fetch(data.path)
                    .then(response => response.text())
                    .then(svgText => {
                        const parser = new DOMParser();
                        const svgDoc = parser.parseFromString(svgText, 'image/svg+xml');
                        const svgElement = svgDoc.querySelector('svg');
                        
                        let svgWidth = 1000;
                        let svgHeight = 1000;
                        
                        // viewBox에서 크기 추출
                        if (svgElement.viewBox && svgElement.viewBox.baseVal) {
                            svgWidth = svgElement.viewBox.baseVal.width;
                            svgHeight = svgElement.viewBox.baseVal.height;
                        } else if (svgElement.getAttribute('viewBox')) {
                            const viewBox = svgElement.getAttribute('viewBox').split(' ');
                            svgWidth = parseFloat(viewBox[2]);
                            svgHeight = parseFloat(viewBox[3]);
                        } else {
                            // width, height 속성에서 추출
                            svgWidth = parseFloat(svgElement.getAttribute('width')) || 1000;
                            svgHeight = parseFloat(svgElement.getAttribute('height')) || 1000;
                        }
                        
                        // Canvas 크기를 SVG 원본 크기로 설정
                        canvas.width = svgWidth;
                        canvas.height = svgHeight;
                        
                        convertToPNG(canvas, ctx, data, svgText);
                    })
                    .catch(() => {
                        // 실패 시 기본값 사용
                        canvas.width = 1000;
                        canvas.height = 1000;
                        convertToPNG(canvas, ctx, data, null);
                    });
            } else {
                // PNG 등 다른 이미지는 원본 크기 사용
                canvas.width = img.naturalWidth || 1000;
                canvas.height = img.naturalHeight || 1000;
                convertToPNG(canvas, ctx, data, null);
            }
        }
        
        function convertToPNG(canvas, ctx, data, svgText) {
            const bgColor = document.getElementById('bgColor').value;
            ctx.fillStyle = bgColor;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // 이미지 그리기
            const imgObj = new Image();
            imgObj.crossOrigin = 'anonymous';
            
            imgObj.onload = function() {
                // 이미지를 캔버스 전체에 그리기 (원본 크기 유지)
                ctx.drawImage(imgObj, 0, 0, canvas.width, canvas.height);
                
                // PNG로 변환하여 다운로드
                canvas.toBlob(function(blob) {
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    const nameWithoutExt = data.filename.substring(0, data.filename.lastIndexOf('.')) || data.filename;
                    a.download = nameWithoutExt + '_' + canvas.width + 'x' + canvas.height + '.png';
                    document.body.appendChild(a);
                    a.click();
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                    
                    console.log(`PNG 다운로드: ${data.filename} -> ${canvas.width}x${canvas.height}`);
                }, 'image/png', 0.95);
            };
            
            imgObj.onerror = function() {
                alert('이미지를 PNG로 변환할 수 없습니다. 원본 파일을 다운로드하세요.');
            };
            
            // 이미지 로드
            if (svgText) {
                // 이미 가져온 SVG 텍스트 사용
                const blob = new Blob([svgText], {type: 'image/svg+xml'});
                const url = URL.createObjectURL(blob);
                imgObj.src = url;
            } else if (data.ext === 'svg') {
                // SVG 파일 로드
                fetch(data.path)
                    .then(response => response.text())
                    .then(text => {
                        const blob = new Blob([text], {type: 'image/svg+xml'});
                        const url = URL.createObjectURL(blob);
                        imgObj.src = url;
                    })
                    .catch(() => {
                        imgObj.src = data.path;
                    });
            } else {
                imgObj.src = data.src || data.path;
            }
        }
    </script>
</body>
</html>
"""
    
    # HTML 파일 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 이미지 갤러리가 생성되었습니다: {output_path}")
    print(f"   총 {len(all_images)}개 이미지")
    
    # 확장자별 통계
    ext_counts = {}
    for img in all_images:
        ext = os.path.splitext(img)[1].lower()[1:]
        ext_counts[ext] = ext_counts.get(ext, 0) + 1
    
    print("   파일 형식별:")
    for ext, count in sorted(ext_counts.items()):
        print(f"   - {ext.upper()}: {count}개")
    
    return True

if __name__ == "__main__":
    create_image_gallery_with_preview()