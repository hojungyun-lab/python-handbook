# 📘 Python Handbook

> **기초부터 전문가까지 — 실행 가능한 40개 학습 스크립트**

Python의 핵심 문법과 고급 패턴을 **3단계 난이도**로 나누어 정리한 핸드북입니다.
모든 스크립트는 **직접 실행**할 수 있으며, 인라인 출력 주석(`# →`)으로 결과를 바로 확인할 수 있습니다.

## 특징

- 🐍 **Python 3.13** 기준, 최신 문법 활용 (PEP 604 Union `|`, match-case 등)
- 📝 모든 `print()` 결과를 **인라인 주석**으로 표기 — 실행 없이도 흐름 파악 가능
- 🏷️ **타입 힌트** 전면 적용
- 📖 **한국어** docstring 및 주석
- ✅ pre-commit (Black, Flake8) 코드 품질 관리

## 목차

### Level 1 — Basic (14개)

| # | 파일 | 주제 |
|---|------|------|
| 100 | `_100_variables.py` | 변수와 데이터 타입 |
| 110 | `_110_strings.py` | 문자열 |
| 120 | `_120_numbers.py` | 숫자 |
| 130 | `_130_lists.py` | 리스트 |
| 140 | `_140_tuples.py` | 튜플 |
| 150 | `_150_dictionaries.py` | 딕셔너리 |
| 160 | `_160_sets.py` | 세트 |
| 170 | `_170_conditionals.py` | 조건문 |
| 180 | `_180_loops.py` | 반복문 |
| 190 | `_190_functions.py` | 함수 |
| 200 | `_200_list_comprehension.py` | 리스트 컴프리헨션 |
| 210 | `_210_file_io.py` | 파일 입출력 |
| 220 | `_220_error_handling.py` | 에러 처리 |
| 230 | `_230_modules_and_packages.py` | 모듈과 패키지 |

### Level 2 — Intermediate (16개)

| # | 파일 | 주제 |
|---|------|------|
| 200 | `_200_classes_basics.py` | 클래스 기초 |
| 210 | `_210_inheritance.py` | 상속 |
| 220 | `_220_magic_methods.py` | 매직 메서드 |
| 230 | `_230_properties_slots.py` | 프로퍼티와 __slots__ |
| 240 | `_240_dataclasses.py` | 데이터클래스 |
| 250 | `_250_enums.py` | Enum |
| 260 | `_260_iterators_generators.py` | 이터레이터와 제너레이터 |
| 270 | `_270_decorators.py` | 데코레이터 |
| 280 | `_280_closures_and_functional.py` | 클로저와 함수형 프로그래밍 |
| 290 | `_290_type_hints_advanced.py` | 고급 타입 힌트 |
| 300 | `_300_context_managers.py` | 컨텍스트 매니저 |
| 310 | `_310_collections_module.py` | collections 모듈 |
| 320 | `_320_datetime_handling.py` | 날짜/시간 처리 |
| 330 | `_330_regular_expressions.py` | 정규표현식 |
| 340 | `_340_logging_module.py` | 로깅 |
| 350 | `_350_testing_basics.py` | 테스트 기초 |

### Level 3 — Expert (10개)

| # | 파일 | 주제 |
|---|------|------|
| 300 | `_300_async_await.py` | 비동기 프로그래밍 |
| 310 | `_310_threading_multiprocessing.py` | 스레딩과 멀티프로세싱 |
| 320 | `_320_descriptors.py` | 디스크립터 |
| 330 | `_330_metaclasses.py` | 메타클래스 |
| 340 | `_340_design_patterns.py` | 디자인 패턴 |
| 350 | `_350_memory_management.py` | 메모리 관리 |
| 360 | `_360_performance_optimization.py` | 성능 최적화 |
| 370 | `_370_c_extensions.py` | C 확장 |
| 380 | `_380_networking.py` | 네트워킹 |
| 390 | `_390_advanced_patterns.py` | 고급 패턴 |

## 시작하기

### 사전 요구사항

- Python 3.13+
- [Poetry](https://python-poetry.org/)

### 설치

```bash
git clone https://github.com/hojungyun-lab/python-handbook.git
cd python-handbook
poetry install
```

### 실행

```bash
# 개별 스크립트 실행
poetry run python level1_basic/_100_variables.py
poetry run python level2_intermediate/_200_classes_basics.py
poetry run python level3_expert/_300_async_await.py
```

## 스크립트 구조

각 스크립트는 동일한 구조를 따릅니다:

```python
"""
모듈 docstring — 다루는 내용 목록
"""

def demonstrate_topic() -> None:
    """주제별 함수 — 개념 설명 + 실행 예제."""
    name: str = "Python"                              # 타입 힌트
    print(f"name = {name}")  # → name = Python        # 인라인 출력 주석

if __name__ == "__main__":
    demonstrate_topic()
```

## 라이선스

MIT
