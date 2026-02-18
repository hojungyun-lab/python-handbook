"""
060_dictionaries.py — 딕셔너리 (Dictionaries)

이 모듈에서 다루는 내용:
  1. 딕셔너리 생성
  2. CRUD 연산 (추가/읽기/수정/삭제)
  3. 딕셔너리 순회
  4. 주요 메서드 (get, setdefault, update, pop)
  5. 딕셔너리 합치기 (| 연산자, Python 3.9+)
  6. Dictionary Comprehension
  7. 중첩 딕셔너리
  8. 실용적인 패턴

실행 방법:
    poetry run python 1_basic/060_dictionaries.py
"""


def demonstrate_dict_creation() -> None:
    """딕셔너리 생성 방법을 보여준다."""
    print("=" * 60)
    print("1. 딕셔너리 생성")
    print("=" * 60)

    # 리터럴
    empty: dict[str, int] = {}
    person: dict[str, str | int] = {"name": "Alice", "age": 30, "city": "Seoul"}
    print(f"empty = {empty}")  # → empty = {}
    print(f"person = {person}")  # → person = {'name': 'Alice', 'age': 30, 'city': 'Seoul'}

    # dict() 생성자
    from_kwargs: dict[str, int] = dict(x=1, y=2, z=3)
    from_pairs: dict[str, int] = dict([("a", 1), ("b", 2)])
    from_zip: dict[str, int] = dict(zip(["x", "y"], [10, 20]))

    print(f"\ndict(x=1, y=2) = {from_kwargs}")  # → dict(x=1, y=2) = {'x': 1, 'y': 2, 'z': 3}
    print(f"dict([('a',1),('b',2)]) = {from_pairs}")  # → dict([('a',1),('b',2)]) = {'a': 1, 'b': 2}
    print(f"dict(zip(...)) = {from_zip}")  # → dict(zip(...)) = {'x': 10, 'y': 20}

    # dict.fromkeys()
    keys: list[str] = ["a", "b", "c"]
    defaults: dict[str, int] = dict.fromkeys(keys, 0)
    print(f"dict.fromkeys(['a','b','c'], 0) = {defaults}")  # → dict.fromkeys(['a','b','c'], 0) = {'a': 0, 'b': 0, 'c': 0}


def demonstrate_crud() -> None:
    """딕셔너리 CRUD 연산을 보여준다."""
    print("\n" + "=" * 60)
    print("2. CRUD 연산")
    print("=" * 60)

    data: dict[str, int] = {"a": 1, "b": 2, "c": 3}
    print(f"초기: {data}")

    # Read
    print(f"\n읽기:")
    print(f"  data['a'] = {data['a']}")  # →   data['a'] = 1
    print(f"  data.get('z', -1) = {data.get('z', -1)}")  # →   data.get('z', -1) = -1

    # Create / Update
    data["d"] = 4             # 새 키 추가
    data["a"] = 10            # 기존 값 수정
    print(f"\n추가/수정 후: {data}")  # → 추가/수정 후: {'a': 10, 'b': 2, 'c': 3, 'd': 4}

    # Delete
    del data["d"]
    print(f"del data['d']: {data}")  # → del data['d']: {'a': 10, 'b': 2, 'c': 3}

    popped: int = data.pop("b")
    print(f"pop('b'): {data}, 제거된 값: {popped}")  # → pop('b'): {'a': 10, 'c': 3}, 제거된 값: 2

    last: tuple[str, int] = data.popitem()  # 마지막 항목 제거
    print(f"popitem(): {data}, 제거된 항목: {last}")  # → popitem(): {'a': 10}, 제거된 항목: ('c', 3)

    # 키 존재 확인
    print(f"\n'a' in data = {'a' in data}")  # → 'a' in data = True

    # 안전한 접근
    try:
        _ = data["nonexistent"]
    except KeyError as e:
        print(f"data['nonexistent'] → KeyError: {e}")  # → data['nonexistent'] → KeyError: 'nonexistent'


def demonstrate_iteration() -> None:
    """딕셔너리 순회를 보여준다."""
    print("\n" + "=" * 60)
    print("3. 딕셔너리 순회")
    print("=" * 60)

    scores: dict[str, int] = {"Alice": 85, "Bob": 92, "Charlie": 78}

    # 키 순회 (기본)
    print("키 순회:")
    for key in scores:
        print(f"  {key}: {scores[key]}")

    # .items() — 키-값 쌍
    print(f"\n.items() 순회:")
    for name, score in scores.items():
        print(f"  {name} = {score}")

    # .keys(), .values()
    print(f"\n.keys()   = {list(scores.keys())}")  # → .keys()   = ['Alice', 'Bob', 'Charlie']
    print(f".values() = {list(scores.values())}")  # → .values() = [85, 92, 78]

    # 뷰 객체의 동적 특성
    keys_view = scores.keys()
    print(f"\n뷰 객체 (동적):")
    print(f"  수정 전: {list(keys_view)}")  # →   수정 전: ['Alice', 'Bob', 'Charlie']
    scores["Diana"] = 90
    print(f"  수정 후: {list(keys_view)}")  # →   수정 후: ['Alice', 'Bob', 'Charlie', 'Diana']


def demonstrate_methods() -> None:
    """주요 딕셔너리 메서드를 보여준다."""
    print("\n" + "=" * 60)
    print("4. 주요 메서드")
    print("=" * 60)

    # get() — 안전한 값 접근
    config: dict[str, str] = {"host": "localhost", "port": "8080"}
    print("get():")
    print(f"  config.get('host') = {config.get('host')!r}")  # →   config.get('host') = 'localhost'
    print(f"  config.get('timeout', '30') = {config.get('timeout', '30')!r}")  # →   config.get('timeout', '30') = '30'

    # setdefault() — 키가 없을 때만 설정
    print(f"\nsetdefault():")
    config.setdefault("timeout", "30")
    config.setdefault("host", "0.0.0.0")  # 이미 있으면 변경 안 함
    print(f"  timeout 추가 후: {config}")

    # update() — 다른 dict으로 업데이트
    extra: dict[str, str] = {"debug": "true", "port": "9090"}
    config.update(extra)
    print(f"\nupdate({extra}):")
    print(f"  결과: {config}")

    # 카운팅 패턴 - setdefault 활용
    text: str = "hello world"
    char_count: dict[str, int] = {}
    for char in text:
        char_count[char] = char_count.get(char, 0) + 1
    print(f"\n문자 카운팅 ({text!r}):")
    print(f"  {char_count}")  # →   {'h': 1, 'e': 1, 'l': 3, 'o': 2, ' ': 1, 'w': 1, 'r': 1, 'd': 1}


def demonstrate_merge() -> None:
    """딕셔너리 합치기를 보여준다 (Python 3.9+)."""
    print("\n" + "=" * 60)
    print("5. 딕셔너리 합치기 (Python 3.9+)")
    print("=" * 60)

    defaults: dict[str, str] = {"color": "red", "size": "M", "style": "plain"}
    custom: dict[str, str] = {"color": "blue", "weight": "bold"}

    # | 연산자 — 새 딕셔너리 생성 (오른쪽이 우선)
    merged: dict[str, str] = defaults | custom
    print(f"defaults | custom = {merged}")  # → defaults | custom = {'color': 'blue', 'size': 'M', 'style': 'plain', 'weight': 'bold'}

    # |= 연산자 — in-place 업데이트
    base: dict[str, int] = {"a": 1, "b": 2}
    base |= {"b": 20, "c": 3}
    print(f"\nbase |= {{'b': 20, 'c': 3}} = {base}")  # → base |= {'b': 20, 'c': 3} = {'a': 1, 'b': 20, 'c': 3}

    # 이전 방식과 비교
    old_way: dict[str, str] = {**defaults, **custom}
    print(f"\n구식: {{**defaults, **custom}} = {old_way}")
    print(f"💡 | 연산자가 더 읽기 쉽고 권장됨")


def demonstrate_comprehension() -> None:
    """Dictionary Comprehension을 보여준다."""
    print("\n" + "=" * 60)
    print("6. Dictionary Comprehension")
    print("=" * 60)

    # 기본
    squares: dict[int, int] = {x: x**2 for x in range(1, 6)}
    print(f"제곱: {squares}")  # → 제곱: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

    # 조건 필터
    even_squares: dict[int, int] = {x: x**2 for x in range(1, 11) if x % 2 == 0}
    print(f"짝수 제곱: {even_squares}")  # → 짝수 제곱: {2: 4, 4: 16, 6: 36, 8: 64, 10: 100}

    # 키-값 뒤집기
    original: dict[str, int] = {"a": 1, "b": 2, "c": 3}
    inverted: dict[int, str] = {v: k for k, v in original.items()}
    print(f"\n키-값 뒤집기: {original} → {inverted}")  # → 키-값 뒤집기: {'a': 1, 'b': 2, 'c': 3} → {1: 'a', 2: 'b', 3: 'c'}

    # 문자열 처리
    words: list[str] = ["hello", "world", "python", "code"]
    lengths: dict[str, int] = {w: len(w) for w in words}
    print(f"단어 길이: {lengths}")  # → 단어 길이: {'hello': 5, 'world': 5, 'python': 6, 'code': 4}

    # 기존 dict 필터링
    scores: dict[str, int] = {"Alice": 85, "Bob": 62, "Charlie": 91, "Diana": 55}
    passed: dict[str, int] = {k: v for k, v in scores.items() if v >= 70}
    print(f"\n합격자: {passed}")  # → 합격자: {'Alice': 85, 'Charlie': 91}

    # 대소문자 변환
    headers: dict[str, str] = {"Content-Type": "json", "Accept": "html"}
    lower_headers: dict[str, str] = {k.lower(): v for k, v in headers.items()}
    print(f"소문자 키: {lower_headers}")  # → 소문자 키: {'content-type': 'json', 'accept': 'html'}


def demonstrate_nested_dict() -> None:
    """중첩 딕셔너리를 보여준다."""
    print("\n" + "=" * 60)
    print("7. 중첩 딕셔너리")
    print("=" * 60)

    users: dict[str, dict[str, str | int]] = {
        "user1": {"name": "Alice", "age": 30, "role": "admin"},
        "user2": {"name": "Bob", "age": 25, "role": "user"},
    }

    print("중첩 딕셔너리:")
    for uid, info in users.items():
        print(f"  {uid}: {info}")

    # 접근
    print(f"\nusers['user1']['name'] = {users['user1']['name']}")  # → users['user1']['name'] = Alice

    # 안전한 중첩 접근
    def safe_get(d: dict, *keys: str, default: object = None) -> object:
        """중첩 딕셔너리에서 안전하게 값을 가져온다."""
        for key in keys:
            if isinstance(d, dict):
                d = d.get(key, default)  # type: ignore[assignment]
            else:
                return default
        return d

    result: object = safe_get(users, "user1", "name")
    missing: object = safe_get(users, "user9", "name", default="Unknown")
    print(f"safe_get('user1', 'name') = {result}")  # → safe_get('user1', 'name') = Alice
    print(f"safe_get('user9', 'name') = {missing}")  # → safe_get('user9', 'name') = Unknown


def demonstrate_practical_patterns() -> None:
    """실용적인 딕셔너리 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("8. 실용적인 패턴")
    print("=" * 60)

    # 그룹핑
    students: list[tuple[str, str]] = [
        ("Alice", "Math"), ("Bob", "Science"),
        ("Charlie", "Math"), ("Diana", "Science"),
        ("Eve", "Math"),
    ]
    groups: dict[str, list[str]] = {}
    for name, dept in students:
        groups.setdefault(dept, []).append(name)
    print(f"그룹핑:")
    for dept, names in groups.items():
        print(f"  {dept}: {names}")

    # 빈도수 계산 (Counter 미사용)
    text: str = "abracadabra"
    freq: dict[str, int] = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    sorted_freq: list[tuple[str, int]] = sorted(
        freq.items(), key=lambda x: x[1], reverse=True
    )
    print(f"\n빈도수 ({text!r}):")
    for ch, count in sorted_freq:
        print(f"  '{ch}': {'█' * count} ({count})")

    # switch/case 대체
    def get_day_type(day: str) -> str:
        """요일 타입을 반환한다."""
        day_map: dict[str, str] = {
            "Monday": "weekday", "Tuesday": "weekday",
            "Wednesday": "weekday", "Thursday": "weekday",
            "Friday": "weekday", "Saturday": "weekend",
            "Sunday": "weekend",
        }
        return day_map.get(day, "unknown")

    print(f"\nswitch 패턴: Friday → {get_day_type('Friday')}")  # → switch 패턴: Friday → weekday
    print(f"switch 패턴: Sunday → {get_day_type('Sunday')}")  # → switch 패턴: Sunday → weekend

    # 캐시/메모이제이션 패턴
    cache: dict[int, int] = {}

    def fibonacci(n: int) -> int:
        """피보나치 수를 캐시를 이용하여 계산한다."""
        if n in cache:
            return cache[n]
        if n <= 1:
            result: int = n
        else:
            result = fibonacci(n - 1) + fibonacci(n - 2)
        cache[n] = result
        return result

    fib_10: int = fibonacci(10)
    print(f"\nfibonacci(10) = {fib_10}")  # → fibonacci(10) = 55
    print(f"캐시: {cache}")


if __name__ == "__main__":
    demonstrate_dict_creation()
    demonstrate_crud()
    demonstrate_iteration()
    demonstrate_methods()
    demonstrate_merge()
    demonstrate_comprehension()
    demonstrate_nested_dict()
    demonstrate_practical_patterns()

    print("\n" + "=" * 60)
    print("✅ 060_dictionaries.py 학습 완료!")
    print("=" * 60)
