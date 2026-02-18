"""
_270_decorators.py — 데코레이터 (Decorators)

이 모듈에서 다루는 내용:
  1. 함수 데코레이터 기본
  2. functools.wraps
  3. 매개변수 있는 데코레이터
  4. 클래스 데코레이터
  5. 스택 데코레이터
  6. 실용적인 데코레이터 패턴

실행 방법:
    poetry run python 2_intermediate/_270_decorators.py
"""

import functools
import time
from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def demonstrate_basic_decorator() -> None:
    """함수 데코레이터 기본을 보여준다."""
    print("=" * 60)
    print("1. 함수 데코레이터 기본")
    print("=" * 60)

    # 데코레이터 = 함수를 받아 함수를 반환하는 함수
    def simple_decorator(func: Callable[P, R]) -> Callable[P, R]:
        """간단한 데코레이터."""
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            print(f"  [{func.__name__}] 호출 전")
            result: R = func(*args, **kwargs)
            print(f"  [{func.__name__}] 호출 후")
            return result
        return wrapper

    @simple_decorator
    def greet(name: str) -> str:
        """인사 메시지를 반환한다."""
        return f"안녕하세요, {name}!"

    # @simple_decorator는 greet = simple_decorator(greet)과 동일
    result: str = greet("Python")
    print(f"  결과: {result}")  # →   결과: 안녕하세요, Python!

    # 데코레이터 없이 수동 적용
    def say_hello(name: str) -> str:
        return f"Hello, {name}!"

    decorated = simple_decorator(say_hello)
    print(f"\n수동 적용: {decorated('World')}")


def demonstrate_functools_wraps() -> None:
    """functools.wraps의 중요성을 보여준다."""
    print("\n" + "=" * 60)
    print("2. functools.wraps")
    print("=" * 60)

    # wraps 없는 데코레이터
    def bad_decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return func(*args, **kwargs)
        return wrapper

    # wraps 있는 데코레이터
    def good_decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            return func(*args, **kwargs)
        return wrapper

    @bad_decorator
    def func_a() -> None:
        """함수 A 독스트링."""

    @good_decorator
    def func_b() -> None:
        """함수 B 독스트링."""

    print(f"wraps 없이:")
    print(f"  __name__ = {func_a.__name__!r}")  # →   __name__ = 'wrapper'
    print(f"  __doc__  = {func_a.__doc__!r}")  # →   __doc__  = None

    print(f"\nwraps 사용:")
    print(f"  __name__ = {func_b.__name__!r}")  # →   __name__ = 'func_b'
    print(f"  __doc__  = {func_b.__doc__!r}")  # →   __doc__  = '함수 B 독스트링.'

    print(f"\n💡 functools.wraps → 원래 함수의 메타데이터 보존!")


def demonstrate_parameterized_decorator() -> None:
    """매개변수 있는 데코레이터를 보여준다."""
    print("\n" + "=" * 60)
    print("3. 매개변수 있는 데코레이터")
    print("=" * 60)

    # 3중 중첩 패턴
    def repeat(n: int) -> Callable[[Callable[P, R]], Callable[P, R]]:
        """함수를 n번 반복 실행하는 데코레이터."""
        def decorator(func: Callable[P, R]) -> Callable[P, R]:
            @functools.wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                result: R = func(*args, **kwargs)  # 기본값
                for _ in range(n - 1):
                    result = func(*args, **kwargs)
                return result
            return wrapper
        return decorator

    @repeat(3)
    def say_hi() -> str:
        print("  Hi!")
        return "done"

    print("repeat(3):")
    say_hi()

    # 타이머 데코레이터
    def timer(
        label: str = "",
    ) -> Callable[[Callable[P, R]], Callable[P, R]]:
        """실행 시간을 측정하는 데코레이터."""
        def decorator(func: Callable[P, R]) -> Callable[P, R]:
            @functools.wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                start: float = time.perf_counter()
                result: R = func(*args, **kwargs)
                elapsed: float = time.perf_counter() - start
                name: str = label or func.__name__
                print(f"  [{name}] {elapsed:.4f}초")
                return result
            return wrapper
        return decorator

    @timer(label="합계 계산")
    def compute_sum(n: int) -> int:
        return sum(range(n))

    print(f"\ntimer 데코레이터:")
    result: int = compute_sum(1_000_000)
    print(f"  결과: {result:,}")


def demonstrate_class_decorator() -> None:
    """클래스 데코레이터를 보여준다."""
    print("\n" + "=" * 60)
    print("4. 클래스 데코레이터")
    print("=" * 60)

    # 클래스를 데코레이트 — 클래스 자체를 수정/래핑
    def add_repr(cls: type) -> type:
        """__repr__을 자동 추가하는 클래스 데코레이터."""
        def __repr__(self: Any) -> str:
            attrs: str = ", ".join(
                f"{k}={v!r}" for k, v in self.__dict__.items()
            )
            return f"{cls.__name__}({attrs})"
        cls.__repr__ = __repr__  # type: ignore[attr-defined]
        return cls

    @add_repr
    class User:
        def __init__(self, name: str, email: str) -> None:
            self.name: str = name
            self.email: str = email

    user: User = User("Alice", "alice@example.com")
    print(f"클래스 데코레이터: {user}")  # → 클래스 데코레이터: User(name='Alice', email='alice@example.com')

    # 호출 가능 객체 (__call__)로 데코레이터 구현
    class CountCalls:
        """호출 횟수를 추적하는 데코레이터 클래스."""

        def __init__(self, func: Callable[..., Any]) -> None:
            functools.update_wrapper(self, func)
            self.func: Callable[..., Any] = func
            self.call_count: int = 0

        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            self.call_count += 1
            return self.func(*args, **kwargs)

    @CountCalls
    def my_function() -> str:
        return "hello"

    my_function()
    my_function()
    my_function()
    print(f"\nCountCalls: {my_function.call_count}번 호출됨")  # → CountCalls: 3번 호출됨


def demonstrate_stacked_decorators() -> None:
    """스택 데코레이터를 보여준다."""
    print("\n" + "=" * 60)
    print("5. 스택 데코레이터")
    print("=" * 60)

    def bold(func: Callable[P, str]) -> Callable[P, str]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
            return f"<b>{func(*args, **kwargs)}</b>"
        return wrapper

    def italic(func: Callable[P, str]) -> Callable[P, str]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
            return f"<i>{func(*args, **kwargs)}</i>"
        return wrapper

    @bold
    @italic
    def hello(name: str) -> str:
        return f"Hello, {name}"

    # 적용 순서: hello = bold(italic(hello))
    # 실행 순서: bold → italic → hello → italic → bold
    print(f"@bold @italic hello('World'):")
    print(f"  {hello('World')}")  # →   <b><i>Hello, World</i></b>
    print(f"  💡 순서: bold(italic(hello)) → <b><i>Hello, World</i></b>")


def demonstrate_practical_patterns() -> None:
    """실용적인 데코레이터 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("6. 실용적인 데코레이터 패턴")
    print("=" * 60)

    # 1. 캐싱 (memoization)
    @functools.lru_cache(maxsize=128)
    def fibonacci(n: int) -> int:
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    print("lru_cache (피보나치):")
    result: int = fibonacci(30)
    print(f"  fibonacci(30) = {result}")  # →   fibonacci(30) = 832040
    print(f"  cache_info: {fibonacci.cache_info()}")

    # 2. 재시도 (Retry)
    def retry(
        max_attempts: int = 3,
        delay: float = 0.1,
    ) -> Callable[[Callable[P, R]], Callable[P, R]]:
        """실패 시 재시도하는 데코레이터."""
        def decorator(func: Callable[P, R]) -> Callable[P, R]:
            @functools.wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                last_error: Exception | None = None
                for attempt in range(1, max_attempts + 1):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        last_error = e
                        print(f"    시도 {attempt}/{max_attempts} 실패: {e}")
                        if attempt < max_attempts:
                            time.sleep(delay)
                raise last_error  # type: ignore[misc]
            return wrapper
        return decorator

    attempt_count: int = 0

    @retry(max_attempts=3, delay=0.01)
    def flaky_function() -> str:
        """간헐적으로 실패하는 함수."""
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 3:
            raise ConnectionError("연결 실패")
        return "성공!"

    print(f"\nretry 데코레이터:")
    result_str: str = flaky_function()
    print(f"  최종 결과: {result_str}")

    # 3. 타입 체크 (단순 버전)
    def validate_types(func: Callable[P, R]) -> Callable[P, R]:
        """매개변수 타입을 런타임에 검증한다."""
        hints = func.__annotations__
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            import inspect
            sig = inspect.signature(func)
            params = list(sig.parameters.keys())
            for i, arg in enumerate(args):
                if i < len(params):
                    param_name = params[i]
                    if param_name in hints and not isinstance(arg, hints[param_name]):
                        raise TypeError(
                            f"{param_name}: expected {hints[param_name].__name__}, "
                            f"got {type(arg).__name__}"
                        )
            return func(*args, **kwargs)
        return wrapper

    @validate_types
    def add(a: int, b: int) -> int:
        return a + b

    print(f"\n타입 검증 데코레이터:")
    print(f"  add(1, 2) = {add(1, 2)}")  # →   add(1, 2) = 3
    try:
        add("1", 2)  # type: ignore[arg-type]
    except TypeError as e:
        print(f"  add('1', 2) → TypeError: {e}")


if __name__ == "__main__":
    demonstrate_basic_decorator()
    demonstrate_functools_wraps()
    demonstrate_parameterized_decorator()
    demonstrate_class_decorator()
    demonstrate_stacked_decorators()
    demonstrate_practical_patterns()

    print("\n" + "=" * 60)
    print("✅ _270_decorators.py 학습 완료!")
    print("=" * 60)
