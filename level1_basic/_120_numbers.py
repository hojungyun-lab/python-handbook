"""
030_numbers.py — 숫자 (Numbers)

이 모듈에서 다루는 내용:
  1. 정수 (int) — 임의 정밀도, 진법 리터럴
  2. 부동소수점 (float) — IEEE 754, 정밀도 한계
  3. 복소수 (complex)
  4. 산술 연산자
  5. math 모듈 주요 함수
  6. decimal.Decimal — 정확한 소수 연산
  7. fractions.Fraction — 분수 연산
  8. 진법 변환과 비트 연산

실행 방법:
    poetry run python 1_basic/030_numbers.py
"""

import math
import sys
from decimal import Decimal, getcontext
from fractions import Fraction


def demonstrate_integers() -> None:
    """정수(int) 타입의 특성을 보여준다."""
    print("=" * 60)
    print("1. 정수 (int) — 임의 정밀도")
    print("=" * 60)

    # Python 정수는 크기 제한이 없음 (임의 정밀도)
    small: int = 42
    big: int = 10**100  # googol
    very_big: int = 2**1000

    print(f"small = {small}")  # → small = 42
    print(f"googol (10^100) = {big}")  # → googol (10^100) = 100000...00000 (101자리)
    print(f"2^1000 자릿수 = {len(str(very_big))}")  # → 2^1000 자릿수 = 302

    # 밑줄 구분자 (Python 3.6+) — 가독성 향상
    population: int = 8_100_000_000
    hex_color: int = 0xFF_AA_CC
    print(f"\npopulation = {population:,}")  # → population = 8,100,000,000
    print(f"hex_color = {hex_color:#010x}")  # → hex_color = 0x00ffaacc

    # 진법 리터럴
    binary: int = 0b1010_1100     # 2진수
    octal: int = 0o755            # 8진수
    hexadecimal: int = 0xDEAD_BEEF  # 16진수

    print(f"\n진법 리터럴:")
    print(f"  0b1010_1100 = {binary} (10진수)")  # →   0b1010_1100 = 172 (10진수)
    print(f"  0o755       = {octal} (10진수)")  # →   0o755       = 493 (10진수)
    print(f"  0xDEAD_BEEF = {hexadecimal} (10진수)")  # →   0xDEAD_BEEF = 3735928559 (10진수)

    # sys.int_info (내부 구현 정보)
    print(f"\nsys.int_info: {sys.int_info}")


def demonstrate_floats() -> None:
    """부동소수점(float) 타입의 특성과 주의점을 보여준다."""
    print("\n" + "=" * 60)
    print("2. 부동소수점 (float) — IEEE 754")
    print("=" * 60)

    pi: float = 3.141592653589793
    avogadro: float = 6.022e23     # 과학적 표기법
    planck: float = 6.626e-34

    print(f"pi = {pi}")  # → pi = 3.141592653589793
    print(f"avogadro = {avogadro:.3e}")  # → avogadro = 6.022e+23
    print(f"planck = {planck:.3e}")  # → planck = 6.626e-34

    # 특수 값
    pos_inf: float = float("inf")
    neg_inf: float = float("-inf")
    nan: float = float("nan")

    print(f"\n특수 값:")
    print(f"  float('inf')  = {pos_inf}")  # →   float('inf')  = inf
    print(f"  float('-inf') = {neg_inf}")  # →   float('-inf') = -inf
    print(f"  float('nan')  = {nan}")  # →   float('nan')  = nan
    print(f"  math.isinf(pos_inf) = {math.isinf(pos_inf)}")  # →   math.isinf(pos_inf) = True
    print(f"  math.isnan(nan)     = {math.isnan(nan)}")  # →   math.isnan(nan)     = True
    print(f"  nan == nan          = {nan == nan}")  # →   nan == nan          = False

    # ⚠️ 부동소수점 정밀도 문제
    print(f"\n⚠️ 정밀도 문제:")
    print(f"  0.1 + 0.2 = {0.1 + 0.2}")  # →   0.1 + 0.2 = 0.30000000000000004
    print(f"  0.1 + 0.2 == 0.3 → {0.1 + 0.2 == 0.3}")  # →   0.1 + 0.2 == 0.3 → False

    # 해결 방법: math.isclose()
    print(f"\n해결 방법:")
    print(f"  math.isclose(0.1+0.2, 0.3) = {math.isclose(0.1 + 0.2, 0.3)}")  # → True
    print(f"  math.isclose(0.1+0.2, 0.3, rel_tol=1e-9) = "
          f"{math.isclose(0.1 + 0.2, 0.3, rel_tol=1e-9)}")  # → True

    # float 정보
    print(f"\nsys.float_info.max = {sys.float_info.max}")
    print(f"sys.float_info.min = {sys.float_info.min}")
    print(f"sys.float_info.epsilon = {sys.float_info.epsilon}")


def demonstrate_complex_numbers() -> None:
    """복소수(complex) 타입을 보여준다."""
    print("\n" + "=" * 60)
    print("3. 복소수 (complex)")
    print("=" * 60)

    z1: complex = 3 + 4j
    z2: complex = complex(1, -2)

    print(f"z1 = {z1}")  # → z1 = (3+4j)
    print(f"z2 = {z2}")  # → z2 = (1-2j)
    print(f"z1.real = {z1.real}, z1.imag = {z1.imag}")  # → z1.real = 3.0, z1.imag = 4.0
    print(f"abs(z1) = {abs(z1)}")  # → abs(z1) = 5.0 (√(3² + 4²))
    print(f"z1.conjugate() = {z1.conjugate()}")  # → z1.conjugate() = (3-4j)
    print(f"z1 + z2 = {z1 + z2}")  # → z1 + z2 = (4+2j)
    print(f"z1 * z2 = {z1 * z2}")  # → z1 * z2 = (11-2j)


def demonstrate_arithmetic() -> None:
    """산술 연산자를 보여준다."""
    print("\n" + "=" * 60)
    print("4. 산술 연산자")
    print("=" * 60)

    a: int = 17
    b: int = 5

    print(f"a = {a}, b = {b}")
    print(f"  a + b  = {a + b:<8} (덧셈)")  # →   a + b  = 22       (덧셈)
    print(f"  a - b  = {a - b:<8} (뺄셈)")  # →   a - b  = 12       (뺄셈)
    print(f"  a * b  = {a * b:<8} (곱셈)")  # →   a * b  = 85       (곱셈)
    print(f"  a / b  = {a / b:<8} (나눗셈 → float)")  # →   a / b  = 3.4      (나눗셈 → float)
    print(f"  a // b = {a // b:<8} (정수 나눗셈, 바닥 나눗셈)")  # →   a // b = 3        (정수 나눗셈, 바닥 나눗셈)
    print(f"  a % b  = {a % b:<8} (나머지)")  # →   a % b  = 2        (나머지)
    print(f"  a ** b = {a ** b:<8} (거듭제곱)")  # →   a ** b = 1419857  (거듭제곱)

    # divmod — 몫과 나머지를 동시에 반환
    quotient: int
    remainder: int
    quotient, remainder = divmod(a, b)
    print(f"\ndivmod({a}, {b}) = ({quotient}, {remainder})")  # → divmod(17, 5) = (3, 2)

    # 음수 나눗셈 주의
    print(f"\n음수 나눗셈 주의:")
    print(f"  -17 // 5  = {-17 // 5}  (바닥 방향)")  # →   -17 // 5  = -4  (바닥 방향)
    print(f"  -17 % 5   = {-17 % 5}   (Python: 항상 양수)")  # →   -17 % 5   = 3   (Python: 항상 양수)
    print(f"  17 // -5  = {17 // -5}")  # →   17 // -5  = -4
    print(f"  17 % -5   = {17 % -5}")  # →   17 % -5   = -3

    # 복합 대입 연산자
    x: int = 10
    print(f"\n복합 대입 (x = {x}):")
    x += 5; print(f"  x += 5  → {x}")  # →   x += 5  → 15
    x -= 3; print(f"  x -= 3  → {x}")  # →   x -= 3  → 12
    x *= 2; print(f"  x *= 2  → {x}")  # →   x *= 2  → 24
    x //= 3; print(f"  x //= 3 → {x}")  # →   x //= 3 → 8
    x **= 2; print(f"  x **= 2 → {x}")  # →   x **= 2 → 64
    x %= 5; print(f"  x %= 5  → {x}")  # →   x %= 5  → 4


def demonstrate_math_module() -> None:
    """math 모듈 주요 함수를 보여준다."""
    print("\n" + "=" * 60)
    print("5. math 모듈")
    print("=" * 60)

    # 상수
    print("상수:")
    print(f"  math.pi  = {math.pi}")  # →   math.pi  = 3.141592653589793
    print(f"  math.e   = {math.e}")  # →   math.e   = 2.718281828459045
    print(f"  math.tau = {math.tau}")  # →   math.tau = 6.283185307179586
    print(f"  math.inf = {math.inf}")  # →   math.inf = inf
    print(f"  math.nan = {math.nan}")  # →   math.nan = nan

    # 반올림/올림/내림
    print(f"\n반올림/올림/내림:")
    print(f"  round(3.7)      = {round(3.7)}")  # →   round(3.7)      = 4
    print(f"  round(2.5)      = {round(2.5)} (은행가 반올림!)")  # →   round(2.5)      = 2 (은행가 반올림!)
    print(f"  round(3.5)      = {round(3.5)} (짝수로 반올림)")  # →   round(3.5)      = 4 (짝수로 반올림)
    print(f"  math.floor(3.7) = {math.floor(3.7)}")  # →   math.floor(3.7) = 3
    print(f"  math.ceil(3.2)  = {math.ceil(3.2)}")  # →   math.ceil(3.2)  = 4
    print(f"  math.trunc(3.7) = {math.trunc(3.7)}")  # →   math.trunc(3.7) = 3
    print(f"  round(3.14159, 2) = {round(3.14159, 2)}")  # →   round(3.14159, 2) = 3.14

    # 주요 함수
    print(f"\n주요 함수:")
    print(f"  math.sqrt(144)     = {math.sqrt(144)}")  # →   math.sqrt(144)     = 12.0
    print(f"  math.pow(2, 10)    = {math.pow(2, 10)}")  # →   math.pow(2, 10)    = 1024.0
    print(f"  math.log(100, 10)  = {math.log(100, 10)}")  # →   math.log(100, 10)  = 2.0
    print(f"  math.log2(1024)    = {math.log2(1024)}")  # →   math.log2(1024)    = 10.0
    print(f"  math.log10(1000)   = {math.log10(1000)}")  # →   math.log10(1000)   = 2.9999...
    print(f"  math.factorial(10) = {math.factorial(10)}")  # →   math.factorial(10) = 3628800
    print(f"  math.gcd(48, 18)   = {math.gcd(48, 18)}")  # →   math.gcd(48, 18)   = 6
    print(f"  math.lcm(12, 18)   = {math.lcm(12, 18)}")  # →   math.lcm(12, 18)   = 36
    print(f"  math.comb(10, 3)   = {math.comb(10, 3)}")  # →   math.comb(10, 3)   = 120
    print(f"  math.perm(10, 3)   = {math.perm(10, 3)}")  # →   math.perm(10, 3)   = 720

    # 삼각함수
    angle: float = math.pi / 4  # 45도
    print(f"\n삼각함수 (45도):")
    print(f"  sin = {math.sin(angle):.4f}")  # →   sin = 0.7071
    print(f"  cos = {math.cos(angle):.4f}")  # →   cos = 0.7071
    print(f"  tan = {math.tan(angle):.4f}")  # →   tan = 1.0000
    print(f"  degrees({angle:.4f}) = {math.degrees(angle)}")  # →   degrees(0.7854) = 45.0
    print(f"  radians(180) = {math.radians(180):.4f}")  # →   radians(180) = 3.1416

    # 합계 (정밀도 높은 합산)
    values: list[float] = [0.1] * 10
    print(f"\n정밀 합계:")
    print(f"  sum([0.1]*10)      = {sum(values)}")  # →   sum([0.1]*10)      = 0.9999999999999999
    print(f"  math.fsum([0.1]*10) = {math.fsum(values)}")  # →   math.fsum([0.1]*10) = 1.0


def demonstrate_decimal() -> None:
    """decimal.Decimal을 이용한 정확한 소수 연산을 보여준다."""
    print("\n" + "=" * 60)
    print("6. decimal.Decimal — 정확한 소수 연산")
    print("=" * 60)

    # float vs Decimal
    print("float vs Decimal:")
    print(f"  float: 0.1 + 0.2 = {0.1 + 0.2}")  # →   float: 0.1 + 0.2 = 0.30000000000000004
    print(f"  Decimal: 0.1 + 0.2 = {Decimal('0.1') + Decimal('0.2')}")  # →   Decimal: 0.1 + 0.2 = 0.3

    # ⚠️ Decimal 생성 시 문자열 사용 권장
    print(f"\n⚠️ Decimal 생성 주의:")
    print(f"  Decimal(0.1)   = {Decimal(0.1)}")  # →   Decimal(0.1)   = 0.10000000000000000555...
    print(f"  Decimal('0.1') = {Decimal('0.1')}")  # →   Decimal('0.1') = 0.1

    # 정밀도 설정
    getcontext().prec = 50
    result: Decimal = Decimal(1) / Decimal(7)
    print(f"\n1/7 (정밀도 50자리):\n  {result}")

    # 금융 계산 예시
    getcontext().prec = 28  # 기본값 복원
    price: Decimal = Decimal("19.99")
    tax_rate: Decimal = Decimal("0.08")
    tax: Decimal = price * tax_rate
    total: Decimal = price + tax

    print(f"\n금융 계산 예시:")
    print(f"  가격: ${price}")  # →   가격: $19.99
    print(f"  세율: {tax_rate}")  # →   세율: 0.08
    print(f"  세금: ${tax.quantize(Decimal('0.01'))}")  # →   세금: $1.60
    print(f"  합계: ${total.quantize(Decimal('0.01'))}")  # →   합계: $21.59


def demonstrate_fractions() -> None:
    """fractions.Fraction을 이용한 분수 연산을 보여준다."""
    print("\n" + "=" * 60)
    print("7. fractions.Fraction — 분수 연산")
    print("=" * 60)

    f1: Fraction = Fraction(1, 3)
    f2: Fraction = Fraction(1, 6)
    f3: Fraction = Fraction("0.125")  # 문자열에서 생성
    f4: Fraction = Fraction(0.5)      # float에서 생성

    print(f"1/3 = {f1}")  # → 1/3 = 1/3
    print(f"1/6 = {f2}")  # → 1/6 = 1/6
    print(f"'0.125' = {f3}")  # → '0.125' = 1/8
    print(f"0.5 = {f4}")  # → 0.5 = 1/2

    print(f"\n분수 연산:")
    print(f"  1/3 + 1/6 = {f1 + f2}")  # →   1/3 + 1/6 = 1/2
    print(f"  1/3 * 1/6 = {f1 * f2}")  # →   1/3 * 1/6 = 1/18
    print(f"  1/3 - 1/6 = {f1 - f2}")  # →   1/3 - 1/6 = 1/6
    print(f"  1/3 / 1/6 = {f1 / f2}")  # →   1/3 / 1/6 = 2

    # float → Fraction 정확한 변환
    print(f"\n0.1의 정확한 분수 표현:")
    print(f"  Fraction(0.1) = {Fraction(0.1)}")  # →   Fraction(0.1) = 3602879701896397/36028797018963968
    print(f"  limit_denominator(10) = {Fraction(0.1).limit_denominator(10)}")  # →   limit_denominator(10) = 1/10


def demonstrate_base_conversion_and_bitwise() -> None:
    """진법 변환과 비트 연산을 보여준다."""
    print("\n" + "=" * 60)
    print("8. 진법 변환과 비트 연산")
    print("=" * 60)

    n: int = 42

    # 진법 변환 함수
    print(f"n = {n}")
    print(f"  bin(n) = {bin(n)}")  # →   bin(n) = 0b101010
    print(f"  oct(n) = {oct(n)}")  # →   oct(n) = 0o52
    print(f"  hex(n) = {hex(n)}")  # →   hex(n) = 0x2a
    print(f"  포맷: {n:08b} (2진), {n:03o} (8진), {n:02x} (16진)")  # →   포맷: 00101010 (2진), 052 (8진), 2a (16진)

    # 문자열 → 정수 (진법 지정)
    print(f"\n문자열 → 정수:")
    print(f"  int('101010', 2) = {int('101010', 2)}")  # →   int('101010', 2) = 42
    print(f"  int('52', 8)     = {int('52', 8)}")  # →   int('52', 8)     = 42
    print(f"  int('2a', 16)    = {int('2a', 16)}")  # →   int('2a', 16)    = 42

    # 비트 연산자
    a: int = 0b1100  # 12
    b: int = 0b1010  # 10

    print(f"\n비트 연산 (a={a:04b}, b={b:04b}):")
    print(f"  a & b  = {a & b:04b} ({a & b:2d})  AND")  # →   a & b  = 1000 ( 8)  AND
    print(f"  a | b  = {a | b:04b} ({a | b:2d})  OR")  # →   a | b  = 1110 (14)  OR
    print(f"  a ^ b  = {a ^ b:04b} ({a ^ b:2d})  XOR")  # →   a ^ b  = 0110 ( 6)  XOR
    print(f"  ~a     = {~a}     NOT (-(a+1))")  # →   ~a     = -13     NOT (-(a+1))
    print(f"  a << 2 = {a << 2:08b} ({a << 2:2d})  좌측 시프트")  # →   a << 2 = 00110000 (48)  좌측 시프트
    print(f"  a >> 1 = {a >> 1:04b} ({a >> 1:2d})  우측 시프트")  # →   a >> 1 = 0110 ( 6)  우측 시프트

    # bit_length, bit_count (Python 3.10+)
    print(f"\n비트 관련 메서드:")
    print(f"  (255).bit_length() = {(255).bit_length()}")  # →   (255).bit_length() = 8
    print(f"  (255).bit_count()  = {(255).bit_count()}")  # →   (255).bit_count()  = 8


if __name__ == "__main__":
    demonstrate_integers()
    demonstrate_floats()
    demonstrate_complex_numbers()
    demonstrate_arithmetic()
    demonstrate_math_module()
    demonstrate_decimal()
    demonstrate_fractions()
    demonstrate_base_conversion_and_bitwise()

    print("\n" + "=" * 60)
    print("✅ 030_numbers.py 학습 완료!")
    print("=" * 60)
