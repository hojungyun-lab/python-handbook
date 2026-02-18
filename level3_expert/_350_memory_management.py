"""
_350_memory_management.py — 메모리 관리 (Memory Management)

이 모듈에서 다루는 내용:
  1. 참조 카운팅
  2. 가비지 컬렉션 (gc)
  3. 약한 참조 (weakref)
  4. __slots__과 메모리 절약
  5. sys.getsizeof와 메모리 프로파일링
  6. 메모리 최적화 패턴

실행 방법:
    poetry run python 3_expert/_350_memory_management.py
"""

import gc
import sys
import weakref
from dataclasses import dataclass


def demonstrate_reference_counting() -> None:
    """참조 카운팅을 보여준다."""
    print("=" * 60)
    print("1. 참조 카운팅")
    print("=" * 60)

    # sys.getrefcount — 참조 수 확인
    a: list[int] = [1, 2, 3]
    print(f"리스트 생성 후 참조 수: {sys.getrefcount(a)}")
    # getrefcount 자체가 임시 참조를 추가하므로 +1

    b = a  # 참조 추가
    print(f"b = a 후: {sys.getrefcount(a)}")

    c = a  # 또 다른 참조
    print(f"c = a 후: {sys.getrefcount(a)}")

    del b  # 참조 해제
    print(f"del b 후: {sys.getrefcount(a)}")

    del c
    print(f"del c 후: {sys.getrefcount(a)}")

    # id() — 객체 식별
    x: int = 42
    y: int = 42
    print(f"\n작은 정수 캐싱:")
    print(f"  id(42) = {id(x)}")
    print(f"  id(42) = {id(y)}")
    print(f"  x is y = {x is y}")  # →   x is y = True

    # 문자열 인터닝
    s1: str = "hello"
    s2: str = "hello"
    print(f"\n문자열 인터닝:")
    print(f"  s1 is s2 = {s1 is s2}")  # →   s1 is s2 = True

    print(f"\n📌 참조 카운팅:")
    print(f"  참조 수가 0 → 즉시 해제 (CPython)")
    print(f"  단점: 순환 참조 감지 불가 → GC 필요")


def demonstrate_garbage_collection() -> None:
    """가비지 컬렉션을 보여준다."""
    print("\n" + "=" * 60)
    print("2. 가비지 컬렉션 (gc)")
    print("=" * 60)

    # GC 상태
    print(f"GC 활성화: {gc.isenabled()}")  # → GC 활성화: True
    print(f"임계값: {gc.get_threshold()}")  # → 임계값: (700, 10, 10)

    # 순환 참조 예시
    class Node:
        def __init__(self, name: str) -> None:
            self.name: str = name
            self.ref: Node | None = None

        def __repr__(self) -> str:
            return f"Node({self.name!r})"

    # 순환 참조 생성
    a: Node = Node("A")
    b: Node = Node("B")
    a.ref = b
    b.ref = a  # 순환!

    # del 해도 참조 카운트 ≠ 0
    del a, b

    # GC가 수거
    collected: int = gc.collect()
    print(f"\n순환 참조 수거: {collected}개 객체")

    # GC 세대 (generation)
    print(f"\nGC 세대별 통계:")
    for i, stats in enumerate(gc.get_stats()):
        print(f"  세대 {i}: {stats}")

    # __del__ 주의사항
    class Resource:
        def __init__(self, name: str) -> None:
            self.name: str = name

        def __del__(self) -> None:
            # __del__에서 예외가 발생하면 무시됨
            pass

    print(f"\n📌 __del__ 주의:")
    print(f"  호출 시점이 보장되지 않음")
    print(f"  순환 참조 시 호출 순서 불확정")
    print(f"  💡 리소스 정리는 컨텍스트 매니저 사용!")


def demonstrate_weakref() -> None:
    """약한 참조를 보여준다."""
    print("\n" + "=" * 60)
    print("3. 약한 참조 (weakref)")
    print("=" * 60)

    class ExpensiveObject:
        """비용이 높은 객체."""

        def __init__(self, name: str) -> None:
            self.name: str = name

        def __repr__(self) -> str:
            return f"ExpensiveObject({self.name!r})"

    # 약한 참조 생성
    obj: ExpensiveObject = ExpensiveObject("Heavy")
    weak: weakref.ref[ExpensiveObject] = weakref.ref(obj)

    print(f"강한 참조: {obj}")  # → 강한 참조: ExpensiveObject('Heavy')
    print(f"약한 참조: {weak()}")  # → 약한 참조: ExpensiveObject('Heavy')
    print(f"약한 참조 alive: {weak() is not None}")  # → 약한 참조 alive: True

    del obj  # 강한 참조 제거
    print(f"\ndel obj 후:")
    print(f"  약한 참조: {weak()}")  # →   약한 참조: None
    print(f"  alive: {weak() is not None}")  # →   alive: False

    # WeakValueDictionary — 캐시
    cache: weakref.WeakValueDictionary[str, ExpensiveObject] = (
        weakref.WeakValueDictionary()
    )

    def get_or_create(key: str) -> ExpensiveObject:
        obj = cache.get(key)
        if obj is None:
            obj = ExpensiveObject(key)
            cache[key] = obj
        return obj

    print(f"\nWeakValueDictionary (캐시):")
    item: ExpensiveObject = get_or_create("data1")
    print(f"  캐시 크기: {len(cache)}")
    del item
    gc.collect()
    print(f"  del 후 크기: {len(cache)}")

    # 콜백
    def on_finalize(ref: weakref.ref) -> None:
        print(f"  객체 해제됨!")

    obj2: ExpensiveObject = ExpensiveObject("Tracked")
    weak2: weakref.ref = weakref.ref(obj2, on_finalize)
    print(f"\n콜백:")
    del obj2
    gc.collect()


def demonstrate_slots_memory() -> None:
    """__slots__과 메모리 절약을 보여준다."""
    print("\n" + "=" * 60)
    print("4. __slots__과 메모리 절약")
    print("=" * 60)

    class WithDict:
        def __init__(self, x: int, y: int) -> None:
            self.x: int = x
            self.y: int = y

    class WithSlots:
        __slots__ = ("x", "y")

        def __init__(self, x: int, y: int) -> None:
            self.x: int = x
            self.y: int = y

    d: WithDict = WithDict(1, 2)
    s: WithSlots = WithSlots(1, 2)

    print(f"__dict__ 있음: {sys.getsizeof(d) + sys.getsizeof(d.__dict__)} bytes")
    print(f"__slots__ 사용: {sys.getsizeof(s)} bytes")

    # 대량 객체에서의 차이
    count: int = 100_000
    dict_objects: list[WithDict] = [WithDict(i, i) for i in range(count)]
    slots_objects: list[WithSlots] = [WithSlots(i, i) for i in range(count)]

    dict_size: int = sum(
        sys.getsizeof(o) + sys.getsizeof(o.__dict__)
        for o in dict_objects[:100]
    ) * (count // 100)
    slots_size: int = sum(
        sys.getsizeof(o) for o in slots_objects[:100]
    ) * (count // 100)

    print(f"\n{count:,}개 객체:")
    print(f"  __dict__: ~{dict_size / 1024 / 1024:.1f} MB")
    print(f"  __slots__: ~{slots_size / 1024 / 1024:.1f} MB")
    print(f"  절약: ~{(dict_size - slots_size) / 1024 / 1024:.1f} MB")

    # slots 제약
    print(f"\n📌 __slots__ 제약:")
    print(f"  ❌ 동적 속성 추가 불가 (별도 __dict__ 없으면)")
    print(f"  ❌ 다중 상속 시 충돌 가능")
    print(f"  ✅ 메모리 절약 + 속성 접근 약간 빠름")
    print(f"  💡 대량 객체 또는 성능 중요 시 사용")


def demonstrate_sizeof() -> None:
    """sys.getsizeof와 메모리 프로파일링을 보여준다."""
    print("\n" + "=" * 60)
    print("5. sys.getsizeof와 메모리 측정")
    print("=" * 60)

    # 기본 타입 크기
    types: list[tuple[str, object]] = [
        ("int(0)", 0),
        ("int(1)", 1),
        ("int(10**100)", 10**100),
        ("float(0.0)", 0.0),
        ("bool(True)", True),
        ("None", None),
        ("str('')", ""),
        ("str('hello')", "hello"),
        ("str('한글')", "한글"),
        ("list([])", []),
        ("list([1,2,3])", [1, 2, 3]),
        ("dict({})", {}),
        ("set()", set()),
        ("tuple(())", ()),
    ]

    print(f"{'타입':<20} {'크기 (bytes)':>12}")
    print(f"{'-'*20} {'-'*12}")
    for name, obj in types:
        print(f"{name:<20} {sys.getsizeof(obj):>12}")

    # 얕은 vs 깊은 크기
    nested: list[list[int]] = [[1, 2, 3], [4, 5, 6]]
    shallow: int = sys.getsizeof(nested)
    deep: int = shallow + sum(sys.getsizeof(item) for item in nested)
    print(f"\n얕은 크기 ([[1,2,3],[4,5,6]]): {shallow} bytes")
    print(f"깊은 크기 (재귀): {deep} bytes")


def demonstrate_memory_optimization() -> None:
    """메모리 최적화 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("6. 메모리 최적화 패턴")
    print("=" * 60)

    # 제너레이터 vs 리스트
    def list_approach(n: int) -> int:
        return sum([x**2 for x in range(n)])

    def gen_approach(n: int) -> int:
        return sum(x**2 for x in range(n))

    # 성능은 비슷하지만 메모리 사용량이 다름
    print("제너레이터 vs 리스트:")
    print(f"  리스트: sum([x²]) → 전체 리스트를 메모리에")
    print(f"  제너레이터: sum(x²) → 한 번에 하나씩")
    list_result: int = list_approach(1_000_000)
    gen_result: int = gen_approach(1_000_000)
    print(f"  결과 동일: {list_result == gen_result}")  # →   결과 동일: True

    # intern — 문자열 중복 제거
    strings: list[str] = [sys.intern(f"key_{i % 100}") for i in range(10000)]
    unique: int = len(set(id(s) for s in strings))
    print(f"\nsys.intern: {len(strings):,}개 문자열 → {unique}개 고유 객체")

    # __slots__ + dataclass
    @dataclass(slots=True)
    class Point:
        x: float
        y: float

    p: Point = Point(1.0, 2.0)
    print(f"\n@dataclass(slots=True): {p}")
    print(f"  크기: {sys.getsizeof(p)} bytes")

    # 메모리 최적화 체크리스트
    print(f"\n📌 메모리 최적화 체크리스트:")
    print(f"  ✅ 제너레이터 사용 (대량 데이터)")
    print(f"  ✅ __slots__ 사용 (대량 객체)")
    print(f"  ✅ sys.intern() (중복 문자열)")
    print(f"  ✅ array.array (동종 숫자 → list 대신)")
    print(f"  ✅ numpy (수치 계산)")
    print(f"  ✅ del + gc.collect() (큰 객체 명시적 해제)")
    print(f"  ✅ weakref (캐시에 약한 참조)")
    print(f"  ❌ 순환 참조 생성 (불가피 시 weakref)")


if __name__ == "__main__":
    demonstrate_reference_counting()
    demonstrate_garbage_collection()
    demonstrate_weakref()
    demonstrate_slots_memory()
    demonstrate_sizeof()
    demonstrate_memory_optimization()

    print("\n" + "=" * 60)
    print("✅ _350_memory_management.py 학습 완료!")
    print("=" * 60)
