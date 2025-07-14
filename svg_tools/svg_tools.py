#!/usr/bin/env python3
"""
SVG 변환 도구 모음
- SVG 패스 뒤집기 (반시계 -> 시계방향)
- SVG 크기 조정
- SVG 심볼 확대 및 중앙 정렬
- SVG 패스 병합
"""

import re
import os
import sys

class SVGTools:
    @staticmethod
    def parse_svg_path(path_data):
        """SVG 경로를 파싱하여 명령어 리스트로 변환"""
        tokens = re.findall(r'[MLCQZmlcqz]|[-+]?\d*\.?\d+', path_data.strip())
        
        commands = []
        i = 0
        
        while i < len(tokens):
            if tokens[i] in 'MLCQZmlcqz':
                cmd = tokens[i]
                i += 1
                
                param_counts = {
                    'M': 2, 'm': 2,
                    'L': 2, 'l': 2,
                    'C': 6, 'c': 6,
                    'Q': 4, 'q': 4,
                    'Z': 0, 'z': 0
                }
                
                params = []
                param_count = param_counts.get(cmd, 0)
                
                for _ in range(param_count):
                    if i < len(tokens) and tokens[i] not in 'MLCQZmlcqz':
                        params.append(float(tokens[i]))
                        i += 1
                
                commands.append((cmd, params))
            else:
                i += 1
        
        return commands

    @staticmethod
    def reverse_path_to_clockwise(path_data):
        """반시계방향 패스를 시계방향으로 변환"""
        commands = SVGTools.parse_svg_path(path_data)
        
        # Z 명령어 제거
        if commands and commands[-1][0] in 'Zz':
            commands = commands[:-1]
        
        # 각 점의 좌표 추출
        points = []
        for cmd, params in commands:
            if cmd == 'M':
                points.append(params)
            elif cmd == 'L':
                points.append(params)
            elif cmd == 'C':
                points.append(params[4:6])
            elif cmd == 'Q':
                points.append(params[2:4])
        
        # 역순으로 새 명령어 생성
        reversed_commands = []
        reversed_commands.append(('M', points[-1]))
        
        for i in range(len(commands) - 1, 0, -1):
            cmd, params = commands[i]
            prev_point = points[i-1]
            
            if cmd == 'L':
                reversed_commands.append(('L', prev_point))
            elif cmd == 'C':
                reversed_commands.append(('C', [params[2], params[3], params[0], params[1], prev_point[0], prev_point[1]]))
            elif cmd == 'Q':
                reversed_commands.append(('Q', [params[0], params[1], prev_point[0], prev_point[1]]))
        
        # 명령어를 문자열로 변환
        result = []
        for cmd, params in reversed_commands:
            if cmd in 'Zz':
                result.append(cmd)
            else:
                if cmd == 'M' or cmd == 'L':
                    result.append(f"{cmd} {params[0]:.2f} {params[1]:.2f}")
                elif cmd == 'C':
                    result.append(f"{cmd} {params[0]:.2f} {params[1]:.2f}, {params[2]:.2f} {params[3]:.2f}, {params[4]:.2f} {params[5]:.2f}")
                elif cmd == 'Q':
                    result.append(f"{cmd} {params[0]:.2f} {params[1]:.2f}, {params[2]:.2f} {params[3]:.2f}")
        
        result.append('Z')
        return '\n  '.join(result)

    @staticmethod
    def resize_svg(input_file, output_file, new_size):
        """SVG 파일 크기 조정"""
        with open(input_file, 'r', encoding='utf-8') as f:
            svg_content = f.read()
        
        # 원본 크기 추출
        viewbox_match = re.search(r'viewBox="[^"]*\s+(\d+\.?\d*)\s+(\d+\.?\d*)"', svg_content)
        if viewbox_match:
            original_size = float(viewbox_match.group(1))
        else:
            print("viewBox를 찾을 수 없습니다.")
            return False
        
        scale_factor = new_size / original_size
        
        # viewBox 변경
        svg_content = re.sub(r'viewBox="[^"]*"', f'viewBox="0.00 0.00 {new_size:.2f} {new_size:.2f}"', svg_content)
        
        # 모든 좌표를 스케일링하는 함수
        def scale_coordinates(match):
            coords = match.group(1)
            numbers = re.findall(r'[-+]?\d*\.?\d+', coords)
            scaled_numbers = []
            
            for num in numbers:
                scaled_value = float(num) * scale_factor
                scaled_numbers.append(f"{scaled_value:.2f}")
            
            result = coords
            for i, num in enumerate(numbers):
                result = result.replace(num, scaled_numbers[i], 1)
            
            return match.group(0).replace(coords, result)
        
        # path d 속성의 좌표 스케일링
        svg_content = re.sub(r'd="([^"]*)"', scale_coordinates, svg_content)
        
        # circle 요소의 cx, cy, r 속성 스케일링
        def scale_circle(match):
            cx = float(match.group(1)) * scale_factor
            cy = float(match.group(2)) * scale_factor
            r = float(match.group(3)) * scale_factor
            return f'<circle fill="#13aefe" cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" />'
        
        svg_content = re.sub(r'<circle[^>]*cx="([\d.]+)"[^>]*cy="([\d.]+)"[^>]*r="([\d.]+)"[^>]*/>',
                            scale_circle, svg_content)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        print(f"SVG가 {original_size}x{original_size}에서 {new_size}x{new_size}로 크기가 조정되었습니다.")
        print(f"결과가 '{output_file}'에 저장되었습니다.")
        return True

    @staticmethod
    def extract_numbers(path_d):
        """패스 데이터에서 모든 숫자 추출"""
        numbers = re.findall(r'[-+]?\d*\.?\d+', path_d)
        coords = []
        for i in range(0, len(numbers), 2):
            if i + 1 < len(numbers):
                coords.append((float(numbers[i]), float(numbers[i+1])))
        return coords

    @staticmethod
    def get_bounding_box(svg_content):
        """SVG의 모든 패스에서 경계 상자 계산"""
        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')
        
        path_pattern = r'<path[^>]*d="([^"]*)"[^>]*>'
        paths = re.findall(path_pattern, svg_content)
        
        for path_d in paths:
            # Fill path는 제외
            if 'M 1000.00 0.00' in path_d or 'M 1448.00 0.00' in path_d:
                continue
                
            coords = SVGTools.extract_numbers(path_d)
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
        
        return min_x, min_y, max_x, max_y

    @staticmethod
    def scale_and_center_symbol(input_file, output_file, canvas_size, target_size):
        """SVG 심볼을 확대하고 중앙 정렬"""
        with open(input_file, 'r', encoding='utf-8') as f:
            svg_content = f.read()
        
        # 현재 심볼의 경계 상자 구하기
        min_x, min_y, max_x, max_y = SVGTools.get_bounding_box(svg_content)
        
        # 현재 심볼의 크기
        current_width = max_x - min_x
        current_height = max_y - min_y
        current_size = max(current_width, current_height)
        
        # 중심점
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        
        print(f"현재 심볼 크기: {current_width:.2f} x {current_height:.2f}")
        print(f"현재 중심점: ({center_x:.2f}, {center_y:.2f})")
        
        # 스케일 팩터 계산
        scale_factor = target_size / current_size
        
        # 새로운 중심점 (캔버스 중앙)
        new_center_x = canvas_size / 2
        new_center_y = canvas_size / 2
        
        # 이동 거리 계산
        translate_x = new_center_x - center_x * scale_factor
        translate_y = new_center_y - center_y * scale_factor
        
        print(f"스케일 팩터: {scale_factor:.4f}")
        print(f"이동 거리: ({translate_x:.2f}, {translate_y:.2f})")
        
        # 좌표 변환 함수
        def transform_coordinates(match):
            coords = match.group(1)
            # Fill path는 변환하지 않음
            if f'M {canvas_size:.2f} 0.00' in coords:
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
                    transformed = num * scale_factor + translate_x
                else:  # y 좌표
                    transformed = num * scale_factor + translate_y
                    
                return f"{transformed:.2f}"
            
            replace_number.index = 0
            result = re.sub(r'[-+]?\d*\.?\d+', replace_number, coords)
            return match.group(0).replace(coords, result)
        
        # path d 속성의 좌표 변환
        svg_content = re.sub(r'd="([^"]*)"', transform_coordinates, svg_content)
        
        # circle 요소의 변환
        def transform_circle(match):
            cx = float(match.group(1)) * scale_factor + translate_x
            cy = float(match.group(2)) * scale_factor + translate_y
            r = float(match.group(3)) * scale_factor
            return f'<circle fill="#13aefe" cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" />'
        
        svg_content = re.sub(r'<circle[^>]*cx="([\d.]+)"[^>]*cy="([\d.]+)"[^>]*r="([\d.]+)"[^>]*/>',
                            transform_circle, svg_content)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        print(f"\n심볼이 {target_size}x{target_size} 크기로 확대되었습니다.")
        print(f"결과가 '{output_file}'에 저장되었습니다.")
        return True

def main():
    print("SVG 변환 도구")
    print("=============")
    print("1. SVG 패스 뒤집기 (반시계 -> 시계)")
    print("2. SVG 크기 조정")
    print("3. SVG 심볼 확대 및 중앙 정렬")
    print("4. 모든 변환 실행")
    
    choice = input("\n선택하세요 (1-4): ")
    
    if choice == '1':
        path_data = input("변환할 패스 데이터를 입력하세요: ")
        result = SVGTools.reverse_path_to_clockwise(path_data)
        print("\n변환된 패스:")
        print(result)
        
    elif choice == '2':
        input_file = input("입력 SVG 파일명: ")
        output_file = input("출력 SVG 파일명: ")
        new_size = float(input("새 크기 (예: 1000): "))
        SVGTools.resize_svg(input_file, output_file, new_size)
        
    elif choice == '3':
        input_file = input("입력 SVG 파일명: ")
        output_file = input("출력 SVG 파일명: ")
        canvas_size = float(input("캔버스 크기 (예: 1000): "))
        target_size = float(input("목표 심볼 크기 (예: 850): "))
        SVGTools.scale_and_center_symbol(input_file, output_file, canvas_size, target_size)
        
    elif choice == '4':
        print("\n전체 변환 프로세스를 시작합니다...")
        if os.path.exists('Icon.svg'):
            # 1. 크기 조정
            print("\n1단계: 1000x1000으로 크기 조정")
            SVGTools.resize_svg('Icon.svg', 'Icon_1000x1000.svg', 1000)
            
            # 2. 심볼 확대
            print("\n2단계: 심볼을 850x850으로 확대")
            SVGTools.scale_and_center_symbol('Icon_1000x1000.svg', 'Icon_1000x1000_scaled.svg', 1000, 850)
            
            print("\n변환 완료!")
        else:
            print("Icon.svg 파일을 찾을 수 없습니다.")

if __name__ == "__main__":
    main()