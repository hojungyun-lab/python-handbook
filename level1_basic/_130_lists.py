"""
040_lists.py — 리스트 (Lists)

이 모듈에서 다루는 내용:
  1. 리스트 생성과 기본 연산
  2. 인덱싱과 슬라이싱
  3. 리스트 수정 (추가, 삽입, 삭제)
  4. 정렬과 역순
  5. 리스트 복사 (shallow vs deep copy)
  6. 중첩 리스트 (2차원 배열)
  7. 리스트와 메모리
  8. 실용적인 리스트 패턴

실행 방법:
    poetry run python 1_basic/040_lists.py
"""

import copy


def demonstrate_list_creation() -> None:
    """리스트 생성 방법을 보여준다."""
    print("=" * 60)
    print("1. 리스트 생성")
    print("=" * 60)

    # 리터럴
    empty: list[int] = []
    numbers: list[int] = [1, 2, 3, 4, 5]
    mixed: list[int | str | bool] = [1, "hello", True, 3.14]

    print(f"empty = {empty}")  # → empty = []
    print(f"numbers = {numbers}")  # → numbers = [1, 2, 3, 4, 5]
    print(f"mixed = {mixed}")  # → mixed = [1, 'hello', True, 3.14]

    # list() 생성자
    from_range: list[int] = list(range(5))
    from_string: list[str] = list("Python")
    from_tuple: list[int] = list((10, 20, 30))

    print(f"\nlist(range(5)) = {from_range}")  # → list(range(5)) = [0, 1, 2, 3, 4]
    print(f"list('Python') = {from_string}")  # → list('Python') = ['P', 'y', 't', 'h', 'o', 'n']
    print(f"list((10,20,30)) = {from_tuple}")  # → list((10,20,30)) = [10, 20, 30]

    # 반복 생성
    zeros: list[int] = [0] * 5
    pattern: list[str] = ["a", "b"] * 3
    print(f"\n[0] * 5 = {zeros}")  # → [0] * 5 = [0, 0, 0, 0, 0]
    print(f"['a','b'] * 3 = {pattern}")  # → ['a','b'] * 3 = ['a', 'b', 'a', 'b', 'a', 'b']

    # 길이, 최소, 최대, 합계
    nums: list[int] = [4, 2, 8, 1, 5]
    print(f"\nnums = {nums}")
    print(f"  len={len(nums)}, min={min(nums)}, max={max(nums)}, sum={sum(nums)}")  # →   len=5, min=1, max=8, sum=20


def demonstrate_indexing_slicing() -> None:
    """리스트 인덱싱과 슬라이싱을 보여준다."""
    print("\n" + "=" * 60)
    print("2. 인덱싱과 슬라이싱")
    print("=" * 60)

    fruits: list[str] = ["apple", "banana", "cherry", "date", "elderberry"]
    print(f"fruits = {fruits}")

    # 인덱싱
    print(f"\n인덱싱:")
    print(f"  fruits[0]  = {fruits[0]!r}")  # →   fruits[0]  = 'apple'
    print(f"  fruits[-1] = {fruits[-1]!r}")  # →   fruits[-1] = 'elderberry'
    print(f"  fruits[2]  = {fruits[2]!r}")  # →   fruits[2]  = 'cherry'

    # 슬라이싱 [start:stop:step]
    print(f"\n슬라이싱:")
    print(f"  fruits[1:3]  = {fruits[1:3]}")  # →   fruits[1:3]  = ['banana', 'cherry']
    print(f"  fruits[:3]   = {fruits[:3]}")  # →   fruits[:3]   = ['apple', 'banana', 'cherry']
    print(f"  fruits[2:]   = {fruits[2:]}")  # →   fruits[2:]   = ['cherry', 'date', 'elderberry']
    print(f"  fruits[::2]  = {fruits[::2]}")  # →   fruits[::2]  = ['apple', 'cherry', 'elderberry']
    print(f"  fruits[::-1] = {fruits[::-1]}")  # →   fruits[::-1] = ['elderberry', 'date', 'cherry', 'banana', 'apple']

    # 슬라이싱으로 수정
    numbers: list[int] = [1, 2, 3, 4, 5]
    numbers[1:4] = [20, 30, 40]
    print(f"\n슬라이싱 수정: [1,2,3,4,5] → {numbers}")  # → 슬라이싱 수정: [1,2,3,4,5] → [1, 20, 30, 40, 5]

    numbers[1:3] = [200]  # 여러 개를 하나로 교체
    print(f"축소 교체: {numbers}")  # → 축소 교체: [1, 200, 40, 5]


def demonstrate_list_modification() -> None:
    """리스트 추가, 삽입, 삭제를 보여준다."""
    print("\n" + "=" * 60)
    print("3. 리스트 수정 (추가/삽입/삭제)")
    print("=" * 60)

    items: list[str] = ["a", "b", "c"]
    print(f"초기: {items}")

    # 추가
    items.append("d")
    print(f"append('d'):  {items}")  # → append('d'):  ['a', 'b', 'c', 'd']

    items.extend(["e", "f"])
    print(f"extend(['e','f']): {items}")  # → extend(['e','f']): ['a', 'b', 'c', 'd', 'e', 'f']

    items.insert(2, "X")
    print(f"insert(2, 'X'): {items}")  # → insert(2, 'X'): ['a', 'b', 'X', 'c', 'd', 'e', 'f']

    # 삭제
    items.remove("X")
    print(f"\nremove('X'):  {items}")  # → remove('X'):  ['a', 'b', 'c', 'd', 'e', 'f']

    popped: str = items.pop()
    print(f"pop():        {items}, 제거된 값: {popped!r}")  # → pop():        ['a', 'b', 'c', 'd', 'e'], 제거된 값: 'f'

    popped = items.pop(1)
    print(f"pop(1):       {items}, 제거된 값: {popped!r}")  # → pop(1):       ['a', 'c', 'd', 'e'], 제거된 값: 'b'

    del items[0]
    print(f"del items[0]: {items}")  # → del items[0]: ['c', 'd', 'e']

    items.clear()
    print(f"clear():      {items}")  # → clear():      []

    # in 연산자
    numbers: list[int] = [1, 2, 3, 4, 5]
    print(f"\n3 in {numbers} → {3 in numbers}")  # → 3 in [1, 2, 3, 4, 5] → True
    print(f"9 in {numbers} → {9 in numbers}")  # → 9 in [1, 2, 3, 4, 5] → False
    print(f"index(3) = {numbers.index(3)}")  # → index(3) = 2
    print(f"count(3) = {numbers.count(3)}")  # → count(3) = 1


def demonstrate_sorting() -> None:
    """리스트 정렬을 보여준다."""
    print("\n" + "=" * 60)
    print("4. 정렬과 역순")
    print("=" * 60)

    # sort() — 원본을 변경 (in-place)
    numbers: list[int] = [3, 1, 4, 1, 5, 9, 2, 6]
    print(f"원본: {numbers}")

    numbers.sort()
    print(f"sort():           {numbers}")  # → sort():           [1, 1, 2, 3, 4, 5, 6, 9]

    numbers.sort(reverse=True)
    print(f"sort(reverse):    {numbers}")  # → sort(reverse):    [9, 6, 5, 4, 3, 2, 1, 1]

    # sorted() — 새 리스트 반환 (원본 유지)
    original: list[int] = [3, 1, 4, 1, 5]
    sorted_list: list[int] = sorted(original)
    print(f"\noriginal: {original}")  # → original: [3, 1, 4, 1, 5]
    print(f"sorted():  {sorted_list}")  # → sorted():  [1, 1, 3, 4, 5]
    print(f"original 유지됨: {original}")  # → original 유지됨: [3, 1, 4, 1, 5]

    # key 매개변수
    words: list[str] = ["banana", "apple", "Cherry", "date"]
    print(f"\nwords: {words}")
    print(f"sorted(key=len): {sorted(words, key=len)}")  # → sorted(key=len): ['date', 'apple', 'banana', 'Cherry']
    print(f"sorted(key=str.lower): {sorted(words, key=str.lower)}")  # → sorted(key=str.lower): ['apple', 'banana', 'Cherry', 'date']

    # 복잡한 정렬
    students: list[tuple[str, int]] = [
        ("Alice", 85), ("Bob", 92), ("Charlie", 85), ("Diana", 90)
    ]
    # 점수 내림차순, 같으면 이름 오름차순
    sorted_students: list[tuple[str, int]] = sorted(
        students, key=lambda s: (-s[1], s[0])
    )
    print(f"\n학생 정렬 (점수↓, 이름↑):")
    for name, score in sorted_students:
        print(f"  {name}: {score}")
        # → Bob: 92
        # → Diana: 90
        # → Alice: 85
        # → Charlie: 85

    # reverse()
    nums: list[int] = [1, 2, 3, 4, 5]
    nums.reverse()
    print(f"\nreverse(): {nums}")  # → reverse(): [5, 4, 3, 2, 1]
    print(f"reversed() 이터레이터: {list(reversed(nums))}")  # → reversed() 이터레이터: [1, 2, 3, 4, 5]


def demonstrate_copying() -> None:
    """리스트 복사 (shallow vs deep copy)를 보여준다."""
    print("\n" + "=" * 60)
    print("5. 리스트 복사 (Shallow vs Deep)")
    print("=" * 60)

    # 할당은 복사가 아님 — 같은 객체를 참조
    original: list[int] = [1, 2, 3]
    alias: list[int] = original
    alias.append(4)
    print(f"할당 (같은 객체):")
    print(f"  original: {original}")  # →   original: [1, 2, 3, 4]
    print(f"  alias:    {alias}")  # →   alias:    [1, 2, 3, 4]
    print(f"  original is alias: {original is alias}")  # →   original is alias: True

    # Shallow Copy — 1차원까지만 독립
    original2: list[int] = [1, 2, 3]
    shallow1: list[int] = original2.copy()    # 방법 1
    shallow2: list[int] = original2[:]        # 방법 2
    shallow3: list[int] = list(original2)     # 방법 3

    shallow1.append(4)
    print(f"\nShallow Copy:")
    print(f"  original: {original2}")  # →   original: [1, 2, 3]
    print(f"  shallow:  {shallow1}")  # →   shallow:  [1, 2, 3, 4]
    print(f"  original is shallow: {original2 is shallow1}")  # →   original is shallow: False

    # Shallow Copy의 한계 — 중첩 객체는 공유
    nested: list[list[int]] = [[1, 2], [3, 4]]
    shallow_nested: list[list[int]] = nested.copy()
    shallow_nested[0].append(99)  # 내부 리스트는 공유됨!
    print(f"\nShallow Copy 한계 (중첩):")
    print(f"  nested: {nested}")  # →   nested: [[1, 2, 99], [3, 4]]
    print(f"  shallow: {shallow_nested}")  # →   shallow: [[1, 2, 99], [3, 4]]
    print(f"  ⚠️ 내부 리스트가 공유됨!")

    # Deep Copy — 완전히 독립된 복사
    nested2: list[list[int]] = [[1, 2], [3, 4]]
    deep: list[list[int]] = copy.deepcopy(nested2)
    deep[0].append(99)
    print(f"\nDeep Copy:")
    print(f"  nested: {nested2}")  # →   nested: [[1, 2], [3, 4]]
    print(f"  deep:   {deep}")  # →   deep:   [[1, 2, 99], [3, 4]]
    print(f"  ✅ 내부 리스트도 독립!")


def demonstrate_nested_lists() -> None:
    """중첩 리스트 (2차원 배열)를 보여준다."""
    print("\n" + "=" * 60)
    print("6. 중첩 리스트 (2차원 배열)")
    print("=" * 60)

    # 2차원 리스트 (행렬)
    matrix: list[list[int]] = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
    ]

    print("행렬:")
    for row in matrix:
        print(f"  {row}")

    print(f"\nmatrix[0][1] = {matrix[0][1]}")  # → matrix[0][1] = 2
    print(f"matrix[2][2] = {matrix[2][2]}")  # → matrix[2][2] = 9

    # 행렬 전치
    transposed: list[list[int]] = [
        [row[i] for row in matrix]
        for i in range(len(matrix[0]))
    ]
    print(f"\n전치 행렬:")
    for row in transposed:
        print(f"  {row}")

    # ⚠️ 2차원 리스트 생성 주의
    print(f"\n⚠️ 2차원 리스트 생성 주의:")
    wrong: list[list[int]] = [[0] * 3] * 3  # 같은 행을 참조!
    wrong[0][0] = 99
    print(f"  [[0]*3]*3 → 수정 후: {wrong}")  # →   [[0]*3]*3 → 수정 후: [[99, 0, 0], [99, 0, 0], [99, 0, 0]]
    print(f"  ⚠️ 모든 행이 같은 객체!")

    correct: list[list[int]] = [[0] * 3 for _ in range(3)]
    correct[0][0] = 99
    print(f"\n  [[0]*3 for _ in range(3)] → 수정 후: {correct}")  # →   [[0]*3 for _ in range(3)] → 수정 후: [[99, 0, 0], [0, 0, 0], [0, 0, 0]]
    print(f"  ✅ 각 행이 독립 객체!")


def demonstrate_list_patterns() -> None:
    """실용적인 리스트 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("7. 실용적인 리스트 패턴")
    print("=" * 60)

    # 리스트 평탄화 (flatten)
    nested: list[list[int]] = [[1, 2], [3, 4], [5, 6]]
    flat: list[int] = [x for sublist in nested for x in sublist]
    print(f"평탄화: {nested} → {flat}")  # → 평탄화: [[1, 2], [3, 4], [5, 6]] → [1, 2, 3, 4, 5, 6]

    # 중복 제거 (순서 유지)
    duplicated: list[int] = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    unique: list[int] = list(dict.fromkeys(duplicated))
    print(f"중복 제거: {duplicated} → {unique}")  # → 중복 제거: [3, 1, 4, 1, 5, 9, 2, 6, 5, 3] → [3, 1, 4, 5, 9, 2, 6]

    # 리스트를 청크로 나누기
    data: list[int] = list(range(10))
    chunk_size: int = 3
    chunks: list[list[int]] = [
        data[i:i + chunk_size] for i in range(0, len(data), chunk_size)
    ]
    print(f"청크 분할: {data} → {chunks}")  # → 청크 분할: [0, 1, 2, ..., 9] → [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

    # zip으로 병합
    names: list[str] = ["Alice", "Bob", "Charlie"]
    scores: list[int] = [85, 92, 78]
    combined: list[tuple[str, int]] = list(zip(names, scores))
    print(f"\nzip 병합: {combined}")  # → zip 병합: [('Alice', 85), ('Bob', 92), ('Charlie', 78)]

    # enumerate
    fruits: list[str] = ["apple", "banana", "cherry"]
    print(f"\nenumerate:")
    for i, fruit in enumerate(fruits, start=1):
        print(f"  {i}. {fruit}")
        # → 1. apple
        # → 2. banana
        # → 3. cherry

    # 리스트 언패킹 (*)
    first: int
    rest: list[int]
    first, *rest = [1, 2, 3, 4, 5]
    print(f"\n언패킹: first={first}, rest={rest}")  # → 언패킹: first=1, rest=[2, 3, 4, 5]

    # 필터링
    numbers: list[int] = list(range(-5, 6))
    positives: list[int] = [x for x in numbers if x > 0]
    print(f"\n양수 필터: {numbers} → {positives}")  # → 양수 필터: [-5, -4, ..., 5] → [1, 2, 3, 4, 5]


if __name__ == "__main__":
    demonstrate_list_creation()
    demonstrate_indexing_slicing()
    demonstrate_list_modification()
    demonstrate_sorting()
    demonstrate_copying()
    demonstrate_nested_lists()
    demonstrate_list_patterns()

    print("\n" + "=" * 60)
    print("✅ 040_lists.py 학습 완료!")
    print("=" * 60)
