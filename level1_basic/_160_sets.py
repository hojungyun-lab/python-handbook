"""
160_sets.py — 집합 (Sets)

이 모듈에서 다루는 내용:
  1. 집합 생성
  2. 집합 연산 (합집합, 교집합, 차집합, 대칭차)
  3. 집합 수정 (추가, 삭제)
  4. frozenset (불변 집합)
  5. Set Comprehension
  6. 실용적인 패턴

실행 방법:
    poetry run python 1_basic/160_sets.py
"""


def demonstrate_set_creation() -> None:
    """집합 생성 방법을 보여준다."""
    print("=" * 60)
    print("1. 집합 생성")
    print("=" * 60)

    # 리터럴 — 중복 자동 제거, 순서 없음
    fruits: set[str] = {"apple", "banana", "cherry", "apple"}
    print(f"fruits = {fruits}")
    print(f"'apple' 중복 → 자동 제거됨!")

    # ⚠️ 빈 집합은 set()으로 생성 ({}는 빈 dict)
    empty_set: set[int] = set()
    empty_dict: dict = {}  # type: ignore[type-arg]
    print(f"\nset() type  = {type(empty_set).__name__}")  # → set() type  = set
    print(f"{{}} type    = {type(empty_dict).__name__}")  # → {} type    = dict

    # set() 생성자
    from_list: set[int] = set([1, 2, 3, 2, 1])
    from_str: set[str] = set("abracadabra")
    from_range: set[int] = set(range(5))

    print(f"\nset([1,2,3,2,1]) = {from_list}")
    print(f"set('abracadabra') = {from_str}")
    print(f"set(range(5)) = {from_range}")

    # 기본 연산
    numbers: set[int] = {3, 1, 4, 1, 5, 9}
    print(f"\nnumbers = {numbers}")
    print(f"  len = {len(numbers)}")  # →   len = 5
    print(f"  3 in numbers = {3 in numbers}")  # →   3 in numbers = True
    print(f"  7 in numbers = {7 in numbers}")  # →   7 in numbers = False


def demonstrate_set_operations() -> None:
    """집합 연산을 보여준다."""
    print("\n" + "=" * 60)
    print("2. 집합 연산")
    print("=" * 60)

    a: set[int] = {1, 2, 3, 4, 5}
    b: set[int] = {4, 5, 6, 7, 8}

    print(f"A = {a}")
    print(f"B = {b}")

    # 합집합 (Union)
    print(f"\n합집합 (A ∪ B):")
    print(f"  a | b        = {a | b}")  # →   a | b        = {1, 2, 3, 4, 5, 6, 7, 8}
    print(f"  a.union(b)   = {a.union(b)}")  # →   a.union(b)   = {1, 2, 3, 4, 5, 6, 7, 8}

    # 교집합 (Intersection)
    print(f"\n교집합 (A ∩ B):")
    print(f"  a & b              = {a & b}")  # →   a & b              = {4, 5}
    print(f"  a.intersection(b)  = {a.intersection(b)}")  # →   a.intersection(b)  = {4, 5}

    # 차집합 (Difference)
    print(f"\n차집합 (A - B):")
    print(f"  a - b            = {a - b}")  # →   a - b            = {1, 2, 3}
    print(f"  a.difference(b)  = {a.difference(b)}")  # →   a.difference(b)  = {1, 2, 3}

    # 대칭차 (Symmetric Difference)
    print(f"\n대칭차 (A △ B):")
    print(f"  a ^ b                      = {a ^ b}")  # →   a ^ b                      = {1, 2, 3, 6, 7, 8}
    print(f"  a.symmetric_difference(b)  = {a.symmetric_difference(b)}")  # →   a.symmetric_difference(b)  = {1, 2, 3, 6, 7, 8}

    # 부분집합, 상위집합
    c: set[int] = {1, 2, 3}
    print(f"\nc = {c}")
    print(f"  c <= a (부분집합) = {c <= a}")  # →   c <= a (부분집합) = True
    print(f"  c.issubset(a)    = {c.issubset(a)}")  # →   c.issubset(a)    = True
    print(f"  a >= c (상위집합) = {a >= c}")  # →   a >= c (상위집합) = True
    print(f"  a.issuperset(c)  = {a.issuperset(c)}")  # →   a.issuperset(c)  = True

    # 서로소
    d: set[int] = {10, 20}
    print(f"\nd = {d}")
    print(f"  a.isdisjoint(d) = {a.isdisjoint(d)}")  # →   a.isdisjoint(d) = True

    # 여러 집합 동시 연산
    x: set[int] = {1, 2, 3}
    y: set[int] = {2, 3, 4}
    z: set[int] = {3, 4, 5}
    print(f"\nx, y, z = {x}, {y}, {z}")
    print(f"  x & y & z = {x & y & z}")  # →   x & y & z = {3}
    print(f"  x | y | z = {x | y | z}")  # →   x | y | z = {1, 2, 3, 4, 5}


def demonstrate_set_modification() -> None:
    """집합 수정 메서드를 보여준다."""
    print("\n" + "=" * 60)
    print("3. 집합 수정 (추가/삭제)")
    print("=" * 60)

    s: set[str] = {"a", "b", "c"}
    print(f"초기: {s}")

    # 추가
    s.add("d")
    print(f"add('d'):    {s}")

    s.update(["e", "f"])
    print(f"update(['e','f']): {s}")

    # 삭제
    s.remove("f")  # 없으면 KeyError
    print(f"remove('f'): {s}")

    s.discard("z")  # 없어도 에러 안 남
    print(f"discard('z'): {s} (에러 없음)")

    popped: str = s.pop()  # 임의의 요소 제거
    print(f"pop(): 제거된={popped!r}, 남은={s}")

    # remove vs discard
    print(f"\n📌 remove vs discard:")
    print(f"  remove('없는키') → KeyError 발생")
    print(f"  discard('없는키') → 에러 없이 무시")

    try:
        s.remove("없는키")
    except KeyError as e:
        print(f"  실제 에러: KeyError({e})")

    # in-place 집합 연산
    a: set[int] = {1, 2, 3, 4}
    b: set[int] = {3, 4, 5, 6}
    print(f"\nin-place 연산:")
    a_copy: set[int] = a.copy()

    a_copy |= b  # union update
    print(f"  a |= b → {a_copy}")  # →   a |= b → {1, 2, 3, 4, 5, 6}

    a_copy = a.copy()
    a_copy &= b  # intersection update
    print(f"  a &= b → {a_copy}")  # →   a &= b → {3, 4}

    a_copy = a.copy()
    a_copy -= b  # difference update
    print(f"  a -= b → {a_copy}")  # →   a -= b → {1, 2}


def demonstrate_frozenset() -> None:
    """frozenset (불변 집합)을 보여준다."""
    print("\n" + "=" * 60)
    print("4. frozenset (불변 집합)")
    print("=" * 60)

    # frozenset — 변경 불가능한 집합
    fs: frozenset[int] = frozenset([1, 2, 3, 4, 5])
    print(f"frozenset = {fs}")

    # 수정 불가
    try:
        fs.add(6)  # type: ignore[attr-defined]
    except AttributeError as e:
        print(f"add() 시도 → AttributeError: {e}")  # → add() 시도 → AttributeError: 'frozenset' object has no attribute 'add'

    # 집합 연산은 가능 (새 frozenset 반환)
    fs2: frozenset[int] = frozenset([4, 5, 6, 7])
    print(f"\n연산 결과:")
    print(f"  fs & fs2 = {fs & fs2}")
    print(f"  fs | fs2 = {fs | fs2}")

    # dict 키나 다른 set의 원소로 사용 가능 (해시 가능)
    print(f"\nhash(frozenset) = {hash(fs)}")  # → hash(frozenset) = <해시값>
    set_of_sets: set[frozenset[int]] = {
        frozenset([1, 2]),
        frozenset([3, 4]),
    }
    print(f"set of frozensets = {set_of_sets}")


def demonstrate_set_comprehension() -> None:
    """Set Comprehension을 보여준다."""
    print("\n" + "=" * 60)
    print("5. Set Comprehension")
    print("=" * 60)

    # 기본
    squares: set[int] = {x**2 for x in range(-5, 6)}
    print(f"제곱 집합: {sorted(squares)}")  # → 제곱 집합: [0, 1, 4, 9, 16, 25]

    # 조건 필터
    evens: set[int] = {x for x in range(20) if x % 2 == 0}
    print(f"짝수 집합: {sorted(evens)}")  # → 짝수 집합: [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

    # 문자열 처리
    sentence: str = "hello world python programming"
    vowels: set[str] = {ch for ch in sentence if ch in "aeiou"}
    print(f"모음 집합: {sorted(vowels)}")  # → 모음 집합: ['a', 'e', 'i', 'o']

    # 중첩
    pairs: set[tuple[int, int]] = {
        (x, y) for x in range(3) for y in range(3) if x != y
    }
    print(f"순서쌍 (x≠y): {sorted(pairs)}")


def demonstrate_practical_patterns() -> None:
    """집합의 실용적 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("6. 실용적인 패턴")
    print("=" * 60)

    # 중복 제거 (순서 무관)
    data: list[int] = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    unique: list[int] = sorted(set(data))
    print(f"중복 제거: {data} → {unique}")

    # 두 리스트의 공통/고유 요소
    list_a: list[str] = ["python", "java", "go", "rust"]
    list_b: list[str] = ["java", "rust", "swift", "kotlin"]
    common: set[str] = set(list_a) & set(list_b)
    only_a: set[str] = set(list_a) - set(list_b)
    only_b: set[str] = set(list_b) - set(list_a)

    print(f"\n공통: {common}")
    print(f"A에만: {only_a}")
    print(f"B에만: {only_b}")

    # 멤버십 테스트 최적화 (O(1) vs O(n))
    # list 검색: O(n), set 검색: O(1)
    allowed_users: set[str] = {"admin", "editor", "viewer"}
    user: str = "editor"
    if user in allowed_users:
        print(f"\n'{user}' 접근 허용 (O(1) 검색)")  # → 'editor' 접근 허용 (O(1) 검색)

    # 고유 단어 수 세기
    text: str = "the quick brown fox jumps over the lazy dog the fox"
    words: list[str] = text.split()
    unique_words: set[str] = set(words)
    print(f"\n전체 단어: {len(words)}개")  # → 전체 단어: 11개
    print(f"고유 단어: {len(unique_words)}개 → {sorted(unique_words)}")

    # 집합으로 데이터 검증
    required: set[str] = {"name", "email", "age"}
    provided: set[str] = {"name", "email", "phone"}
    missing: set[str] = required - provided
    extra: set[str] = provided - required

    print(f"\n데이터 검증:")
    print(f"  필수 필드: {required}")
    print(f"  제공 필드: {provided}")
    print(f"  누락 필드: {missing}")
    print(f"  추가 필드: {extra}")


if __name__ == "__main__":
    demonstrate_set_creation()
    demonstrate_set_operations()
    demonstrate_set_modification()
    demonstrate_frozenset()
    demonstrate_set_comprehension()
    demonstrate_practical_patterns()

    print("\n" + "=" * 60)
    print("✅ 160_sets.py 학습 완료!")
    print("=" * 60)
