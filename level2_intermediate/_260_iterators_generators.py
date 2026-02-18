"""
_260_iterators_generators.py — 이터레이터와 제너레이터

이 모듈에서 다루는 내용:
  1. 이터레이터 프로토콜 (__iter__, __next__)
  2. 커스텀 이터레이터
  3. 제너레이터 함수 (yield)
  4. yield from
  5. 제너레이터 send()와 양방향 통신
  6. itertools 활용

실행 방법:
    poetry run python 2_intermediate/_260_iterators_generators.py
"""

import itertools
from collections.abc import Iterator, Generator


def demonstrate_iterator_protocol() -> None:
    """이터레이터 프로토콜을 보여준다."""
    print("=" * 60)
    print("1. 이터레이터 프로토콜")
    print("=" * 60)

    # 이터러블 → __iter__() → 이터레이터 → __next__()
    numbers: list[int] = [10, 20, 30]
    it: Iterator[int] = iter(numbers)  # __iter__() 호출

    print(f"iter([10, 20, 30])")
    print(f"  next(it) = {next(it)}")  # →   next(it) = 10
    print(f"  next(it) = {next(it)}")  # →   next(it) = 20
    print(f"  next(it) = {next(it)}")  # →   next(it) = 30
    try:
        next(it)
    except StopIteration:
        print(f"  next(it) → StopIteration (소진됨)")

    # for 루프의 내부 동작
    print(f"\nfor 루프 내부:")
    print(f"  1. iter(iterable) 호출 → 이터레이터 생성")
    print(f"  2. next(iterator) 반복 호출")
    print(f"  3. StopIteration → 루프 종료")

    # 모든 이터러블
    print(f"\n이터러블 타입들:")
    iterables: list[tuple[str, object]] = [
        ("list", [1, 2, 3]),
        ("str", "abc"),
        ("dict", {"a": 1}),
        ("range", range(3)),
        ("set", {1, 2, 3}),
    ]
    for name, obj in iterables:
        it = iter(obj)
        print(f"  {name:<6} → {list(it)}")


def demonstrate_custom_iterator() -> None:
    """커스텀 이터레이터를 보여준다."""
    print("\n" + "=" * 60)
    print("2. 커스텀 이터레이터")
    print("=" * 60)

    class CountDown:
        """카운트다운 이터레이터."""

        def __init__(self, start: int) -> None:
            self.current: int = start

        def __iter__(self) -> "CountDown":
            return self

        def __next__(self) -> int:
            if self.current <= 0:
                raise StopIteration
            value: int = self.current
            self.current -= 1
            return value

    print("CountDown(5):")
    for n in CountDown(5):
        print(f"  {n}", end=" ")
    print()

    # 이터러블 vs 이터레이터 분리
    class FibonacciSequence:
        """피보나치 이터러블 (재사용 가능)."""

        def __init__(self, max_count: int) -> None:
            self.max_count: int = max_count

        def __iter__(self) -> Iterator[int]:
            """새 이터레이터를 생성한다."""
            a: int = 0
            b: int = 1
            count: int = 0
            while count < self.max_count:
                yield a  # 제너레이터로 이터레이터 생성
                a, b = b, a + b
                count += 1

    fib: FibonacciSequence = FibonacciSequence(10)
    print(f"\nFibonacci(10): {list(fib)}")  # → Fibonacci(10): [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    print(f"재사용:        {list(fib)}")  # → 재사용:        [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


def demonstrate_generator_function() -> None:
    """제너레이터 함수를 보여준다."""
    print("\n" + "=" * 60)
    print("3. 제너레이터 함수 (yield)")
    print("=" * 60)

    # 기본 제너레이터
    def count_up_to(n: int) -> Generator[int, None, None]:
        """n까지 카운트하는 제너레이터."""
        i: int = 1
        while i <= n:
            yield i  # 값을 생성하고 일시 중지
            i += 1

    gen = count_up_to(5)
    print(f"type: {type(gen)}")
    print(f"count_up_to(5): {list(count_up_to(5))}")  # → count_up_to(5): [1, 2, 3, 4, 5]

    # yield의 동작 원리
    def demo_yield() -> Generator[str, None, None]:
        """yield 동작을 보여준다."""
        print("  [시작]")
        yield "첫 번째"
        print("  [첫 yield 후]")
        yield "두 번째"
        print("  [두 번째 yield 후]")
        yield "세 번째"
        print("  [종료]")

    print(f"\nyield 동작:")
    g = demo_yield()
    print(f"  next → {next(g)!r}")
    print(f"  next → {next(g)!r}")
    print(f"  next → {next(g)!r}")

    # 무한 제너레이터
    def infinite_counter(start: int = 0) -> Generator[int, None, None]:
        """무한 카운터."""
        n: int = start
        while True:
            yield n
            n += 1

    print(f"\n무한 제너레이터 (처음 5개):")
    for i, n in zip(range(5), infinite_counter(100)):
        print(f"  {n}", end=" ")
    print()

    # 파이프라인 패턴
    def read_data() -> Generator[int, None, None]:
        """데이터를 읽는다."""
        yield from range(1, 11)

    def filter_even(data: Generator[int, None, None]) -> Generator[int, None, None]:
        """짝수만 필터한다."""
        for x in data:
            if x % 2 == 0:
                yield x

    def square(data: Generator[int, None, None]) -> Generator[int, None, None]:
        """제곱한다."""
        for x in data:
            yield x ** 2

    pipeline = square(filter_even(read_data()))
    print(f"\n파이프라인: {list(pipeline)}")  # → 파이프라인: [4, 16, 36, 64, 100]


def demonstrate_yield_from() -> None:
    """yield from을 보여준다."""
    print("\n" + "=" * 60)
    print("4. yield from")
    print("=" * 60)

    # yield from — 하위 이터러블을 위임
    def flatten(nested: list[list[int]]) -> Generator[int, None, None]:
        """중첩 리스트를 평탄화한다."""
        for sublist in nested:
            yield from sublist  # for item in sublist: yield item 와 동일

    data: list[list[int]] = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
    print(f"flatten: {list(flatten(data))}")  # → flatten: [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # 재귀 + yield from
    def deep_flatten(lst: list) -> Generator:
        """깊은 중첩을 평탄화한다."""
        for item in lst:
            if isinstance(item, list):
                yield from deep_flatten(item)
            else:
                yield item

    deep: list = [1, [2, [3, 4]], [5, [6, [7]]]]
    print(f"deep_flatten: {list(deep_flatten(deep))}")  # → deep_flatten: [1, 2, 3, 4, 5, 6, 7]

    # 여러 제너레이터 연결
    def chain_generators() -> Generator[str, None, None]:
        """여러 소스를 연결한다."""
        yield from ["a", "b", "c"]
        yield from ("x", "y", "z")
        yield from "123"

    print(f"chain: {list(chain_generators())}")  # → chain: ['a', 'b', 'c', 'x', 'y', 'z', '1', '2', '3']


def demonstrate_send() -> None:
    """제너레이터 send()를 보여준다."""
    print("\n" + "=" * 60)
    print("5. send()와 양방향 통신")
    print("=" * 60)

    def accumulator() -> Generator[float, float, None]:
        """누산기 — send()로 값을 받아 합산."""
        total: float = 0
        while True:
            value: float = yield total
            total += value

    acc = accumulator()
    next(acc)  # 제너레이터 시작 (첫 yield까지)

    print("누산기:")
    for v in [10, 20, 30, 40]:
        result: float = acc.send(v)
        print(f"  send({v}) → total = {result}")

    # close() — 제너레이터 종료
    acc.close()
    print(f"\nclose() 후 제너레이터 종료")

    # throw() — 제너레이터에 예외 전달
    def careful_gen() -> Generator[int, None, None]:
        """예외를 처리하는 제너레이터."""
        try:
            yield 1
            yield 2
            yield 3
        except ValueError:
            print("  ValueError 처리됨!")
            yield -1

    g = careful_gen()
    print(f"\nthrow() 데모:")
    print(f"  next → {next(g)}")
    print(f"  throw → {g.throw(ValueError)}")


def demonstrate_itertools() -> None:
    """itertools 활용을 보여준다."""
    print("\n" + "=" * 60)
    print("6. itertools 활용")
    print("=" * 60)

    # 무한 이터레이터
    print("무한 이터레이터:")
    print(f"  count(10, 2):   {list(itertools.islice(itertools.count(10, 2), 5))}")  # →   count(10, 2):   [10, 12, 14, 16, 18]
    print(f"  cycle('AB'):    {list(itertools.islice(itertools.cycle('AB'), 6))}")  # →   cycle('AB'):    ['A', 'B', 'A', 'B', 'A', 'B']
    print(f"  repeat(7, 3):   {list(itertools.repeat(7, 3))}")  # →   repeat(7, 3):   [7, 7, 7]

    # 조합/순열
    print(f"\n조합/순열:")
    print(f"  permutations('AB', 2):  {list(itertools.permutations('AB', 2))}")  # →   ... [('A', 'B'), ('B', 'A')]
    print(f"  combinations('ABC', 2): {list(itertools.combinations('ABC', 2))}")  # →   ... [('A', 'B'), ('A', 'C'), ('B', 'C')]
    print(f"  product('AB', '12'):    {list(itertools.product('AB', '12'))}")  # →   ... [('A', '1'), ('A', '2'), ('B', '1'), ('B', '2')]

    # 유틸리티
    print(f"\n유틸리티:")
    data: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    # chain — 여러 이터러블 연결
    chained: list[int] = list(itertools.chain([1, 2], [3, 4], [5]))
    print(f"  chain: {chained}")  # →   chain: [1, 2, 3, 4, 5]

    # groupby — 연속 같은 값 그룹화
    sorted_data: list[tuple[str, int]] = [
        ("A", 1), ("A", 2), ("B", 3), ("B", 4), ("A", 5)
    ]
    print(f"  groupby:")
    for key, group in itertools.groupby(sorted_data, key=lambda x: x[0]):
        print(f"    {key}: {list(group)}")

    # accumulate — 누적 계산
    acc: list[int] = list(itertools.accumulate([1, 2, 3, 4, 5]))
    print(f"  accumulate: {acc}")  # →   accumulate: [1, 3, 6, 10, 15]

    # takewhile / dropwhile
    tw: list[int] = list(itertools.takewhile(lambda x: x < 5, data))
    dw: list[int] = list(itertools.dropwhile(lambda x: x < 5, data))
    print(f"  takewhile(<5): {tw}")  # →   takewhile(<5): [1, 2, 3, 4]
    print(f"  dropwhile(<5): {dw}")  # →   dropwhile(<5): [5, 6, 7, 8, 9]

    # batched (Python 3.12+)
    try:
        batched: list[tuple[int, ...]] = list(itertools.batched(data, 3))
        print(f"  batched(3): {batched}")
    except AttributeError:
        print(f"  batched: Python 3.12+ 필요")


if __name__ == "__main__":
    demonstrate_iterator_protocol()
    demonstrate_custom_iterator()
    demonstrate_generator_function()
    demonstrate_yield_from()
    demonstrate_send()
    demonstrate_itertools()

    print("\n" + "=" * 60)
    print("✅ _260_iterators_generators.py 학습 완료!")
    print("=" * 60)
