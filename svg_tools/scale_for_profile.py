#!/usr/bin/env python3
"""
SVG를 원형 프로필에 맞게 스케일링
트위터, 디스코드 등의 원형 프로필 이미지에 맞춤
"""

import re
import math
import sys
import os

def extract_numbers(path_d):
    """패스 데이터에서 모든 숫자 추출"""
    numbers = re.findall(r'[-+]?\d*\.?\d+', path_d)
    coords = []
    for i in range(0, len(numbers), 2):
        if i + 1 < len(numbers):
            coords.append((float(numbers[i]), float(numbers[i+1])))
    return coords

def get_bounding_box_and_corners(svg_content):
    """SVG의 경계 상자와 각 모서리까지의 거리 계산"""
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')
    
    # 모든 path 요소 찾기 (Fill 제외)
    path_pattern = r'<path[^>]*d="([^"]*)"[^>]*>'
    paths = re.findall(path_pattern, svg_content)
    
    all_coords = []
    
    for path_d in paths:
        # Fill path는 제외
        if 'M 1000.00 0.00' in path_d:
            continue
            
        coords = extract_numbers(path_d)
        all_coords.extend(coords)
        for x, y in coords:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
    
    # circle 요소도 고려
    circle_pattern = r'<circle[^>]*cx="([\d.]+)"[^>]*cy="([\d.]+)"[^>]*r="([\d.]+)"[^>]*>'
    circles = re.findall(circle_pattern, svg_content)
    for cx_str, cy_str, r_str in circles:
        cx, cy, r = float(cx_str), float(cy_str), float(r_str)
        min_x = min(min_x, cx - r)
        min_y = min(min_y, cy - r)
        max_x = max(max_x, cx + r)
        max_y = max(max_y, cy + r)
        # 원의 8방향 점들도 추가
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x = cx + r * math.cos(rad)
            y = cy + r * math.sin(rad)
            all_coords.append((x, y))
    
    return min_x, min_y, max_x, max_y, all_coords

def scale_for_circular_profile(input_file, output_file, canvas_size=1000):
    """SVG를 원형 프로필에 맞게 스케일링"""
    with open(input_file, 'r', encoding='utf-8') as f:
        svg_content = f.read()
    
    # 현재 심볼의 경계 상자와 모든 좌표 구하기
    min_x, min_y, max_x, max_y, all_coords = get_bounding_box_and_corners(svg_content)
    
    # 현재 심볼의 중심점
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    
    # 캔버스 중심
    canvas_center = canvas_size / 2
    
    # 각 점에서 캔버스 중심까지의 거리 계산
    max_distance = 0
    critical_point = None
    
    # 현재 중심이 캔버스 중심에 있다고 가정하고 거리 계산
    translate_x = canvas_center - center_x
    translate_y = canvas_center - center_y
    
    for x, y in all_coords:
        # 이동 후 좌표
        translated_x = x + translate_x
        translated_y = y + translate_y
        
        # 캔버스 중심에서의 거리
        dist_from_center = math.sqrt(
            (translated_x - canvas_center) ** 2 + 
            (translated_y - canvas_center) ** 2
        )
        
        if dist_from_center > max_distance:
            max_distance = dist_from_center
            critical_point = (x, y)
    
    # 원의 반지름 (여유 공간 고려)
    circle_radius = canvas_center * 0.98  # 2% 여유
    
    # 필요한 스케일 팩터
    if max_distance > 0:
        scale_factor = circle_radius / max_distance
    else:
        scale_factor = 1.0
    
    print(f"현재 심볼 크기: {max_x - min_x:.2f} x {max_y - min_y:.2f}")
    print(f"현재 중심점: ({center_x:.2f}, {center_y:.2f})")
    print(f"가장 먼 점: {critical_point}")
    print(f"최대 거리: {max_distance:.2f}")
    print(f"목표 반지름: {circle_radius:.2f}")
    print(f"스케일 팩터: {scale_factor:.4f}")
    
    # 새로운 중심 위치 계산 (스케일링 후)
    new_translate_x = canvas_center - center_x * scale_factor
    new_translate_y = canvas_center - center_y * scale_factor
    
    # 좌표 변환 함수
    def transform_coordinates(match):
        coords = match.group(1)
        # Fill path는 변환하지 않음
        if 'M 1000.00 0.00' in coords:
            return match.group(0)
            
        # 숫자 패턴 찾기
        def replace_number(num_match):
            num = float(num_match.group(0))
            if hasattr(replace_number, 'index'):
                replace_number.index += 1
            else:
                replace_number.index = 0
                
            # 홀수 인덱스는 x좌표, 짝수 인덱스는 y좌표
            if replace_number.index % 2 == 1:  # x 좌표
                transformed = num * scale_factor + new_translate_x
            else:  # y 좌표
                transformed = num * scale_factor + new_translate_y
                
            return f"{transformed:.2f}"
        
        replace_number.index = 0
        result = re.sub(r'[-+]?\d*\.?\d+', replace_number, coords)
        return match.group(0).replace(coords, result)
    
    # path d 속성의 좌표 변환
    svg_content = re.sub(r'd="([^"]*)"', transform_coordinates, svg_content)
    
    # circle 요소의 변환
    def transform_circle(match):
        cx = float(match.group(1)) * scale_factor + new_translate_x
        cy = float(match.group(2)) * scale_factor + new_translate_y
        r = float(match.group(3)) * scale_factor
        return f'<circle fill="#13aefe" cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" />'
    
    svg_content = re.sub(r'<circle[^>]*cx="([\d.]+)"[^>]*cy="([\d.]+)"[^>]*r="([\d.]+)"[^>]*/>',
                        transform_circle, svg_content)
    
    # 결과 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    print(f"\n심볼이 원형 프로필에 맞게 조정되었습니다.")
    print(f"결과가 '{output_file}'에 저장되었습니다.")

def main():
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.svg', '_profile.svg')
    else:
        # 기본값
        input_file = '../Images/Icon_WithoutTail_1000x1000_profile.svg'
        output_file = '../Images/Icon_WithoutTail_1000x1000_profile2.svg'
    
    if not os.path.exists(input_file):
        print(f"파일을 찾을 수 없습니다: {input_file}")
        return
    
    scale_for_circular_profile(input_file, output_file)

if __name__ == "__main__":
    main()