"""
_230_modules_and_packages.py — 모듈과 패키지 (Modules & Packages)

이 모듈에서 다루는 내용:
  1. import 문과 모듈 시스템
  2. __name__과 __main__
  3. __all__과 공개 API
  4. 패키지 구조와 __init__.py
  5. 상대/절대 임포트
  6. sys.path와 모듈 검색 경로
  7. 표준 라이브러리 모듈 하이라이트

실행 방법:
    poetry run python 1_basic/_230_modules_and_packages.py
"""

import importlib
import math
import os
import sys
from pathlib import Path


def demonstrate_import_basics() -> None:
    """import 문의 다양한 사용법을 보여준다."""
    print("=" * 60)
    print("1. import 문과 모듈 시스템")
    print("=" * 60)

    # 기본 import
    import collections
    print(f"import collections: {type(collections)}")

    # from ... import ...
    from datetime import datetime, timedelta
    now: datetime = datetime.now()
    print(f"from datetime import datetime: {now:%Y-%m-%d %H:%M}")

    # 별칭 (alias)
    import json as j
    data: str = j.dumps({"key": "value"})
    print(f"import json as j: {data}")

    # from ... import * (비권장)
    print(f"\n📌 import 방식과 권장도:")
    print(f"  ✅ import math")
    print(f"  ✅ from math import sqrt, pi")
    print(f"  ✅ import numpy as np  (널리 쓰이는 별칭)")
    print(f"  ⚠️ from math import *  (네임스페이스 오염)")

    # 모듈 속성
    print(f"\n모듈 속성:")
    print(f"  math.__name__ = {math.__name__!r}")  # →   math.__name__ = 'math'
    print(f"  math.__file__ = {math.__file__!r}")
    print(f"  math.__doc__[:50] = {math.__doc__[:50] if math.__doc__ else 'None'}...")

    # dir() — 모듈의 공개 이름 목록
    public_attrs: list[str] = [a for a in dir(math) if not a.startswith("_")]
    print(f"  dir(math) 공개 속성 수: {len(public_attrs)}")
    print(f"  처음 10개: {public_attrs[:10]}")


def demonstrate_name_main() -> None:
    """__name__과 __main__ 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("2. __name__과 __main__")
    print("=" * 60)

    print(f"현재 __name__ = {__name__!r}")  # → 현재 __name__ = '__main__'

    # __name__ == "__main__" 패턴 설명
    print(f"""
📌 if __name__ == "__main__": 패턴

  직접 실행 시: __name__ == "__main__"  → 코드 실행
  import 시:    __name__ == "모듈이름"  → 코드 스킵

  사용 이유:
  1. 모듈로 import 될 때 불필요한 코드 실행 방지
  2. 테스트/데모 코드를 모듈 하단에 배치
  3. 스크립트와 라이브러리 겸용 가능
""")

    # 현재 파일이 직접 실행되었는지 확인
    if __name__ == "__main__":
        print(f"  → 이 파일은 직접 실행되었습니다!")


def demonstrate_all() -> None:
    """__all__과 공개 API를 보여준다."""
    print("\n" + "=" * 60)
    print("3. __all__과 공개 API")
    print("=" * 60)

    print("""__all__ 리스트:
  - from module import * 시 노출될 이름을 명시적으로 지정
  - 모듈의 공개 API를 문서화하는 역할
  - __all__이 없으면 _ 로 시작하지 않는 모든 이름이 노출됨

예시:
  __all__ = ["PublicClass", "public_function", "PUBLIC_CONSTANT"]

  class PublicClass: ...        # ✅ 노출됨
  class _PrivateClass: ...      # ❌ 미노출 (관례)
  def public_function(): ...    # ✅ 노출됨
  def _helper(): ...            # ❌ 미노출 (관례)
""")

    # os 모듈의 __all__ 확인
    if hasattr(os, "__all__"):
        all_count: int = len(os.__all__)  # type: ignore[arg-type]
        print(f"os.__all__ 항목 수: {all_count}")
    else:
        print(f"os 모듈은 __all__ 미정의")


def demonstrate_package_structure() -> None:
    """패키지 구조를 보여준다."""
    print("\n" + "=" * 60)
    print("4. 패키지 구조와 __init__.py")
    print("=" * 60)

    print("""패키지 디렉토리 구조:

  mypackage/
  ├── __init__.py         # 패키지 초기화 (필수 또는 선택)
  ├── module_a.py
  ├── module_b.py
  └── subpackage/
      ├── __init__.py
      └── module_c.py

__init__.py 역할:
  1. 디렉토리를 Python 패키지로 인식
  2. 패키지 초기화 코드 실행
  3. __all__ 정의로 공개 API 제어
  4. 하위 모듈 자동 import 설정

Python 3.3+:
  - __init__.py 없이도 네임스페이스 패키지로 인식 가능
  - 하지만 명시적 패키지에는 __init__.py 권장

__init__.py 예시:
  # mypackage/__init__.py
  from mypackage.module_a import ClassA
  from mypackage.module_b import function_b

  __all__ = ["ClassA", "function_b"]
  __version__ = "1.0.0"
""")


def demonstrate_import_paths() -> None:
    """모듈 검색 경로를 보여준다."""
    print("\n" + "=" * 60)
    print("5. 상대/절대 임포트와 sys.path")
    print("=" * 60)

    # sys.path — 모듈 검색 경로
    print("sys.path (모듈 검색 경로):")
    for i, path in enumerate(sys.path[:5]):
        print(f"  [{i}] {path}")
    if len(sys.path) > 5:
        print(f"  ... 외 {len(sys.path) - 5}개")

    # import 검색 순서
    print(f"""
📌 모듈 검색 순서:
  1. sys.modules (이미 로드된 모듈 캐시)
  2. built-in 모듈
  3. sys.path 순서대로:
     - 현재 스크립트 디렉토리
     - PYTHONPATH 환경 변수
     - 설치된 패키지 (site-packages)
""")

    # 상대 vs 절대 임포트
    print("""상대 임포트 vs 절대 임포트:

  절대 임포트 (권장):
    from mypackage.module_a import ClassA
    from mypackage.subpackage.module_c import func

  상대 임포트 (패키지 내부에서만):
    from . import module_b           # 같은 패키지
    from .module_b import func       # 같은 패키지의 모듈
    from .. import module_a          # 상위 패키지
    from ..subpackage import module  # 형제 패키지

  ⚠️ 상대 임포트는 스크립트 직접 실행 시 작동하지 않음
""")

    # importlib — 동적 import
    print("동적 import (importlib):")
    collections_mod = importlib.import_module("collections")
    counter_class = getattr(collections_mod, "Counter")
    result = counter_class("hello world")
    print(f"  importlib.import_module('collections').Counter('hello world')")
    print(f"  → {dict(result)}")


def demonstrate_stdlib_highlights() -> None:
    """자주 쓰이는 표준 라이브러리 모듈을 보여준다."""
    print("\n" + "=" * 60)
    print("6. 표준 라이브러리 하이라이트")
    print("=" * 60)

    # 자주 쓰이는 표준 라이브러리
    stdlib_modules: list[tuple[str, str]] = [
        ("os", "운영체제 인터페이스"),
        ("sys", "인터프리터 관련 변수/함수"),
        ("pathlib", "객체지향 파일 경로"),
        ("json", "JSON 파싱/생성"),
        ("csv", "CSV 파일 처리"),
        ("datetime", "날짜/시간 처리"),
        ("re", "정규표현식"),
        ("collections", "특수 컨테이너 (Counter, deque 등)"),
        ("itertools", "이터레이터 유틸리티"),
        ("functools", "고차 함수 유틸리티"),
        ("math", "수학 함수"),
        ("logging", "로깅 시스템"),
        ("unittest", "테스트 프레임워크"),
        ("typing", "타입 힌트 지원"),
        ("dataclasses", "데이터 클래스"),
        ("enum", "열거형"),
        ("abc", "추상 기본 클래스"),
        ("contextlib", "컨텍스트 매니저 유틸리티"),
        ("argparse", "명령줄 인수 파싱"),
        ("hashlib", "해시 알고리즘"),
        ("secrets", "보안 랜덤 생성"),
        ("tempfile", "임시 파일/디렉토리"),
        ("shutil", "파일 고수준 연산"),
        ("subprocess", "서브프로세스 관리"),
        ("asyncio", "비동기 I/O"),
        ("socket", "네트워크 소켓"),
        ("sqlite3", "SQLite 데이터베이스"),
        ("http.server", "HTTP 서버"),
        ("urllib", "URL 처리"),
    ]

    print(f"{'모듈':<15} {'설명'}")
    print(f"{'-'*15} {'-'*40}")
    for mod, desc in stdlib_modules:
        print(f"  {mod:<15} {desc}")

    # 실제 사용 예시
    import hashlib
    import secrets

    # secrets — 보안 랜덤
    token: str = secrets.token_hex(16)
    print(f"\nsecrets.token_hex(16) = {token}")

    # hashlib — 해시
    hash_value: str = hashlib.sha256(b"Hello").hexdigest()
    print(f"sha256('Hello') = {hash_value[:20]}...")

    # sys 정보
    print(f"\nsys 정보:")
    print(f"  sys.version = {sys.version.split()[0]}")
    print(f"  sys.platform = {sys.platform}")  # →   sys.platform = darwin
    print(f"  sys.executable = {Path(sys.executable).name}")
    print(f"  sys.maxsize = {sys.maxsize}")


if __name__ == "__main__":
    demonstrate_import_basics()
    demonstrate_name_main()
    demonstrate_all()
    demonstrate_package_structure()
    demonstrate_import_paths()
    demonstrate_stdlib_highlights()

    print("\n" + "=" * 60)
    print("✅ _230_modules_and_packages.py 학습 완료!")
    print("=" * 60)
