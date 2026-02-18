"""
_290_type_hints_advanced.py — 고급 타입 힌트

이 모듈에서 다루는 내용:
  1. TypeVar와 Generic
  2. ParamSpec과 Callable
  3. Protocol과 구조적 타이핑
  4. Literal, Final, TypeGuard
  5. type 문과 class Foo[T]: (Python 3.12+)
  6. TypedDict와 고급 패턴

실행 방법:
    poetry run python 2_intermediate/_290_type_hints_advanced.py
"""

from collections.abc import Callable, Sequence
from typing import (
    Any,
    Final,
    Generic,
    Literal,
    ParamSpec,
    Protocol,
    TypeGuard,
    TypeVar,
    TypedDict,
    overload,
    reveal_type,
    runtime_checkable,
)


def demonstrate_typevar_generic() -> None:
    """TypeVar와 Generic을 보여준다."""
    print("=" * 60)
    print("1. TypeVar와 Generic")
    print("=" * 60)

    # TypeVar — 타입 변수
    T = TypeVar("T")

    def first(items: Sequence[T]) -> T:
        """시퀀스의 첫 번째 요소를 반환한다."""
        return items[0]

    print(f"first([1, 2, 3]) = {first([1, 2, 3])}")  # → first([1, 2, 3]) = 1
    print(f"first('abc') = {first('abc')!r}")  # → first('abc') = 'a'

    # 바운드 타입 변수
    Num = TypeVar("Num", bound=int | float)

    def double(x: Num) -> Num:
        return x * 2  # type: ignore[return-value]

    print(f"\nbound TypeVar:")
    print(f"  double(5) = {double(5)}")  # →   double(5) = 10
    print(f"  double(3.14) = {double(3.14)}")  # →   double(3.14) = 6.28

    # Generic 클래스 (pre-3.12 style)
    V = TypeVar("V")

    class Stack(Generic[V]):
        """제네릭 스택."""

        def __init__(self) -> None:
            self._items: list[V] = []

        def push(self, item: V) -> None:
            self._items.append(item)

        def pop(self) -> V:
            return self._items.pop()

        def is_empty(self) -> bool:
            return len(self._items) == 0

        def __repr__(self) -> str:
            return f"Stack({self._items})"

    int_stack: Stack[int] = Stack()
    int_stack.push(1)
    int_stack.push(2)
    print(f"\nStack[int]: {int_stack}")  # → Stack[int]: Stack([1, 2])
    print(f"  pop: {int_stack.pop()}")  # →   pop: 2


def demonstrate_modern_generics() -> None:
    """Python 3.12+ 제네릭 문법을 보여준다."""
    print("\n" + "=" * 60)
    print("2. type 문과 class Foo[T]: (Python 3.12+)")
    print("=" * 60)

    # Python 3.12+ 새 문법: class ClassName[T]:
    class Box[T]:
        """제네릭 박스 (Python 3.12+ 문법)."""

        def __init__(self, value: T) -> None:
            self.value: T = value

        def get(self) -> T:
            return self.value

        def map[U](self, func: Callable[[T], U]) -> "Box[U]":
            """값을 변환한다."""
            return Box(func(self.value))

        def __repr__(self) -> str:
            return f"Box({self.value!r})"

    str_box: Box[str] = Box("hello")
    int_box: Box[int] = Box(42)

    print(f"Box('hello') = {str_box}")  # → Box('hello') = Box('hello')
    print(f"Box(42) = {int_box}")  # → Box(42) = Box(42)
    print(f"Box('hello').map(len) = {str_box.map(len)}")  # → Box('hello').map(len) = Box(5)

    # type 문 (Python 3.12+)
    type Vector = list[float]
    type Matrix = list[Vector]

    v: Vector = [1.0, 2.0, 3.0]
    m: Matrix = [[1.0, 0.0], [0.0, 1.0]]
    print(f"\ntype Vector: {v}")
    print(f"type Matrix: {m}")

    # 제네릭 함수 (Python 3.12+)
    def first_or_default[T](items: Sequence[T], default: T) -> T:
        """첫 번째 요소 또는 기본값을 반환한다."""
        return items[0] if items else default

    print(f"\n제네릭 함수: {first_or_default([1, 2], 0)}")  # → 제네릭 함수: 1
    print(f"기본값: {first_or_default([], 'N/A')}")  # → 기본값: N/A


def demonstrate_paramspec_callable() -> None:
    """ParamSpec과 Callable을 보여준다."""
    print("\n" + "=" * 60)
    print("3. ParamSpec과 Callable")
    print("=" * 60)

    P = ParamSpec("P")
    R = TypeVar("R")

    # ParamSpec — 매개변수 사양 보존
    def logged(func: Callable[P, R]) -> Callable[P, R]:
        """호출을 로깅하는 데코레이터 (타입 보존)."""
        import functools

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            print(f"  → {func.__name__} 호출됨")
            return func(*args, **kwargs)
        return wrapper

    @logged
    def add(x: int, y: int) -> int:
        return x + y

    print(f"ParamSpec:")
    result: int = add(3, 5)
    print(f"  결과: {result}")  # →   결과: 8

    # Callable 타입 힌트
    Transformer = Callable[[str], str]

    def apply_all(text: str, transforms: list[Transformer]) -> str:
        """모든 변환을 순서대로 적용한다."""
        for t in transforms:
            text = t(text)
        return text

    transforms: list[Transformer] = [str.strip, str.lower, str.title]
    print(f"\nCallable 리스트:")
    print(f"  apply_all('  HELLO  ') = {apply_all('  HELLO  ', transforms)!r}")  # →   apply_all('  HELLO  ') = 'Hello'


def demonstrate_protocol() -> None:
    """Protocol과 구조적 타이핑을 보여준다."""
    print("\n" + "=" * 60)
    print("4. Protocol과 구조적 타이핑")
    print("=" * 60)

    @runtime_checkable
    class Renderable(Protocol):
        """렌더링 가능한 객체."""

        def render(self) -> str:
            ...

    class Button:
        def __init__(self, label: str) -> None:
            self.label = label
        def render(self) -> str:
            return f"[{self.label}]"

    class Image:
        def __init__(self, src: str) -> None:
            self.src = src
        def render(self) -> str:
            return f"<img:{self.src}>"

    def display(item: Renderable) -> None:
        print(f"  {item.render()}")

    print("Protocol (구조적 타이핑):")
    display(Button("OK"))
    display(Image("logo.png"))

    # runtime_checkable
    btn: Button = Button("Submit")
    print(f"\nisinstance 체크: {isinstance(btn, Renderable)}")  # → isinstance 체크: True

    # 추가 프로토콜 예시
    class SupportsLen(Protocol):
        def __len__(self) -> int: ...

    def print_length(obj: SupportsLen) -> None:
        print(f"  길이: {len(obj)}")

    print(f"\nSupportsLen:")
    print_length([1, 2, 3])
    print_length("hello")
    print_length({"a": 1})


def demonstrate_literal_final_typeguard() -> None:
    """Literal, Final, TypeGuard를 보여준다."""
    print("\n" + "=" * 60)
    print("5. Literal, Final, TypeGuard")
    print("=" * 60)

    # Literal — 특정 값만 허용
    def set_mode(mode: Literal["r", "w", "a"]) -> str:
        return f"모드: {mode}"

    print(f"Literal:")
    print(f"  set_mode('r') = {set_mode('r')}")  # →   set_mode('r') = 모드: r
    print(f"  set_mode('w') = {set_mode('w')}")  # →   set_mode('w') = 모드: w

    # Final — 재할당 불가 상수
    MAX_SIZE: Final[int] = 100
    API_URL: Final[str] = "https://api.example.com"
    print(f"\nFinal:")
    print(f"  MAX_SIZE = {MAX_SIZE}")  # →   MAX_SIZE = 100
    print(f"  API_URL = {API_URL}")  # →   API_URL = https://api.example.com

    # TypeGuard — 타입 좁히기
    def is_string_list(lst: list[object]) -> TypeGuard[list[str]]:
        """모든 요소가 문자열인지 확인한다."""
        return all(isinstance(item, str) for item in lst)

    data: list[object] = ["hello", "world"]
    if is_string_list(data):
        # 여기서 data는 list[str]로 좁혀짐
        joined: str = ", ".join(data)
        print(f"\nTypeGuard: {joined}")  # → TypeGuard: hello, world


def demonstrate_typeddict() -> None:
    """TypedDict와 고급 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("6. TypedDict와 고급 패턴")
    print("=" * 60)

    # TypedDict — 키별 타입이 다른 딕셔너리
    class UserInfo(TypedDict):
        name: str
        age: int
        email: str

    user: UserInfo = {"name": "Alice", "age": 30, "email": "alice@example.com"}
    print(f"TypedDict: {user}")
    print(f"  name: {user['name']}")  # →   name: Alice

    # total=False — 선택적 키
    class Config(TypedDict, total=False):
        debug: bool
        port: int
        host: str

    cfg: Config = {"port": 8080}  # 일부 키만 필수가 아님
    print(f"\ntotal=False: {cfg}")  # → total=False: {'port': 8080}

    # overload — 함수 오버로딩
    @overload
    def process(data: str) -> list[str]: ...
    @overload
    def process(data: int) -> list[int]: ...

    def process(data: str | int) -> list[str] | list[int]:
        """타입에 따라 다른 처리."""
        if isinstance(data, str):
            return data.split()
        return list(range(data))

    print(f"\noverload:")
    print(f"  process('a b c') = {process('a b c')}")  # →   process('a b c') = ['a', 'b', 'c']
    print(f"  process(5) = {process(5)}")  # →   process(5) = [0, 1, 2, 3, 4]

    # 타입 힌트 모범 사례 요약
    print(f"\n📌 타입 힌트 모범 사례:")
    print(f"  ✅ 내장 타입: list[int], dict[str, int], tuple[int, ...]")
    print(f"  ✅ Union: int | str (PEP 604)")
    print(f"  ✅ Optional: str | None")
    print(f"  ✅ TypeVar: 제네릭 함수/클래스")
    print(f"  ✅ Protocol: 구조적 타이핑")
    print(f"  ❌ from typing import List, Dict, Optional, Union")


if __name__ == "__main__":
    demonstrate_typevar_generic()
    demonstrate_modern_generics()
    demonstrate_paramspec_callable()
    demonstrate_protocol()
    demonstrate_literal_final_typeguard()
    demonstrate_typeddict()

    print("\n" + "=" * 60)
    print("✅ _290_type_hints_advanced.py 학습 완료!")
    print("=" * 60)
