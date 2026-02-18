"""
_280_closures_and_functional.py — 클로저와 함수형 프로그래밍

이 모듈에서 다루는 내용:
  1. 클로저 (Closures)
  2. lambda 함수
  3. map, filter, reduce
  4. functools (partial, lru_cache, cache, reduce)
  5. operator 모듈
  6. 함수형 패턴 조합

실행 방법:
    poetry run python 2_intermediate/_280_closures_and_functional.py
"""

import functools
import operator
from collections.abc import Callable


def demonstrate_closures() -> None:
    """클로저를 보여준다."""
    print("=" * 60)
    print("1. 클로저 (Closures)")
    print("=" * 60)

    # 클로저 = 자유 변수를 캡처한 내부 함수
    def make_greeter(greeting: str) -> Callable[[str], str]:
        """인사 함수를 생성하는 팩토리."""
        def greeter(name: str) -> str:
            return f"{greeting}, {name}!"  # greeting = 자유 변수
        return greeter

    hello: Callable[[str], str] = make_greeter("Hello")
    annyeong: Callable[[str], str] = make_greeter("안녕하세요")

    print(f"hello('World') = {hello('World')}")  # → hello('World') = Hello, World!
    print(f"annyeong('Python') = {annyeong('Python')}")  # → annyeong('Python') = 안녕하세요, Python!

    # __closure__ 확인
    print(f"\n클로저 내부:")
    if hello.__closure__:
        for cell in hello.__closure__:
            print(f"  캡처된 값: {cell.cell_contents!r}")

    # 상태를 가진 클로저
    def make_accumulator(initial: float = 0) -> Callable[[float], float]:
        """누산기 클로저."""
        total: list[float] = [initial]  # 가변 객체로 상태 유지

        def add(value: float) -> float:
            total[0] += value
            return total[0]

        return add

    acc: Callable[[float], float] = make_accumulator()
    print(f"\n누산기:")
    for v in [10, 20, 30]:
        print(f"  add({v}) = {acc(v)}")

    # nonlocal로 상태 유지
    def counter() -> Callable[[], int]:
        count: int = 0
        def increment() -> int:
            nonlocal count
            count += 1
            return count
        return increment

    c: Callable[[], int] = counter()
    print(f"\nnonlocal 카운터: {c()}, {c()}, {c()}")  # → nonlocal 카운터: 1, 2, 3


def demonstrate_lambda() -> None:
    """lambda 함수를 보여준다."""
    print("\n" + "=" * 60)
    print("2. lambda 함수")
    print("=" * 60)

    # 기본 lambda
    square: Callable[[int], int] = lambda x: x ** 2
    add: Callable[[int, int], int] = lambda x, y: x + y

    print(f"lambda x: x**2 → square(5) = {square(5)}")  # → ... = 25
    print(f"lambda x, y: x+y → add(3, 4) = {add(3, 4)}")  # → ... = 7

    # 정렬에 활용
    students: list[dict[str, str | int]] = [
        {"name": "Charlie", "grade": 85},
        {"name": "Alice", "grade": 92},
        {"name": "Bob", "grade": 78},
    ]
    by_grade: list[dict[str, str | int]] = sorted(
        students, key=lambda s: s["grade"], reverse=True
    )
    print(f"\n성적순 정렬: {[s['name'] for s in by_grade]}")  # → 성적순 정렬: ['Alice', 'Charlie', 'Bob']

    # 조건부 lambda
    classify: Callable[[int], str] = lambda x: "양수" if x > 0 else "음수" if x < 0 else "영"
    print(f"\n분류: {classify(5)}, {classify(-3)}, {classify(0)}")  # → 분류: 양수, 음수, 영

    # lambda vs def
    print(f"\n📌 lambda vs def:")
    print(f"  lambda: 간단한 한 줄 표현식, 이름 없는 함수")
    print(f"  def:    복잡한 로직, 여러 문장, 독스트링")
    print(f"  💡 lambda를 변수에 할당하는 것은 비권장 → def 사용")


def demonstrate_map_filter_reduce() -> None:
    """map, filter, reduce를 보여준다."""
    print("\n" + "=" * 60)
    print("3. map, filter, reduce")
    print("=" * 60)

    numbers: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # map — 변환
    squared: list[int] = list(map(lambda x: x**2, numbers))
    print(f"map(x²): {squared}")  # → map(x²): [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

    # 여러 이터러블 map
    a: list[int] = [1, 2, 3]
    b: list[int] = [10, 20, 30]
    sums: list[int] = list(map(lambda x, y: x + y, a, b))
    print(f"map(x+y): {sums}")  # → map(x+y): [11, 22, 33]

    # filter — 필터링
    evens: list[int] = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"\nfilter(짝수): {evens}")  # → filter(짝수): [2, 4, 6, 8, 10]

    # None으로 Falsy 제거
    data: list[str | int | None] = ["hello", "", 0, "world", None, 42]
    truthy: list[str | int | None] = list(filter(None, data))
    print(f"filter(None): {truthy}")  # → filter(None): ['hello', 'world', 42]

    # reduce — 누적 연산
    total: int = functools.reduce(lambda acc, x: acc + x, numbers)
    print(f"\nreduce(합계): {total}")  # → reduce(합계): 55

    product: int = functools.reduce(lambda acc, x: acc * x, numbers)
    print(f"reduce(곱): {product}")  # → reduce(곱): 3628800

    # 초기값이 있는 reduce
    total_100: int = functools.reduce(lambda acc, x: acc + x, numbers, 100)
    print(f"reduce(합계, 초기=100): {total_100}")  # → reduce(합계, 초기=100): 155

    # 컴프리헨션 대안
    print(f"\n📌 map/filter vs 컴프리헨션:")
    print(f"  map:    list(map(func, items))")
    print(f"  comp:   [func(x) for x in items]     ← 더 Pythonic")
    print(f"  filter: list(filter(pred, items))")
    print(f"  comp:   [x for x in items if pred(x)] ← 더 Pythonic")


def demonstrate_functools() -> None:
    """functools 모듈을 보여준다."""
    print("\n" + "=" * 60)
    print("4. functools (partial, lru_cache, cache)")
    print("=" * 60)

    # partial — 인수 고정
    def power(base: int, exp: int) -> int:
        return base ** exp

    square_fn: functools.partial[int] = functools.partial(power, exp=2)
    cube_fn: functools.partial[int] = functools.partial(power, exp=3)

    print(f"partial:")
    print(f"  square(5) = {square_fn(5)}")  # →   square(5) = 25
    print(f"  cube(5) = {cube_fn(5)}")  # →   cube(5) = 125

    # lru_cache — 최근 사용 캐시
    @functools.lru_cache(maxsize=128)
    def expensive_calc(n: int) -> int:
        """비용이 높은 계산 (캐시됨)."""
        return sum(i**2 for i in range(n))

    print(f"\nlru_cache:")
    for n in [100, 200, 100, 200]:  # 100, 200은 캐시 히트
        result: int = expensive_calc(n)
        print(f"  expensive_calc({n}) = {result:,}")
    print(f"  cache_info: {expensive_calc.cache_info()}")

    # cache (Python 3.9+) — 무제한 캐시
    @functools.cache
    def fibonacci(n: int) -> int:
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    print(f"\ncache (fibonacci):")
    print(f"  fibonacci(30) = {fibonacci(30)}")  # →   fibonacci(30) = 832040

    # singledispatch — 타입별 함수 오버로딩
    @functools.singledispatch
    def process(data: object) -> str:
        return f"기본: {data}"

    @process.register(int)
    def _(data: int) -> str:
        return f"정수: {data * 2}"

    @process.register(str)
    def _(data: str) -> str:
        return f"문자열: {data.upper()}"

    @process.register(list)
    def _(data: list) -> str:
        return f"리스트: {len(data)}개"

    print(f"\nsingledispatch:")
    print(f"  process(42) = {process(42)}")  # →   process(42) = 정수: 84
    print(f"  process('hi') = {process('hi')}")  # →   process('hi') = 문자열: HI
    print(f"  process([1,2]) = {process([1, 2])}")  # →   process([1,2]) = 리스트: 2개
    print(f"  process(3.14) = {process(3.14)}")  # →   process(3.14) = 기본: 3.14


def demonstrate_operator_module() -> None:
    """operator 모듈을 보여준다."""
    print("\n" + "=" * 60)
    print("5. operator 모듈")
    print("=" * 60)

    # operator 함수 — lambda 대체
    print("operator 함수:")
    print(f"  operator.add(3, 5) = {operator.add(3, 5)}")  # →   operator.add(3, 5) = 8
    print(f"  operator.mul(4, 6) = {operator.mul(4, 6)}")  # →   operator.mul(4, 6) = 24
    print(f"  operator.neg(7) = {operator.neg(7)}")  # →   operator.neg(7) = -7

    # 정렬에 활용 (lambda 대체)
    students: list[tuple[str, int]] = [
        ("Charlie", 85), ("Alice", 92), ("Bob", 78)
    ]
    by_name: list[tuple[str, int]] = sorted(students, key=operator.itemgetter(0))
    by_grade: list[tuple[str, int]] = sorted(students, key=operator.itemgetter(1))
    print(f"\nitemgetter 정렬:")
    print(f"  이름순: {by_name}")
    print(f"  성적순: {by_grade}")

    # attrgetter — 속성 접근
    from dataclasses import dataclass

    @dataclass
    class Student:
        name: str
        grade: int

    students_obj: list[Student] = [
        Student("Charlie", 85), Student("Alice", 92), Student("Bob", 78)
    ]
    sorted_students: list[Student] = sorted(
        students_obj, key=operator.attrgetter("grade"), reverse=True
    )
    print(f"\nattrgetter 정렬:")
    for s in sorted_students:
        print(f"  {s}")

    # reduce + operator
    numbers: list[int] = [1, 2, 3, 4, 5]
    total: int = functools.reduce(operator.add, numbers)
    product: int = functools.reduce(operator.mul, numbers)
    print(f"\nreduce + operator:")
    print(f"  합: {total}, 곱: {product}")  # →   합: 15, 곱: 120


def demonstrate_functional_patterns() -> None:
    """함수형 프로그래밍 패턴 조합을 보여준다."""
    print("\n" + "=" * 60)
    print("6. 함수형 패턴 조합")
    print("=" * 60)

    # 함수 합성 (compose)
    def compose(*funcs: Callable) -> Callable:
        """여러 함수를 합성한다 (오른쪽에서 왼쪽)."""
        def composed(x: object) -> object:
            result: object = x
            for f in reversed(funcs):
                result = f(result)
            return result
        return composed

    double: Callable[[int], int] = lambda x: x * 2
    add_one: Callable[[int], int] = lambda x: x + 1
    square: Callable[[int], int] = lambda x: x ** 2

    transform = compose(square, add_one, double)
    print(f"compose(square, add_one, double)(3):")
    print(f"  3 → ×2 → +1 → ² = {transform(3)}")  # →   3 → ×2 → +1 → ² = 49

    # 파이프라인
    data: list[int] = list(range(1, 11))
    result: list[int] = list(
        map(lambda x: x ** 2,
            filter(lambda x: x % 2 == 0,
                   data))
    )
    print(f"\n파이프라인 (짝수의 제곱): {result}")  # → ... [4, 16, 36, 64, 100]

    # 같은 결과를 컴프리헨션으로 (더 Pythonic)
    result2: list[int] = [x ** 2 for x in data if x % 2 == 0]
    print(f"컴프리헨션 (동일): {result2}")  # → 컴프리헨션 (동일): [4, 16, 36, 64, 100]

    print(f"\n📌 함수형 프로그래밍 요약:")
    print(f"  ✅ 순수 함수: 부수 효과 없음, 같은 입력 → 같은 출력")
    print(f"  ✅ 불변 데이터: 원본 변경 대신 새 객체 생성")
    print(f"  ✅ 고차 함수: 함수를 인수/반환값으로 사용")
    print(f"  💡 Python은 멀티 패러다임 — 적절히 조합 사용")


if __name__ == "__main__":
    demonstrate_closures()
    demonstrate_lambda()
    demonstrate_map_filter_reduce()
    demonstrate_functools()
    demonstrate_operator_module()
    demonstrate_functional_patterns()

    print("\n" + "=" * 60)
    print("✅ _280_closures_and_functional.py 학습 완료!")
    print("=" * 60)
