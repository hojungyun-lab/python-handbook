"""
050_tuples.py — 튜플 (Tuples)

이 모듈에서 다루는 내용:
  1. 튜플 생성과 기본 연산
  2. 튜플의 불변성 (Immutability)
  3. 튜플 언패킹
  4. Named Tuple (collections.namedtuple, typing.NamedTuple)
  5. 리스트 vs 튜플 비교
  6. 튜플의 활용 패턴

실행 방법:
    poetry run python 1_basic/050_tuples.py
"""

from collections import namedtuple
from typing import NamedTuple


def demonstrate_tuple_creation() -> None:
    """튜플 생성 방법을 보여준다."""
    print("=" * 60)
    print("1. 튜플 생성")
    print("=" * 60)

    # 리터럴 — 괄호는 선택사항 (쉼표가 핵심)
    empty: tuple[()] = ()
    single: tuple[int] = (42,)  # ⚠️ 쉼표 필수!
    not_tuple: int = (42)       # 이것은 그냥 int!
    numbers: tuple[int, ...] = (1, 2, 3, 4, 5)
    mixed: tuple[int, str, bool] = (1, "hello", True)

    print(f"empty = {empty}")  # → empty = ()
    print(f"single = {single}, type = {type(single).__name__}")  # → single = (42,), type = tuple
    print(f"not_tuple = {not_tuple}, type = {type(not_tuple).__name__}")  # → not_tuple = 42, type = int
    print(f"numbers = {numbers}")  # → numbers = (1, 2, 3, 4, 5)
    print(f"mixed = {mixed}")  # → mixed = (1, 'hello', True)

    # 괄호 없이 생성
    without_parens: tuple[int, int, int] = 1, 2, 3
    print(f"\n괄호 없이: {without_parens}")  # → 괄호 없이: (1, 2, 3)

    # tuple() 생성자
    from_list: tuple[int, ...] = tuple([1, 2, 3])
    from_range: tuple[int, ...] = tuple(range(5))
    from_str: tuple[str, ...] = tuple("Python")

    print(f"\ntuple([1,2,3]) = {from_list}")  # → tuple([1,2,3]) = (1, 2, 3)
    print(f"tuple(range(5)) = {from_range}")  # → tuple(range(5)) = (0, 1, 2, 3, 4)
    print(f"tuple('Python') = {from_str}")  # → tuple('Python') = ('P', 'y', 't', 'h', 'o', 'n')

    # 기본 연산
    print(f"\n기본 연산:")
    print(f"  len(numbers) = {len(numbers)}")  # →   len(numbers) = 5
    print(f"  min(numbers) = {min(numbers)}")  # →   min(numbers) = 1
    print(f"  max(numbers) = {max(numbers)}")  # →   max(numbers) = 5
    print(f"  sum(numbers) = {sum(numbers)}")  # →   sum(numbers) = 15
    print(f"  3 in numbers = {3 in numbers}")  # →   3 in numbers = True
    print(f"  numbers.index(3) = {numbers.index(3)}")  # →   numbers.index(3) = 2
    print(f"  numbers.count(3) = {numbers.count(3)}")  # →   numbers.count(3) = 1

    # 연결과 반복
    t1: tuple[int, ...] = (1, 2)
    t2: tuple[int, ...] = (3, 4)
    print(f"\n연결: {t1} + {t2} = {t1 + t2}")  # → 연결: (1, 2) + (3, 4) = (1, 2, 3, 4)
    print(f"반복: {t1} * 3 = {t1 * 3}")  # → 반복: (1, 2) * 3 = (1, 2, 1, 2, 1, 2)


def demonstrate_immutability() -> None:
    """튜플의 불변성을 보여준다."""
    print("\n" + "=" * 60)
    print("2. 튜플의 불변성")
    print("=" * 60)

    t: tuple[int, int, int] = (1, 2, 3)

    try:
        t[0] = 10  # type: ignore[index]
    except TypeError as e:
        print(f"t[0] = 10 → TypeError: {e}")  # → t[0] = 10 → TypeError: 'tuple' object does not support item assignment

    # ⚠️ 튜플 안의 가변 객체는 수정 가능!
    mutable_inside: tuple[list[int], list[int]] = ([1, 2], [3, 4])
    print(f"\n⚠️ 튜플 안의 가변 객체:")
    print(f"  수정 전: {mutable_inside}")  # →   수정 전: ([1, 2], [3, 4])
    mutable_inside[0].append(99)
    print(f"  수정 후: {mutable_inside}")  # →   수정 후: ([1, 2, 99], [3, 4])
    print(f"  💡 튜플의 '참조'는 변경 불가, 참조된 객체 내부는 변경 가능!")

    # 해시 가능성 — 내부에 가변 객체가 없을 때만
    hashable: tuple[int, str] = (1, "hello")
    print(f"\nhash((1, 'hello')) = {hash(hashable)}")  # → hash((1, 'hello')) = <해시값>

    try:
        hash(mutable_inside)
    except TypeError as e:
        print(f"hash(([1,2],[3,4])) → TypeError: {e}")  # → hash(([1,2],[3,4])) → TypeError: unhashable type: 'list'


def demonstrate_unpacking() -> None:
    """튜플 언패킹을 보여준다."""
    print("\n" + "=" * 60)
    print("3. 튜플 언패킹")
    print("=" * 60)

    # 기본 언패킹
    point: tuple[int, int] = (10, 20)
    x: int
    y: int
    x, y = point
    print(f"x, y = (10, 20) → x={x}, y={y}")  # → x, y = (10, 20) → x=10, y=20

    # 변수 스왑
    a: int = 1
    b: int = 2
    a, b = b, a
    print(f"\n스왑: a={a}, b={b}")

    # 확장 언패킹 (starred)
    first: int
    middle: list[int]
    last: int
    first, *middle, last = (1, 2, 3, 4, 5)
    print(f"\nfirst, *middle, last = (1,2,3,4,5)")
    print(f"  first={first}, middle={middle}, last={last}")  # →   first=1, middle=[2, 3, 4], last=5

    # 함수 반환값으로 활용
    def get_stats(numbers: list[int]) -> tuple[int, int, float]:
        """리스트의 최솟값, 최댓값, 평균을 반환한다."""
        return min(numbers), max(numbers), sum(numbers) / len(numbers)

    nums: list[int] = [4, 2, 8, 1, 5]
    lo: int
    hi: int
    avg: float
    lo, hi, avg = get_stats(nums)
    print(f"\nget_stats({nums}):")
    print(f"  min={lo}, max={hi}, avg={avg}")  # →   min=1, max=8, avg=4.0

    # _ 로 불필요한 값 무시
    _, _, avg_only = get_stats(nums)
    print(f"\n평균만 필요: avg={avg_only}")  # → 평균만 필요: avg=4.0

    # 중첩 언패킹
    data: tuple[str, tuple[int, int]] = ("Seoul", (37, 127))
    city: str
    lat: int
    lon: int
    city, (lat, lon) = data
    print(f"\n중첩 언패킹: city={city!r}, lat={lat}, lon={lon}")  # → 중첩 언패킹: city='Seoul', lat=37, lon=127


def demonstrate_named_tuple() -> None:
    """Named Tuple을 보여준다."""
    print("\n" + "=" * 60)
    print("4. Named Tuple")
    print("=" * 60)

    # collections.namedtuple (클래식 방식)
    Point2D = namedtuple("Point2D", ["x", "y"])
    p: Point2D = Point2D(3, 4)
    print("collections.namedtuple:")
    print(f"  p = {p}")  # →   p = Point2D(x=3, y=4)
    print(f"  p.x = {p.x}, p.y = {p.y}")  # →   p.x = 3, p.y = 4
    print(f"  p[0] = {p[0]}, p[1] = {p[1]}")  # →   p[0] = 3, p[1] = 4

    # typing.NamedTuple (권장 방식 — 타입 힌트 지원)
    class Point3D(NamedTuple):
        """3차원 좌표를 나타내는 Named Tuple."""
        x: float
        y: float
        z: float = 0.0  # 기본값 가능

    p3: Point3D = Point3D(1.0, 2.0)
    print(f"\ntyping.NamedTuple:")
    print(f"  p3 = {p3}")  # →   p3 = Point3D(x=1.0, y=2.0, z=0.0)
    print(f"  p3.z (기본값) = {p3.z}")  # →   p3.z (기본값) = 0.0

    # _asdict(), _replace()
    d: dict[str, float] = p3._asdict()
    print(f"  _asdict() = {d}")  # →   _asdict() = {'x': 1.0, 'y': 2.0, 'z': 0.0}
    p3_moved: Point3D = p3._replace(z=5.0)
    print(f"  _replace(z=5.0) = {p3_moved}")  # →   _replace(z=5.0) = Point3D(x=1.0, y=2.0, z=5.0)

    # 실용 예시: RGB 색상
    class Color(NamedTuple):
        """RGB 색상을 나타내는 Named Tuple."""
        red: int
        green: int
        blue: int

        def hex_code(self) -> str:
            """16진수 색상 코드를 반환한다."""
            return f"#{self.red:02X}{self.green:02X}{self.blue:02X}"

    coral: Color = Color(255, 127, 80)
    print(f"\nColor 예시:")
    print(f"  coral = {coral}")  # →   coral = Color(red=255, green=127, blue=80)
    print(f"  hex = {coral.hex_code()}")  # →   hex = #FF7F50


def demonstrate_list_vs_tuple() -> None:
    """리스트와 튜플의 차이를 비교한다."""
    print("\n" + "=" * 60)
    print("5. 리스트 vs 튜플 비교")
    print("=" * 60)

    import sys

    # 메모리 사용량 비교
    list_data: list[int] = [1, 2, 3, 4, 5]
    tuple_data: tuple[int, ...] = (1, 2, 3, 4, 5)

    print(f"메모리 비교:")
    print(f"  list  {list_data}: {sys.getsizeof(list_data)} bytes")  # →   list  [1, 2, 3, 4, 5]: <사이즈> bytes
    print(f"  tuple {tuple_data}: {sys.getsizeof(tuple_data)} bytes")  # →   tuple (1, 2, 3, 4, 5): <사이즈> bytes
    print(f"  💡 튜플이 더 적은 메모리를 사용!")

    # 속도 비교 (생성)
    import timeit

    list_time: float = timeit.timeit("[1,2,3,4,5]", number=1_000_000)
    tuple_time: float = timeit.timeit("(1,2,3,4,5)", number=1_000_000)
    print(f"\n생성 속도 (100만 회):")
    print(f"  list:  {list_time:.4f}초")
    print(f"  tuple: {tuple_time:.4f}초")

    # 사용 가이드라인
    print(f"\n📌 언제 무엇을 사용?")
    print(f"  tuple: 변경 불필요, 고정 구조 (좌표, 색상, DB 행)")
    print(f"  tuple: dict 키, set 원소로 사용 가능 (해시 가능)")
    print(f"  tuple: 함수 다중 반환값")
    print(f"  list:  요소 추가/삭제 필요, 동적 크기")
    print(f"  list:  같은 타입의 가변 컬렉션")


def demonstrate_tuple_patterns() -> None:
    """튜플의 실용적 활용 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("6. 튜플 활용 패턴")
    print("=" * 60)

    # dict 키로 사용
    grid: dict[tuple[int, int], str] = {
        (0, 0): "origin",
        (1, 0): "right",
        (0, 1): "up",
    }
    print(f"dict 키로 사용: grid[(0,0)] = {grid[(0, 0)]!r}")  # → dict 키로 사용: grid[(0,0)] = 'origin'

    # enumerate와 조합
    items: list[str] = ["apple", "banana", "cherry"]
    indexed: list[tuple[int, str]] = list(enumerate(items))
    print(f"\nenumerate: {indexed}")  # → enumerate: [(0, 'apple'), (1, 'banana'), (2, 'cherry')]

    # zip과 조합
    names: list[str] = ["Alice", "Bob"]
    scores: list[int] = [85, 92]
    pairs: list[tuple[str, int]] = list(zip(names, scores))
    print(f"zip: {pairs}")  # → zip: [('Alice', 85), ('Bob', 92)]

    # 튜플을 이용한 다중 비교
    version1: tuple[int, int, int] = (3, 12, 0)
    version2: tuple[int, int, int] = (3, 13, 0)
    print(f"\n버전 비교: {version1} < {version2} = {version1 < version2}")  # → 버전 비교: (3, 12, 0) < (3, 13, 0) = True
    print(f"💡 튜플 비교는 사전식(lexicographic) 순서")

    # 불변 레코드로 사용
    Record = tuple[str, int, str]
    records: list[Record] = [
        ("Alice", 30, "Engineer"),
        ("Bob", 25, "Designer"),
        ("Charlie", 35, "Manager"),
    ]
    print(f"\n레코드:")
    for name, age, role in records:
        print(f"  {name} ({age}) — {role}")


if __name__ == "__main__":
    demonstrate_tuple_creation()
    demonstrate_immutability()
    demonstrate_unpacking()
    demonstrate_named_tuple()
    demonstrate_list_vs_tuple()
    demonstrate_tuple_patterns()

    print("\n" + "=" * 60)
    print("✅ 050_tuples.py 학습 완료!")
    print("=" * 60)
