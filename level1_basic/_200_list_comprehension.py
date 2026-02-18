"""
_200_list_comprehension.py — 컴프리헨션 (Comprehensions)

이 모듈에서 다루는 내용:
  1. 리스트 컴프리헨션 기본
  2. 조건부 필터링
  3. 중첩 컴프리헨션
  4. 딕셔너리 컴프리헨션
  5. 셋 컴프리헨션
  6. 제너레이터 표현식과 비교
  7. 실용적인 패턴과 주의사항

실행 방법:
    poetry run python 1_basic/_200_list_comprehension.py
"""

import sys


def demonstrate_basic_comprehension() -> None:
    """리스트 컴프리헨션 기본을 보여준다."""
    print("=" * 60)
    print("1. 리스트 컴프리헨션 기본")
    print("=" * 60)

    # 전통적 방법 vs 컴프리헨션
    # 전통적
    squares_loop: list[int] = []
    for x in range(1, 6):
        squares_loop.append(x ** 2)

    # 컴프리헨션
    squares_comp: list[int] = [x ** 2 for x in range(1, 6)]

    print(f"전통적 방법: {squares_loop}")  # → 전통적 방법: [1, 4, 9, 16, 25]
    print(f"컴프리헨션:  {squares_comp}")  # → 컴프리헨션:  [1, 4, 9, 16, 25]

    # 문법: [expression for variable in iterable]
    names: list[str] = ["alice", "bob", "charlie"]
    upper_names: list[str] = [name.upper() for name in names]
    lengths: list[int] = [len(name) for name in names]

    print(f"\n대문자: {upper_names}")  # → 대문자: ['ALICE', 'BOB', 'CHARLIE']
    print(f"길이:   {lengths}")  # → 길이:   [5, 3, 7]

    # 함수 호출과 조합
    numbers: list[int] = [-3, -1, 0, 2, 5]
    absolutes: list[int] = [abs(n) for n in numbers]
    print(f"절대값: {numbers} → {absolutes}")  # → 절대값: [-3, -1, 0, 2, 5] → [3, 1, 0, 2, 5]


def demonstrate_conditional() -> None:
    """조건부 필터링을 보여준다."""
    print("\n" + "=" * 60)
    print("2. 조건부 필터링")
    print("=" * 60)

    # if 필터 (후위)
    numbers: list[int] = list(range(1, 21))
    evens: list[int] = [x for x in numbers if x % 2 == 0]
    print(f"짝수: {evens}")  # → 짝수: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

    # 다중 조건
    fizzbuzz_free: list[int] = [
        x for x in range(1, 31)
        if x % 3 != 0 and x % 5 != 0
    ]
    print(f"3,5의 배수 아닌 수: {fizzbuzz_free}")  # → 3,5의 배수 아닌 수: [1, 2, 4, 7, 8, 11, 13, 14, 16, 17, 19, 22, 23, 26, 28, 29]

    # if-else (삼항, expression 위치)
    labels: list[str] = [
        "짝수" if x % 2 == 0 else "홀수"
        for x in range(1, 6)
    ]
    print(f"\n짝홀 라벨: {labels}")  # → 짝홀 라벨: ['홀수', '짝수', '홀수', '짝수', '홀수']

    # FizzBuzz
    fizzbuzz: list[str] = [
        "FizzBuzz" if x % 15 == 0
        else "Fizz" if x % 3 == 0
        else "Buzz" if x % 5 == 0
        else str(x)
        for x in range(1, 16)
    ]
    print(f"FizzBuzz: {fizzbuzz}")

    # None 필터링
    data: list[int | None] = [1, None, 3, None, 5, 6, None]
    filtered: list[int] = [x for x in data if x is not None]
    print(f"\nNone 제거: {data} → {filtered}")  # → None 제거: [1, None, 3, None, 5, 6, None] → [1, 3, 5, 6]


def demonstrate_nested() -> None:
    """중첩 컴프리헨션을 보여준다."""
    print("\n" + "=" * 60)
    print("3. 중첩 컴프리헨션")
    print("=" * 60)

    # 2중 루프 — 평탄화
    matrix: list[list[int]] = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flat: list[int] = [x for row in matrix for x in row]
    print(f"평탄화: {flat}")  # → 평탄화: [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(f"💡 읽는 순서: for row ... → for x ...")

    # 순서쌍
    pairs: list[tuple[int, int]] = [
        (x, y) for x in range(3) for y in range(3) if x != y
    ]
    print(f"순서쌍 (x≠y): {pairs}")  # → 순서쌍 (x≠y): [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]

    # 행렬 전치
    transposed: list[list[int]] = [
        [row[i] for row in matrix] for i in range(3)
    ]
    print(f"\n전치 행렬:")
    for row in transposed:
        print(f"  {row}")

    # 문자열 처리
    sentences: list[str] = ["hello world", "python is great"]
    words: list[str] = [
        word for sentence in sentences for word in sentence.split()
    ]
    print(f"\n단어 추출: {words}")  # → 단어 추출: ['hello', 'world', 'python', 'is', 'great']


def demonstrate_dict_comprehension() -> None:
    """딕셔너리 컴프리헨션을 보여준다."""
    print("\n" + "=" * 60)
    print("4. 딕셔너리 컴프리헨션")
    print("=" * 60)

    # 기본
    squares: dict[int, int] = {x: x**2 for x in range(1, 6)}
    print(f"제곱 dict: {squares}")  # → 제곱 dict: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

    # 키-값 뒤집기
    original: dict[str, int] = {"a": 1, "b": 2, "c": 3}
    inverted: dict[int, str] = {v: k for k, v in original.items()}
    print(f"뒤집기: {original} → {inverted}")  # → 뒤집기: {'a': 1, 'b': 2, 'c': 3} → {1: 'a', 2: 'b', 3: 'c'}

    # 조건부 필터
    scores: dict[str, int] = {
        "Alice": 85, "Bob": 62, "Charlie": 91, "Diana": 55
    }
    passed: dict[str, int] = {k: v for k, v in scores.items() if v >= 70}
    print(f"\n합격: {passed}")  # → 합격: {'Alice': 85, 'Charlie': 91}

    # 두 리스트에서 dict 생성
    keys: list[str] = ["name", "age", "city"]
    values: list[str | int] = ["Alice", 30, "Seoul"]
    combined: dict[str, str | int] = {k: v for k, v in zip(keys, values)}
    print(f"zip → dict: {combined}")  # → zip → dict: {'name': 'Alice', 'age': 30, 'city': 'Seoul'}

    # 값 변환
    prices_usd: dict[str, float] = {"apple": 1.5, "banana": 0.8, "cherry": 3.0}
    rate: float = 1300.0
    prices_krw: dict[str, float] = {
        item: round(price * rate) for item, price in prices_usd.items()
    }
    print(f"\nUSD→KRW: {prices_krw}")


def demonstrate_set_comprehension() -> None:
    """셋 컴프리헨션을 보여준다."""
    print("\n" + "=" * 60)
    print("5. 셋 컴프리헨션")
    print("=" * 60)

    # 기본
    squares: set[int] = {x**2 for x in range(-5, 6)}
    print(f"제곱 set: {sorted(squares)}")  # → 제곱 set: [0, 1, 4, 9, 16, 25]

    # 문자열에서 고유 문자
    text: str = "hello world python"
    vowels: set[str] = {ch for ch in text if ch in "aeiou"}
    print(f"모음: {sorted(vowels)}")  # → 모음: ['e', 'o']

    # 중복 제거 + 변환
    words: list[str] = ["Hello", "WORLD", "hello", "World"]
    unique_lower: set[str] = {w.lower() for w in words}
    print(f"고유 단어: {sorted(unique_lower)}")  # → 고유 단어: ['hello', 'world']


def demonstrate_generator_expression() -> None:
    """제너레이터 표현식과 컴프리헨션을 비교한다."""
    print("\n" + "=" * 60)
    print("6. 제너레이터 표현식 vs 컴프리헨션")
    print("=" * 60)

    # 리스트 컴프리헨션 — 전체 결과를 메모리에 저장
    list_comp: list[int] = [x**2 for x in range(10)]

    # 제너레이터 표현식 — 필요할 때 하나씩 생성 (lazy)
    gen_expr = (x**2 for x in range(10))

    print(f"리스트 컴프리헨션: {list_comp}")  # → 리스트 컴프리헨션: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
    print(f"제너레이터 표현식: {gen_expr}")
    print(f"제너레이터 → list: {list(gen_expr)}")

    # 메모리 비교
    list_size: int = sys.getsizeof([x for x in range(10000)])
    gen_size: int = sys.getsizeof(x for x in range(10000))
    print(f"\n메모리 비교 (10,000개):")
    print(f"  list comp: {list_size:,} bytes")
    print(f"  generator: {gen_size:,} bytes")
    print(f"  💡 제너레이터는 크기에 무관하게 일정한 메모리!")

    # sum, max, min 등에서 직접 사용 (괄호 생략 가능)
    total: int = sum(x**2 for x in range(1, 11))
    maximum: int = max(x**2 for x in range(1, 11))
    print(f"\nsum(x² for x in 1~10) = {total}")  # → sum(x² for x in 1~10) = 385
    print(f"max(x² for x in 1~10) = {maximum}")  # → max(x² for x in 1~10) = 100

    # any, all과 조합
    numbers: list[int] = [2, 4, 6, 8, 10]
    all_even: bool = all(x % 2 == 0 for x in numbers)
    any_gt_5: bool = any(x > 5 for x in numbers)
    print(f"\nall(짝수): {all_even}")  # → all(짝수): True
    print(f"any(>5): {any_gt_5}")  # → any(>5): True


def demonstrate_practical_patterns() -> None:
    """실용적인 컴프리헨션 패턴과 주의사항을 보여준다."""
    print("\n" + "=" * 60)
    print("7. 실용 패턴과 주의사항")
    print("=" * 60)

    # 왈러스 연산자 활용 (Python 3.8+)
    data: list[str] = ["hello", "hi", "hey", "howdy", "hola"]
    results: list[tuple[str, int]] = [
        (word, length) for word in data
        if (length := len(word)) > 3
    ]
    print(f"왈러스 + 컴프리헨션: {results}")  # → 왈러스 + 컴프리헨션: [('hello', 5), ('howdy', 5)]

    # 중첩 함수 호출 최적화
    import math
    values: list[float] = [1.5, 2.7, 3.14, 4.0, 5.9]
    processed: list[tuple[float, float]] = [
        (v, rounded)
        for v in values
        if (rounded := math.floor(v)) > 2
    ]
    print(f"floor > 2: {processed}")  # → floor > 2: [(3.14, 3), (4.0, 4), (5.9, 5)]

    # ⚠️ 가독성 주의
    print(f"\n📌 컴프리헨션 가독성 가이드:")
    print(f"  ✅ 간단한 변환/필터에 사용")
    print(f"  ✅ 한 줄에 들어가는 간단한 표현식")
    print(f"  ❌ 3중 이상 중첩 → 일반 루프 사용")
    print(f"  ❌ 부수 효과(side effect) 포함 금지")
    print(f"  ❌ 너무 복잡한 조건 → 함수 분리")

    # ❌ 안티패턴: 부수 효과
    # [print(x) for x in range(5)]  ← 결과 리스트를 버리는 낭비

    # ✅ 대안: 일반 for 루프
    print(f"\n✅ 부수 효과는 for 루프:")
    for x in range(3):
        print(f"  처리: {x}")

    # 성능: 컴프리헨션 vs 루프 vs map
    import timeit

    n: int = 100_000
    loop_time: float = timeit.timeit(
        "result = []\nfor x in range(1000):\n result.append(x**2)",
        number=1000,
    )
    comp_time: float = timeit.timeit(
        "[x**2 for x in range(1000)]",
        number=1000,
    )
    map_time: float = timeit.timeit(
        "list(map(lambda x: x**2, range(1000)))",
        number=1000,
    )

    print(f"\n성능 비교 (1000개 × 1000회):")
    print(f"  루프:         {loop_time:.4f}초")
    print(f"  컴프리헨션:   {comp_time:.4f}초")
    print(f"  map+lambda:   {map_time:.4f}초")
    print(f"  💡 컴프리헨션이 보통 가장 빠름!")


if __name__ == "__main__":
    demonstrate_basic_comprehension()
    demonstrate_conditional()
    demonstrate_nested()
    demonstrate_dict_comprehension()
    demonstrate_set_comprehension()
    demonstrate_generator_expression()
    demonstrate_practical_patterns()

    print("\n" + "=" * 60)
    print("✅ _200_list_comprehension.py 학습 완료!")
    print("=" * 60)
