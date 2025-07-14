#!/usr/bin/env python3
"""
Images 폴더의 모든 이미지를 표시하는 갤러리 HTML 생성
"""

import os
import glob
import base64
from pathlib import Path

def get_image_data_uri(image_path):
    """이미지를 data URI로 변환"""
    try:
        with open(image_path, 'rb') as f:
            data = f.read()
            ext = os.path.splitext(image_path)[1].lower()
            mime_map = {
                '.svg': 'image/svg+xml',
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.webp': 'image/webp'
            }
            mime_type = mime_map.get(ext, 'image/png')
            
            if ext == '.svg':
                # SVG는 텍스트로 직접 포함
                return data.decode('utf-8')
            else:
                # 다른 이미지는 base64로 인코딩
                b64 = base64.b64encode(data).decode('utf-8')
                return f'<img src="data:{mime_type};base64,{b64}" alt="{os.path.basename(image_path)}">'
    except Exception as e:
        print(f"Error reading {image_path}: {e}")
        return None

def create_image_gallery():
    """이미지 갤러리 HTML 생성"""
    
    # Images 폴더 경로
    images_dir = '../Images'
    if not os.path.exists(images_dir):
        print(f"Images 폴더를 찾을 수 없습니다: {images_dir}")
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
    
    # HTML 생성
    html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Gallery - Images Folder</title>
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
        .controls select, .controls input {
            margin: 0 5px;
            padding: 5px 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .filter-buttons {
            display: inline-block;
            margin-left: 20px;
        }
        .filter-btn {
            padding: 5px 15px;
            margin: 0 3px;
            border: 1px solid #ddd;
            background: white;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .filter-btn:hover {
            background: #f0f0f0;
        }
        .filter-btn.active {
            background: #13aefe;
            color: white;
            border-color: #13aefe;
        }
        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
        }
        .image-item {
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
            display: none;
        }
        .image-item.visible {
            display: block;
        }
        .image-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }
        .image-container {
            position: relative;
            padding-top: 100%;
            background: #fafafa;
            border-bottom: 1px solid #eee;
        }
        .image-container > * {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            max-width: 90%;
            max-height: 90%;
            width: auto;
            height: auto;
        }
        .image-container svg {
            width: 90%;
            height: 90%;
        }
        .circle-overlay {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 96%;
            height: 96%;
            border: 2px dashed #ff0000;
            border-radius: 50%;
            pointer-events: none;
            display: none;
            z-index: 10;
        }
        .show-circle .circle-overlay {
            display: block;
        }
        .image-info {
            padding: 15px;
        }
        .image-title {
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
            word-break: break-all;
            font-size: 14px;
        }
        .image-meta {
            font-size: 12px;
            color: #666;
        }
        .image-actions {
            padding: 0 15px 15px;
            display: flex;
            gap: 10px;
        }
        .btn {
            flex: 1;
            padding: 8px 12px;
            border: 1px solid #ddd;
            background: white;
            border-radius: 5px;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.3s;
            text-align: center;
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
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 1000;
            cursor: pointer;
        }
        .modal-content {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            max-width: 90%;
            max-height: 90%;
            background: white;
            padding: 20px;
            border-radius: 10px;
        }
        .modal-content img, .modal-content svg {
            max-width: 100%;
            max-height: 80vh;
            display: block;
        }
        .close-modal {
            position: absolute;
            top: 10px;
            right: 10px;
            width: 30px;
            height: 30px;
            background: rgba(0,0,0,0.5);
            color: white;
            border: none;
            border-radius: 50%;
            cursor: pointer;
            font-size: 20px;
            line-height: 1;
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
            </select>
        </label>
        <div class="filter-buttons">
            필터:
            <button class="filter-btn active" onclick="filterImages('all')">전체</button>
            <button class="filter-btn" onclick="filterImages('svg')">SVG</button>
            <button class="filter-btn" onclick="filterImages('png')">PNG</button>
            <button class="filter-btn" onclick="filterImages('jpg')">JPG</button>
        </div>
    </div>
    
    <div class="gallery" id="gallery">
"""
    
    # 각 이미지 아이템 추가
    for i, image_path in enumerate(all_images):
        filename = os.path.basename(image_path)
        ext = os.path.splitext(filename)[1].lower()[1:]  # 확장자 (점 제외)
        file_size = os.path.getsize(image_path) / 1024  # KB
        
        # 이미지 콘텐츠 가져오기
        if ext == 'svg':
            with open(image_path, 'r', encoding='utf-8') as f:
                image_content = f.read()
        else:
            image_content = get_image_data_uri(image_path)
        
        html_content += f"""
        <div class="image-item visible" data-type="{ext}" data-index="{i}">
            <div class="image-container" id="container-{i}">
                {image_content}
                <div class="circle-overlay"></div>
            </div>
            <div class="image-info">
                <div class="image-title">{filename}</div>
                <div class="image-meta">{ext.upper()} • {file_size:.1f} KB</div>
            </div>
            <div class="image-actions">
                <button class="btn" onclick="viewFullsize({i})">전체 크기</button>
                <button class="btn btn-primary" onclick="downloadImage({i})">다운로드</button>
            </div>
        </div>
"""
    
    html_content += """
    </div>
    
    <div class="modal" id="modal" onclick="closeModal()">
        <div class="modal-content" onclick="event.stopPropagation()">
            <button class="close-modal" onclick="closeModal()">×</button>
            <div id="modal-body"></div>
        </div>
    </div>
    
    <script>
        // 이미지 데이터
        const imageData = """ + str([{
            'filename': os.path.basename(img),
            'path': img,
            'ext': os.path.splitext(img)[1].lower()[1:]
        } for img in all_images]) + """;
        
        function toggleCircles() {
            const containers = document.querySelectorAll('.image-container');
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
            const containers = document.querySelectorAll('.image-container');
            
            containers.forEach(container => {
                container.style.backgroundColor = color;
            });
        }
        
        function filterImages(type) {
            const items = document.querySelectorAll('.image-item');
            const buttons = document.querySelectorAll('.filter-btn');
            
            // 버튼 상태 업데이트
            buttons.forEach(btn => {
                btn.classList.remove('active');
                if (btn.textContent.toLowerCase().includes(type) || 
                    (type === 'all' && btn.textContent === '전체')) {
                    btn.classList.add('active');
                }
            });
            
            // 이미지 필터링
            items.forEach(item => {
                const itemType = item.dataset.type;
                if (type === 'all' || itemType === type || 
                    (type === 'jpg' && (itemType === 'jpg' || itemType === 'jpeg'))) {
                    item.classList.add('visible');
                } else {
                    item.classList.remove('visible');
                }
            });
        }
        
        function viewFullsize(index) {
            const modal = document.getElementById('modal');
            const modalBody = document.getElementById('modal-body');
            const container = document.getElementById(`container-${index}`);
            
            modalBody.innerHTML = container.innerHTML;
            modal.style.display = 'block';
        }
        
        function closeModal() {
            document.getElementById('modal').style.display = 'none';
        }
        
        function downloadImage(index) {
            const data = imageData[index];
            const container = document.getElementById(`container-${index}`);
            
            if (data.ext === 'svg') {
                // SVG 다운로드
                const svg = container.querySelector('svg');
                const svgString = new XMLSerializer().serializeToString(svg);
                const blob = new Blob([svgString], {type: 'image/svg+xml'});
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = data.filename;
                a.click();
                URL.revokeObjectURL(url);
            } else {
                // 다른 이미지 다운로드
                const img = container.querySelector('img');
                const a = document.createElement('a');
                a.href = img.src;
                a.download = data.filename;
                a.click();
            }
        }
        
        // ESC 키로 모달 닫기
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeModal();
            }
        });
    </script>
</body>
</html>
"""
    
    # HTML 파일 저장
    output_path = '../image_gallery.html'
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
    create_image_gallery()