"""
180_loops.py — 반복문 (Loops)

이 모듈에서 다루는 내용:
  1. for 반복문과 이터러블
  2. while 반복문
  3. range() 함수
  4. enumerate()와 zip()
  5. break, continue, else
  6. 중첩 루프
  7. 실용적인 반복 패턴

실행 방법:
    poetry run python 1_basic/180_loops.py
"""

from itertools import product


def demonstrate_for_loop() -> None:
    """for 반복문을 보여준다."""
    print("=" * 60)
    print("1. for 반복문")
    print("=" * 60)

    # 리스트 순회
    fruits: list[str] = ["apple", "banana", "cherry"]
    print("리스트 순회:")
    for fruit in fruits:
        print(f"  {fruit}")
        # → apple
        # → banana
        # → cherry

    # 문자열 순회
    print(f"\n문자열 순회 ('Py'):")
    for ch in "Py":
        print(f"  {ch!r}")
        # → 'P'
        # → 'y'

    # 딕셔너리 순회
    scores: dict[str, int] = {"Alice": 85, "Bob": 92}
    print(f"\n딕셔너리 순회:")
    for name, score in scores.items():
        print(f"  {name}: {score}")
        # → Alice: 85
        # → Bob: 92

    # 집합 순회 (순서 보장 안 됨)
    colors: set[str] = {"red", "green", "blue"}
    print(f"\n집합 순회: {sorted(colors)}")


def demonstrate_while_loop() -> None:
    """while 반복문을 보여준다."""
    print("\n" + "=" * 60)
    print("2. while 반복문")
    print("=" * 60)

    # 기본 while
    count: int = 0
    print("기본 while:")
    while count < 5:
        print(f"  count = {count}")
        count += 1
    # → count = 0 ~ count = 4

    # 조건부 종료
    total: int = 0
    n: int = 1
    while total < 20:
        total += n
        n += 1
    print(f"\n1부터 합산하여 20 이상: total={total}, n={n - 1}까지")  # → 1부터 합산하여 20 이상: total=21, n=6까지

    # 왈러스 연산자와 while (Python 3.8+)
    data: list[int] = [3, 7, 2, 8, 1, 5]
    idx: int = 0
    print(f"\n왈러스 + while (5 초과 값 찾기):")
    while idx < len(data) and (val := data[idx]) <= 5:
        idx += 1
    if idx < len(data):
        print(f"  인덱스 {idx}에서 {val} 발견")  # →   인덱스 1에서 7 발견


def demonstrate_range() -> None:
    """range() 함수를 보여준다."""
    print("\n" + "=" * 60)
    print("3. range() 함수")
    print("=" * 60)

    # range(stop)
    print(f"range(5) = {list(range(5))}")  # → range(5) = [0, 1, 2, 3, 4]

    # range(start, stop)
    print(f"range(2, 8) = {list(range(2, 8))}")  # → range(2, 8) = [2, 3, 4, 5, 6, 7]

    # range(start, stop, step)
    print(f"range(0, 20, 3) = {list(range(0, 20, 3))}")  # → range(0, 20, 3) = [0, 3, 6, 9, 12, 15, 18]

    # 역순
    print(f"range(10, 0, -1) = {list(range(10, 0, -1))}")  # → range(10, 0, -1) = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

    # range는 시퀀스 프로토콜 지원
    r: range = range(100)
    print(f"\nrange(100):")
    print(f"  50 in r = {50 in r}")  # →   50 in r = True
    print(f"  r[99] = {r[99]}")  # →   r[99] = 99
    print(f"  len(r) = {len(r)}")  # →   len(r) = 100
    print(f"  💡 range는 메모리를 거의 사용하지 않음 (lazy)")


def demonstrate_enumerate_zip() -> None:
    """enumerate()와 zip()을 보여준다."""
    print("\n" + "=" * 60)
    print("4. enumerate()와 zip()")
    print("=" * 60)

    # enumerate — 인덱스와 값을 동시에
    languages: list[str] = ["Python", "Rust", "Go"]
    print("enumerate (start=1):")
    for i, lang in enumerate(languages, start=1):
        print(f"  {i}. {lang}")
        # → 1. Python
        # → 2. Rust
        # → 3. Go

    # zip — 여러 이터러블을 병렬 순회
    names: list[str] = ["Alice", "Bob", "Charlie"]
    scores: list[int] = [85, 92, 78]
    grades: list[str] = ["B", "A", "C"]

    print(f"\nzip (병렬 순회):")
    for name, score, grade in zip(names, scores, grades):
        print(f"  {name}: {score}점 ({grade})")
        # → Alice: 85점 (B)
        # → Bob: 92점 (A)
        # → Charlie: 78점 (C)

    # zip의 길이가 다른 경우
    short: list[int] = [1, 2]
    long: list[int] = [10, 20, 30, 40]
    print(f"\nzip (길이 다름): {list(zip(short, long))}")  # → zip (길이 다름): [(1, 10), (2, 20)]
    print(f"💡 짧은 쪽에 맞춰 잘림")

    # zip strict (Python 3.10+) — 길이가 다르면 ValueError
    try:
        list(zip(short, long, strict=True))
    except ValueError as e:
        print(f"zip(strict=True) → ValueError: {e}")

    # zip으로 dict 만들기
    keys: list[str] = ["name", "age", "city"]
    values: list[str | int] = ["Alice", 30, "Seoul"]
    d: dict[str, str | int] = dict(zip(keys, values))
    print(f"\ndict(zip(keys, values)) = {d}")  # → dict(zip(keys, values)) = {'name': 'Alice', 'age': 30, 'city': 'Seoul'}

    # unzip
    pairs: list[tuple[str, int]] = [("a", 1), ("b", 2), ("c", 3)]
    letters: tuple[str, ...]
    nums: tuple[int, ...]
    letters, nums = zip(*pairs)  # type: ignore[assignment]
    print(f"unzip: {list(letters)}, {list(nums)}")  # → unzip: ['a', 'b', 'c'], [1, 2, 3]


def demonstrate_break_continue_else() -> None:
    """break, continue, else를 보여준다."""
    print("\n" + "=" * 60)
    print("5. break, continue, else")
    print("=" * 60)

    # break — 루프 즉시 종료
    print("break (첫 음수 찾기):")
    numbers: list[int] = [3, 7, -2, 8, -5]
    for n in numbers:
        if n < 0:
            print(f"  첫 음수 발견: {n}")
            break
        print(f"  확인: {n}")

    # continue — 현재 반복 건너뛰기
    print(f"\ncontinue (양수만 출력):")
    for n in numbers:
        if n < 0:
            continue
        print(f"  {n}")

    # for-else — break 없이 완료되면 else 실행
    print(f"\nfor-else (소수 판별):")

    def is_prime(n: int) -> bool:
        """n이 소수인지 판별한다."""
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % 2 == 0:
                return False
        else:
            # break 없이 루프 완료 → 소수
            return True
        return False  # break로 빠져나온 경우

    for num in [2, 7, 10, 13, 15, 23]:
        result: str = "소수" if is_prime(num) else "합성수"
        print(f"  {num}: {result}")

    # while-else
    print(f"\nwhile-else:")
    count: int = 0
    while count < 3:
        print(f"  count = {count}")
        count += 1
    else:
        print(f"  루프 정상 완료! (count = {count})")


def demonstrate_nested_loops() -> None:
    """중첩 루프를 보여준다."""
    print("\n" + "=" * 60)
    print("6. 중첩 루프")
    print("=" * 60)

    # 구구단 (일부)
    print("구구단 (2~4단):")
    for i in range(2, 5):
        line: str = ""
        for j in range(1, 10):
            line += f"{i}×{j}={i*j:<4}"
        print(f"  {line}")

    # itertools.product — 중첩 루프 대체
    print(f"\nitertools.product:")
    colors: list[str] = ["red", "blue"]
    sizes: list[str] = ["S", "M", "L"]
    for color, size in product(colors, sizes):
        print(f"  {color}-{size}", end="  ")
    print()

    # 중첩 break (플래그 사용)
    print(f"\n중첩 루프 탈출 (플래그):")
    found: bool = False
    matrix: list[list[int]] = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    target: int = 5
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            if val == target:
                print(f"  {target} 발견: [{i}][{j}]")
                found = True
                break
        if found:
            break


def demonstrate_loop_patterns() -> None:
    """실용적인 반복 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("7. 실용적인 반복 패턴")
    print("=" * 60)

    # 누적 합계 (running total)
    values: list[int] = [10, 20, 30, 40, 50]
    running: list[int] = []
    total: int = 0
    for v in values:
        total += v
        running.append(total)
    print(f"누적 합계: {values} → {running}")  # → 누적 합계: [10, 20, 30, 40, 50] → [10, 30, 60, 100, 150]

    # 슬라이딩 윈도우
    data: list[int] = [1, 3, 5, 7, 9, 11]
    window_size: int = 3
    averages: list[float] = [
        sum(data[i:i + window_size]) / window_size
        for i in range(len(data) - window_size + 1)
    ]
    print(f"이동평균 (윈도우={window_size}): {averages}")  # → 이동평균 (윈도우=3): [3.0, 5.0, 7.0, 9.0]

    # 인접 쌍
    items: list[str] = ["a", "b", "c", "d"]
    pairs: list[tuple[str, str]] = list(zip(items, items[1:]))
    print(f"\n인접 쌍: {items} → {pairs}")  # → 인접 쌍: ['a', 'b', 'c', 'd'] → [('a', 'b'), ('b', 'c'), ('c', 'd')]

    # 인덱스 없는 반복 vs 인덱스 필요 반복
    colors: list[str] = ["red", "green", "blue"]
    print(f"\n❌ 비Pythonic (C 스타일):")
    for i in range(len(colors)):
        print(f"  colors[{i}] = {colors[i]}")

    print(f"\n✅ Pythonic:")
    for i, color in enumerate(colors):
        print(f"  {i}: {color}")

    # reversed() — 역순 순회 (원본 유지)
    nums: list[int] = [1, 2, 3, 4, 5]
    print(f"\nreversed({nums}): {list(reversed(nums))}")  # → reversed([1, 2, 3, 4, 5]): [5, 4, 3, 2, 1]

    # 무한 루프 패턴
    import itertools
    print(f"\nitertools.count (제한 순회):")
    for i in itertools.islice(itertools.count(10, 5), 5):
        print(f"  {i}", end=" ")
    print()


if __name__ == "__main__":
    demonstrate_for_loop()
    demonstrate_while_loop()
    demonstrate_range()
    demonstrate_enumerate_zip()
    demonstrate_break_continue_else()
    demonstrate_nested_loops()
    demonstrate_loop_patterns()

    print("\n" + "=" * 60)
    print("✅ 180_loops.py 학습 완료!")
    print("=" * 60)
