"""
_220_error_handling.py — 예외 처리 (Error Handling)

이 모듈에서 다루는 내용:
  1. try / except / else / finally
  2. 내장 예외 계층 구조
  3. 사용자 정의 예외
  4. 예외 체이닝 (from)
  5. ExceptionGroup (Python 3.11+)
  6. 예외 처리 모범 사례

실행 방법:
    poetry run python 1_basic/_220_error_handling.py
"""


def demonstrate_try_except() -> None:
    """try/except/else/finally 구조를 보여준다."""
    print("=" * 60)
    print("1. try / except / else / finally")
    print("=" * 60)

    # 기본 try-except
    try:
        result: float = 10 / 0
    except ZeroDivisionError:
        print("예외 처리됨: ZeroDivisionError")

    # 예외 객체 접근
    try:
        numbers: list[int] = [1, 2, 3]
        _ = numbers[10]
    except IndexError as e:
        print(f"\nIndexError: {e}")  # → IndexError: list index out of range

    # 여러 예외 처리
    def safe_divide(a: str, b: str) -> float | None:
        """안전한 나눗셈을 수행한다."""
        try:
            x: float = float(a)
            y: float = float(b)
            result: float = x / y
        except ValueError:
            print(f"  ValueError: '{a}' 또는 '{b}'는 숫자가 아님")
            return None
        except ZeroDivisionError:
            print(f"  ZeroDivisionError: 0으로 나눌 수 없음")
            return None
        except (TypeError, ArithmeticError) as e:
            print(f"  기타 에러: {e}")
            return None
        else:
            # 예외가 없을 때만 실행
            print(f"  성공: {a}/{b} = {result}")
            return result
        finally:
            # 항상 실행 (예외 여부 무관)
            print(f"  finally 블록: 항상 실행됨")

    print(f"\n여러 예외 처리:")
    safe_divide("10", "3")
    safe_divide("abc", "2")
    safe_divide("10", "0")

    # else vs finally
    print(f"\n📌 else vs finally:")
    print(f"  else:    예외 없을 때만 실행 (성공 시 로직)")
    print(f"  finally: 항상 실행 (정리 작업: 파일 닫기 등)")


def demonstrate_exception_hierarchy() -> None:
    """내장 예외 계층 구조를 보여준다."""
    print("\n" + "=" * 60)
    print("2. 내장 예외 계층 구조")
    print("=" * 60)

    print("BaseException")
    print("├── SystemExit")
    print("├── KeyboardInterrupt")
    print("├── GeneratorExit")
    print("└── Exception")
    print("    ├── ArithmeticError")
    print("    │   ├── ZeroDivisionError")
    print("    │   ├── OverflowError")
    print("    │   └── FloatingPointError")
    print("    ├── LookupError")
    print("    │   ├── IndexError")
    print("    │   └── KeyError")
    print("    ├── ValueError")
    print("    ├── TypeError")
    print("    ├── AttributeError")
    print("    ├── OSError (= IOError)")
    print("    │   ├── FileNotFoundError")
    print("    │   ├── PermissionError")
    print("    │   └── IsADirectoryError")
    print("    ├── RuntimeError")
    print("    │   └── RecursionError")
    print("    └── StopIteration")

    # 부모 클래스로 잡기
    print(f"\n부모 클래스로 잡기:")
    try:
        _ = {}["missing"]
    except LookupError as e:
        # KeyError는 LookupError의 하위 클래스
        print(f"  LookupError 잡힘: {type(e).__name__}: {e}")  # →   LookupError 잡힘: KeyError: 'missing'

    # 주요 예외 데모
    exceptions_demo: list[tuple[str, str]] = [
        ("1/0", "ZeroDivisionError"),
        ("int('abc')", "ValueError"),
        ("'str' + 1", "TypeError"),
        ("{'a': 1}['b']", "KeyError"),
        ("[1,2][5]", "IndexError"),
    ]
    print(f"\n주요 예외 데모:")
    for code, expected in exceptions_demo:
        try:
            eval(code)
        except Exception as e:
            print(f"  {code:<20} → {type(e).__name__}: {e}")


def demonstrate_custom_exceptions() -> None:
    """사용자 정의 예외를 보여준다."""
    print("\n" + "=" * 60)
    print("3. 사용자 정의 예외")
    print("=" * 60)

    # 기본 사용자 정의 예외
    class AppError(Exception):
        """애플리케이션 기본 예외."""

    class ValidationError(AppError):
        """데이터 검증 예외."""

        def __init__(self, field: str, message: str) -> None:
            self.field: str = field
            self.message: str = message
            super().__init__(f"{field}: {message}")

    class NotFoundError(AppError):
        """리소스 미발견 예외."""

        def __init__(self, resource: str, resource_id: int | str) -> None:
            self.resource: str = resource
            self.resource_id: int | str = resource_id
            super().__init__(f"{resource} #{resource_id} not found")

    # 사용
    def validate_age(age: int) -> None:
        """나이를 검증한다."""
        if age < 0:
            raise ValidationError("age", "나이는 음수일 수 없습니다")
        if age > 150:
            raise ValidationError("age", "비현실적인 나이입니다")

    try:
        validate_age(-5)
    except ValidationError as e:
        print(f"ValidationError: {e}")  # → ValidationError: age: 나이는 음수일 수 없습니다
        print(f"  field: {e.field}, message: {e.message}")  # →   field: age, message: 나이는 음수일 수 없습니다

    try:
        raise NotFoundError("User", 42)
    except NotFoundError as e:
        print(f"\nNotFoundError: {e}")  # → NotFoundError: User #42 not found
        print(f"  resource: {e.resource}, id: {e.resource_id}")  # →   resource: User, id: 42

    # 예외 계층 확인
    try:
        raise ValidationError("email", "형식 오류")
    except AppError as e:
        # ValidationError는 AppError의 하위 클래스
        print(f"\nAppError로 잡힘: {type(e).__name__}: {e}")  # → AppError로 잡힘: ValidationError: email: 형식 오류


def demonstrate_exception_chaining() -> None:
    """예외 체이닝을 보여준다."""
    print("\n" + "=" * 60)
    print("4. 예외 체이닝 (from)")
    print("=" * 60)

    class DatabaseError(Exception):
        """데이터베이스 에러."""

    class ServiceError(Exception):
        """서비스 레이어 에러."""

    # raise ... from ... (명시적 체이닝)
    def get_user(user_id: int) -> dict[str, str | int]:
        """사용자를 조회한다."""
        try:
            # 데이터베이스 에러 시뮬레이션
            if user_id < 0:
                raise DatabaseError("DB connection failed")
            return {"id": user_id, "name": "Alice"}
        except DatabaseError as e:
            raise ServiceError(f"User {user_id} 조회 실패") from e

    try:
        get_user(-1)
    except ServiceError as e:
        print(f"ServiceError: {e}")  # → ServiceError: User -1 조회 실패
        print(f"  원인 (from): {e.__cause__}")  # →   원인 (from): DB connection failed

    # raise ... from None (원인 숨기기)
    def parse_config(data: str) -> dict[str, str]:
        """설정을 파싱한다."""
        try:
            key, value = data.split("=")
            return {key.strip(): value.strip()}
        except ValueError:
            raise ValueError(f"잘못된 설정 형식: {data!r}") from None

    try:
        parse_config("invalid_data")
    except ValueError as e:
        print(f"\nfrom None: {e}")  # → from None: 잘못된 설정 형식: 'invalid_data'
        print(f"  __cause__: {e.__cause__}")  # →   __cause__: None


def demonstrate_exception_group() -> None:
    """ExceptionGroup을 보여준다 (Python 3.11+)."""
    print("\n" + "=" * 60)
    print("5. ExceptionGroup (Python 3.11+)")
    print("=" * 60)

    # ExceptionGroup — 여러 예외를 동시에 처리
    def validate_form(data: dict[str, str]) -> None:
        """폼 데이터를 검증한다 (여러 에러를 동시에 수집)."""
        errors: list[Exception] = []

        if not data.get("name"):
            errors.append(ValueError("name은 필수입니다"))
        if not data.get("email"):
            errors.append(ValueError("email은 필수입니다"))
        if data.get("age") and not data["age"].isdigit():
            errors.append(TypeError("age는 숫자여야 합니다"))

        if errors:
            raise ExceptionGroup("폼 검증 실패", errors)

    # except* — ExceptionGroup 처리 (Python 3.11+)
    form_data: dict[str, str] = {"name": "", "email": "", "age": "abc"}

    try:
        validate_form(form_data)
    except* ValueError as eg:
        print(f"ValueError 그룹 ({len(eg.exceptions)}개):")
        for e in eg.exceptions:
            print(f"  - {e}")
    except* TypeError as eg:
        print(f"TypeError 그룹 ({len(eg.exceptions)}개):")
        for e in eg.exceptions:
            print(f"  - {e}")

    # 일반 ExceptionGroup 처리
    try:
        raise ExceptionGroup("여러 에러", [
            OSError("파일 에러"),
            ValueError("값 에러"),
            RuntimeError("실행 에러"),
        ])
    except ExceptionGroup as eg:
        print(f"\nExceptionGroup: {eg}")
        print(f"  예외 수: {len(eg.exceptions)}")
        for e in eg.exceptions:
            print(f"    {type(e).__name__}: {e}")


def demonstrate_best_practices() -> None:
    """예외 처리 모범 사례를 보여준다."""
    print("\n" + "=" * 60)
    print("6. 예외 처리 모범 사례")
    print("=" * 60)

    # ❌ 안티패턴: 너무 넓은 except
    print("❌ 안티패턴들:")
    print("  except:                 # 모든 예외 → 디버깅 어려움")
    print("  except Exception:       # 너무 넓음")
    print("  except: pass            # 에러 무시")

    # ✅ 모범 사례
    print(f"\n✅ 모범 사례:")
    print(f"  1. 구체적인 예외 타입 지정")
    print(f"  2. 예외 메시지에 컨텍스트 포함")
    print(f"  3. 리소스 정리는 finally 또는 with 사용")
    print(f"  4. 사용자 정의 예외 계층 구조 설계")
    print(f"  5. 예외 체이닝으로 원인 추적")

    # EAFP vs LBYL
    print(f"\n📌 EAFP vs LBYL:")

    # LBYL (Look Before You Leap) — 사전 확인
    data: dict[str, int] = {"key": 42}
    if "key" in data:
        value: int = data["key"]
        print(f"  LBYL: {value}")  # →   LBYL: 42

    # EAFP (Easier to Ask Forgiveness) — 시도 후 처리 (Python 권장)
    try:
        value = data["key"]
        print(f"  EAFP: {value}")  # →   EAFP: 42
    except KeyError:
        value = 0

    print(f"\n  💡 Python은 EAFP 스타일 권장!")

    # assert 문 (디버깅/개발용, 프로덕션에서 비활성화 가능)
    def calculate_average(numbers: list[int]) -> float:
        """평균을 계산한다."""
        assert len(numbers) > 0, "빈 리스트의 평균은 계산할 수 없음"
        return sum(numbers) / len(numbers)

    print(f"\nassert 문:")
    print(f"  calculate_average([1,2,3]) = {calculate_average([1, 2, 3])}")  # →   calculate_average([1,2,3]) = 2.0
    try:
        calculate_average([])
    except AssertionError as e:  # noqa: F821
        print(f"  AssertionError: {e}")
    except AssertionError:  # noqa: F821
        print(f"  AssertionError 발생")
    except Exception as e:
        print(f"  {type(e).__name__}: {e}")

    print(f"  ⚠️ assert는 -O 플래그로 비활성화 가능 → 비즈니스 로직에 사용 금지")


if __name__ == "__main__":
    demonstrate_try_except()
    demonstrate_exception_hierarchy()
    demonstrate_custom_exceptions()
    demonstrate_exception_chaining()
    demonstrate_exception_group()
    demonstrate_best_practices()

    print("\n" + "=" * 60)
    print("✅ _220_error_handling.py 학습 완료!")
    print("=" * 60)
