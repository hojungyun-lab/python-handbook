"""
_190_functions.py — 함수 (Functions)

이 모듈에서 다루는 내용:
  1. 함수 정의와 호출
  2. 매개변수: 기본값, *args, **kwargs
  3. 반환값과 다중 반환
  4. 타입 힌트와 독스트링
  5. 스코프 (LEGB 규칙)
  6. 일급 함수 (First-class Functions)
  7. 고급 매개변수 패턴
  8. 재귀 함수

실행 방법:
    poetry run python 1_basic/_190_functions.py
"""

import functools
from collections.abc import Callable


def demonstrate_basic_functions() -> None:
    """함수 정의와 호출을 보여준다."""
    print("=" * 60)
    print("1. 함수 정의와 호출")
    print("=" * 60)

    # 기본 함수
    def greet(name: str) -> str:
        """인사 메시지를 반환한다."""
        return f"안녕하세요, {name}!"

    print(greet("Python"))  # → 안녕하세요, Python!

    # 반환값이 없는 함수 → None 반환
    def print_separator() -> None:
        """구분선을 출력한다."""
        print("-" * 40)

    result: None = print_separator()
    print(f"반환값: {result}")  # → 반환값: None

    # 빈 함수 — pass 또는 ... (Ellipsis)
    def not_implemented_yet() -> None:
        """아직 구현되지 않은 함수."""
        ...  # pass 대신 Ellipsis도 사용 가능

    # 다중 반환
    def divide(a: int, b: int) -> tuple[int, int]:
        """몫과 나머지를 반환한다."""
        return a // b, a % b

    q: int
    r: int
    q, r = divide(17, 5)
    print(f"\n17 ÷ 5 = 몫 {q}, 나머지 {r}")  # → 17 ÷ 5 = 몫 3, 나머지 2


def demonstrate_parameters() -> None:
    """매개변수 종류를 보여준다."""
    print("\n" + "=" * 60)
    print("2. 매개변수: 기본값, *args, **kwargs")
    print("=" * 60)

    # 기본값 매개변수
    def power(base: int, exp: int = 2) -> int:
        """거듭제곱을 계산한다."""
        return base ** exp

    print(f"power(3) = {power(3)}")  # → power(3) = 9
    print(f"power(3, 3) = {power(3, 3)}")  # → power(3, 3) = 27

    # ⚠️ 가변 기본값 주의!
    def bad_append(item: int, lst: list[int] = []) -> list[int]:
        """⚠️ 안티패턴: 가변 기본값."""
        lst.append(item)
        return lst

    print(f"\n⚠️ 가변 기본값 문제:")
    print(f"  bad_append(1) = {bad_append(1)}")  # →   bad_append(1) = [1]
    print(f"  bad_append(2) = {bad_append(2)}")  # →   bad_append(2) = [1, 2]  — 의도치 않은 공유!

    # ✅ 올바른 방법
    def good_append(item: int, lst: list[int] | None = None) -> list[int]:
        """✅ 올바른 패턴: None을 기본값으로 사용."""
        if lst is None:
            lst = []
        lst.append(item)
        return lst

    print(f"\n✅ 올바른 패턴:")
    print(f"  good_append(1) = {good_append(1)}")  # →   good_append(1) = [1]
    print(f"  good_append(2) = {good_append(2)}")  # →   good_append(2) = [2]

    # *args — 가변 위치 인수
    def total(*numbers: int) -> int:
        """모든 인수의 합을 반환한다."""
        return sum(numbers)

    print(f"\n*args: total(1,2,3,4,5) = {total(1, 2, 3, 4, 5)}")  # → *args: total(1,2,3,4,5) = 15

    # **kwargs — 가변 키워드 인수
    def build_profile(**info: str | int) -> dict[str, str | int]:
        """프로필 딕셔너리를 생성한다."""
        return dict(info)

    profile: dict[str, str | int] = build_profile(
        name="Alice", age=30, city="Seoul"
    )
    print(f"**kwargs: {profile}")  # → **kwargs: {'name': 'Alice', 'age': 30, 'city': 'Seoul'}

    # 모든 매개변수 조합
    def full_example(
        a: int,
        b: int = 10,
        *args: int,
        key: str = "default",
        **kwargs: str,
    ) -> None:
        """모든 매개변수 유형을 보여준다."""
        print(f"  a={a}, b={b}, args={args}, key={key!r}, kwargs={kwargs}")

    print(f"\n모든 매개변수 조합:")
    full_example(1)
    full_example(1, 2, 3, 4, key="custom", extra="value")


def demonstrate_type_hints_docstring() -> None:
    """타입 힌트와 독스트링을 보여준다."""
    print("\n" + "=" * 60)
    print("3. 타입 힌트와 독스트링")
    print("=" * 60)

    # Google-style docstring
    def calculate_bmi(
        weight_kg: float,
        height_m: float,
    ) -> dict[str, float | str]:
        """BMI(체질량지수)를 계산한다.

        Args:
            weight_kg: 체중 (킬로그램).
            height_m: 키 (미터).

        Returns:
            BMI 값과 분류를 포함하는 딕셔너리.

        Raises:
            ValueError: 음수 값이 입력된 경우.

        Examples:
            >>> calculate_bmi(70, 1.75)
            {'bmi': 22.86, 'category': '정상'}
        """
        if weight_kg <= 0 or height_m <= 0:
            raise ValueError("양수 값을 입력하세요")

        bmi: float = round(weight_kg / (height_m ** 2), 2)

        if bmi < 18.5:
            category: str = "저체중"
        elif bmi < 25:
            category = "정상"
        elif bmi < 30:
            category = "과체중"
        else:
            category = "비만"

        return {"bmi": bmi, "category": category}

    result: dict[str, float | str] = calculate_bmi(70, 1.75)
    print(f"BMI: {result}")  # → BMI: {'bmi': 22.86, 'category': '정상'}

    # 콜러블 타입 힌트
    from collections.abc import Callable

    def apply_operation(
        x: int,
        y: int,
        operation: Callable[[int, int], int],
    ) -> int:
        """두 수에 연산을 적용한다."""
        return operation(x, y)

    add: Callable[[int, int], int] = lambda a, b: a + b
    result_val: int = apply_operation(3, 5, add)
    print(f"\nCallable 타입 힌트: apply_operation(3, 5, add) = {result_val}")  # → Callable 타입 힌트: apply_operation(3, 5, add) = 8

    # 독스트링 접근
    print(f"\n독스트링 접근: calculate_bmi.__doc__[:50]...")
    print(f"  {calculate_bmi.__doc__[:50] if calculate_bmi.__doc__ else 'None'}...")


def demonstrate_scope() -> None:
    """스코프 (LEGB 규칙)를 보여준다."""
    print("\n" + "=" * 60)
    print("4. 스코프 (LEGB 규칙)")
    print("=" * 60)

    # LEGB: Local → Enclosing → Global → Built-in
    global_var: str = "전역"

    def outer() -> None:
        """외부 함수."""
        enclosing_var: str = "둘러싸는"

        def inner() -> None:
            """내부 함수."""
            local_var: str = "지역"
            print(f"  Local: {local_var}")  # →   Local: 지역
            print(f"  Enclosing: {enclosing_var}")  # →   Enclosing: 둘러싸는
            print(f"  Global: {global_var}")  # →   Global: 전역
            print(f"  Built-in: {len.__name__}")  # →   Built-in: len

        inner()

    print("LEGB 규칙:")
    outer()

    # nonlocal 키워드로 외부 스코프 변수 수정
    counter: int = 0

    def increment() -> None:
        """둘러싸는 스코프의 변수를 수정한다."""
        nonlocal counter
        counter += 1

    increment()
    increment()
    print(f"\nnonlocal 키워드: counter = {counter}")  # → nonlocal 키워드: counter = 2

    # nonlocal 키워드
    def make_counter() -> Callable[[], int]:
        """클로저를 이용한 카운터를 생성한다."""
        count: int = 0

        def increment() -> int:
            nonlocal count
            count += 1
            return count

        return increment

    my_counter: Callable[[], int] = make_counter()
    print(f"\nnonlocal (클로저 카운터):")
    print(f"  {my_counter()}, {my_counter()}, {my_counter()}")  # →   1, 2, 3


def demonstrate_first_class() -> None:
    """일급 함수 특성을 보여준다."""
    print("\n" + "=" * 60)
    print("5. 일급 함수 (First-class Functions)")
    print("=" * 60)

    # 함수를 변수에 할당
    def square(x: int) -> int:
        return x ** 2

    func: Callable[[int], int] = square
    print(f"함수를 변수에 할당: func(5) = {func(5)}")  # → 함수를 변수에 할당: func(5) = 25

    # 함수를 인수로 전달
    numbers: list[int] = [1, 2, 3, 4, 5]
    squared: list[int] = list(map(square, numbers))
    print(f"map(square, {numbers}) = {squared}")  # → map(square, [1, 2, 3, 4, 5]) = [1, 4, 9, 16, 25]

    # 함수를 반환
    def make_multiplier(factor: int) -> Callable[[int], int]:
        """팩터 곱셈 함수를 반환한다."""
        def multiply(x: int) -> int:
            return x * factor
        return multiply

    double: Callable[[int], int] = make_multiplier(2)
    triple: Callable[[int], int] = make_multiplier(3)
    print(f"\n함수 팩토리:")
    print(f"  double(5) = {double(5)}")  # →   double(5) = 10
    print(f"  triple(5) = {triple(5)}")  # →   triple(5) = 15

    # 함수를 리스트에 저장
    from collections.abc import Callable as Cb  # noqa: F811

    operations: list[tuple[str, Callable[[int, int], int]]] = [
        ("add", lambda a, b: a + b),
        ("sub", lambda a, b: a - b),
        ("mul", lambda a, b: a * b),
    ]
    print(f"\n함수 리스트:")
    for name, op in operations:
        print(f"  {name}(10, 3) = {op(10, 3)}")
        # → add(10, 3) = 13
        # → sub(10, 3) = 7
        # → mul(10, 3) = 30

    # 함수 속성
    print(f"\n함수 속성:")
    print(f"  square.__name__ = {square.__name__!r}")  # →   square.__name__ = 'square'
    print(f"  square.__module__ = {square.__module__!r}")  # →   square.__module__ = '__main__'
    print(f"  callable(square) = {callable(square)}")  # →   callable(square) = True


def demonstrate_advanced_params() -> None:
    """고급 매개변수 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("6. 고급 매개변수 패턴")
    print("=" * 60)

    # 위치 전용 매개변수 (/) — Python 3.8+
    def greet(name: str, /, greeting: str = "Hello") -> str:
        """name은 위치 전용, greeting은 위치 또는 키워드."""
        return f"{greeting}, {name}!"

    print("위치 전용 (/) :")
    print(f"  greet('Alice') = {greet('Alice')}")  # →   greet('Alice') = Hello, Alice!
    print(f"  greet('Alice', greeting='Hi') = {greet('Alice', greeting='Hi')}")  # →   greet('Alice', greeting='Hi') = Hi, Alice!
    try:
        greet(name="Alice")  # type: ignore[misc]
    except TypeError as e:
        print(f"  greet(name='Alice') → TypeError: {e}")

    # 키워드 전용 매개변수 (*)
    def connect(host: str, *, port: int = 443, timeout: int = 30) -> str:
        """port, timeout은 키워드 전용."""
        return f"{host}:{port} (timeout={timeout}s)"

    print(f"\n키워드 전용 (*) :")
    print(f"  connect('localhost', port=8080) = {connect('localhost', port=8080)}")  # →   connect('localhost', port=8080) = localhost:8080 (timeout=30s)

    # 언패킹으로 호출
    args: list[int] = [1, 2, 3]
    kwargs: dict[str, str] = {"sep": " + ", "end": " = ?\n"}
    print(f"\n언패킹 호출:")
    print(*args, **kwargs)

    # functools.partial
    def power(base: int, exp: int) -> int:
        return base ** exp

    square = functools.partial(power, exp=2)
    cube = functools.partial(power, exp=3)
    print(f"\nfunctools.partial:")
    print(f"  square(5) = {square(5)}")  # →   square(5) = 25
    print(f"  cube(5)   = {cube(5)}")  # →   cube(5)   = 125


def demonstrate_recursion() -> None:
    """재귀 함수를 보여준다."""
    print("\n" + "=" * 60)
    print("7. 재귀 함수")
    print("=" * 60)

    # 팩토리얼
    def factorial(n: int) -> int:
        """재귀적으로 팩토리얼을 계산한다."""
        if n <= 1:
            return 1
        return n * factorial(n - 1)

    print(f"factorial(5) = {factorial(5)}")  # → factorial(5) = 120
    print(f"factorial(10) = {factorial(10)}")  # → factorial(10) = 3628800

    # 피보나치 (메모이제이션)
    @functools.cache
    def fibonacci(n: int) -> int:
        """캐시된 피보나치 수를 반환한다."""
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    fib_values: list[int] = [fibonacci(i) for i in range(11)]
    print(f"\nfibonacci(0~10) = {fib_values}")  # → fibonacci(0~10) = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

    # 재귀 제한
    import sys
    print(f"\n재귀 제한: {sys.getrecursionlimit()}")  # → 재귀 제한: 1000
    print(f"💡 깊은 재귀는 반복문으로 변환 권장")

    # 꼬리 재귀 최적화 (Python은 미지원, 수동 변환 필요)
    def factorial_iter(n: int) -> int:
        """반복문으로 팩토리얼을 계산한다."""
        result: int = 1
        for i in range(2, n + 1):
            result *= i
        return result

    print(f"\n반복문 factorial(20) = {factorial_iter(20)}")  # → 반복문 factorial(20) = 2432902008176640000


if __name__ == "__main__":
    demonstrate_basic_functions()
    demonstrate_parameters()
    demonstrate_type_hints_docstring()
    demonstrate_scope()
    demonstrate_first_class()
    demonstrate_advanced_params()
    demonstrate_recursion()

    print("\n" + "=" * 60)
    print("✅ _190_functions.py 학습 완료!")
    print("=" * 60)
