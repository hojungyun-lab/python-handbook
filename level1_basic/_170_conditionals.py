"""
170_conditionals.py — 조건문 (Conditionals)

이 모듈에서 다루는 내용:
  1. if / elif / else
  2. 비교 연산자와 논리 연산자
  3. 삼항 연산자 (Conditional Expression)
  4. Truthy / Falsy 값
  5. match-case 구조적 패턴 매칭 (Python 3.10+)
  6. 실용적인 조건문 패턴

실행 방법:
    poetry run python 1_basic/170_conditionals.py
"""


def demonstrate_if_elif_else() -> None:
    """if / elif / else 기본 구조를 보여준다."""
    print("=" * 60)
    print("1. if / elif / else")
    print("=" * 60)

    score: int = 85

    # 기본 if-elif-else
    if score >= 90:
        grade: str = "A"
    elif score >= 80:
        grade = "B"
    elif score >= 70:
        grade = "C"
    elif score >= 60:
        grade = "D"
    else:
        grade = "F"

    print(f"점수 {score} → 등급 {grade}")  # → 점수 85 → 등급 B

    # 단일 조건
    age: int = 20
    if age >= 18:
        print(f"\n나이 {age} → 성인")  # → 나이 20 → 성인

    # 중첩 조건 (비권장 → elif 사용 권장)
    x: int = 15
    if x > 0:
        if x > 10:
            print(f"\nx = {x}: 10보다 큼")  # → x = 15: 10보다 큼
        else:
            print(f"\nx = {x}: 0~10 사이")


def demonstrate_comparison_logical() -> None:
    """비교 연산자와 논리 연산자를 보여준다."""
    print("\n" + "=" * 60)
    print("2. 비교 연산자와 논리 연산자")
    print("=" * 60)

    # 비교 연산자
    a: int = 10
    b: int = 20
    print(f"a = {a}, b = {b}")
    print(f"  a == b → {a == b}")  # →   a == b → False
    print(f"  a != b → {a != b}")  # →   a != b → True
    print(f"  a <  b → {a < b}")  # →   a <  b → True
    print(f"  a <= b → {a <= b}")  # →   a <= b → True
    print(f"  a >  b → {a > b}")  # →   a >  b → False
    print(f"  a >= b → {a >= b}")  # →   a >= b → False

    # 체이닝 비교 (Python 고유 기능!)
    x: int = 15
    print(f"\n체이닝 비교 (x = {x}):")
    print(f"  10 < x < 20 → {10 < x < 20}")  # →   10 < x < 20 → True
    print(f"  10 < x < 12 → {10 < x < 12}")  # →   10 < x < 12 → False
    print(f"  1 <= x <= 100 → {1 <= x <= 100}")  # →   1 <= x <= 100 → True

    # 논리 연산자
    print(f"\n논리 연산자:")
    print(f"  True and False → {True and False}")  # →   True and False → False
    print(f"  True or False  → {True or False}")  # →   True or False  → True
    print(f"  not True       → {not True}")  # →   not True       → False

    # 단축 평가 (Short-circuit evaluation)
    print(f"\n단축 평가:")
    print(f"  0 and 'hello'  → {0 and 'hello'!r}")    # 0 (첫 False)
    print(f"  1 and 'hello'  → {1 and 'hello'!r}")    # 'hello' (마지막 True)
    print(f"  0 or 'default' → {0 or 'default'!r}")   # 'default'
    print(f"  1 or 'default' → {1 or 'default'!r}")   # 1

    # is vs ==
    x_list: list[int] = [1, 2, 3]
    y_list: list[int] = [1, 2, 3]
    print(f"\nis vs ==:")
    print(f"  x == y → {x_list == y_list}  (값 비교)")  # →   x == y → True  (값 비교)
    print(f"  x is y → {x_list is y_list}  (동일 객체?)")  # →   x is y → False  (동일 객체?)
    print(f"  None is None → {None is None}")  # →   None is None → True
    print(f"  💡 None 비교는 항상 is / is not 사용")


def demonstrate_ternary() -> None:
    """삼항 연산자를 보여준다."""
    print("\n" + "=" * 60)
    print("3. 삼항 연산자 (Conditional Expression)")
    print("=" * 60)

    age: int = 20
    status: str = "성인" if age >= 18 else "미성년"
    print(f"age = {age} → {status}")  # → age = 20 → 성인

    # 중첩 삼항 (가독성 주의)
    score: int = 85
    grade: str = "A" if score >= 90 else "B" if score >= 80 else "C"
    print(f"score = {score} → {grade}")  # → score = 85 → B
    print(f"💡 중첩 삼항은 가독성이 떨어지므로 if-elif 권장")

    # 실용 예시
    numbers: list[int] = [1, -2, 3, -4, 5]
    abs_values: list[int] = [x if x >= 0 else -x for x in numbers]
    print(f"\n절대값: {numbers} → {abs_values}")  # → 절대값: [1, -2, 3, -4, 5] → [1, 2, 3, 4, 5]

    # None 기본값 패턴
    user_input: str | None = None
    name: str = user_input if user_input is not None else "Guest"
    print(f"기본값 패턴: {name!r}")  # → 기본값 패턴: 'Guest'

    # or를 이용한 기본값 (Falsy 주의)
    value: str = "" or "default"
    print(f"'' or 'default' = {value!r}")  # → '' or 'default' = 'default'
    print(f"⚠️ or 패턴은 0, '', [] 등 Falsy 값도 대체함")


def demonstrate_truthy_falsy() -> None:
    """Truthy/Falsy 값을 보여준다."""
    print("\n" + "=" * 60)
    print("4. Truthy / Falsy 값")
    print("=" * 60)

    # Falsy 값 목록
    falsy_values: list[tuple[str, object]] = [
        ("None", None),
        ("False", False),
        ("0", 0),
        ("0.0", 0.0),
        ("0j", 0j),
        ("''", ""),
        ("[]", []),
        ("()", ()),
        ("{}", {}),
        ("set()", set()),
        ("range(0)", range(0)),
    ]

    print("Falsy 값 (bool() → False):")
    for label, val in falsy_values:
        print(f"  {label:<12} → bool = {bool(val)}")

    # Truthy 예시
    print(f"\nTruthy 값 (bool() → True):")
    truthy_examples: list[tuple[str, object]] = [
        ("42", 42), ("-1", -1), ("'hello'", "hello"),
        ("[0]", [0]), ("{'a': 1}", {"a": 1}),
    ]
    for label, val in truthy_examples:
        print(f"  {label:<12} → bool = {bool(val)}")

    # 예외: __bool__() 또는 __len__() 이 정의되면 커스텀 가능
    print(f"\n📌 관용적 Pythonic 패턴:")
    items: list[int] = [1, 2, 3]
    print(f"  if items:        (✅ Pythonic)")
    print(f"  if len(items) > 0: (❌ 비Pythonic)")

    name: str = ""
    print(f"  if not name:     (✅ Pythonic)")
    print(f"  if name == '':   (❌ 비Pythonic)")


def demonstrate_match_case() -> None:
    """match-case 구조적 패턴 매칭을 보여준다 (Python 3.10+)."""
    print("\n" + "=" * 60)
    print("5. match-case 패턴 매칭 (Python 3.10+)")
    print("=" * 60)

    # 기본 값 매칭
    def get_http_status(code: int) -> str:
        """HTTP 상태 코드의 설명을 반환한다."""
        match code:
            case 200:
                return "OK"
            case 301:
                return "Moved Permanently"
            case 404:
                return "Not Found"
            case 500:
                return "Internal Server Error"
            case _:
                return f"Unknown ({code})"

    print("값 매칭:")
    for code in [200, 404, 500, 418]:
        print(f"  {code} → {get_http_status(code)}")

    # OR 패턴
    def classify_day(day: str) -> str:
        """요일을 분류한다."""
        match day.lower():
            case "monday" | "tuesday" | "wednesday" | "thursday" | "friday":
                return "평일"
            case "saturday" | "sunday":
                return "주말"
            case _:
                return "알 수 없음"

    print(f"\nOR 패턴:")
    print(f"  monday → {classify_day('monday')}")  # →   monday → 평일
    print(f"  sunday → {classify_day('sunday')}")  # →   sunday → 주말

    # 구조 분해 (Destructuring)
    def process_command(command: tuple[str, ...]) -> str:
        """명령어를 처리한다."""
        match command:
            case ("quit",):
                return "프로그램 종료"
            case ("hello", name):
                return f"안녕하세요, {name}!"
            case ("add", x, y):
                return f"{x} + {y} = {int(x) + int(y)}"
            case ("move", direction, *rest):
                return f"{direction}으로 이동 (추가: {rest})"
            case _:
                return "알 수 없는 명령"

    print(f"\n구조 분해:")
    commands: list[tuple[str, ...]] = [
        ("quit",),
        ("hello", "Python"),
        ("add", "3", "5"),
        ("move", "north", "10", "fast"),
    ]
    for cmd in commands:
        print(f"  {cmd} → {process_command(cmd)}")

    # 클래스 패턴
    def describe_value(value: object) -> str:
        """값의 타입을 설명한다."""
        match value:
            case int(n) if n > 0:
                return f"양의 정수: {n}"
            case int(n) if n < 0:
                return f"음의 정수: {n}"
            case int():
                return "영(0)"
            case str(s) if len(s) > 10:
                return f"긴 문자열: {s[:10]}..."
            case str(s):
                return f"문자열: {s!r}"
            case list() as lst:
                return f"리스트 (길이 {len(lst)})"
            case _:
                return f"기타: {type(value).__name__}"

    print(f"\n클래스 + 가드 패턴:")
    test_values: list[object] = [42, -5, 0, "hi", "a very long string here", [1, 2]]
    for v in test_values:
        print(f"  {v!r} → {describe_value(v)}")

    # 딕셔너리 매핑 패턴
    def process_event(event: dict[str, str | int]) -> str:
        """이벤트를 처리한다."""
        match event:
            case {"type": "click", "x": x, "y": y}:
                return f"클릭 at ({x}, {y})"
            case {"type": "keypress", "key": key}:
                return f"키 입력: {key}"
            case {"type": event_type}:
                return f"기타 이벤트: {event_type}"
            case _:
                return "알 수 없는 이벤트"

    print(f"\n매핑 패턴:")
    events: list[dict[str, str | int]] = [
        {"type": "click", "x": 100, "y": 200},
        {"type": "keypress", "key": "Enter"},
        {"type": "scroll", "direction": "up"},
    ]
    for event in events:
        print(f"  {event} → {process_event(event)}")


def demonstrate_practical_patterns() -> None:
    """실용적인 조건문 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("6. 실용적인 조건문 패턴")
    print("=" * 60)

    # 가드 절 (Guard Clause) — 조기 반환
    def process_data(data: list[int] | None) -> str:
        """데이터를 처리한다 (가드 절 패턴)."""
        if data is None:
            return "데이터 없음"
        if not data:
            return "빈 리스트"
        if len(data) > 100:
            return "데이터 너무 많음"
        return f"처리 완료: {sum(data)}"

    print("가드 절 패턴:")
    print(f"  None → {process_data(None)}")  # →   None → 데이터 없음
    print(f"  [] → {process_data([])}")  # →   [] → 빈 리스트
    print(f"  [1,2,3] → {process_data([1, 2, 3])}")  # →   [1,2,3] → 처리 완료: 6

    # any() / all()
    numbers: list[int] = [2, 4, 6, 8, 10]
    print(f"\nnumbers = {numbers}")
    print(f"  all(x > 0) = {all(x > 0 for x in numbers)}")  # →   all(x > 0) = True
    print(f"  all(x > 5) = {all(x > 5 for x in numbers)}")  # →   all(x > 5) = False
    print(f"  any(x > 5) = {any(x > 5 for x in numbers)}")  # →   any(x > 5) = True
    print(f"  any(x > 20) = {any(x > 20 for x in numbers)}")  # →   any(x > 20) = False

    # 왈러스 연산자 := (Python 3.8+)
    data: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    if (n := len(data)) > 5:
        print(f"\n왈러스 연산자: 길이 {n} > 5 → 처리")  # → 왈러스 연산자: 길이 10 > 5 → 처리

    # 필터링에서 왈러스 활용
    results: list[float] = [
        y for x in range(10)
        if (y := x ** 0.5) > 2
    ]
    print(f"sqrt > 2: {[round(r, 2) for r in results]}")  # → sqrt > 2: [2.24, 2.45, 2.65, 2.83, 3.0]


if __name__ == "__main__":
    demonstrate_if_elif_else()
    demonstrate_comparison_logical()
    demonstrate_ternary()
    demonstrate_truthy_falsy()
    demonstrate_match_case()
    demonstrate_practical_patterns()

    print("\n" + "=" * 60)
    print("✅ 170_conditionals.py 학습 완료!")
    print("=" * 60)
