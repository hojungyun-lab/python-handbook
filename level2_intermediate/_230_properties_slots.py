"""
_230_properties_slots.py — 프로퍼티와 __slots__ (Properties & Slots)

이 모듈에서 다루는 내용:
  1. @property 데코레이터
  2. setter와 deleter
  3. 데이터 검증 패턴
  4. 계산된 프로퍼티
  5. __slots__
  6. __slots__ + 상속

실행 방법:
    poetry run python 2_intermediate/_230_properties_slots.py
"""

import sys


def demonstrate_property_basic() -> None:
    """@property 기본 사용법을 보여준다."""
    print("=" * 60)
    print("1. @property 데코레이터")
    print("=" * 60)

    class Circle:
        """원 — property로 반지름과 면적을 관리."""

        def __init__(self, radius: float) -> None:
            self._radius: float = radius  # protected

        @property
        def radius(self) -> float:
            """반지름을 반환한다 (getter)."""
            return self._radius

        @radius.setter
        def radius(self, value: float) -> None:
            """반지름을 설정한다 (setter + 검증)."""
            if value < 0:
                raise ValueError("반지름은 음수일 수 없습니다")
            self._radius = value

        @property
        def area(self) -> float:
            """면적을 계산한다 (읽기 전용)."""
            import math
            return math.pi * self._radius ** 2

        @property
        def diameter(self) -> float:
            """지름을 반환한다."""
            return self._radius * 2

        def __repr__(self) -> str:
            return f"Circle(radius={self._radius})"

    c: Circle = Circle(5)
    print(f"circle = {c}")  # → circle = Circle(radius=5)
    print(f"  radius = {c.radius}")  # →   radius = 5
    print(f"  diameter = {c.diameter}")  # →   diameter = 10
    print(f"  area = {c.area:.2f}")  # →   area = 78.54

    # setter 사용
    c.radius = 10
    print(f"\nradius = 10 설정 후:")
    print(f"  area = {c.area:.2f}")  # →   area = 314.16

    # 검증
    try:
        c.radius = -1
    except ValueError as e:
        print(f"\n음수 반지름 → ValueError: {e}")

    # 읽기 전용 프로퍼티 (setter 없음)
    try:
        c.area = 100  # type: ignore[attr-defined]
    except AttributeError as e:
        print(f"area 설정 → AttributeError: {e}")


def demonstrate_setter_deleter() -> None:
    """setter와 deleter를 보여준다."""
    print("\n" + "=" * 60)
    print("2. setter와 deleter")
    print("=" * 60)

    class User:
        """사용자 — 이메일 검증 포함."""

        def __init__(self, name: str, email: str) -> None:
            self._name: str = name
            self._email: str = ""
            self.email = email  # setter를 통해 검증

        @property
        def name(self) -> str:
            return self._name

        @name.setter
        def name(self, value: str) -> None:
            if not value.strip():
                raise ValueError("이름은 빈 문자열일 수 없습니다")
            self._name = value.strip()

        @property
        def email(self) -> str:
            return self._email

        @email.setter
        def email(self, value: str) -> None:
            if "@" not in value:
                raise ValueError(f"유효하지 않은 이메일: {value!r}")
            self._email = value.lower()

        @email.deleter
        def email(self) -> None:
            print("  이메일 삭제됨")
            self._email = ""

        def __repr__(self) -> str:
            return f"User({self._name!r}, {self._email!r})"

    user: User = User("Alice", "Alice@Example.com")
    print(f"user = {user}")  # → user = User('Alice', 'alice@example.com')
    print(f"  email = {user.email}")  # →   email = alice@example.com

    # setter 검증
    try:
        user.email = "invalid-email"
    except ValueError as e:
        print(f"\n잘못된 이메일 → ValueError: {e}")

    # deleter
    del user.email
    print(f"삭제 후: {user}")  # → 삭제 후: User('Alice', '')


def demonstrate_validation_pattern() -> None:
    """데이터 검증 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("3. 데이터 검증 패턴")
    print("=" * 60)

    class Product:
        """상품 — 다양한 검증 패턴 적용."""

        def __init__(
            self,
            name: str,
            price: float,
            quantity: int = 0,
        ) -> None:
            self.name = name        # setter 통해 검증
            self.price = price
            self.quantity = quantity

        @property
        def name(self) -> str:
            return self._name

        @name.setter
        def name(self, value: str) -> None:
            if not isinstance(value, str) or len(value) < 1:
                raise ValueError("상품명은 비어있을 수 없습니다")
            self._name: str = value

        @property
        def price(self) -> float:
            return self._price

        @price.setter
        def price(self, value: float) -> None:
            if value < 0:
                raise ValueError("가격은 음수일 수 없습니다")
            self._price: float = float(value)

        @property
        def quantity(self) -> int:
            return self._quantity

        @quantity.setter
        def quantity(self, value: int) -> None:
            if not isinstance(value, int) or value < 0:
                raise ValueError("수량은 0 이상 정수여야 합니다")
            self._quantity: int = value

        @property
        def total_value(self) -> float:
            """총 가치를 반환한다 (계산된 프로퍼티)."""
            return self._price * self._quantity

        def __repr__(self) -> str:
            return (
                f"Product({self._name!r}, "
                f"price={self._price}, qty={self._quantity})"
            )

    p: Product = Product("Python 책", 35_000, 3)
    print(f"product = {p}")
    print(f"  total_value = ₩{p.total_value:,.0f}")  # →   total_value = ₩105,000

    # 검증
    errors: list[tuple[str, str, object]] = [
        ("name", "", "빈 문자열"),
        ("price", -100, "음수 가격"),
        ("quantity", -1, "음수 수량"),
    ]
    print(f"\n검증 테스트:")
    for attr, value, desc in errors:
        try:
            setattr(p, attr, value)
        except (ValueError, TypeError) as e:
            print(f"  {desc} → {e}")


def demonstrate_computed_properties() -> None:
    """계산된 프로퍼티를 보여준다."""
    print("\n" + "=" * 60)
    print("4. 계산된 프로퍼티")
    print("=" * 60)

    class Rectangle:
        """직사각형 — 계산된 프로퍼티 다수."""

        def __init__(self, width: float, height: float) -> None:
            self.width: float = width
            self.height: float = height

        @property
        def area(self) -> float:
            return self.width * self.height

        @property
        def perimeter(self) -> float:
            return 2 * (self.width + self.height)

        @property
        def is_square(self) -> bool:
            return self.width == self.height

        @property
        def diagonal(self) -> float:
            return (self.width ** 2 + self.height ** 2) ** 0.5

        def __repr__(self) -> str:
            return f"Rectangle({self.width} × {self.height})"

    rect: Rectangle = Rectangle(3, 4)
    print(f"rect = {rect}")
    print(f"  area = {rect.area}")  # →   area = 12
    print(f"  perimeter = {rect.perimeter}")  # →   perimeter = 14
    print(f"  diagonal = {rect.diagonal:.2f}")  # →   diagonal = 5.00
    print(f"  is_square = {rect.is_square}")  # →   is_square = False

    sq: Rectangle = Rectangle(5, 5)
    print(f"\nsq = {sq}")
    print(f"  is_square = {sq.is_square}")  # →   is_square = True

    # 캐시된 프로퍼티 (functools.cached_property)
    from functools import cached_property

    class DataAnalyzer:
        """비용이 높은 계산을 캐시하는 클래스."""

        def __init__(self, data: list[float]) -> None:
            self._data: list[float] = data

        @cached_property
        def statistics(self) -> dict[str, float]:
            """통계를 계산한다 (비용 높은 연산 — 캐시)."""
            print("  [통계 계산 중...]")
            n: int = len(self._data)
            mean: float = sum(self._data) / n
            variance: float = sum((x - mean) ** 2 for x in self._data) / n
            return {
                "mean": round(mean, 2),
                "variance": round(variance, 2),
                "std": round(variance ** 0.5, 2),
                "min": min(self._data),
                "max": max(self._data),
            }

    print(f"\ncached_property:")
    analyzer: DataAnalyzer = DataAnalyzer([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(f"  첫 번째 접근: {analyzer.statistics}")
    print(f"  두 번째 접근: {analyzer.statistics}")
    print(f"  💡 '[통계 계산 중...]'이 한 번만 출력됨!")


def demonstrate_slots() -> None:
    """__slots__를 보여준다."""
    print("\n" + "=" * 60)
    print("5. __slots__")
    print("=" * 60)

    # 일반 클래스 — __dict__ 사용
    class PointDict:
        def __init__(self, x: float, y: float) -> None:
            self.x: float = x
            self.y: float = y

    # __slots__ 클래스 — 고정 속성, 메모리 절약
    class PointSlots:
        __slots__ = ("x", "y")

        def __init__(self, x: float, y: float) -> None:
            self.x: float = x
            self.y: float = y

    pd: PointDict = PointDict(1.0, 2.0)
    ps: PointSlots = PointSlots(1.0, 2.0)

    print(f"PointDict.__dict__: {pd.__dict__}")  # → PointDict.__dict__: {'x': 1.0, 'y': 2.0}
    try:
        _ = ps.__dict__
    except AttributeError:
        print(f"PointSlots: __dict__ 없음!")

    # 메모리 비교
    size_dict: int = sys.getsizeof(pd) + sys.getsizeof(pd.__dict__)
    size_slots: int = sys.getsizeof(ps)
    print(f"\n메모리 비교:")
    print(f"  PointDict:  {size_dict} bytes (__dict__ 포함)")
    print(f"  PointSlots: {size_slots} bytes")
    print(f"  절감: {size_dict - size_slots} bytes ({(1 - size_slots/size_dict)*100:.0f}%)")

    # __slots__에 없는 속성 추가 불가
    try:
        ps.z = 3.0  # type: ignore[attr-defined]
    except AttributeError as e:
        print(f"\n없는 속성 추가 → AttributeError: {e}")

    # 일반 클래스는 자유롭게 추가
    pd.z = 3.0  # type: ignore[attr-defined]
    print(f"PointDict에 z 추가: {pd.__dict__}")

    print(f"\n📌 __slots__ 사용 가이드:")
    print(f"  ✅ 인스턴스 수가 많을 때 (수천~수백만)")
    print(f"  ✅ 속성이 고정적일 때")
    print(f"  ✅ 메모리/속도가 중요할 때")
    print(f"  ❌ 동적 속성 추가가 필요할 때")
    print(f"  ❌ 다중 상속 시 복잡해질 수 있음")


def demonstrate_slots_inheritance() -> None:
    """__slots__과 상속의 관계를 보여준다."""
    print("\n" + "=" * 60)
    print("6. __slots__ + 상속")
    print("=" * 60)

    class Base:
        __slots__ = ("x",)

        def __init__(self, x: int) -> None:
            self.x: int = x

    class Child(Base):
        __slots__ = ("y",)  # 추가 슬롯만 정의

        def __init__(self, x: int, y: int) -> None:
            super().__init__(x)
            self.y: int = y

    c: Child = Child(1, 2)
    print(f"Child: x={c.x}, y={c.y}")  # → Child: x=1, y=2

    # 부모/자식 슬롯 모두 사용 가능
    print(f"Base.__slots__ = {Base.__slots__}")  # → Base.__slots__ = ('x',)
    print(f"Child.__slots__ = {Child.__slots__}")  # → Child.__slots__ = ('y',)

    # __slots__ 없는 부모와 혼합
    class MixedChild(Child):
        pass  # __slots__ 미정의 → __dict__ 생성

    mc: MixedChild = MixedChild(1, 2)
    mc.z = 3  # type: ignore[attr-defined]
    print(f"\nMixedChild (slots 누락): z={mc.z}, __dict__={mc.__dict__}")
    print(f"  ⚠️ __slots__의 메모리 이점이 사라짐!")


if __name__ == "__main__":
    demonstrate_property_basic()
    demonstrate_setter_deleter()
    demonstrate_validation_pattern()
    demonstrate_computed_properties()
    demonstrate_slots()
    demonstrate_slots_inheritance()

    print("\n" + "=" * 60)
    print("✅ _230_properties_slots.py 학습 완료!")
    print("=" * 60)
