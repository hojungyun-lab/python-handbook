"""
_350_testing_basics.py — 테스트 기초 (Testing Basics)

이 모듈에서 다루는 내용:
  1. assert 문
  2. unittest 기본
  3. pytest 스타일
  4. 테스트 패턴 (AAA, fixture)
  5. parametrize (매개변수화)
  6. mock과 테스트 모범 사례

실행 방법:
    poetry run python 2_intermediate/_350_testing_basics.py
"""

import unittest
from unittest.mock import MagicMock, patch


# ========================================
# 테스트 대상 코드
# ========================================

def add(a: int, b: int) -> int:
    """두 수를 더한다."""
    return a + b

def divide(a: float, b: float) -> float:
    """두 수를 나눈다."""
    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다")
    return a / b

def is_palindrome(text: str) -> bool:
    """회문인지 확인한다."""
    cleaned: str = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]

class Calculator:
    """간단한 계산기."""

    def __init__(self) -> None:
        self.history: list[str] = []

    def add(self, a: float, b: float) -> float:
        result: float = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def multiply(self, a: float, b: float) -> float:
        result: float = a * b
        self.history.append(f"{a} × {b} = {result}")
        return result


# ========================================
# 데모 함수들
# ========================================

def demonstrate_assert() -> None:
    """assert 문을 보여준다."""
    print("=" * 60)
    print("1. assert 문")
    print("=" * 60)

    # 기본 assert
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    print("✅ add() 테스트 통과")

    # 메시지 포함 assert
    result: int = add(10, 20)
    assert result == 30, f"Expected 30, got {result}"
    print("✅ add(10, 20) == 30 통과")

    # 예외 assert
    try:
        divide(10, 0)
        assert False, "ValueError가 발생해야 합니다"
    except ValueError:
        pass
    print("✅ divide(10, 0) → ValueError 통과")

    # 회문 테스트
    assert is_palindrome("racecar")
    assert is_palindrome("A man a plan a canal Panama")
    assert not is_palindrome("hello")
    print("✅ is_palindrome() 테스트 통과")

    print(f"\n📌 assert 주의사항:")
    print(f"  python -O 옵션으로 assert 비활성화 가능")
    print(f"  → 프로덕션 검증에는 if/raise 사용!")


def demonstrate_unittest() -> None:
    """unittest 기본을 보여준다."""
    print("\n" + "=" * 60)
    print("2. unittest 기본")
    print("=" * 60)

    class TestAdd(unittest.TestCase):
        """add 함수 테스트."""

        def test_positive_numbers(self) -> None:
            self.assertEqual(add(2, 3), 5)

        def test_negative_numbers(self) -> None:
            self.assertEqual(add(-1, -2), -3)

        def test_zero(self) -> None:
            self.assertEqual(add(0, 0), 0)

    class TestDivide(unittest.TestCase):
        """divide 함수 테스트."""

        def test_normal_division(self) -> None:
            self.assertAlmostEqual(divide(10, 3), 3.333, places=3)

        def test_divide_by_zero(self) -> None:
            with self.assertRaises(ValueError):
                divide(10, 0)

    # 프로그래밍 방식으로 테스트 실행
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAdd)
    suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(TestDivide)
    )
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # 주요 assert 메서드
    print(f"\n📌 unittest 주요 assert 메서드:")
    methods: list[tuple[str, str]] = [
        ("assertEqual(a, b)", "a == b"),
        ("assertNotEqual(a, b)", "a != b"),
        ("assertTrue(x)", "bool(x) is True"),
        ("assertFalse(x)", "bool(x) is False"),
        ("assertIs(a, b)", "a is b"),
        ("assertIn(a, b)", "a in b"),
        ("assertRaises(exc)", "예외 발생 확인"),
        ("assertAlmostEqual(a, b)", "float 비교 (7자리)"),
    ]
    for method, desc in methods:
        print(f"  {method:<30} {desc}")


def demonstrate_pytest_style() -> None:
    """pytest 스타일 테스트를 보여준다."""
    print("\n" + "=" * 60)
    print("3. pytest 스타일")
    print("=" * 60)

    # pytest는 단순 assert 사용 (unittest 상속 불필요)
    print("pytest 스타일 테스트 (단순 함수):\n")

    def test_add_basic() -> None:
        assert add(1, 2) == 3

    def test_add_negative() -> None:
        assert add(-1, -1) == -2

    def test_palindrome() -> None:
        assert is_palindrome("kayak")
        assert not is_palindrome("python")

    # 수동 실행
    tests: list[tuple[str, callable]] = [
        ("test_add_basic", test_add_basic),
        ("test_add_negative", test_add_negative),
        ("test_palindrome", test_palindrome),
    ]
    for name, test_fn in tests:
        try:
            test_fn()
            print(f"  ✅ {name}")
        except AssertionError as e:
            print(f"  ❌ {name}: {e}")

    # pytest 명령어
    print(f"\n📌 pytest 명령어:")
    print(f"  pytest                    # 전체 실행")
    print(f"  pytest -v                 # 상세 출력")
    print(f"  pytest test_file.py       # 특정 파일")
    print(f"  pytest -k 'test_add'      # 이름으로 필터")
    print(f"  pytest --tb=short         # 짧은 트레이스백")
    print(f"  pytest -x                 # 첫 실패 시 중단")


def demonstrate_test_patterns() -> None:
    """테스트 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("4. 테스트 패턴 (AAA, fixture)")
    print("=" * 60)

    # AAA 패턴: Arrange, Act, Assert
    print("AAA 패턴:")

    def test_calculator_add() -> None:
        # Arrange (준비)
        calc: Calculator = Calculator()

        # Act (실행)
        result: float = calc.add(3, 5)

        # Assert (검증)
        assert result == 8
        assert len(calc.history) == 1
        assert "3 + 5 = 8" in calc.history[0]

    test_calculator_add()
    print("  ✅ Calculator.add — AAA 패턴 통과")

    # setUp/tearDown (unittest)
    class TestCalculator(unittest.TestCase):
        def setUp(self) -> None:
            """각 테스트 전에 실행."""
            self.calc = Calculator()

        def test_add(self) -> None:
            self.assertEqual(self.calc.add(2, 3), 5)

        def test_multiply(self) -> None:
            self.assertEqual(self.calc.multiply(4, 5), 20)

        def test_history(self) -> None:
            self.calc.add(1, 2)
            self.calc.multiply(3, 4)
            self.assertEqual(len(self.calc.history), 2)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculator)
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(suite)
    print(f"\n  unittest setUp: {result.testsRun}개 테스트, "
          f"{'✅ 전체 통과' if result.wasSuccessful() else '❌ 실패'}")

    # pytest fixture (개념 설명)
    print(f"\n📌 pytest fixture:")
    print(f"  @pytest.fixture")
    print(f"  def calculator():")
    print(f"      return Calculator()")
    print(f"")
    print(f"  def test_add(calculator):")
    print(f"      assert calculator.add(1, 2) == 3")


def demonstrate_parametrize() -> None:
    """매개변수화 테스트를 보여준다."""
    print("\n" + "=" * 60)
    print("5. 매개변수화 (parametrize)")
    print("=" * 60)

    # 수동 매개변수화
    test_cases: list[tuple[int, int, int]] = [
        (1, 2, 3),
        (-1, 1, 0),
        (0, 0, 0),
        (100, 200, 300),
        (-5, -10, -15),
    ]

    print("매개변수화 테스트:")
    for a, b, expected in test_cases:
        result: int = add(a, b)
        status: str = "✅" if result == expected else "❌"
        print(f"  {status} add({a}, {b}) = {result} (expected {expected})")

    # pytest.mark.parametrize (개념)
    print(f"\n📌 pytest.mark.parametrize:")
    print(f"  @pytest.mark.parametrize('a, b, expected', [")
    print(f"      (1, 2, 3),")
    print(f"      (-1, 1, 0),")
    print(f"  ])")
    print(f"  def test_add(a, b, expected):")
    print(f"      assert add(a, b) == expected")


def demonstrate_mock() -> None:
    """mock 사용법을 보여준다."""
    print("\n" + "=" * 60)
    print("6. mock과 테스트 모범 사례")
    print("=" * 60)

    # MagicMock 기본
    mock_db: MagicMock = MagicMock()
    mock_db.query.return_value = [{"id": 1, "name": "Alice"}]

    result = mock_db.query("SELECT * FROM users")
    print(f"MagicMock:")
    print(f"  결과: {result}")  # →   결과: [{'id': 1, 'name': 'Alice'}]
    print(f"  호출됨: {mock_db.query.called}")  # →   호출됨: True
    print(f"  호출 횟수: {mock_db.query.call_count}")  # →   호출 횟수: 1

    # patch 데코레이터 (개념 시연)
    class UserService:
        def get_user_count(self) -> int:
            """외부 API를 호출한다 (테스트 시 mock)."""
            raise NotImplementedError("실제 API 호출")

    service: UserService = UserService()
    with patch.object(service, "get_user_count", return_value=42):
        count: int = service.get_user_count()
        print(f"\npatch.object: get_user_count = {count}")  # → patch.object: get_user_count = 42

    # 테스트 모범 사례
    print(f"\n📌 테스트 모범 사례:")
    print(f"  ✅ 테스트 파일: test_*.py 또는 *_test.py")
    print(f"  ✅ 테스트 함수: test_* 접두어")
    print(f"  ✅ AAA 패턴 (Arrange, Act, Assert)")
    print(f"  ✅ 각 테스트는 독립적이어야 함")
    print(f"  ✅ 외부 의존성은 mock 사용")
    print(f"  ✅ 경계값과 에지 케이스 테스트")
    print(f"  ❌ 테스트 간 상태 공유")
    print(f"  ❌ 구현 세부사항 테스트 (API/동작 테스트)")


if __name__ == "__main__":
    demonstrate_assert()
    demonstrate_unittest()
    demonstrate_pytest_style()
    demonstrate_test_patterns()
    demonstrate_parametrize()
    demonstrate_mock()

    print("\n" + "=" * 60)
    print("✅ _350_testing_basics.py 학습 완료!")
    print("=" * 60)
