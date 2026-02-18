"""
010_variables.py — 변수와 데이터 타입

이 모듈에서 다루는 내용:
  1. 변수 선언과 동적 타이핑
  2. 기본 데이터 타입: int, float, str, bool, None
  3. 타입 힌트 (Type Hints)
  4. type() 함수로 타입 확인
  5. 타입 캐스팅 (형변환)
  6. 변수 네이밍 규칙과 관례
  7. 변수의 메모리와 id()
  8. 상수 관례 (UPPER_CASE)

실행 방법:
    poetry run python 1_basic/010_variables.py
"""


def demonstrate_dynamic_typing() -> None:
    """Python의 동적 타이핑을 보여준다.

    Python은 변수에 타입을 선언하지 않아도 값에 따라 타입이 자동 결정된다.
    같은 변수에 다른 타입의 값을 재할당할 수도 있다. (권장하지 않음)
    """
    print("=" * 60)
    print("1. 동적 타이핑 (Dynamic Typing)")
    print("=" * 60)

    # 변수 선언 — 타입 선언 없이 값을 할당하면 자동으로 타입이 결정됨
    name: str = "Python"
    version: float = 3.13
    is_awesome: bool = True

    print(f"name = {name!r}, type: {type(name).__name__}")  # → name = 'Python', type: str
    print(f"version = {version}, type: {type(version).__name__}")  # → version = 3.13, type: float
    print(f"is_awesome = {is_awesome}, type: {type(is_awesome).__name__}")  # → is_awesome = True, type: bool

    # 동적 타이핑: 같은 변수에 다른 타입 재할당 가능 (비권장)
    value: int | str = 42
    print(f"\nvalue = {value}, type: {type(value).__name__}")  # → value = 42, type: int
    value = "이제 문자열"  # 타입이 바뀜
    print(f"value = {value!r}, type: {type(value).__name__}")  # → value = '이제 문자열', type: str
    print("⚠️  같은 변수에 다른 타입을 재할당하는 것은 비권장됩니다.")


def demonstrate_basic_types() -> None:
    """Python의 기본 데이터 타입을 보여준다.

    int, float, str, bool, None — 이 5가지가 가장 기본적인 타입이다.
    """
    print("\n" + "=" * 60)
    print("2. 기본 데이터 타입 (Built-in Types)")
    print("=" * 60)

    # int: 정수 (크기 제한 없음 — Python은 임의 정밀도 정수 지원)
    small_int: int = 42
    big_int: int = 10**100  # 구골(googol) — 매우 큰 정수도 OK
    binary: int = 0b1010  # 2진수 리터럴
    octal: int = 0o17  # 8진수 리터럴
    hexadecimal: int = 0xFF  # 16진수 리터럴
    readable_int: int = 1_000_000  # 밑줄로 가독성 향상 (Python 3.6+)

    print(f"small_int = {small_int}")  # → small_int = 42
    print(f"big_int (10^100) = {big_int}")  # → big_int (10^100) = 100000...00000 (101자리)
    print(f"binary (0b1010) = {binary}")  # → binary (0b1010) = 10
    print(f"octal (0o17) = {octal}")  # → octal (0o17) = 15
    print(f"hexadecimal (0xFF) = {hexadecimal}")  # → hexadecimal (0xFF) = 255
    print(f"readable_int = {readable_int:,}")  # → readable_int = 1,000,000

    # float: 부동소수점 (IEEE 754 double precision, 약 15-17자리 유효숫자)
    pi: float = 3.141592653589793
    scientific: float = 2.998e8  # 과학적 표기법 (빛의 속도)
    infinity: float = float("inf")
    not_a_number: float = float("nan")

    print(f"\npi = {pi}")  # → pi = 3.141592653589793
    print(f"scientific (빛의 속도) = {scientific:,.0f} m/s")  # → scientific (빛의 속도) = 299,800,000 m/s
    print(f"infinity = {infinity}")  # → infinity = inf
    print(f"not_a_number = {not_a_number}")  # → not_a_number = nan

    # ⚠️ 부동소수점 주의사항
    result: float = 0.1 + 0.2
    print(f"\n⚠️  0.1 + 0.2 = {result}  (정확히 0.3이 아님!)")  # → ⚠️  0.1 + 0.2 = 0.30000000000000004  (정확히 0.3이 아님!)
    print(f"   0.1 + 0.2 == 0.3 → {result == 0.3}")  # → 0.1 + 0.2 == 0.3 → False

    # str: 문자열
    single: str = '작은따옴표'
    double: str = "큰따옴표"
    multiline: str = """여러 줄
문자열"""

    print(f"\nsingle = {single!r}")  # → single = '작은따옴표'
    print(f"double = {double!r}")  # → double = '큰따옴표'
    print(f"multiline = {multiline!r}")  # → multiline = '여러 줄\n문자열'

    # bool: 불리언 (True/False) — int의 서브클래스
    is_valid: bool = True
    is_empty: bool = False
    print(f"\nis_valid = {is_valid}")  # → is_valid = True
    print(f"is_empty = {is_empty}")  # → is_empty = False
    print(f"bool은 int의 서브클래스: True + True = {True + True}")  # → bool은 int의 서브클래스: True + True = 2
    print(f"issubclass(bool, int) = {issubclass(bool, int)}")  # → issubclass(bool, int) = True

    # None: 값이 없음을 나타내는 싱글톤 객체
    nothing: None = None
    print(f"\nnothing = {nothing}")  # → nothing = None
    print(f"type(None) = {type(nothing).__name__}")  # → type(None) = NoneType
    print(f"nothing is None = {nothing is None}  (is 연산자로 비교)")  # → nothing is None = True  (is 연산자로 비교)


def demonstrate_type_hints() -> None:
    """Python 3.10+ 스타일 타입 힌트를 보여준다.

    PEP 604 (Python 3.10+): Union 대신 | 연산자 사용
    빌트인 타입을 직접 제네릭으로 사용 (list[int] 등)
    """
    print("\n" + "=" * 60)
    print("3. 타입 힌트 (Type Hints) — Python 3.10+ 스타일")
    print("=" * 60)

    # 기본 타입 힌트
    name: str = "Python"
    age: int = 33
    height: float = 1.75
    is_active: bool = True

    # 컬렉션 타입 힌트 (빌트인 타입 파라미터 — Python 3.9+)
    numbers: list[int] = [1, 2, 3]
    mapping: dict[str, int] = {"a": 1, "b": 2}
    coordinates: tuple[float, float] = (37.5665, 126.9780)
    unique_ids: set[int] = {1, 2, 3}

    # Union 타입 (PEP 604 — Python 3.10+)
    value: int | str = 42  # int 또는 str
    optional_name: str | None = None  # Optional[str]과 동일

    print(f"name: str = {name!r}")  # → name: str = 'Python'
    print(f"numbers: list[int] = {numbers}")  # → numbers: list[int] = [1, 2, 3]
    print(f"mapping: dict[str, int] = {mapping}")  # → mapping: dict[str, int] = {'a': 1, 'b': 2}
    print(f"coordinates: tuple[float, float] = {coordinates}")  # → coordinates: tuple[float, float] = (37.5665, 126.978)
    print(f"unique_ids: set[int] = {unique_ids}")  # → unique_ids: set[int] = {1, 2, 3}
    print(f"value: int | str = {value}")  # → value: int | str = 42
    print(f"optional_name: str | None = {optional_name}")  # → optional_name: str | None = None


def demonstrate_type_checking() -> None:
    """type()과 isinstance()를 이용한 타입 확인 방법을 보여준다."""
    print("\n" + "=" * 60)
    print("4. 타입 확인 (Type Checking)")
    print("=" * 60)

    values: list[object] = [42, 3.14, "hello", True, None, [1, 2], (3, 4), {5, 6}]

    print(f"{'값':<15} {'type()':<20} {'isinstance 예시'}")
    print("-" * 55)
    for v in values:
        type_name: str = type(v).__name__
        # isinstance는 상속 관계도 확인 (bool은 int의 서브클래스)
        # 튜플 중 하나라도 해당되면 True. Python 3.10+: isinstance(v, int | float)도 가능
        is_numeric: bool = isinstance(v, (int, float))
        print(f"{str(v):<15} {type_name:<20} numeric={is_numeric}")
        # → 42              int                  numeric=True
        # → 3.14            float                numeric=True
        # → hello           str                  numeric=False
        # → True            bool                 numeric=True
        # → None            NoneType             numeric=False
        # → [1, 2]          list                 numeric=False
        # → (3, 4)          tuple                numeric=False
        # → {5, 6}          set                  numeric=False

    # type() vs isinstance() 차이
    print("\n📌 type() vs isinstance() 차이:")
    print(f"   type(True) == int → {type(True) == int}")  # → False
    print(f"   isinstance(True, int) → {isinstance(True, int)}")  # → True
    print("   → isinstance()는 상속 관계를 고려하므로 더 권장됨")


def demonstrate_type_casting() -> None:
    """타입 캐스팅(형변환) 방법을 보여준다."""
    print("\n" + "=" * 60)
    print("5. 타입 캐스팅 (Type Casting)")
    print("=" * 60)

    # int 변환
    from_float: int = int(3.7)  # 소수점 이하 버림 (반올림 아님!)
    from_str: int = int("42")
    from_bool: int = int(True)
    from_hex_str: int = int("ff", 16)  # 두 번째 인자 = base(진법), 16진수 "ff" → 15×16+15 = 255
    from_bin_str: int = int("1010", 2)  # base=2, 2진수 "1010" → 8+0+2+0 = 10

    print("int() 변환:")
    print(f"  int(3.7) = {from_float}  (버림, 반올림 아님!)")  # → int(3.7) = 3  (버림, 반올림 아님!)
    print(f"  int('42') = {from_str}")  # → int('42') = 42
    print(f"  int(True) = {from_bool}")  # → int(True) = 1
    print(f"  int('ff', 16) = {from_hex_str}")  # → int('ff', 16) = 255
    print(f"  int('1010', 2) = {from_bin_str}")  # → int('1010', 2) = 10

    # float 변환
    float_from_int: float = float(42)
    float_from_str: float = float("3.14")
    float_from_bool: float = float(False)

    print(f"\nfloat() 변환:")
    print(f"  float(42) = {float_from_int}")  # → float(42) = 42.0
    print(f"  float('3.14') = {float_from_str}")  # → float('3.14') = 3.14
    print(f"  float(False) = {float_from_bool}")  # → float(False) = 0.0

    # str 변환
    str_from_int: str = str(42)
    str_from_float: str = str(3.14)
    str_from_bool: str = str(True)
    str_from_list: str = str([1, 2, 3])

    print(f"\nstr() 변환:")
    print(f"  str(42) = {str_from_int!r}")  # → str(42) = '42'
    print(f"  str(3.14) = {str_from_float!r}")  # → str(3.14) = '3.14'
    print(f"  str(True) = {str_from_bool!r}")  # → str(True) = 'True'
    print(f"  str([1, 2, 3]) = {str_from_list!r}")  # → str([1, 2, 3]) = '[1, 2, 3]'

    # bool 변환 (Truthy / Falsy)
    print(f"\nbool() 변환 (Falsy 값들):")
    falsy_values: list[object] = [0, 0.0, "", [], {}, set(), None, False]
    for v in falsy_values:
        print(f"  bool({v!r:>10}) = {bool(v)}")
        # → bool(         0) = False
        # → bool(       0.0) = False
        # → bool(        '') = False
        # → bool(        []) = False
        # → bool(        {}) = False
        # → bool(     set()) = False
        # → bool(      None) = False
        # → bool(     False) = False

    print(f"\nbool() 변환 (Truthy 값들):")
    truthy_values: list[object] = [1, -1, 0.1, "hello", [0], {"a": 1}, {0}]
    for v in truthy_values:
        print(f"  bool({v!r:>15}) = {bool(v)}")
        # → bool(              1) = True
        # → bool(             -1) = True
        # → bool(            0.1) = True
        # → bool(        'hello') = True
        # → bool(            [0]) = True
        # → bool(       {'a': 1}) = True
        # → bool(            {0}) = True


def demonstrate_variable_identity() -> None:
    """변수의 메모리 주소(id)와 identity 비교를 보여준다."""
    print("\n" + "=" * 60)
    print("6. 변수의 메모리와 id()")
    print("=" * 60)

    # 정수 캐싱 (Integer Interning)
    # CPython은 -5 ~ 256 범위의 정수를 시작 시 미리 생성하여 캐싱
    # 이 범위 내 같은 값은 항상 동일 객체 → is True
    # 범위 밖 (예: 257)은 매번 새 객체 생성 → is False
    a: int = 256
    b: int = 256
    print(f"a = {a}, id(a) = {id(a)}")  # → a = 256, id(a) = <캐싱된 정수 주소>
    print(f"b = {b}, id(b) = {id(b)}")  # → b = 256, id(b) = <동일 주소>
    print(f"a is b = {a is b}")  # → a is b = True

    # 문자열 인터닝 (String Interning)
    # 식별자 형태(영문, 숫자, _)의 짧은 문자열은 자동 인터닝
    # 공백/특수문자 포함 문자열은 인터닝 보장되지 않음
    s1: str = "hello"
    s2: str = "hello"
    print(f"\ns1 = {s1!r}, id(s1) = {id(s1)}")  # → s1 = 'hello', id(s1) = <인터닝된 주소>
    print(f"s2 = {s2!r}, id(s2) = {id(s2)}")  # → s2 = 'hello', id(s2) = <동일 주소>
    print(f"s1 is s2 = {s1 is s2}")  # → s1 is s2 = True

    # ⚠️ int 캐싱, str 인터닝 모두 CPython 구현 세부사항
    # 값 비교는 반드시 == 사용! (is는 동일 객체 확인 용도)

    # == vs is
    c: list[int] = [1, 2, 3]
    d: list[int] = [1, 2, 3]
    print(f"\nc = {c}, id(c) = {id(c)}")  # → c = [1, 2, 3], id(c) = <주소A>
    print(f"d = {d}, id(d) = {id(d)}")  # → d = [1, 2, 3], id(d) = <주소B (다름)>
    print(f"c == d = {c == d}  (값 비교)")  # → c == d = True  (값 비교)
    print(f"c is d = {c is d}  (동일 객체 비교)")  # → c is d = False  (동일 객체 비교)
    print("📌 == 는 값 비교, is 는 동일 객체(메모리 주소) 비교")


def demonstrate_naming_conventions() -> None:
    """Python 변수 네이밍 규칙과 관례를 보여준다."""
    print("\n" + "=" * 60)
    print("7. 네이밍 규칙과 관례")
    print("=" * 60)

    # 상수 관례 (UPPER_CASE) — Python에는 진짜 상수가 없음
    MAX_RETRIES: int = 3
    PI: float = 3.141592653589793
    BASE_URL: str = "https://api.example.com"
    # Python 3.8+: typing.Final로 상수 의도 표현 가능
    # from typing import Final
    # MAX_RETRIES: Final[int] = 3

    print("상수 관례 (UPPER_SNAKE_CASE):")
    print(f"  MAX_RETRIES = {MAX_RETRIES}")  # → MAX_RETRIES = 3
    print(f"  PI = {PI}")  # → PI = 3.141592653589793
    print(f"  BASE_URL = {BASE_URL!r}")  # → BASE_URL = 'https://api.example.com'

    print("\n📌 Python 네이밍 규칙 요약:")
    print("  ✅ snake_case     → 변수, 함수, 메서드, 모듈")
    print("  ✅ PascalCase     → 클래스")
    print("  ✅ UPPER_CASE     → 상수")
    print("  ✅ _private       → 내부 사용 (관례)")
    print("  ✅ __mangled      → 이름 맹글링 (클래스 내)")
    print("  ✅ __dunder__     → 특수 메서드 (매직 메서드)")
    print("  ❌ camelCase      → Python에서는 비권장")

    # 예약어는 변수명으로 사용 불가
    import keyword
    print(f"\n예약어 목록 ({len(keyword.kwlist)}개):")  # → 35개
    for i in range(0, len(keyword.kwlist), 5):
        chunk: list[str] = keyword.kwlist[i:i + 5]
        print(f"  {', '.join(chunk)}")
        # → False, None, True, and, as
        # → assert, async, await, break, class
        # → continue, def, del, elif, else
        # → except, finally, for, from, global
        # → if, import, in, is, lambda
        # → nonlocal, not, or, pass, raise
        # → return, try, while, with, yield


def demonstrate_multiple_assignment() -> None:
    """다중 할당, 스왑, 언패킹 등 고급 할당 기법을 보여준다."""
    print("\n" + "=" * 60)
    print("8. 다중 할당과 언패킹")
    print("=" * 60)

    # 다중 할당
    x: int
    y: int
    z: int
    x, y, z = 1, 2, 3
    print(f"x, y, z = 1, 2, 3 → x={x}, y={y}, z={z}")  # → x, y, z = 1, 2, 3 → x=1, y=2, z=3

    # 변수 스왑 (임시 변수 불필요)
    a: int = 10
    b: int = 20
    a, b = b, a
    print(f"\na, b 스왑 후: a={a}, b={b}")  # → a, b 스왑 후: a=20, b=10

    # 동일 값 할당
    p: int
    q: int
    r: int
    p = q = r = 0
    print(f"\np = q = r = 0 → p={p}, q={q}, r={r}")  # → p = q = r = 0 → p=0, q=0, r=0

    # 확장 언패킹 (starred expression)
    first: int
    rest: list[int]
    last: int
    first, *rest, last = [1, 2, 3, 4, 5]
    print(f"\nfirst, *rest, last = [1,2,3,4,5]")
    print(f"  first={first}, rest={rest}, last={last}")  # → first=1, rest=[2, 3, 4], last=5

    # 언더스코어로 불필요한 값 무시
    name: str
    _: object  # 사용하지 않는 값
    age: int
    name, _, age = ("Alice", "ignored_value", 30)
    print(f"\nname, _, age = ('Alice', 'ignored', 30)")
    print(f"  name={name!r}, age={age}")  # → name='Alice', age=30


if __name__ == "__main__":
    demonstrate_dynamic_typing()
    demonstrate_basic_types()
    demonstrate_type_hints()
    demonstrate_type_checking()
    demonstrate_type_casting()
    demonstrate_variable_identity()
    demonstrate_naming_conventions()
    demonstrate_multiple_assignment()

    print("\n" + "=" * 60)
    print("✅ 010_variables.py 학습 완료!")
    print("=" * 60)
