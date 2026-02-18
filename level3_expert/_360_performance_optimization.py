"""
_360_performance_optimization.py — 성능 최적화 (Performance Optimization)

이 모듈에서 다루는 내용:
  1. timeit으로 벤치마킹
  2. cProfile 프로파일링
  3. 자료 구조 선택 (시간 복잡도)
  4. 문자열 최적화
  5. 캐싱 전략
  6. 최적화 체크리스트

실행 방법:
    poetry run python 3_expert/_360_performance_optimization.py
"""

import cProfile
import functools
import io
import pstats
import timeit
from collections import deque


def demonstrate_timeit() -> None:
    """timeit 벤치마킹을 보여준다."""
    print("=" * 60)
    print("1. timeit 벤치마킹")
    print("=" * 60)

    # 리스트 생성 방법 비교
    n: int = 10_000

    methods: list[tuple[str, str]] = [
        ("리스트 컴프리헨션", "[i**2 for i in range(n)]"),
        ("map + list", "list(map(lambda i: i**2, range(n)))"),
        ("for 루프", """
result = []
for i in range(n):
    result.append(i**2)
"""),
    ]

    print(f"리스트 생성 ({n:,}개):")
    for name, code in methods:
        t: float = timeit.timeit(code, globals={"n": n}, number=100)
        print(f"  {name:<20}: {t:.4f}초 (×100)")

    # 문자열 결합 비교
    strings: list[str] = [str(i) for i in range(1000)]

    str_methods: list[tuple[str, str]] = [
        ("join", "''.join(strings)"),
        ("+ 연결", """
result = ''
for s in strings:
    result += s
"""),
    ]

    print(f"\n문자열 결합 (1000개):")
    for name, code in str_methods:
        t = timeit.timeit(code, globals={"strings": strings}, number=1000)
        print(f"  {name:<15}: {t:.4f}초 (×1000)")

    # 딕셔너리 vs 리스트 탐색
    data_list: list[int] = list(range(10_000))
    data_set: set[int] = set(data_list)

    print(f"\n멤버십 확인 (10K 중 마지막):")
    t_list: float = timeit.timeit("9999 in data", globals={"data": data_list}, number=10000)
    t_set: float = timeit.timeit("9999 in data", globals={"data": data_set}, number=10000)
    print(f"  list 'in': {t_list:.4f}초")
    print(f"  set  'in': {t_set:.4f}초")
    print(f"  set은 {t_list/t_set:.0f}배 빠름!")


def demonstrate_cprofile() -> None:
    """cProfile 프로파일링을 보여준다."""
    print("\n" + "=" * 60)
    print("2. cProfile 프로파일링")
    print("=" * 60)

    def slow_function() -> int:
        """의도적으로 느린 함수."""
        total: int = 0
        for i in range(100):
            total += compute(i)
        return total

    def compute(n: int) -> int:
        return sum(i**2 for i in range(n))

    # 프로파일링
    profiler: cProfile.Profile = cProfile.Profile()
    profiler.enable()
    result: int = slow_function()
    profiler.disable()

    # 결과 분석
    stream: io.StringIO = io.StringIO()
    stats: pstats.Stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats("cumulative")
    stats.print_stats(5)  # 상위 5개

    print(f"결과: {result:,}")
    print(f"\ncProfile 출력 (상위 5):")
    for line in stream.getvalue().splitlines()[:10]:
        print(f"  {line}")

    print(f"\n📌 프로파일 지표:")
    print(f"  ncalls:    호출 횟수")
    print(f"  tottime:   함수 자체 실행 시간")
    print(f"  cumtime:   하위 함수 포함 누적 시간")
    print(f"  percall:   호출 당 시간")


def demonstrate_data_structure_choice() -> None:
    """자료 구조 선택을 보여준다."""
    print("\n" + "=" * 60)
    print("3. 자료 구조 시간 복잡도")
    print("=" * 60)

    print(f"{'연산':<25} {'list':>8} {'dict/set':>8} {'deque':>8}")
    print(f"{'-'*25} {'-'*8} {'-'*8} {'-'*8}")
    operations: list[tuple[str, str, str, str]] = [
        ("인덱스 접근 [i]", "O(1)", "O(1)", "O(n)"),
        ("앞에 추가", "O(n)", "—", "O(1)"),
        ("뒤에 추가", "O(1)*", "—", "O(1)"),
        ("탐색 (in)", "O(n)", "O(1)", "O(n)"),
        ("삽입 (중간)", "O(n)", "—", "O(n)"),
        ("삭제 (중간)", "O(n)", "O(1)", "O(n)"),
        ("정렬", "O(nlogn)", "—", "—"),
        ("길이", "O(1)", "O(1)", "O(1)"),
    ]
    for op, lst, dct, dq in operations:
        print(f"{op:<25} {lst:>8} {dct:>8} {dq:>8}")

    # 실측 비교: 앞에 삽입
    n: int = 50_000

    # list — O(n) per insert at 0
    lst: list[int] = []
    t_list: float = timeit.timeit(
        "lst.insert(0, 0)", globals={"lst": lst}, number=n
    )

    # deque — O(1) per appendleft
    dq: deque[int] = deque()
    t_deque: float = timeit.timeit(
        "dq.appendleft(0)", globals={"dq": dq}, number=n
    )

    print(f"\n앞에 삽입 {n:,}회:")
    print(f"  list.insert(0): {t_list:.4f}초")
    print(f"  deque.appendleft: {t_deque:.4f}초")
    print(f"  deque가 {t_list/t_deque:.0f}배 빠름!")


def demonstrate_string_optimization() -> None:
    """문자열 최적화를 보여준다."""
    print("\n" + "=" * 60)
    print("4. 문자열 최적화")
    print("=" * 60)

    n: int = 50_000

    # f-string vs format vs %
    name: str = "World"
    methods_str: list[tuple[str, str]] = [
        ("f-string", "f'Hello, {name}!'"),
        (".format()", "'Hello, {}!'.format(name)"),
        ("% 연산", "'Hello, %s!' % name"),
        ("+ 연결", "'Hello, ' + name + '!'"),
    ]

    print(f"문자열 포맷팅 ({n:,}회):")
    for label, code in methods_str:
        t: float = timeit.timeit(code, globals={"name": name}, number=n)
        print(f"  {label:<12}: {t:.4f}초")

    # 리스트 vs 제너레이터 (합계)
    print(f"\n합계 계산 (100K):")
    t_list: float = timeit.timeit(
        "sum([i for i in range(100_000)])", number=100
    )
    t_gen: float = timeit.timeit(
        "sum(i for i in range(100_000))", number=100
    )
    print(f"  리스트 컴프리헨션: {t_list:.4f}초")
    print(f"  제너레이터 표현식: {t_gen:.4f}초")

    # 딕셔너리 컴프리헨션 vs dict()
    print(f"\n딕셔너리 생성:")
    t1: float = timeit.timeit(
        "{i: i**2 for i in range(1000)}", number=1000
    )
    t2: float = timeit.timeit(
        "dict((i, i**2) for i in range(1000))", number=1000
    )
    print(f"  컴프리헨션: {t1:.4f}초")
    print(f"  dict():     {t2:.4f}초")


def demonstrate_caching() -> None:
    """캐싱 전략을 보여준다."""
    print("\n" + "=" * 60)
    print("5. 캐싱 전략")
    print("=" * 60)

    # lru_cache
    call_count: int = 0

    @functools.lru_cache(maxsize=128)
    def fibonacci(n: int) -> int:
        nonlocal call_count
        call_count += 1
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    result: int = fibonacci(30)
    print(f"fibonacci(30) = {result:,}")  # → fibonacci(30) = 832,040
    print(f"  실제 함수 호출: {call_count}회 (캐시 덕분)")  # →   실제 함수 호출: 31회 (캐시 덕분)
    print(f"  cache_info: {fibonacci.cache_info()}")

    # 수동 캐시 (dict)
    print(f"\n수동 캐시 (dict):")
    cache: dict[str, int] = {}
    miss_count: int = 0

    def cached_compute(key: str) -> int:
        nonlocal miss_count
        if key not in cache:
            miss_count += 1
            cache[key] = len(key) ** 3
        return cache[key]

    for word in "apple banana apple cherry banana apple".split():
        cached_compute(word)
    print(f"  캐시 크기: {len(cache)}, 미스: {miss_count}")

    # 캐시 전략
    print(f"\n📌 캐싱 전략:")
    print(f"  lru_cache:   최근 사용 기반, 자동 관리")
    print(f"  cache:       무제한 캐시 (메모리 주의)")
    print(f"  dict:        수동 관리, 유연함")
    print(f"  TTL 캐시:    시간 기반 만료 (직접 구현)")
    print(f"  💡 functools.lru_cache가 가장 간편!")


def demonstrate_optimization_checklist() -> None:
    """최적화 체크리스트를 보여준다."""
    print("\n" + "=" * 60)
    print("6. 최적화 체크리스트")
    print("=" * 60)

    print(f"📌 성능 최적화 원칙:")
    print(f"")
    print(f"  1️⃣  측정 먼저! (Premature optimization is the root of all evil)")
    print(f"     → timeit, cProfile, line_profiler, memory_profiler")
    print(f"")
    print(f"  2️⃣  알고리즘/자료구조 선택")
    print(f"     → O(n²) → O(n log n) 개선이 가장 효과적")
    print(f"     → set/dict 멤버십 O(1) vs list O(n)")
    print(f"")
    print(f"  3️⃣  Python 내장 함수 활용")
    print(f"     → sum(), min(), max(), sorted() (C 구현)")
    print(f"     → ''.join() vs += 문자열 결합")
    print(f"     → 컴프리헨션 > for 루프 > map/filter")
    print(f"")
    print(f"  4️⃣  캐싱")
    print(f"     → functools.lru_cache / functools.cache")
    print(f"     → 메모이제이션으로 중복 계산 제거")
    print(f"")
    print(f"  5️⃣  병렬화")
    print(f"     → I/O-bound: asyncio / ThreadPoolExecutor")
    print(f"     → CPU-bound: ProcessPoolExecutor / multiprocessing")
    print(f"")
    print(f"  6️⃣  외부 라이브러리")
    print(f"     → numpy (수치), pandas (데이터)")
    print(f"     → uvloop (asyncio), orjson (JSON)")
    print(f"     → Cython, PyO3 (C/Rust 확장)")


if __name__ == "__main__":
    demonstrate_timeit()
    demonstrate_cprofile()
    demonstrate_data_structure_choice()
    demonstrate_string_optimization()
    demonstrate_caching()
    demonstrate_optimization_checklist()

    print("\n" + "=" * 60)
    print("✅ _360_performance_optimization.py 학습 완료!")
    print("=" * 60)
