"""
_210_inheritance.py — 상속 (Inheritance)

이 모듈에서 다루는 내용:
  1. 단일 상속과 super()
  2. 메서드 오버라이딩
  3. 다중 상속과 MRO
  4. 추상 클래스 (ABC)
  5. Protocol (구조적 서브타이핑)
  6. isinstance()와 issubclass()

실행 방법:
    poetry run python 2_intermediate/_210_inheritance.py
"""

import math
from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable


def demonstrate_single_inheritance() -> None:
    """단일 상속과 super()를 보여준다."""
    print("=" * 60)
    print("1. 단일 상속과 super()")
    print("=" * 60)

    class Animal:
        """동물 기본 클래스."""

        def __init__(self, name: str, age: int) -> None:
            self.name: str = name
            self.age: int = age

        def speak(self) -> str:
            return f"{self.name}: ..."

        def info(self) -> str:
            return f"{self.name} ({self.age}살)"

    class Dog(Animal):
        """개 클래스 — Animal 상속."""

        def __init__(self, name: str, age: int, breed: str) -> None:
            super().__init__(name, age)  # 부모 __init__ 호출
            self.breed: str = breed

        def speak(self) -> str:
            return f"{self.name}: 멍멍!"

        def info(self) -> str:
            return f"{super().info()} - {self.breed}"

    class Cat(Animal):
        """고양이 클래스."""

        def speak(self) -> str:
            return f"{self.name}: 야옹~"

    # 사용
    dog: Dog = Dog("초코", 3, "골든리트리버")
    cat: Cat = Cat("나비", 2)

    print(f"dog.info() = {dog.info()}")  # → dog.info() = 초코 (3살) - 골든리트리버
    print(f"dog.speak() = {dog.speak()}")  # → dog.speak() = 초코: 멍멍!
    print(f"cat.speak() = {cat.speak()}")  # → cat.speak() = 나비: 야옹~

    # 상속 관계 확인
    print(f"\nisinstance(dog, Dog) = {isinstance(dog, Dog)}")  # → isinstance(dog, Dog) = True
    print(f"isinstance(dog, Animal) = {isinstance(dog, Animal)}")  # → isinstance(dog, Animal) = True
    print(f"issubclass(Dog, Animal) = {issubclass(Dog, Animal)}")  # → issubclass(Dog, Animal) = True


def demonstrate_method_override() -> None:
    """메서드 오버라이딩과 super() 활용을 보여준다."""
    print("\n" + "=" * 60)
    print("2. 메서드 오버라이딩")
    print("=" * 60)

    class Logger:
        """기본 로거."""

        def log(self, message: str) -> None:
            print(f"  [LOG] {message}")

    class TimestampLogger(Logger):
        """타임스탬프 추가 로거."""

        def log(self, message: str) -> None:
            from datetime import datetime
            ts: str = datetime.now().strftime("%H:%M:%S")
            super().log(f"[{ts}] {message}")

    class PrefixLogger(Logger):
        """접두어 추가 로거."""

        def __init__(self, prefix: str) -> None:
            self.prefix: str = prefix

        def log(self, message: str) -> None:
            super().log(f"{self.prefix}: {message}")

    print("Logger:")
    Logger().log("기본 메시지")

    print("\nTimestampLogger:")
    TimestampLogger().log("타임스탬프 포함")

    print("\nPrefixLogger:")
    PrefixLogger("ERROR").log("에러 발생!")


def demonstrate_multiple_inheritance() -> None:
    """다중 상속과 MRO를 보여준다."""
    print("\n" + "=" * 60)
    print("3. 다중 상속과 MRO")
    print("=" * 60)

    class A:
        def method(self) -> str:
            return "A"

    class B(A):
        def method(self) -> str:
            return "B"

    class C(A):
        def method(self) -> str:
            return "C"

    class D(B, C):
        pass

    # MRO (Method Resolution Order) — C3 선형화 알고리즘
    d: D = D()
    print(f"D().method() = {d.method()!r}")  # → D().method() = 'B'
    print(f"\nMRO: {[cls.__name__ for cls in D.__mro__]}")  # → MRO: ['D', 'B', 'C', 'A', 'object']
    print(f"💡 D → B → C → A → object 순서로 탐색")

    # Mixin 패턴 — 다중 상속의 올바른 활용
    class JsonMixin:
        """JSON 직렬화 기능을 제공하는 Mixin."""

        def to_json(self) -> str:
            import json
            return json.dumps(self.__dict__, ensure_ascii=False)

    class PrintableMixin:
        """출력 기능을 제공하는 Mixin."""

        def display(self) -> None:
            attrs: str = ", ".join(
                f"{k}={v!r}" for k, v in self.__dict__.items()
            )
            print(f"  {type(self).__name__}({attrs})")

    class User(JsonMixin, PrintableMixin):
        """사용자 클래스 (Mixin 다중 상속)."""

        def __init__(self, name: str, email: str) -> None:
            self.name: str = name
            self.email: str = email

    print(f"\nMixin 패턴:")
    user: User = User("Alice", "alice@example.com")
    user.display()
    print(f"  JSON: {user.to_json()}")

    print(f"\nUser MRO: {[cls.__name__ for cls in User.__mro__]}")  # → User MRO: ['User', 'JsonMixin', 'PrintableMixin', 'object']

    print(f"\n📌 다중 상속 가이드:")
    print(f"  ✅ Mixin 패턴 (단일 기능 추가)")
    print(f"  ❌ 다이아몬드 상속 (복잡성 증가)")
    print(f"  💡 Composition over Inheritance 원칙 고려")


def demonstrate_abc() -> None:
    """추상 클래스를 보여준다."""
    print("\n" + "=" * 60)
    print("4. 추상 클래스 (ABC)")
    print("=" * 60)

    class Shape(ABC):
        """도형 추상 클래스."""

        @abstractmethod
        def area(self) -> float:
            """면적을 반환한다."""
            ...

        @abstractmethod
        def perimeter(self) -> float:
            """둘레를 반환한다."""
            ...

        # 일반 메서드도 가능
        def description(self) -> str:
            """도형 설명을 반환한다."""
            return (
                f"{type(self).__name__}: "
                f"면적={self.area():.2f}, 둘레={self.perimeter():.2f}"
            )

    class Circle(Shape):
        """원 클래스."""

        def __init__(self, radius: float) -> None:
            self.radius: float = radius

        def area(self) -> float:
            return math.pi * self.radius ** 2

        def perimeter(self) -> float:
            return 2 * math.pi * self.radius

    class Rectangle(Shape):
        """직사각형 클래스."""

        def __init__(self, width: float, height: float) -> None:
            self.width: float = width
            self.height: float = height

        def area(self) -> float:
            return self.width * self.height

        def perimeter(self) -> float:
            return 2 * (self.width + self.height)

    # 추상 클래스는 직접 인스턴스화 불가
    try:
        Shape()  # type: ignore[abstract]
    except TypeError as e:
        print(f"Shape() → TypeError: {e}")

    # 구현 클래스 사용
    shapes: list[Shape] = [Circle(5), Rectangle(4, 6)]
    print(f"\n도형 목록:")
    for shape in shapes:
        print(f"  {shape.description()}")

    # 추상 프로퍼티
    class Configurable(ABC):
        """설정 가능한 추상 클래스."""

        @property
        @abstractmethod
        def config_key(self) -> str:
            """설정 키를 반환한다."""
            ...

    class AppConfig(Configurable):
        @property
        def config_key(self) -> str:
            return "app_settings"

    cfg: AppConfig = AppConfig()
    print(f"\n추상 프로퍼티: {cfg.config_key}")  # → 추상 프로퍼티: app_settings


def demonstrate_protocol() -> None:
    """Protocol (구조적 서브타이핑)을 보여준다."""
    print("\n" + "=" * 60)
    print("5. Protocol (구조적 서브타이핑)")
    print("=" * 60)

    # Protocol — 덕 타이핑을 타입 시스템에 반영
    @runtime_checkable
    class Drawable(Protocol):
        """그릴 수 있는 객체의 프로토콜."""

        def draw(self) -> str:
            """객체를 그린다."""
            ...

    class Square:
        """정사각형 (Drawable을 상속하지 않지만 draw 메서드 보유)."""

        def __init__(self, size: int) -> None:
            self.size: int = size

        def draw(self) -> str:
            return f"□ (size={self.size})"

    class TextLabel:
        """텍스트 레이블 (draw 메서드 보유)."""

        def __init__(self, text: str) -> None:
            self.text: str = text

        def draw(self) -> str:
            return f"📝 {self.text}"

    # Protocol — 상속 없이 구조적으로 호환
    def render(item: Drawable) -> None:
        """Drawable 프로토콜을 따르는 객체를 렌더한다."""
        print(f"  렌더링: {item.draw()}")

    print("Protocol (구조적 서브타이핑):")
    render(Square(10))
    render(TextLabel("Hello"))

    # runtime_checkable: isinstance() 사용 가능
    sq: Square = Square(5)
    print(f"\nisinstance(Square, Drawable) = {isinstance(sq, Drawable)}")  # → isinstance(Square, Drawable) = True

    # ABC vs Protocol 비교
    print(f"\n📌 ABC vs Protocol:")
    print(f"  ABC:      명시적 상속 필요 (명목적 타이핑)")
    print(f"  Protocol: 메서드 구조만 일치하면 OK (구조적 타이핑)")
    print(f"  💡 외부 라이브러리 타입과 호환 필요 → Protocol 사용")


def demonstrate_isinstance_issubclass() -> None:
    """isinstance()와 issubclass()를 보여준다."""
    print("\n" + "=" * 60)
    print("6. isinstance()와 issubclass()")
    print("=" * 60)

    class Base:
        pass

    class Child(Base):
        pass

    class GrandChild(Child):
        pass

    obj: GrandChild = GrandChild()

    print("isinstance() — 인스턴스 타입 확인:")
    print(f"  isinstance(obj, GrandChild) = {isinstance(obj, GrandChild)}")  # →   isinstance(obj, GrandChild) = True
    print(f"  isinstance(obj, Child) = {isinstance(obj, Child)}")  # →   isinstance(obj, Child) = True
    print(f"  isinstance(obj, Base) = {isinstance(obj, Base)}")  # →   isinstance(obj, Base) = True
    print(f"  isinstance(obj, object) = {isinstance(obj, object)}")  # →   isinstance(obj, object) = True

    # 여러 타입 확인 (tuple)
    value: int = 42
    print(f"\n다중 타입 확인:")
    print(f"  isinstance(42, (int, float)) = {isinstance(value, (int, float))}")  # →   isinstance(42, (int, float)) = True

    print(f"\nissubclass() — 클래스 상속 관계 확인:")
    print(f"  issubclass(GrandChild, Child) = {issubclass(GrandChild, Child)}")  # →   issubclass(GrandChild, Child) = True
    print(f"  issubclass(GrandChild, Base) = {issubclass(GrandChild, Base)}")  # →   issubclass(GrandChild, Base) = True
    print(f"  issubclass(Child, GrandChild) = {issubclass(Child, GrandChild)}")  # →   issubclass(Child, GrandChild) = False

    print(f"\n📌 type() vs isinstance():")
    print(f"  type(obj) == Child         → {type(obj) == Child} (정확한 타입만)")  # → ... → False
    print(f"  isinstance(obj, Child)     → {isinstance(obj, Child)} (상속 포함)")  # → ... → True
    print(f"  💡 isinstance() 사용 권장!")


if __name__ == "__main__":
    demonstrate_single_inheritance()
    demonstrate_method_override()
    demonstrate_multiple_inheritance()
    demonstrate_abc()
    demonstrate_protocol()
    demonstrate_isinstance_issubclass()

    print("\n" + "=" * 60)
    print("✅ _210_inheritance.py 학습 완료!")
    print("=" * 60)
