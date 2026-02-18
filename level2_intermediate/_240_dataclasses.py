"""
_240_dataclasses.py — 데이터클래스 (Dataclasses)

이 모듈에서 다루는 내용:
  1. @dataclass 기본
  2. field()와 기본값
  3. __post_init__
  4. frozen (불변 데이터클래스)
  5. kw_only, slots (Python 3.10+)
  6. 상속과 실용 패턴

실행 방법:
    poetry run python 2_intermediate/_240_dataclasses.py
"""

from dataclasses import dataclass, field, asdict, astuple, replace
from typing import ClassVar


def demonstrate_basic_dataclass() -> None:
    """@dataclass 기본을 보여준다."""
    print("=" * 60)
    print("1. @dataclass 기본")
    print("=" * 60)

    @dataclass
    class Point:
        """2차원 좌표."""
        x: float
        y: float

    # 자동 생성되는 메서드들
    p1: Point = Point(3.0, 4.0)
    p2: Point = Point(3.0, 4.0)
    p3: Point = Point(1.0, 2.0)

    print(f"자동 __init__:  Point(3.0, 4.0) → {p1}")  # → ... → Point(x=3.0, y=4.0)
    print(f"자동 __repr__:  {p1!r}")  # → 자동 __repr__:  Point(x=3.0, y=4.0)
    print(f"자동 __eq__:    p1 == p2 → {p1 == p2}")  # → ... → True
    print(f"                p1 == p3 → {p1 == p3}")  # → ... → False

    # 정렬을 위해 order=True
    @dataclass(order=True)
    class Student:
        """학생 (이름순 정렬)."""
        name: str
        grade: int

    students: list[Student] = [
        Student("Charlie", 3),
        Student("Alice", 1),
        Student("Bob", 2),
    ]
    print(f"\norder=True 정렬: {sorted(students)}")

    # 일반 클래스와 비교
    print(f"\n📌 @dataclass는 자동 생성:")
    print(f"  __init__, __repr__, __eq__, (옵션: __lt__ 등)")
    print(f"  → 보일러플레이트 코드 대폭 감소!")


def demonstrate_field() -> None:
    """field()와 기본값을 보여준다."""
    print("\n" + "=" * 60)
    print("2. field()와 기본값")
    print("=" * 60)

    @dataclass
    class Config:
        """설정 클래스."""
        name: str
        debug: bool = False
        max_retries: int = 3
        tags: list[str] = field(default_factory=list)  # 가변 기본값!
        _internal: str = field(default="hidden", repr=False)

        # ClassVar — 데이터클래스 필드가 아닌 클래스 변수
        version: ClassVar[str] = "1.0"

    c1: Config = Config("production")
    c2: Config = Config("dev", debug=True, tags=["test"])

    print(f"c1 = {c1}")  # → c1 = Config(name='production', debug=False, max_retries=3, tags=[])
    print(f"c2 = {c2}")  # → c2 = Config(name='dev', debug=True, max_retries=3, tags=['test'])
    print(f"ClassVar: Config.version = {Config.version!r}")  # → ClassVar: Config.version = '1.0'

    # ⚠️ 가변 기본값 — default_factory 필수!
    print(f"\n⚠️ 가변 기본값:")
    print(f"  tags: list[str] = [] → ❌ 에러!")
    print(f"  tags: list[str] = field(default_factory=list) → ✅ 올바름")

    # field() 매개변수
    print(f"\nfield() 주요 매개변수:")
    print(f"  default:         고정 기본값")
    print(f"  default_factory: 가변 기본값 (list, dict 등)")
    print(f"  repr:            __repr__ 포함 여부 (기본 True)")
    print(f"  compare:         __eq__ 비교 포함 여부 (기본 True)")
    print(f"  hash:            __hash__ 포함 여부")
    print(f"  init:            __init__ 매개변수 포함 여부 (기본 True)")
    print(f"  kw_only:         키워드 전용 여부 (3.10+)")


def demonstrate_post_init() -> None:
    """__post_init__을 보여준다."""
    print("\n" + "=" * 60)
    print("3. __post_init__")
    print("=" * 60)

    @dataclass
    class Rectangle:
        """직사각형 — 파생 속성 계산."""
        width: float
        height: float
        area: float = field(init=False)       # __init__에서 제외
        perimeter: float = field(init=False)

        def __post_init__(self) -> None:
            """파생 속성을 계산한다."""
            if self.width <= 0 or self.height <= 0:
                raise ValueError("너비와 높이는 양수여야 합니다")
            self.area = self.width * self.height
            self.perimeter = 2 * (self.width + self.height)

    r: Rectangle = Rectangle(3, 4)
    print(f"Rectangle(3, 4) = {r}")

    try:
        Rectangle(-1, 5)
    except ValueError as e:
        print(f"검증: {e}")

    # InitVar — __post_init__에만 전달되는 변수
    from dataclasses import InitVar

    @dataclass
    class DatabaseRecord:
        """DB 레코드 — 생성 시 자동 변환."""
        name: str
        raw_data: InitVar[str]  # __post_init__에만 전달
        processed_data: list[str] = field(init=False)

        def __post_init__(self, raw_data: str) -> None:
            """raw_data를 처리하여 저장한다."""
            self.processed_data = [
                item.strip() for item in raw_data.split(",")
            ]

    record: DatabaseRecord = DatabaseRecord("test", "a, b, c, d")
    print(f"\nInitVar: {record}")  # → InitVar: DatabaseRecord(name='test', processed_data=['a', 'b', 'c', 'd'])
    print(f"  processed_data = {record.processed_data}")  # →   processed_data = ['a', 'b', 'c', 'd']


def demonstrate_frozen() -> None:
    """frozen (불변) 데이터클래스를 보여준다."""
    print("\n" + "=" * 60)
    print("4. frozen (불변 데이터클래스)")
    print("=" * 60)

    @dataclass(frozen=True)
    class Color:
        """불변 색상 클래스."""
        r: int
        g: int
        b: int

        @property
        def hex(self) -> str:
            return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    red: Color = Color(255, 0, 0)
    blue: Color = Color(0, 0, 255)

    print(f"red = {red}, hex = {red.hex}")  # → red = Color(r=255, g=0, b=0), hex = #ff0000
    print(f"blue = {blue}, hex = {blue.hex}")  # → blue = Color(r=0, g=0, b=255), hex = #0000ff

    # 변경 시도 → 에러
    try:
        red.r = 128  # type: ignore[misc]
    except AttributeError as e:
        print(f"\n수정 시도 → {e}")

    # frozen → 자동으로 __hash__ 생성 → set/dict 키로 사용 가능
    colors: set[Color] = {red, blue, Color(255, 0, 0)}
    print(f"\nset에 저장: {colors}")
    print(f"  길이: {len(colors)} (중복 제거)")  # →   길이: 2 (중복 제거)

    # replace() — 불변 객체 복사 + 수정
    pink: Color = replace(red, g=192, b=203)
    print(f"\nreplace: red → pink = {pink}, hex = {pink.hex}")  # → ... = Color(r=255, g=192, b=203), hex = #ffc0cb


def demonstrate_modern_features() -> None:
    """Python 3.10+ 기능을 보여준다."""
    print("\n" + "=" * 60)
    print("5. kw_only, slots (Python 3.10+)")
    print("=" * 60)

    # kw_only — 키워드 전용 인수
    @dataclass(kw_only=True)
    class APIConfig:
        """API 설정 (모든 필드 키워드 전용)."""
        host: str
        port: int = 8080
        timeout: int = 30

    cfg: APIConfig = APIConfig(host="localhost", port=3000)
    print(f"kw_only: {cfg}")

    # slots=True — __slots__ 자동 생성
    @dataclass(slots=True)
    class PointSlots:
        """슬롯 데이터클래스."""
        x: float
        y: float

    import sys
    ps: PointSlots = PointSlots(1.0, 2.0)
    print(f"\nslots=True: {ps}")
    print(f"  __slots__ = {PointSlots.__slots__}")
    print(f"  크기: {sys.getsizeof(ps)} bytes")

    # match_args (기본 True)
    @dataclass
    class Command:
        """명령 (match-case 호환)."""
        action: str
        target: str

    cmd: Command = Command("move", "north")
    match cmd:
        case Command(action="move", target=direction):
            print(f"\nmatch_args: {direction}으로 이동!")
        case _:
            print("알 수 없는 명령")


def demonstrate_utility_functions() -> None:
    """유틸리티 함수와 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("6. 유틸리티 함수와 실용 패턴")
    print("=" * 60)

    @dataclass
    class Employee:
        name: str
        department: str
        salary: int

    emp: Employee = Employee("Alice", "Engineering", 85000)

    # asdict — 딕셔너리 변환
    d: dict = asdict(emp)
    print(f"asdict: {d}")  # → asdict: {'name': 'Alice', 'department': 'Engineering', 'salary': 85000}

    # astuple — 튜플 변환
    t: tuple = astuple(emp)
    print(f"astuple: {t}")  # → astuple: ('Alice', 'Engineering', 85000)

    # replace — 복사 + 수정
    emp2: Employee = replace(emp, salary=95000)
    print(f"replace: {emp2}")  # → replace: Employee(name='Alice', department='Engineering', salary=95000)

    # JSON 직렬화 패턴
    import json
    json_str: str = json.dumps(asdict(emp), ensure_ascii=False)
    print(f"\nJSON: {json_str}")

    # 상속
    @dataclass
    class Manager(Employee):
        team_size: int = 0

    mgr: Manager = Manager("Bob", "Engineering", 120000, team_size=10)
    print(f"\n상속: {mgr}")
    print(f"  isinstance(mgr, Employee) = {isinstance(mgr, Employee)}")  # →   isinstance(mgr, Employee) = True

    # 비교: dataclass vs NamedTuple vs 일반 클래스
    print(f"\n📌 데이터 컨테이너 선택 가이드:")
    print(f"  @dataclass:  가변 데이터 (기본), 검증/메서드 필요")
    print(f"  frozen DC:   불변 데이터, 해시 필요")
    print(f"  NamedTuple:  불변, 경량, 튜플 호환 필요")
    print(f"  dict:        스키마 미고정, 동적 키")
    print(f"  TypedDict:   dict의 타입 힌트")


if __name__ == "__main__":
    demonstrate_basic_dataclass()
    demonstrate_field()
    demonstrate_post_init()
    demonstrate_frozen()
    demonstrate_modern_features()
    demonstrate_utility_functions()

    print("\n" + "=" * 60)
    print("✅ _240_dataclasses.py 학습 완료!")
    print("=" * 60)
