"""
_340_design_patterns.py — 디자인 패턴 (Design Patterns)

이 모듈에서 다루는 내용:
  1. 생성 패턴 (Factory, Builder, Singleton)
  2. 구조 패턴 (Adapter, Decorator, Proxy)
  3. 행동 패턴 (Observer, Strategy, Command)
  4. Python스러운 패턴 (Mixin, Context Manager, Iterator)

실행 방법:
    poetry run python 3_expert/_340_design_patterns.py
"""

from abc import ABC, abstractmethod
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field


def demonstrate_creational_patterns() -> None:
    """생성 패턴을 보여준다."""
    print("=" * 60)
    print("1. 생성 패턴 (Factory, Builder, Singleton)")
    print("=" * 60)

    # --- Factory Method ---
    class Notification(ABC):
        @abstractmethod
        def send(self, message: str) -> str: ...

    class EmailNotification(Notification):
        def send(self, message: str) -> str:
            return f"📧 Email: {message}"

    class SMSNotification(Notification):
        def send(self, message: str) -> str:
            return f"📱 SMS: {message}"

    class PushNotification(Notification):
        def send(self, message: str) -> str:
            return f"🔔 Push: {message}"

    def notification_factory(channel: str) -> Notification:
        """팩토리 메서드."""
        factories: dict[str, type[Notification]] = {
            "email": EmailNotification,
            "sms": SMSNotification,
            "push": PushNotification,
        }
        if channel not in factories:
            raise ValueError(f"Unknown channel: {channel}")
        return factories[channel]()

    print("Factory Method:")
    for ch in ["email", "sms", "push"]:
        n: Notification = notification_factory(ch)
        print(f"  {n.send('Hello!')}")

    # --- Builder ---
    @dataclass
    class Query:
        table: str = ""
        columns: list[str] = field(default_factory=list)
        conditions: list[str] = field(default_factory=list)
        limit: int | None = None

        def to_sql(self) -> str:
            cols: str = ", ".join(self.columns) or "*"
            sql: str = f"SELECT {cols} FROM {self.table}"
            if self.conditions:
                sql += " WHERE " + " AND ".join(self.conditions)
            if self.limit:
                sql += f" LIMIT {self.limit}"
            return sql

    class QueryBuilder:
        """SQL 쿼리 빌더."""

        def __init__(self) -> None:
            self._query: Query = Query()

        def table(self, name: str) -> "QueryBuilder":
            self._query.table = name
            return self

        def select(self, *columns: str) -> "QueryBuilder":
            self._query.columns.extend(columns)
            return self

        def where(self, condition: str) -> "QueryBuilder":
            self._query.conditions.append(condition)
            return self

        def limit(self, n: int) -> "QueryBuilder":
            self._query.limit = n
            return self

        def build(self) -> Query:
            return self._query

    print(f"\nBuilder:")
    query: Query = (
        QueryBuilder()
        .table("users")
        .select("name", "email")
        .where("age > 18")
        .where("active = true")
        .limit(10)
        .build()
    )
    print(f"  {query.to_sql()}")  # →   SELECT name, email FROM users WHERE age > 18 AND active = true LIMIT 10

    # --- Singleton (Pythonic) ---
    class Singleton:
        _instance: "Singleton | None" = None

        def __new__(cls) -> "Singleton":
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    s1: Singleton = Singleton()
    s2: Singleton = Singleton()
    print(f"\nSingleton: s1 is s2 = {s1 is s2}")  # → Singleton: s1 is s2 = True


def demonstrate_structural_patterns() -> None:
    """구조 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("2. 구조 패턴 (Adapter, Decorator, Proxy)")
    print("=" * 60)

    # --- Adapter ---
    class LegacyPrinter:
        """레거시 프린터 (변경 불가)."""
        def print_old(self, text: str) -> str:
            return f"[LEGACY] {text}"

    class ModernPrinter:
        """현대 프린터 인터페이스."""
        def print_text(self, text: str) -> str:
            return f"[MODERN] {text}"

    class PrinterAdapter:
        """어댑터: LegacyPrinter를 ModernPrinter처럼 사용."""
        def __init__(self, legacy: LegacyPrinter) -> None:
            self._legacy: LegacyPrinter = legacy

        def print_text(self, text: str) -> str:
            return self._legacy.print_old(text)

    adapter: PrinterAdapter = PrinterAdapter(LegacyPrinter())
    modern: ModernPrinter = ModernPrinter()
    print(f"Adapter:")
    print(f"  {adapter.print_text('Hello')}")  # →   [LEGACY] Hello
    print(f"  {modern.print_text('Hello')}")  # →   [MODERN] Hello

    # --- Decorator (구조 패턴) ---
    class TextProcessor:
        """텍스트 처리기."""
        def process(self, text: str) -> str:
            return text

    class UpperCaseDecorator:
        """대문자 변환 데코레이터."""
        def __init__(self, processor: TextProcessor) -> None:
            self._inner: TextProcessor = processor
        def process(self, text: str) -> str:
            return self._inner.process(text).upper()

    class TrimDecorator:
        """공백 제거 데코레이터."""
        def __init__(self, processor: TextProcessor) -> None:
            self._inner: TextProcessor = processor
        def process(self, text: str) -> str:
            return self._inner.process(text).strip()

    print(f"\nDecorator (구조 패턴):")
    proc = UpperCaseDecorator(TrimDecorator(TextProcessor()))
    print(f"  ' hello world ' → {proc.process(' hello world ')!r}")  # →   ' hello world ' → 'HELLO WORLD'

    # --- Proxy ---
    class HeavyResource:
        """생성 비용이 높은 리소스."""
        def __init__(self) -> None:
            self.loaded: bool = True

        def process(self) -> str:
            return "처리 완료"

    class LazyProxy:
        """지연 로딩 프록시."""
        def __init__(self) -> None:
            self._resource: HeavyResource | None = None

        def _load(self) -> HeavyResource:
            if self._resource is None:
                print(f"  [리소스 로딩 중...]")
                self._resource = HeavyResource()
            return self._resource

        def process(self) -> str:
            return self._load().process()

    print(f"\nProxy (지연 로딩):")
    proxy: LazyProxy = LazyProxy()
    print(f"  첫 호출: {proxy.process()}")
    print(f"  두 번째: {proxy.process()}")


def demonstrate_behavioral_patterns() -> None:
    """행동 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("3. 행동 패턴 (Observer, Strategy, Command)")
    print("=" * 60)

    # --- Observer ---
    class EventEmitter:
        """이벤트 발행자."""

        def __init__(self) -> None:
            self._listeners: dict[str, list[Callable]] = {}

        def on(self, event: str, callback: Callable) -> None:
            self._listeners.setdefault(event, []).append(callback)

        def emit(self, event: str, *args: object) -> None:
            for cb in self._listeners.get(event, []):
                cb(*args)

    print("Observer:")
    emitter: EventEmitter = EventEmitter()
    emitter.on("data", lambda d: print(f"  로거: {d}"))
    emitter.on("data", lambda d: print(f"  분석: len={len(str(d))}"))
    emitter.emit("data", "Hello World")

    # --- Strategy ---
    @dataclass
    class ShippingOrder:
        weight: float
        distance: float

    # 전략을 함수로 (Pythonic)
    def express_shipping(order: ShippingOrder) -> float:
        return order.weight * 5.0 + order.distance * 2.0

    def standard_shipping(order: ShippingOrder) -> float:
        return order.weight * 2.0 + order.distance * 0.5

    def free_shipping(order: ShippingOrder) -> float:
        return 0.0

    ShippingStrategy = Callable[[ShippingOrder], float]

    def calculate_cost(
        order: ShippingOrder, strategy: ShippingStrategy
    ) -> float:
        return strategy(order)

    order: ShippingOrder = ShippingOrder(weight=10, distance=100)
    print(f"\nStrategy (함수 기반):")
    strategies: dict[str, ShippingStrategy] = {
        "express": express_shipping,
        "standard": standard_shipping,
        "free": free_shipping,
    }
    for name, strat in strategies.items():
        cost: float = calculate_cost(order, strat)
        print(f"  {name}: ${cost:.0f}")

    # --- Command ---
    @dataclass
    class TextEditor:
        content: str = ""
        _history: list[str] = field(default_factory=list)

        def execute(self, command: "Command") -> None:
            self._history.append(self.content)
            command.execute(self)

        def undo(self) -> None:
            if self._history:
                self.content = self._history.pop()

    class Command(ABC):
        @abstractmethod
        def execute(self, editor: TextEditor) -> None: ...

    class InsertCommand(Command):
        def __init__(self, text: str) -> None:
            self.text: str = text
        def execute(self, editor: TextEditor) -> None:
            editor.content += self.text

    class DeleteCommand(Command):
        def __init__(self, count: int) -> None:
            self.count: int = count
        def execute(self, editor: TextEditor) -> None:
            editor.content = editor.content[:-self.count]

    print(f"\nCommand + Undo:")
    editor: TextEditor = TextEditor()
    editor.execute(InsertCommand("Hello "))
    editor.execute(InsertCommand("World"))
    print(f"  삽입 후: {editor.content!r}")  # →   삽입 후: 'Hello World'
    editor.execute(DeleteCommand(5))
    print(f"  삭제 후: {editor.content!r}")  # →   삭제 후: 'Hello '
    editor.undo()
    print(f"  undo:   {editor.content!r}")  # →   undo:   'Hello World'


def demonstrate_pythonic_patterns() -> None:
    """Python스러운 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("4. Pythonic 패턴")
    print("=" * 60)

    # --- Mixin ---
    class JSONMixin:
        """JSON 직렬화 Mixin."""
        def to_json(self) -> str:
            import json
            return json.dumps(self.__dict__, default=str)

    class LogMixin:
        """로깅 Mixin."""
        def log(self, message: str) -> None:
            print(f"  [{type(self).__name__}] {message}")

    @dataclass
    class User(JSONMixin, LogMixin):
        name: str
        email: str

    user: User = User("Alice", "alice@example.com")
    user.log("생성됨")
    print(f"  JSON: {user.to_json()}")

    # --- Iterator 패턴 (내장) ---
    class Countdown:
        """카운트다운 이터레이터."""

        def __init__(self, start: int) -> None:
            self.current: int = start

        def __iter__(self) -> Iterator[int]:
            return self

        def __next__(self) -> int:
            if self.current <= 0:
                raise StopIteration
            value: int = self.current
            self.current -= 1
            return value

    print(f"\nIterator:")
    print(f"  {list(Countdown(5))}")  # →   [5, 4, 3, 2, 1]

    # --- Null Object ---
    class NullLogger:
        """Null Object: 아무것도 하지 않는 로거."""
        def info(self, msg: str) -> None:
            pass
        def error(self, msg: str) -> None:
            pass

    class ConsoleLogger:
        def info(self, msg: str) -> None:
            print(f"  INFO: {msg}")
        def error(self, msg: str) -> None:
            print(f"  ERROR: {msg}")

    def process_data(logger: ConsoleLogger | NullLogger = NullLogger()) -> None:
        logger.info("처리 시작")

    print(f"\nNull Object:")
    process_data(ConsoleLogger())
    process_data()  # NullLogger — 출력 없음
    print(f"  (NullLogger: 아무 출력 없이 조용히 통과)")

    print(f"\n📌 Python 디자인 패턴 요약:")
    print(f"  Strategy → 함수/callable로 간결하게")
    print(f"  Observer → 리스트 + 콜백")
    print(f"  Singleton → 모듈 자체가 싱글턴")
    print(f"  Iterator → __iter__/__next__")
    print(f"  Context Manager → __enter__/__exit__")
    print(f"  💡 Python에서는 많은 패턴이 언어 기능으로 내장!")


if __name__ == "__main__":
    demonstrate_creational_patterns()
    demonstrate_structural_patterns()
    demonstrate_behavioral_patterns()
    demonstrate_pythonic_patterns()

    print("\n" + "=" * 60)
    print("✅ _340_design_patterns.py 학습 완료!")
    print("=" * 60)
