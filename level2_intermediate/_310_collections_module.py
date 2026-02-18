"""
_310_collections_module.py — collections 모듈

이 모듈에서 다루는 내용:
  1. defaultdict
  2. Counter
  3. deque (양방향 큐)
  4. OrderedDict
  5. ChainMap
  6. namedtuple 복습 + 실용 패턴

실행 방법:
    poetry run python 2_intermediate/_310_collections_module.py
"""

from collections import (
    ChainMap,
    Counter,
    OrderedDict,
    defaultdict,
    deque,
    namedtuple,
)


def demonstrate_defaultdict() -> None:
    """defaultdict를 보여준다."""
    print("=" * 60)
    print("1. defaultdict")
    print("=" * 60)

    # 기본 사용 — 누락 키에 기본값 자동 생성
    word_count: defaultdict[str, int] = defaultdict(int)
    text: str = "apple banana apple cherry banana apple"
    for word in text.split():
        word_count[word] += 1
    print(f"단어 빈도: {dict(word_count)}")  # → 단어 빈도: {'apple': 3, 'banana': 2, 'cherry': 1}

    # 그룹핑
    students: list[tuple[str, str]] = [
        ("Alice", "Math"), ("Bob", "Science"),
        ("Charlie", "Math"), ("Diana", "Science"),
        ("Eve", "Math"),
    ]
    by_subject: defaultdict[str, list[str]] = defaultdict(list)
    for name, subject in students:
        by_subject[subject].append(name)
    print(f"\n과목별 그룹: {dict(by_subject)}")

    # 중첩 defaultdict
    nested: defaultdict[str, defaultdict[str, int]] = defaultdict(
        lambda: defaultdict(int)
    )
    nested["USA"]["Python"] += 10
    nested["Korea"]["Python"] += 5
    nested["Korea"]["Java"] += 3
    print(f"\n중첩 defaultdict:")
    for country, langs in nested.items():
        print(f"  {country}: {dict(langs)}")

    # 일반 dict 대비 장점
    print(f"\n📌 defaultdict vs dict.setdefault():")
    print(f"  defaultdict: 코드가 간결, 성능이 약간 더 좋음")
    print(f"  setdefault:  defaultdict 불필요 시 사용")


def demonstrate_counter() -> None:
    """Counter를 보여준다."""
    print("\n" + "=" * 60)
    print("2. Counter")
    print("=" * 60)

    # 기본 사용
    words: list[str] = "the cat sat on the mat the cat".split()
    counter: Counter[str] = Counter(words)
    print(f"Counter: {counter}")

    # most_common
    print(f"most_common(2): {counter.most_common(2)}")  # → most_common(2): [('the', 3), ('cat', 2)]

    # 문자열 Counter
    char_count: Counter[str] = Counter("mississippi")
    print(f"\n문자 빈도: {char_count}")

    # 산술 연산
    a: Counter[str] = Counter("aabbc")
    b: Counter[str] = Counter("abcdd")
    print(f"\na = {a}")
    print(f"b = {b}")
    print(f"a + b = {a + b}")
    print(f"a - b = {a - b}")  # 음수 제거
    print(f"a & b = {a & b}")  # 교집합 (최소)
    print(f"a | b = {a | b}")  # 합집합 (최대)

    # 유용한 메서드
    print(f"\ntotal (3.10+): {counter.total()}")  # → total (3.10+): 8
    print(f"elements: {list(Counter({'a': 2, 'b': 1}).elements())}")  # → elements: ['a', 'a', 'b']

    # 실용 예시
    inventory: Counter[str] = Counter(apples=5, bananas=3, oranges=7)
    sale: Counter[str] = Counter(apples=2, oranges=3)
    remaining: Counter[str] = inventory - sale
    print(f"\n재고 관리:")
    print(f"  재고: {dict(inventory)}")
    print(f"  판매: {dict(sale)}")
    print(f"  잔여: {dict(remaining)}")


def demonstrate_deque() -> None:
    """deque를 보여준다."""
    print("\n" + "=" * 60)
    print("3. deque (양방향 큐)")
    print("=" * 60)

    # 기본 사용
    dq: deque[int] = deque([1, 2, 3, 4, 5])
    print(f"deque: {dq}")

    # 양쪽 추가/제거 — O(1)
    dq.appendleft(0)
    dq.append(6)
    print(f"appendleft(0), append(6): {dq}")  # → appendleft(0), append(6): deque([0, 1, 2, 3, 4, 5, 6])

    left: int = dq.popleft()
    right: int = dq.pop()
    print(f"popleft → {left}, pop → {right}: {dq}")  # → popleft → 0, pop → 6: deque([1, 2, 3, 4, 5])

    # 확장
    dq.extendleft([-2, -1])  # 역순 추가됨!
    print(f"extendleft([-2,-1]): {dq}")  # → extendleft([-2,-1]): deque([-1, -2, 1, 2, 3, 4, 5])

    # 회전
    dq2: deque[int] = deque([1, 2, 3, 4, 5])
    dq2.rotate(2)   # 오른쪽으로 2칸
    print(f"\nrotate(2):  {dq2}")  # → rotate(2):  deque([4, 5, 1, 2, 3])
    dq2.rotate(-2)  # 왼쪽으로 2칸 (원복)
    print(f"rotate(-2): {dq2}")  # → rotate(-2): deque([1, 2, 3, 4, 5])

    # maxlen — 고정 크기 버퍼
    buffer: deque[str] = deque(maxlen=3)
    for item in ["a", "b", "c", "d", "e"]:
        buffer.append(item)
        print(f"  append({item!r}): {list(buffer)}")
    print(f"💡 maxlen=3 → 오래된 항목 자동 제거")

    # 성능 비교
    print(f"\n📌 list vs deque:")
    print(f"  list.append:     O(1)   |  deque.append:     O(1)")
    print(f"  list.insert(0):  O(n)   |  deque.appendleft: O(1)")
    print(f"  list[i]:         O(1)   |  deque[i]:         O(n)")
    print(f"  💡 양쪽 끝 조작 → deque, 랜덤 접근 → list")


def demonstrate_ordereddict() -> None:
    """OrderedDict를 보여준다."""
    print("\n" + "=" * 60)
    print("4. OrderedDict")
    print("=" * 60)

    # Python 3.7+에서 dict도 삽입 순서를 보장하지만
    # OrderedDict는 추가 기능 제공
    od: OrderedDict[str, int] = OrderedDict()
    od["c"] = 3
    od["a"] = 1
    od["b"] = 2
    print(f"OrderedDict: {od}")

    # move_to_end
    od.move_to_end("c")        # 맨 뒤로
    print(f"move_to_end('c'): {od}")

    od.move_to_end("b", last=False)  # 맨 앞으로
    print(f"move_to_end('b', False): {od}")

    # popitem — 마지막/처음 제거
    last: tuple[str, int] = od.popitem()         # 마지막
    print(f"popitem(): {last}")  # → popitem(): ('c', 3)
    first: tuple[str, int] = od.popitem(last=False)  # 처음
    print(f"popitem(False): {first}")  # → popitem(False): ('b', 2)

    # 순서가 평등 비교에 영향
    d1: OrderedDict[str, int] = OrderedDict([("a", 1), ("b", 2)])
    d2: OrderedDict[str, int] = OrderedDict([("b", 2), ("a", 1)])
    print(f"\n순서 비교:")
    print(f"  d1 == d2 (OrderedDict): {d1 == d2}")  # →   d1 == d2 (OrderedDict): False
    print(f"  dict(d1) == dict(d2):   {dict(d1) == dict(d2)}")  # →   dict(d1) == dict(d2):   True

    print(f"\n📌 dict vs OrderedDict:")
    print(f"  dict:        삽입 순서 보장 (3.7+), 가벼움")
    print(f"  OrderedDict: move_to_end, popitem(last=False), 순서 비교")


def demonstrate_chainmap() -> None:
    """ChainMap을 보여준다."""
    print("\n" + "=" * 60)
    print("5. ChainMap")
    print("=" * 60)

    # 여러 딕셔너리를 체인으로 연결 (우선순위 순서)
    defaults: dict[str, str | int] = {"color": "red", "size": 10, "font": "Arial"}
    user_settings: dict[str, str | int] = {"color": "blue", "size": 14}
    cli_args: dict[str, int] = {"size": 20}

    config: ChainMap[str, str | int] = ChainMap(cli_args, user_settings, defaults)
    print(f"ChainMap (우선순위: CLI > User > Default):")
    print(f"  color = {config['color']!r}")  # →   color = 'blue'
    print(f"  size = {config['size']}")       # →   size = 20
    print(f"  font = {config['font']!r}")     # →   font = 'Arial'

    # maps 속성
    print(f"\nmaps:")
    for i, m in enumerate(config.maps):
        print(f"  [{i}] {m}")

    # 새 컨텍스트 추가
    with_extra: ChainMap[str, str | int] = config.new_child({"debug": True})
    print(f"\nnew_child: debug = {with_extra.get('debug')}")
    print(f"  원본 config에는 없음: {config.get('debug', 'N/A')}")

    # 실용 예시: 환경 변수 계층
    import os
    env: ChainMap[str, str] = ChainMap(
        {"APP_ENV": "test"},  # 오버라이드
        dict(os.environ),     # 실제 환경 변수
    )
    print(f"\n환경 변수 체인: APP_ENV = {env.get('APP_ENV')!r}")


def demonstrate_namedtuple_patterns() -> None:
    """namedtuple 실용 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("6. namedtuple 실용 패턴")
    print("=" * 60)

    # collections.namedtuple
    Point = namedtuple("Point", ["x", "y"])
    p: Point = Point(3, 4)
    print(f"namedtuple: {p}")
    print(f"  p.x={p.x}, p[0]={p[0]}")  # →   p.x=3, p[0]=3

    # 기본값 (Python 3.6.1+)
    Point3D = namedtuple("Point3D", ["x", "y", "z"], defaults=[0])
    p3: Point3D = Point3D(1, 2)
    print(f"\n기본값: {p3}")

    # _asdict, _replace
    d: dict[str, int] = p._asdict()
    p2: Point = p._replace(x=10)
    print(f"_asdict: {d}")  # → _asdict: {'x': 3, 'y': 4}
    print(f"_replace: {p2}")  # → _replace: Point(x=10, y=4)

    # typing.NamedTuple (권장)
    from typing import NamedTuple

    class Employee(NamedTuple):
        """직원 (타입 힌트 포함)."""
        name: str
        department: str
        salary: int = 50000

    emp: Employee = Employee("Alice", "Dev", 80000)
    print(f"\ntyping.NamedTuple: {emp}")

    # namedtuple vs dataclass 비교
    print(f"\n📌 NamedTuple vs @dataclass:")
    print(f"  NamedTuple: 불변, 튜플 호환, 가벼움, 언패킹 가능")
    print(f"  dataclass:  가변(기본), 메서드 추가 용이, slots 옵션")
    print(f"  💡 불변 데이터 → NamedTuple, 그 외 → dataclass")


if __name__ == "__main__":
    demonstrate_defaultdict()
    demonstrate_counter()
    demonstrate_deque()
    demonstrate_ordereddict()
    demonstrate_chainmap()
    demonstrate_namedtuple_patterns()

    print("\n" + "=" * 60)
    print("✅ _310_collections_module.py 학습 완료!")
    print("=" * 60)
