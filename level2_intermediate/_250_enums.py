"""
_250_enums.py — 열거형 (Enums)

이 모듈에서 다루는 내용:
  1. Enum 기본
  2. IntEnum, StrEnum
  3. auto()와 값 자동 할당
  4. Flag와 비트 연산
  5. 커스텀 Enum 패턴

실행 방법:
    poetry run python 2_intermediate/_250_enums.py
"""

from enum import Enum, IntEnum, StrEnum, Flag, auto, unique


def demonstrate_basic_enum() -> None:
    """Enum 기본을 보여준다."""
    print("=" * 60)
    print("1. Enum 기본")
    print("=" * 60)

    class Color(Enum):
        """색상 열거형."""
        RED = 1
        GREEN = 2
        BLUE = 3

    # 접근 방법
    print(f"Color.RED = {Color.RED}")  # → Color.RED = Color.RED
    print(f"Color.RED.name = {Color.RED.name!r}")  # → Color.RED.name = 'RED'
    print(f"Color.RED.value = {Color.RED.value}")  # → Color.RED.value = 1

    # 값으로 접근
    c: Color = Color(2)
    print(f"\nColor(2) = {c}")  # → Color(2) = Color.GREEN

    # 이름으로 접근
    c2: Color = Color["BLUE"]
    print(f"Color['BLUE'] = {c2}")  # → Color['BLUE'] = Color.BLUE

    # 비교
    print(f"\nColor.RED == Color.RED → {Color.RED == Color.RED}")  # → ... → True
    print(f"Color.RED is Color.RED → {Color.RED is Color.RED}")  # → ... → True
    print(f"Color.RED == 1 → {Color.RED == 1}")  # → ... → False

    # 순회
    print(f"\n모든 멤버:")
    for color in Color:
        print(f"  {color.name}: {color.value}")

    # 리스트/딕트 변환
    names: list[str] = [c.name for c in Color]
    print(f"\n이름 목록: {names}")  # → 이름 목록: ['RED', 'GREEN', 'BLUE']


def demonstrate_int_str_enum() -> None:
    """IntEnum과 StrEnum을 보여준다."""
    print("\n" + "=" * 60)
    print("2. IntEnum, StrEnum")
    print("=" * 60)

    # IntEnum — int와 비교/연산 가능
    class StatusCode(IntEnum):
        """HTTP 상태 코드."""
        OK = 200
        NOT_FOUND = 404
        SERVER_ERROR = 500

    print(f"IntEnum:")
    print(f"  StatusCode.OK == 200 → {StatusCode.OK == 200}")  # →   ... → True
    print(f"  StatusCode.OK > 100 → {StatusCode.OK > 100}")  # →   ... → True
    print(f"  StatusCode.OK + 1 = {StatusCode.OK + 1}")  # →   StatusCode.OK + 1 = 201

    # StrEnum (Python 3.11+) — str과 호환
    class Direction(StrEnum):
        """방향 열거형."""
        NORTH = "north"
        SOUTH = "south"
        EAST = "east"
        WEST = "west"

    print(f"\nStrEnum:")
    print(f"  Direction.NORTH == 'north' → {Direction.NORTH == 'north'}")  # →   ... → True
    print(f"  f-string: 방향={Direction.EAST}")  # →   f-string: 방향=east
    print(f"  upper: {Direction.NORTH.upper()}")  # →   upper: NORTH

    # 언제 무엇을 사용?
    print(f"\n📌 Enum 타입 선택:")
    print(f"  Enum:     값 비교 불가 (가장 안전)")
    print(f"  IntEnum:  int와 호환 필요 시")
    print(f"  StrEnum:  str과 호환 필요 시")


def demonstrate_auto() -> None:
    """auto()와 값 자동 할당을 보여준다."""
    print("\n" + "=" * 60)
    print("3. auto()와 값 자동 할당")
    print("=" * 60)

    class Season(Enum):
        """계절 (자동 값)."""
        SPRING = auto()
        SUMMER = auto()
        AUTUMN = auto()
        WINTER = auto()

    print("auto() 기본 (1부터 시작):")
    for s in Season:
        print(f"  {s.name} = {s.value}")

    # StrEnum + auto() → 이름의 소문자
    class Animal(StrEnum):
        CAT = auto()
        DOG = auto()
        BIRD = auto()

    print(f"\nStrEnum + auto():")
    for a in Animal:
        print(f"  {a.name} = {a.value!r}")

    # @unique — 중복 값 방지
    @unique
    class Priority(Enum):
        """우선순위 (중복 불가)."""
        LOW = 1
        MEDIUM = 2
        HIGH = 3

    print(f"\n@unique 데코레이터: 중복 값 방지")

    # 중복 시 에러 시연
    try:
        @unique
        class BadEnum(Enum):
            A = 1
            B = 1  # 중복!
    except ValueError as e:
        print(f"  중복 값 에러: {e}")


def demonstrate_flag() -> None:
    """Flag와 비트 연산을 보여준다."""
    print("\n" + "=" * 60)
    print("4. Flag와 비트 연산")
    print("=" * 60)

    class Permission(Flag):
        """파일 권한 플래그."""
        READ = auto()     # 1
        WRITE = auto()    # 2
        EXECUTE = auto()  # 4

    # 조합
    rw: Permission = Permission.READ | Permission.WRITE
    print(f"READ | WRITE = {rw}")
    print(f"  값: {rw.value}")  # →   값: 3

    all_perms: Permission = Permission.READ | Permission.WRITE | Permission.EXECUTE
    print(f"모든 권한: {all_perms}")

    # 포함 확인
    print(f"\nREAD in rw → {Permission.READ in rw}")  # → READ in rw → True
    print(f"EXECUTE in rw → {Permission.EXECUTE in rw}")  # → EXECUTE in rw → False

    # 제거
    result: Permission = all_perms & ~Permission.WRITE
    print(f"\n모든 권한에서 WRITE 제거: {result}")

    # 실용 예시
    def check_permission(
        user_perms: Permission,
        required: Permission,
    ) -> bool:
        """필요한 권한이 있는지 확인한다."""
        return required in user_perms

    admin: Permission = Permission.READ | Permission.WRITE | Permission.EXECUTE
    viewer: Permission = Permission.READ

    print(f"\n권한 체크:")
    print(f"  admin WRITE? {check_permission(admin, Permission.WRITE)}")  # →   admin WRITE? True
    print(f"  viewer WRITE? {check_permission(viewer, Permission.WRITE)}")  # →   viewer WRITE? False


def demonstrate_custom_patterns() -> None:
    """커스텀 Enum 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("5. 커스텀 Enum 패턴")
    print("=" * 60)

    # 메서드가 있는 Enum
    class Planet(Enum):
        """행성 (질량, 반지름 포함)."""
        MERCURY = (3.303e23, 2.4397e6)
        VENUS = (4.869e24, 6.0518e6)
        EARTH = (5.976e24, 6.37814e6)
        MARS = (6.421e23, 3.3972e6)

        def __init__(self, mass: float, radius: float) -> None:
            self.mass: float = mass
            self.radius: float = radius

        @property
        def surface_gravity(self) -> float:
            """표면 중력을 반환한다."""
            g: float = 6.67430e-11
            return g * self.mass / (self.radius ** 2)

    print("행성 표면 중력:")
    for planet in Planet:
        print(f"  {planet.name:<8} 중력: {planet.surface_gravity:.2f} m/s²")

    # Enum을 활용한 상태 머신
    class OrderStatus(StrEnum):
        """주문 상태."""
        PENDING = "pending"
        CONFIRMED = "confirmed"
        SHIPPED = "shipped"
        DELIVERED = "delivered"
        CANCELLED = "cancelled"

    # 허용된 전이 정의
    TRANSITIONS: dict[OrderStatus, list[OrderStatus]] = {
        OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
        OrderStatus.CONFIRMED: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
        OrderStatus.SHIPPED: [OrderStatus.DELIVERED],
        OrderStatus.DELIVERED: [],
        OrderStatus.CANCELLED: [],
    }

    def can_transition(
        current: OrderStatus,
        target: OrderStatus,
    ) -> bool:
        """상태 전이가 가능한지 확인한다."""
        return target in TRANSITIONS.get(current, [])

    print(f"\n상태 머신 (주문):")
    current: OrderStatus = OrderStatus.PENDING
    for target in OrderStatus:
        ok: bool = can_transition(current, target)
        print(f"  {current} → {target}: {'✅' if ok else '❌'}")


if __name__ == "__main__":
    demonstrate_basic_enum()
    demonstrate_int_str_enum()
    demonstrate_auto()
    demonstrate_flag()
    demonstrate_custom_patterns()

    print("\n" + "=" * 60)
    print("✅ _250_enums.py 학습 완료!")
    print("=" * 60)
