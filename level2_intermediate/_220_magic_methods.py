"""
_220_magic_methods.py — 매직 메서드 (Magic/Dunder Methods)

이 모듈에서 다루는 내용:
  1. 비교 메서드 (__eq__, __lt__ 등)
  2. 산술 메서드 (__add__, __mul__ 등)
  3. 컨테이너 메서드 (__len__, __getitem__, __contains__)
  4. __hash__와 해시 가능 객체
  5. __call__ (호출 가능 객체)
  6. __format__와 커스텀 포맷팅

실행 방법:
    poetry run python 2_intermediate/_220_magic_methods.py
"""

from collections.abc import Iterator
from functools import total_ordering


def demonstrate_comparison() -> None:
    """비교 매직 메서드를 보여준다."""
    print("=" * 60)
    print("1. 비교 메서드 (__eq__, __lt__ 등)")
    print("=" * 60)

    @total_ordering  # __eq__와 __lt__만 정의하면 나머지 자동 생성
    class Temperature:
        """온도를 나타내는 클래스."""

        def __init__(self, celsius: float) -> None:
            self.celsius: float = celsius

        def __eq__(self, other: object) -> bool:
            if not isinstance(other, Temperature):
                return NotImplemented
            return self.celsius == other.celsius

        def __lt__(self, other: object) -> bool:
            if not isinstance(other, Temperature):
                return NotImplemented
            return self.celsius < other.celsius

        def __repr__(self) -> str:
            return f"Temperature({self.celsius}°C)"

    t1: Temperature = Temperature(20)
    t2: Temperature = Temperature(25)
    t3: Temperature = Temperature(20)

    print(f"t1 = {t1}, t2 = {t2}, t3 = {t3}")
    print(f"t1 == t3 → {t1 == t3}")  # → t1 == t3 → True
    print(f"t1 < t2  → {t1 < t2}")  # → t1 < t2  → True
    print(f"t1 >= t2 → {t1 >= t2}")  # → t1 >= t2 → False
    print(f"sorted: {sorted([t2, t1, t3])}")  # → sorted: [Temperature(20°C), Temperature(20°C), Temperature(25°C)]

    # NotImplemented 반환의 중요성
    print(f"\nt1 == 20 → {t1 == 20}")  # → t1 == 20 → False
    print(f"💡 NotImplemented 반환 → Python이 반대쪽 __eq__ 시도")


def demonstrate_arithmetic() -> None:
    """산술 매직 메서드를 보여준다."""
    print("\n" + "=" * 60)
    print("2. 산술 메서드 (__add__, __mul__ 등)")
    print("=" * 60)

    class Vector:
        """2차원 벡터 클래스."""

        def __init__(self, x: float, y: float) -> None:
            self.x: float = x
            self.y: float = y

        def __add__(self, other: "Vector") -> "Vector":
            """벡터 덧셈."""
            return Vector(self.x + other.x, self.y + other.y)

        def __sub__(self, other: "Vector") -> "Vector":
            """벡터 뺄셈."""
            return Vector(self.x - other.x, self.y - other.y)

        def __mul__(self, scalar: float) -> "Vector":
            """스칼라 곱."""
            return Vector(self.x * scalar, self.y * scalar)

        def __rmul__(self, scalar: float) -> "Vector":
            """역방향 스칼라 곱 (3 * vector)."""
            return self.__mul__(scalar)

        def __neg__(self) -> "Vector":
            """부호 반전."""
            return Vector(-self.x, -self.y)

        def __abs__(self) -> float:
            """벡터 크기."""
            return (self.x ** 2 + self.y ** 2) ** 0.5

        def __bool__(self) -> bool:
            """영벡터가 아닌지."""
            return self.x != 0 or self.y != 0

        def __repr__(self) -> str:
            return f"Vector({self.x}, {self.y})"

    v1: Vector = Vector(3, 4)
    v2: Vector = Vector(1, 2)

    print(f"v1 = {v1}, v2 = {v2}")
    print(f"v1 + v2 = {v1 + v2}")  # → v1 + v2 = Vector(4, 6)
    print(f"v1 - v2 = {v1 - v2}")  # → v1 - v2 = Vector(2, 2)
    print(f"v1 * 3  = {v1 * 3}")  # → v1 * 3  = Vector(9, 12)
    print(f"3 * v1  = {3 * v1}")  # → 3 * v1  = Vector(9, 12)
    print(f"-v1     = {-v1}")  # → -v1     = Vector(-3, -4)
    print(f"abs(v1) = {abs(v1)}")  # → abs(v1) = 5.0
    print(f"bool(Vector(0,0)) = {bool(Vector(0, 0))}")  # → bool(Vector(0,0)) = False

    # 복합 할당 연산자
    class Counter:
        """카운터 (+=, -= 지원)."""

        def __init__(self, count: int = 0) -> None:
            self.count: int = count

        def __iadd__(self, value: int) -> "Counter":
            """복합 덧셈 할당 (+=)."""
            self.count += value
            return self  # 반드시 self 반환!

        def __repr__(self) -> str:
            return f"Counter({self.count})"

    c: Counter = Counter(10)
    c += 5
    print(f"\n복합 할당: Counter +=5 → {c}")  # → 복합 할당: Counter +=5 → Counter(15)


def demonstrate_container() -> None:
    """컨테이너 매직 메서드를 보여준다."""
    print("\n" + "=" * 60)
    print("3. 컨테이너 메서드 (__len__, __getitem__ 등)")
    print("=" * 60)

    class Playlist:
        """재생 목록 (컨테이너 프로토콜 구현)."""

        def __init__(self, name: str, songs: list[str] | None = None) -> None:
            self.name: str = name
            self._songs: list[str] = songs or []

        def __len__(self) -> int:
            """곡 수를 반환한다."""
            return len(self._songs)

        def __getitem__(self, index: int | slice) -> str | list[str]:
            """인덱스로 곡에 접근한다."""
            return self._songs[index]

        def __setitem__(self, index: int, song: str) -> None:
            """인덱스로 곡을 변경한다."""
            self._songs[index] = song

        def __delitem__(self, index: int) -> None:
            """인덱스로 곡을 삭제한다."""
            del self._songs[index]

        def __contains__(self, song: str) -> bool:
            """곡이 있는지 확인한다."""
            return song in self._songs

        def __iter__(self) -> Iterator[str]:
            """곡을 순회한다."""
            return iter(self._songs)

        def __reversed__(self) -> Iterator[str]:
            """역순으로 순회한다."""
            return reversed(self._songs)

        def __repr__(self) -> str:
            return f"Playlist({self.name!r}, {len(self)} songs)"

    pl: Playlist = Playlist("My Music", ["Let It Be", "Yesterday", "Help!"])

    print(f"플레이리스트: {pl}")  # → 플레이리스트: Playlist('My Music', 3 songs)
    print(f"len(pl) = {len(pl)}")  # → len(pl) = 3
    print(f"pl[0] = {pl[0]!r}")  # → pl[0] = 'Let It Be'
    print(f"pl[-1] = {pl[-1]!r}")  # → pl[-1] = 'Help!'
    print(f"pl[0:2] = {pl[0:2]}")  # → pl[0:2] = ['Let It Be', 'Yesterday']
    print(f"'Help!' in pl = {'Help!' in pl}")  # → 'Help!' in pl = True

    # 순회
    print(f"\n순회:")
    for song in pl:
        print(f"  ♪ {song}")

    # 수정/삭제
    pl[1] = "Come Together"
    print(f"\n수정 후: {list(pl)}")  # → 수정 후: ['Let It Be', 'Come Together', 'Help!']

    del pl[0]
    print(f"삭제 후: {list(pl)}")  # → 삭제 후: ['Come Together', 'Help!']


def demonstrate_hash() -> None:
    """__hash__와 해시 가능 객체를 보여준다."""
    print("\n" + "=" * 60)
    print("4. __hash__와 해시 가능 객체")
    print("=" * 60)

    class Coordinate:
        """좌표 클래스 (해시 가능)."""

        def __init__(self, x: int, y: int) -> None:
            self._x: int = x
            self._y: int = y

        @property
        def x(self) -> int:
            return self._x

        @property
        def y(self) -> int:
            return self._y

        def __eq__(self, other: object) -> bool:
            if not isinstance(other, Coordinate):
                return NotImplemented
            return self._x == other._x and self._y == other._y

        def __hash__(self) -> int:
            return hash((self._x, self._y))

        def __repr__(self) -> str:
            return f"Coordinate({self._x}, {self._y})"

    c1: Coordinate = Coordinate(1, 2)
    c2: Coordinate = Coordinate(1, 2)
    c3: Coordinate = Coordinate(3, 4)

    print(f"c1 == c2     → {c1 == c2}")  # → c1 == c2     → True
    print(f"hash(c1) == hash(c2) → {hash(c1) == hash(c2)}")  # → hash(c1) == hash(c2) → True

    # set과 dict에서 사용 가능
    coords: set[Coordinate] = {c1, c2, c3}
    print(f"\nset에 저장: {coords}")
    print(f"  길이: {len(coords)} (c1과 c2는 동일)")  # →   길이: 2 (c1과 c2는 동일)

    lookup: dict[Coordinate, str] = {
        c1: "시작점",
        c3: "도착점",
    }
    print(f"dict 키: {lookup}")
    print(f"  lookup[c2] = {lookup[c2]!r}")  # →   lookup[c2] = '시작점'  (c1과 동일하므로 찾아짐)

    print(f"\n📌 __hash__ 규칙:")
    print(f"  1. __eq__ 정의 시 __hash__도 함께 정의")
    print(f"  2. a == b이면 hash(a) == hash(b)이어야 함")
    print(f"  3. 가변 객체는 __hash__ = None (unhashable)")


def demonstrate_call() -> None:
    """__call__ 매직 메서드를 보여준다."""
    print("\n" + "=" * 60)
    print("5. __call__ (호출 가능 객체)")
    print("=" * 60)

    class Validator:
        """범위 검증기 (호출 가능 객체)."""

        def __init__(self, min_val: float, max_val: float) -> None:
            self.min_val: float = min_val
            self.max_val: float = max_val

        def __call__(self, value: float) -> bool:
            """값이 범위 내인지 검증한다."""
            return self.min_val <= value <= self.max_val

        def __repr__(self) -> str:
            return f"Validator({self.min_val}, {self.max_val})"

    # 함수처럼 호출 가능
    is_percentage: Validator = Validator(0, 100)
    is_adult_age: Validator = Validator(18, 120)

    print(f"is_percentage(50) = {is_percentage(50)}")  # → is_percentage(50) = True
    print(f"is_percentage(150) = {is_percentage(150)}")  # → is_percentage(150) = False
    print(f"is_adult_age(25) = {is_adult_age(25)}")  # → is_adult_age(25) = True
    print(f"is_adult_age(10) = {is_adult_age(10)}")  # → is_adult_age(10) = False

    # callable() 확인
    print(f"\ncallable(is_percentage) = {callable(is_percentage)}")  # → callable(is_percentage) = True

    # 상태를 가진 함수 대용
    class Accumulator:
        """상태를 가진 누산기."""

        def __init__(self) -> None:
            self.values: list[float] = []

        def __call__(self, value: float) -> float:
            """값을 추가하고 평균을 반환한다."""
            self.values.append(value)
            return sum(self.values) / len(self.values)

    avg: Accumulator = Accumulator()
    print(f"\n누산기 (이동 평균):")
    for v in [10, 20, 30, 40, 50]:
        print(f"  avg({v}) = {avg(v):.1f}")


def demonstrate_format() -> None:
    """__format__과 커스텀 포맷팅을 보여준다."""
    print("\n" + "=" * 60)
    print("6. __format__와 커스텀 포맷팅")
    print("=" * 60)

    class Money:
        """금액 클래스 (커스텀 포맷팅 지원)."""

        def __init__(self, amount: float, currency: str = "KRW") -> None:
            self.amount: float = amount
            self.currency: str = currency

        def __format__(self, spec: str) -> str:
            """커스텀 포맷 스펙을 처리한다.

            spec:
                'k' → 한국 원화 형식
                'u' → USD 형식
                ',' → 천 단위 구분
                기타 → 기본 float 포맷
            """
            if spec == "k":
                return f"₩{self.amount:,.0f}"
            elif spec == "u":
                return f"${self.amount:,.2f}"
            elif spec == ",":
                return f"{self.amount:,.0f} {self.currency}"
            else:
                return format(self.amount, spec or ".2f")

        def __repr__(self) -> str:
            return f"Money({self.amount}, {self.currency!r})"

    price: Money = Money(1_500_000)
    print(f"기본:      {price}")  # → 기본:      Money(1500000, 'KRW')
    print(f"한국 원화: {price:k}")  # → 한국 원화: ₩1,500,000
    print(f"USD:       {price:u}")  # → USD:       $1,500,000.00
    print(f"천단위:    {price:,}")  # → 천단위:    1,500,000 KRW

    # 매직 메서드 총정리
    print(f"\n📌 주요 매직 메서드 카테고리:")
    print(f"  생성/소멸: __init__, __new__, __del__")
    print(f"  문자열:    __str__, __repr__, __format__")
    print(f"  비교:      __eq__, __lt__, __le__, __gt__, __ge__")
    print(f"  산술:      __add__, __sub__, __mul__, __truediv__")
    print(f"  역산술:    __radd__, __rsub__, __rmul__")
    print(f"  복합할당:  __iadd__, __isub__, __imul__")
    print(f"  컨테이너:  __len__, __getitem__, __setitem__, __contains__")
    print(f"  이터러블:  __iter__, __next__, __reversed__")
    print(f"  호출:      __call__")
    print(f"  해시:      __hash__")
    print(f"  컨텍스트:  __enter__, __exit__")


if __name__ == "__main__":
    demonstrate_comparison()
    demonstrate_arithmetic()
    demonstrate_container()
    demonstrate_hash()
    demonstrate_call()
    demonstrate_format()

    print("\n" + "=" * 60)
    print("✅ _220_magic_methods.py 학습 완료!")
    print("=" * 60)
