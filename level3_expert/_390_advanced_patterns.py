"""
_390_advanced_patterns.py — 고급 패턴 (Advanced Patterns)

이 모듈에서 다루는 내용:
  1. 모나드 패턴 (Maybe/Result)
  2. 파이프라인 패턴
  3. 의존성 주입 (DI)
  4. 불변 데이터 구조
  5. 타입 안전 패턴
  6. Python 최신 기능 (3.10-3.13)

실행 방법:
    poetry run python 3_expert/_390_advanced_patterns.py
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Generic, TypeVar

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E")


def demonstrate_result_pattern() -> None:
    """Result(Maybe) 패턴을 보여준다."""
    print("=" * 60)
    print("1. Result 패턴 (에러 처리)")
    print("=" * 60)

    @dataclass(frozen=True)
    class Ok(Generic[T]):
        value: T
        def is_ok(self) -> bool: return True
        def is_err(self) -> bool: return False

    @dataclass(frozen=True)
    class Err(Generic[E]):
        error: E
        def is_ok(self) -> bool: return False
        def is_err(self) -> bool: return True

    type Result[T, E] = Ok[T] | Err[E]

    def safe_divide(a: float, b: float) -> Result[float, str]:
        if b == 0:
            return Err("0으로 나눌 수 없습니다")
        return Ok(a / b)

    def safe_sqrt(x: float) -> Result[float, str]:
        if x < 0:
            return Err("음수의 제곱근 불가")
        return Ok(x ** 0.5)

    print("Result 패턴:")
    for a, b in [(10, 3), (10, 0)]:
        result = safe_divide(a, b)
        match result:
            case Ok(value):
                print(f"  {a}/{b} = {value:.2f}")
            case Err(error):
                print(f"  {a}/{b} → 에러: {error}")

    for x in [16, -4]:
        result = safe_sqrt(x)
        match result:
            case Ok(v):
                print(f"  sqrt({x}) = {v:.2f}")
            case Err(e):
                print(f"  sqrt({x}) → 에러: {e}")


def demonstrate_pipeline() -> None:
    """파이프라인 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("2. 파이프라인 패턴")
    print("=" * 60)

    class Pipeline[T]:
        """함수형 파이프라인."""
        def __init__(self, value: T) -> None:
            self._value: T = value

        def pipe(self, func: Callable[[T], U]) -> "Pipeline[U]":
            return Pipeline(func(self._value))

        def result(self) -> T:
            return self._value

    # 문자열 변환 파이프라인
    output: str = (
        Pipeline("  Hello, World!  ")
        .pipe(str.strip)
        .pipe(str.lower)
        .pipe(lambda s: s.replace("world", "python"))
        .pipe(str.title)
        .result()
    )
    print(f"파이프라인: {output!r}")  # → 파이프라인: 'Hello, Python!'

    # 데이터 처리 파이프라인
    data: list[int] = list(range(1, 21))
    result: list[int] = (
        Pipeline(data)
        .pipe(lambda xs: [x for x in xs if x % 2 == 0])
        .pipe(lambda xs: [x ** 2 for x in xs])
        .pipe(lambda xs: sorted(xs, reverse=True))
        .pipe(lambda xs: xs[:5])
        .result()
    )
    print(f"데이터 파이프라인: {result}")  # → 데이터 파이프라인: [400, 324, 256, 196, 144]


def demonstrate_dependency_injection() -> None:
    """의존성 주입을 보여준다."""
    print("\n" + "=" * 60)
    print("3. 의존성 주입 (DI)")
    print("=" * 60)

    from typing import Protocol

    class Logger(Protocol):
        def log(self, message: str) -> None: ...

    class Repository(Protocol):
        def find(self, id: int) -> dict | None: ...

    # 구현체들
    class ConsoleLogger:
        def log(self, message: str) -> None:
            print(f"    LOG: {message}")

    class InMemoryRepo:
        def __init__(self) -> None:
            self._data: dict[int, dict] = {
                1: {"name": "Alice"}, 2: {"name": "Bob"},
            }
        def find(self, id: int) -> dict | None:
            return self._data.get(id)

    # DI 사용하는 서비스
    class UserService:
        def __init__(self, repo: Repository, logger: Logger) -> None:
            self._repo = repo
            self._logger = logger

        def get_user(self, user_id: int) -> dict | None:
            self._logger.log(f"사용자 조회: {user_id}")
            return self._repo.find(user_id)

    # 조립
    service = UserService(InMemoryRepo(), ConsoleLogger())
    print("의존성 주입:")
    user = service.get_user(1)
    print(f"  결과: {user}")  # →   결과: {'name': 'Alice'}

    # 테스트용 Mock
    class MockLogger:
        def __init__(self) -> None:
            self.messages: list[str] = []
        def log(self, message: str) -> None:
            self.messages.append(message)

    mock_logger = MockLogger()
    test_service = UserService(InMemoryRepo(), mock_logger)
    test_service.get_user(2)
    print(f"  Mock 로그: {mock_logger.messages}")  # →   Mock 로그: ['사용자 조회: 2']


def demonstrate_immutable_data() -> None:
    """불변 데이터 구조를 보여준다."""
    print("\n" + "=" * 60)
    print("4. 불변 데이터 구조")
    print("=" * 60)

    @dataclass(frozen=True, slots=True)
    class Money:
        amount: int
        currency: str = "KRW"

        def add(self, other: "Money") -> "Money":
            assert self.currency == other.currency
            return Money(self.amount + other.amount, self.currency)

        def multiply(self, factor: int) -> "Money":
            return Money(self.amount * factor, self.currency)

    price = Money(1000, "KRW")
    tax = Money(100, "KRW")
    total = price.add(tax).multiply(3)

    print(f"불변 Money:")
    print(f"  가격: {price}")  # →   가격: Money(amount=1000, currency='KRW')
    print(f"  세금: {tax}")  # →   세금: Money(amount=100, currency='KRW')
    print(f"  총합(×3): {total}")  # →   총합(×3): Money(amount=3300, currency='KRW')

    try:
        price.amount = 2000  # type: ignore
    except AttributeError:
        print(f"  ✅ frozen=True → 수정 불가!")

    # frozenset, tuple
    config: frozenset[str] = frozenset({"debug", "verbose"})
    point: tuple[int, int] = (3, 4)
    print(f"\n  frozenset: {config}")
    print(f"  tuple (불변): {point}")


def demonstrate_type_safe_patterns() -> None:
    """타입 안전 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("5. 타입 안전 패턴")
    print("=" * 60)

    from typing import NewType

    # NewType — 타입 별칭에 안전성 추가
    UserId = NewType("UserId", int)
    OrderId = NewType("OrderId", int)

    def get_user(user_id: UserId) -> str:
        return f"User-{user_id}"

    uid: UserId = UserId(42)
    print(f"NewType: {get_user(uid)}")  # → NewType: User-42

    # Literal + match (타입 안전 상태 머신)
    from typing import Literal

    type OrderStatus = Literal["pending", "confirmed", "shipped", "delivered"]

    @dataclass
    class Order:
        id: int
        status: OrderStatus = "pending"

        def transition(self, new_status: OrderStatus) -> None:
            valid: dict[OrderStatus, list[OrderStatus]] = {
                "pending": ["confirmed"],
                "confirmed": ["shipped"],
                "shipped": ["delivered"],
                "delivered": [],
            }
            if new_status not in valid[self.status]:
                raise ValueError(f"{self.status} → {new_status} 불가!")
            self.status = new_status

    order = Order(1)
    print(f"\n상태 머신:")
    for status in ["confirmed", "shipped", "delivered"]:
        order.transition(status)  # type: ignore[arg-type]
        print(f"  → {order.status}")


def demonstrate_modern_python() -> None:
    """Python 최신 기능을 보여준다."""
    print("\n" + "=" * 60)
    print("6. Python 최신 기능 (3.10-3.13)")
    print("=" * 60)

    # match/case (3.10)
    def process_command(cmd: dict) -> str:
        match cmd:
            case {"action": "greet", "name": str(name)}:
                return f"Hello, {name}!"
            case {"action": "calc", "op": "+", "a": int(a), "b": int(b)}:
                return f"{a} + {b} = {a + b}"
            case {"action": "calc", "op": "*", "a": int(a), "b": int(b)}:
                return f"{a} × {b} = {a * b}"
            case _:
                return "알 수 없는 명령"

    print("match/case (3.10):")
    cmds: list[dict] = [
        {"action": "greet", "name": "Python"},
        {"action": "calc", "op": "+", "a": 3, "b": 5},
        {"action": "unknown"},
    ]
    for cmd in cmds:
        print(f"  {cmd} → {process_command(cmd)}")

    # type 문 (3.12)
    type Vector = list[float]
    type Mapper[T, U] = Callable[[T], U]

    v: Vector = [1.0, 2.0, 3.0]
    print(f"\ntype 문 (3.12): Vector = {v}")

    # ExceptionGroup (3.11)
    print(f"\nExceptionGroup (3.11):")
    try:
        raise ExceptionGroup("여러 에러", [
            ValueError("값 오류"),
            TypeError("타입 오류"),
        ])
    except* ValueError as eg:
        print(f"  ValueError: {eg.exceptions}")
    except* TypeError as eg:
        print(f"  TypeError: {eg.exceptions}")

    # f-string 개선 (3.12) — 따옴표 중첩
    names: list[str] = ["Alice", "Bob"]
    print(f"\nf-string 개선 (3.12):")
    print(f"  {f"Names: {', '.join(names)}"}")

    print(f"\n📌 Python 버전별 핵심 기능:")
    print(f"  3.10: match/case, ParamSpec, TypeGuard")
    print(f"  3.11: ExceptionGroup, TaskGroup, tomllib")
    print(f"  3.12: type 문, class Foo[T]:, f-string 개선")
    print(f"  3.13: free-threading (실험), JIT (실험)")


if __name__ == "__main__":
    demonstrate_result_pattern()
    demonstrate_pipeline()
    demonstrate_dependency_injection()
    demonstrate_immutable_data()
    demonstrate_type_safe_patterns()
    demonstrate_modern_python()

    print("\n" + "=" * 60)
    print("✅ _390_advanced_patterns.py 학습 완료!")
    print("=" * 60)
