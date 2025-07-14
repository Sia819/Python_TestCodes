# SVG 변환 도구 사용 가이드

이 프로젝트는 SVG 파일 변환을 위한 Python 도구 모음입니다.

## 주요 기능

1. **SVG 패스 방향 변환**: 반시계방향 패스를 시계방향으로 변환
2. **SVG 크기 조정**: SVG 파일의 전체 크기 변경
3. **심볼 확대 및 중앙 정렬**: SVG 내 심볼을 원하는 크기로 확대하고 중앙 정렬
4. **패스 병합**: 여러 개의 패스를 하나로 통합

## 사용 방법

### 통합 도구 실행
```bash
python3 svg_tools.py
```

실행 후 메뉴에서 원하는 기능을 선택하세요:
- 1: SVG 패스 뒤집기
- 2: SVG 크기 조정
- 3: SVG 심볼 확대 및 중앙 정렬
- 4: 모든 변환 실행

### 개별 스크립트 사용

#### 1. SVG 패스 뒤집기
```bash
python3 reverse_svg_path.py
```
- 반시계방향 패스를 시계방향으로 변환
- 결과는 `clockwise_path.txt`에 저장

#### 2. SVG 크기 조정
```bash
python3 resize_svg.py
```
- `Icon.svg`를 1000x1000 크기로 변환
- 결과는 `Icon_1000x1000.svg`에 저장

#### 3. 심볼 확대 및 중앙 정렬
```bash
python3 scale_symbol.py
```
- 심볼을 850x850 크기로 확대
- 1000x1000 캔버스 중앙에 정렬
- 결과는 `Icon_1000x1000_scaled.svg`에 저장

#### 4. 패스 병합
```bash
python3 merge_paths_correct.py
```
- 두 개의 분리된 패스를 하나로 통합
- 중복되는 보간점 제거
- 결과는 `merged_path_final.txt`에 저장

## 예제

### 전체 변환 프로세스
```bash
# 1. SVG 크기를 1000x1000으로 조정
python3 resize_svg.py

# 2. 심볼을 850x850으로 확대하고 중앙 정렬
python3 scale_symbol.py

# 또는 통합 도구에서 옵션 4 선택
python3 svg_tools.py
# > 4 입력
```

### 커스텀 변환
```python
from svg_tools import SVGTools

# SVG 크기 조정
SVGTools.resize_svg('input.svg', 'output.svg', 1200)

# 심볼 확대
SVGTools.scale_and_center_symbol('input.svg', 'output.svg', 1000, 900)

# 패스 뒤집기
path_data = "M 100 100 L 200 200 L 300 100 Z"
reversed_path = SVGTools.reverse_path_to_clockwise(path_data)
```

## 파일 구조

```
.
├── svg_tools.py          # 통합 도구
├── reverse_svg_path.py   # 패스 방향 변환
├── resize_svg.py         # 크기 조정
├── scale_symbol.py       # 심볼 확대
├── merge_paths_correct.py # 패스 병합
└── README_SVG_TOOLS.md   # 이 문서
```

## 주의사항

- Python 3.6 이상 필요
- SVG 파일은 UTF-8 인코딩이어야 함
- 변환 전 원본 파일 백업 권장

## 문제 해결

### "파일을 찾을 수 없음" 오류
- 작업 디렉토리에 SVG 파일이 있는지 확인
- 파일명과 경로가 정확한지 확인

### 좌표 변환 오류
- SVG 파일의 viewBox 속성이 올바른지 확인
- 패스 데이터가 표준 SVG 형식인지 확인