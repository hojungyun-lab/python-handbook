"""
_200_classes_basics.py — 클래스 기초 (Classes Basics)

이 모듈에서 다루는 내용:
  1. 클래스 정의와 인스턴스 생성
  2. __init__과 인스턴스 변수
  3. 인스턴스 메서드, 클래스 메서드, 스태틱 메서드
  4. 클래스 변수 vs 인스턴스 변수
  5. __str__과 __repr__
  6. 접근 제어 관례 (_, __)

실행 방법:
    poetry run python 2_intermediate/_200_classes_basics.py
"""

from datetime import datetime


def demonstrate_class_definition() -> None:
    """클래스 정의와 인스턴스 생성을 보여준다."""
    print("=" * 60)
    print("1. 클래스 정의와 인스턴스 생성")
    print("=" * 60)

    # 가장 기본적인 클래스
    class Dog:
        """강아지를 나타내는 클래스."""

        def __init__(self, name: str, breed: str, age: int = 0) -> None:
            """Dog 인스턴스를 초기화한다.

            Args:
                name: 강아지 이름.
                breed: 품종.
                age: 나이 (기본값 0).
            """
            self.name: str = name       # 인스턴스 변수
            self.breed: str = breed
            self.age: int = age

        def bark(self) -> str:
            """짖는 소리를 반환한다."""
            return f"{self.name}: 멍멍!"

        def info(self) -> str:
            """강아지 정보를 반환한다."""
            return f"{self.name} ({self.breed}, {self.age}살)"

    # 인스턴스 생성
    dog1: Dog = Dog("초코", "골든리트리버", 3)
    dog2: Dog = Dog("모카", "푸들")

    print(f"dog1 = {dog1.info()}")  # → dog1 = 초코 (골든리트리버, 3살)
    print(f"dog2 = {dog2.info()}")  # → dog2 = 모카 (푸들, 0살)
    print(f"dog1.bark() = {dog1.bark()}")  # → dog1.bark() = 초코: 멍멍!

    # type과 isinstance
    print(f"\ntype(dog1) = {type(dog1)}")
    print(f"isinstance(dog1, Dog) = {isinstance(dog1, Dog)}")  # → isinstance(dog1, Dog) = True


def demonstrate_instance_class_vars() -> None:
    """클래스 변수와 인스턴스 변수의 차이를 보여준다."""
    print("\n" + "=" * 60)
    print("2. 클래스 변수 vs 인스턴스 변수")
    print("=" * 60)

    class Employee:
        """직원을 나타내는 클래스."""

        # 클래스 변수 — 모든 인스턴스가 공유
        company: str = "TechCorp"
        employee_count: int = 0

        def __init__(self, name: str, salary: int) -> None:
            # 인스턴스 변수 — 각 인스턴스마다 독립
            self.name: str = name
            self.salary: int = salary
            Employee.employee_count += 1

        def info(self) -> str:
            return f"{self.name} @ {self.company} (${self.salary:,})"

    e1: Employee = Employee("Alice", 80000)
    e2: Employee = Employee("Bob", 90000)

    print(f"e1: {e1.info()}")  # → e1: Alice @ TechCorp ($80,000)
    print(f"e2: {e2.info()}")  # → e2: Bob @ TechCorp ($90,000)
    print(f"총 직원 수: {Employee.employee_count}")  # → 총 직원 수: 2

    # 클래스 변수 vs 인스턴스 변수 접근
    print(f"\n클래스 변수 접근:")
    print(f"  Employee.company = {Employee.company!r}")  # →   Employee.company = 'TechCorp'
    print(f"  e1.company = {e1.company!r}")  # →   e1.company = 'TechCorp'

    # 인스턴스에서 클래스 변수를 "덮어쓰면" 인스턴스 변수가 생성됨
    e1.company = "NewCorp"  # ⚠️ 인스턴스 변수 생성!
    print(f"\ne1.company = 'NewCorp' 후:")
    print(f"  e1.company = {e1.company!r} (인스턴스 변수)")  # →   e1.company = 'NewCorp' (인스턴스 변수)
    print(f"  e2.company = {e2.company!r} (여전히 클래스 변수)")  # →   e2.company = 'TechCorp' (여전히 클래스 변수)
    print(f"  Employee.company = {Employee.company!r}")  # →   Employee.company = 'TechCorp'

    # __dict__ 확인
    print(f"\ne1.__dict__ = {e1.__dict__}")
    print(f"e2.__dict__ = {e2.__dict__}")


def demonstrate_methods() -> None:
    """세 가지 메서드 타입을 보여준다."""
    print("\n" + "=" * 60)
    print("3. 인스턴스 / 클래스 / 스태틱 메서드")
    print("=" * 60)

    class DateUtil:
        """날짜 관련 유틸리티 클래스."""

        default_format: str = "%Y-%m-%d"

        def __init__(self, year: int, month: int, day: int) -> None:
            self.year: int = year
            self.month: int = month
            self.day: int = day

        # 인스턴스 메서드 — self를 통해 인스턴스에 접근
        def format(self, fmt: str | None = None) -> str:
            """날짜를 포맷팅한다."""
            date: datetime = datetime(self.year, self.month, self.day)
            return date.strftime(fmt or self.default_format)

        # 클래스 메서드 — cls를 통해 클래스에 접근 (대체 생성자)
        @classmethod
        def from_string(cls, date_str: str) -> "DateUtil":
            """문자열에서 DateUtil 인스턴스를 생성한다."""
            parts: list[str] = date_str.split("-")
            return cls(int(parts[0]), int(parts[1]), int(parts[2]))

        @classmethod
        def today(cls) -> "DateUtil":
            """오늘 날짜로 DateUtil 인스턴스를 생성한다."""
            now: datetime = datetime.now()
            return cls(now.year, now.month, now.day)

        # 스태틱 메서드 — self도 cls도 없음 (유틸리티 함수)
        @staticmethod
        def is_leap_year(year: int) -> bool:
            """윤년인지 판별한다."""
            return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    # 인스턴스 메서드
    d: DateUtil = DateUtil(2025, 12, 25)
    print(f"인스턴스 메서드: {d.format()}")  # → 인스턴스 메서드: 2025-12-25
    print(f"커스텀 포맷: {d.format('%Y년 %m월 %d일')}")  # → 커스텀 포맷: 2025년 12월 25일

    # 클래스 메서드 (대체 생성자)
    d2: DateUtil = DateUtil.from_string("2024-06-15")
    print(f"\n클래스 메서드 (from_string): {d2.format()}")  # → 클래스 메서드 (from_string): 2024-06-15

    d3: DateUtil = DateUtil.today()
    print(f"클래스 메서드 (today): {d3.format()}")

    # 스태틱 메서드
    print(f"\n스태틱 메서드:")
    print(f"  2024 윤년? {DateUtil.is_leap_year(2024)}")  # →   2024 윤년? True
    print(f"  2025 윤년? {DateUtil.is_leap_year(2025)}")  # →   2025 윤년? False

    # 언제 무엇을 사용?
    print(f"\n📌 메서드 선택 가이드:")
    print(f"  인스턴스 메서드: 인스턴스 데이터에 접근 필요 (대부분)")
    print(f"  클래스 메서드:   대체 생성자, 클래스 변수 조작")
    print(f"  스태틱 메서드:   클래스/인스턴스 불필요한 유틸리티")


def demonstrate_str_repr() -> None:
    """__str__과 __repr__을 보여준다."""
    print("\n" + "=" * 60)
    print("4. __str__과 __repr__")
    print("=" * 60)

    class Point:
        """2차원 좌표를 나타내는 클래스."""

        def __init__(self, x: float, y: float) -> None:
            self.x: float = x
            self.y: float = y

        def __repr__(self) -> str:
            """개발자용 문자열 표현 (재생성 가능하게)."""
            return f"Point({self.x}, {self.y})"

        def __str__(self) -> str:
            """사용자용 문자열 표현."""
            return f"({self.x}, {self.y})"

    p: Point = Point(3.0, 4.0)
    print(f"str(p)  = {str(p)}")       # → str(p)  = (3.0, 4.0)
    print(f"repr(p) = {repr(p)}")      # → repr(p) = Point(3.0, 4.0)
    print(f"print(p) → {p}")           # → print(p) → (3.0, 4.0)
    print(f"리스트 안: {[p]}")         # → 리스트 안: [Point(3.0, 4.0)]

    # __repr__만 정의하면 __str__ 대체
    class Color:
        """색상 클래스 (__repr__만 정의)."""

        def __init__(self, r: int, g: int, b: int) -> None:
            self.r: int = r
            self.g: int = g
            self.b: int = b

        def __repr__(self) -> str:
            return f"Color(r={self.r}, g={self.g}, b={self.b})"

    c: Color = Color(255, 128, 0)
    print(f"\n__repr__만 정의: {c}")  # → __repr__만 정의: Color(r=255, g=128, b=0)
    print(f"  str(c) = {str(c)}")  # →   str(c) = Color(r=255, g=128, b=0)
    print(f"  repr(c) = {repr(c)}")  # →   repr(c) = Color(r=255, g=128, b=0)

    print(f"\n📌 규칙:")
    print(f"  __repr__: 항상 정의 (디버깅용, eval() 재생성 가능 권장)")
    print(f"  __str__:  사용자 출력이 다를 때만 추가 정의")


def demonstrate_access_control() -> None:
    """접근 제어 관례를 보여준다."""
    print("\n" + "=" * 60)
    print("5. 접근 제어 관례 (_, __)")
    print("=" * 60)

    class BankAccount:
        """은행 계좌 (접근 제어 데모)."""

        def __init__(self, owner: str, balance: float = 0) -> None:
            self.owner: str = owner          # public
            self._balance: float = balance   # protected (관례)
            self.__pin: str = "1234"         # private (이름 맹글링)
            self.__transaction_count: int = 0

        def deposit(self, amount: float) -> None:
            """입금한다."""
            if amount > 0:
                self._balance += amount
                self.__transaction_count += 1

        def get_balance(self) -> float:
            """잔액을 반환한다."""
            return self._balance

        def _internal_check(self) -> None:
            """내부 점검 (관례상 private)."""
            print(f"  내부 점검: 거래 {self.__transaction_count}건")

    acc: BankAccount = BankAccount("Alice", 1000)
    acc.deposit(500)

    # public 접근
    print(f"owner (public): {acc.owner}")  # → owner (public): Alice

    # protected 접근 — 관례적으로만 private (실제 접근 가능)
    print(f"_balance (protected): {acc._balance}")  # → _balance (protected): 1500

    # private — 이름 맹글링 (Name Mangling)
    # acc.__pin → AttributeError
    try:
        _ = acc.__pin  # type: ignore[attr-defined]
    except AttributeError as e:
        print(f"\n__pin 직접 접근 → AttributeError: {e}")

    # 맹글링된 이름으로는 접근 가능 (하지만 비권장)
    print(f"_BankAccount__pin = {acc._BankAccount__pin!r}")  # → _BankAccount__pin = '1234'  # type: ignore[attr-defined]

    # 가이드라인
    print(f"\n📌 접근 제어 가이드:")
    print(f"  public (name):     외부에서 자유롭게 접근")
    print(f"  protected (_name): '내부용' 관례 (접근은 가능)")
    print(f"  private (__name):  이름 맹글링으로 직접 접근 방지")
    print(f"  💡 Python은 강제 은닉 없음 — '우리는 모두 성인'")


if __name__ == "__main__":
    demonstrate_class_definition()
    demonstrate_instance_class_vars()
    demonstrate_methods()
    demonstrate_str_repr()
    demonstrate_access_control()

    print("\n" + "=" * 60)
    print("✅ _200_classes_basics.py 학습 완료!")
    print("=" * 60)
