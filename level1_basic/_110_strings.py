"""
020_strings.py — 문자열 (Strings)

이 모듈에서 다루는 내용:
  1. 문자열 생성 (작은따옴표, 큰따옴표, 멀티라인)
  2. f-string 포매팅 (Python 3.6+)
  3. 문자열 인덱싱과 슬라이싱
  4. 주요 문자열 메서드
  5. 문자열 불변성 (Immutability)
  6. Raw String과 이스케이프 시퀀스
  7. 문자열 인코딩 (Unicode, bytes)
  8. 고급 포매팅 기법

실행 방법:
    poetry run python 1_basic/020_strings.py
"""

import re
from string import Template


def demonstrate_string_creation() -> None:
    """문자열 생성 방법을 보여준다."""
    print("=" * 60)
    print("1. 문자열 생성")
    print("=" * 60)

    single: str = '작은따옴표 문자열'
    double: str = "큰따옴표 문자열"
    print(f"single = {single!r}")  # → single = '작은따옴표 문자열'
    print(f"double = {double!r}")  # → double = '큰따옴표 문자열'

    quote1: str = "He said 'hello'"
    quote2: str = 'She said "hi"'
    quote3: str = "It's a \"test\""
    print(f"quote1 = {quote1}")  # → quote1 = He said 'hello'
    print(f"quote2 = {quote2}")  # → quote2 = She said "hi"
    print(f"quote3 = {quote3}")  # → quote3 = It's a "test"

    multiline: str = """첫 번째 줄
두 번째 줄
세 번째 줄"""
    print(f"\nmultiline:\n{multiline}")

    greeting: str = "Hello" + " " + "World"
    repeated: str = "ha" * 3
    print(f"\ngreeting = {greeting!r}")  # → greeting = 'Hello World'
    print(f"repeated = {repeated!r}")  # → repeated = 'hahaha'

    long_string: str = ("이것은 매우 긴 문자열을 "
                         "여러 줄에 걸쳐 "
                         "작성하는 방법입니다.")
    print(f"long_string = {long_string!r}")  # → long_string = '이것은 매우 긴 문자열을 여러 줄에 걸쳐 작성하는 방법입니다.'


def demonstrate_fstring() -> None:
    """f-string 포매팅을 보여준다 (Python 3.6+)."""
    print("\n" + "=" * 60)
    print("2. f-string 포매팅")
    print("=" * 60)

    name: str = "Python"
    version: float = 3.13
    items: list[str] = ["a", "b", "c"]

    print(f"이름: {name}, 버전: {version}")  # → 이름: Python, 버전: 3.13

    x: int = 10
    y: int = 3
    print(f"{x} + {y} = {x + y}")  # → 10 + 3 = 13
    print(f"{x} / {y} = {x / y:.2f}")  # → 10 / 3 = 3.33

    # 디버깅용 = (Python 3.8+)
    print(f"{name = }")  # → name = 'Python'
    print(f"{len(items) = }")  # → len(items) = 3

    # 포맷 지정자
    pi: float = 3.141592653589793
    big_number: int = 1234567890
    percentage: float = 0.856

    print(f"\n포맷 지정자 예시:")
    print(f"  소수점 2자리: {pi:.2f}")  # →   소수점 2자리: 3.14
    print(f"  천 단위 콤마: {big_number:,}")  # →   천 단위 콤마: 1,234,567,890
    print(f"  백분율: {percentage:.1%}")  # →   백분율: 85.6%
    print(f"  과학적 표기: {big_number:.2e}")  # →   과학적 표기: 1.23e+09
    print(f"  2진수: {255:08b}")  # →   2진수: 11111111
    print(f"  16진수: {255:x} / {255:X}")  # →   16진수: ff / FF

    # 정렬
    print(f"\n정렬 예시:")
    print(f"  {'left':<20}|")  # →   left                |
    print(f"  {'center':^20}|")  # →          center       |
    print(f"  {'right':>20}|")  # →                  right|
    print(f"  {'padded':*^20}|")  # →   *******padded*******|


def demonstrate_indexing_slicing() -> None:
    """문자열 인덱싱과 슬라이싱을 보여준다."""
    print("\n" + "=" * 60)
    print("3. 인덱싱과 슬라이싱")
    print("=" * 60)

    text: str = "Hello, Python!"
    print(f"text = {text!r}, len = {len(text)}")  # → text = 'Hello, Python!', len = 14

    print(f"\n인덱싱:")
    print(f"  text[0] = {text[0]!r}")  # →   text[0] = 'H'
    print(f"  text[-1] = {text[-1]!r}")  # →   text[-1] = '!'
    print(f"  text[7] = {text[7]!r}")  # →   text[7] = 'P'

    print(f"\n슬라이싱 [start:stop:step]:")
    print(f"  text[0:5] = {text[0:5]!r}")  # →   text[0:5] = 'Hello'
    print(f"  text[7:] = {text[7:]!r}")  # →   text[7:] = 'Python!'
    print(f"  text[:5] = {text[:5]!r}")  # →   text[:5] = 'Hello'
    print(f"  text[::2] = {text[::2]!r}")  # →   text[::2] = 'Hlo yhn'
    print(f"  text[::-1] = {text[::-1]!r}")  # →   text[::-1] = '!nohtyP ,olleH'


def demonstrate_string_methods() -> None:
    """주요 문자열 메서드를 보여준다."""
    print("\n" + "=" * 60)
    print("4. 주요 문자열 메서드")
    print("=" * 60)

    text: str = "  Hello, Python World!  "

    print("공백 제거:")
    print(f"  strip()  = {text.strip()!r}")  # →   strip()  = 'Hello, Python World!'
    print(f"  lstrip() = {text.lstrip()!r}")  # →   lstrip() = 'Hello, Python World!  '
    print(f"  rstrip() = {text.rstrip()!r}")  # →   rstrip() = '  Hello, Python World!'

    sample: str = "hello WORLD Python"
    print(f"\n대소문자 변환 ({sample!r}):")
    print(f"  upper()      = {sample.upper()!r}")  # →   upper()      = 'HELLO WORLD PYTHON'
    print(f"  lower()      = {sample.lower()!r}")  # →   lower()      = 'hello world python'
    print(f"  title()      = {sample.title()!r}")  # →   title()      = 'Hello World Python'
    print(f"  capitalize() = {sample.capitalize()!r}")  # →   capitalize() = 'Hello world python'
    print(f"  swapcase()   = {sample.swapcase()!r}")  # →   swapcase()   = 'HELLO world pYTHON'

    sentence: str = "Python is great and Python is fun"
    print(f"\n검색 ({sentence!r}):")
    print(f"  find('Python')   = {sentence.find('Python')}")  # →   find('Python')   = 0
    print(f"  rfind('Python')  = {sentence.rfind('Python')}")  # →   rfind('Python')  = 24
    print(f"  count('Python')  = {sentence.count('Python')}")  # →   count('Python')  = 2
    print(f"  startswith('Py') = {sentence.startswith('Py')}")  # →   startswith('Py') = True
    print(f"  endswith('fun')  = {sentence.endswith('fun')}")  # →   endswith('fun')  = True

    csv_line: str = "apple,banana,cherry,date"
    print(f"\n치환과 분할:")
    print(f"  replace: {sentence.replace('Python', 'Java')!r}")  # →   replace: 'Java is great and Java is fun'
    print(f"  split(','):  {csv_line.split(',')}")  # →   split(','):  ['apple', 'banana', 'cherry', 'date']
    print(f"  join: {' | '.join(csv_line.split(','))!r}")  # →   join: 'apple | banana | cherry | date'

    print(f"\n판별 메서드:")
    print(f"  '123'.isdigit()    = {'123'.isdigit()}")  # →   '123'.isdigit()    = True
    print(f"  'abc'.isalpha()    = {'abc'.isalpha()}")  # →   'abc'.isalpha()    = True
    print(f"  'abc123'.isalnum() = {'abc123'.isalnum()}")  # →   'abc123'.isalnum() = True
    print(f"  '   '.isspace()    = {'   '.isspace()}")  # →   '   '.isspace()    = True

    # removeprefix / removesuffix (Python 3.9+)
    filename: str = "test_data.csv"
    print(f"\nremoveprefix/removesuffix (3.9+):")
    print(f"  '{filename}'.removeprefix('test_') = {filename.removeprefix('test_')!r}")  # → 'data.csv'
    print(f"  '{filename}'.removesuffix('.csv') = {filename.removesuffix('.csv')!r}")  # → 'test_data'


def demonstrate_immutability() -> None:
    """문자열의 불변성을 보여준다."""
    print("\n" + "=" * 60)
    print("5. 문자열 불변성 (Immutability)")
    print("=" * 60)

    text: str = "Hello"
    print(f"text = {text!r}, id = {id(text)}")  # → text = 'Hello', id = <주소>

    new_text: str = text + " World"
    print(f"text + ' World' = {new_text!r}, id = {id(new_text)}")  # → text + ' World' = 'Hello World', id = <새 주소>
    print(f"원본 text = {text!r} (변경 안 됨)")  # → 원본 text = 'Hello' (변경 안 됨)

    try:
        text[0] = "h"  # type: ignore[index]
    except TypeError as e:
        print(f"\n⚠️  text[0] = 'h' → TypeError: {e}")  # → ⚠️  text[0] = 'h' → TypeError: 'str' object does not support item assignment

    modified: str = "h" + text[1:]
    print(f"수정 방법: 'h' + text[1:] = {modified!r}")  # → 수정 방법: 'h' + text[1:] = 'hello'


def demonstrate_raw_strings() -> None:
    """Raw string과 이스케이프 시퀀스를 보여준다."""
    print("\n" + "=" * 60)
    print("6. Raw String과 이스케이프 시퀀스")
    print("=" * 60)

    print("주요 이스케이프:")
    print(f"  \\n (줄바꿈), \\t (탭), \\\\ (백슬래시)")

    normal: str = "C:\\new\\test"
    raw: str = r"C:\new\test"
    print(f"\n일반 문자열: {normal}")  # → 일반 문자열: C:\new\test
    print(f"Raw 문자열:  {raw}")  # → Raw 문자열:  C:\new\test

    pattern: str = r"\d+\.\d+"
    print(f"\n정규식 Raw 패턴: {pattern!r}")  # → 정규식 Raw 패턴: '\\d+\\.\\d+'
    print(f"  결과: {re.findall(pattern, 'pi=3.14, e=2.72')}")  # →   결과: ['3.14', '2.72']


def demonstrate_encoding() -> None:
    """문자열 인코딩과 Unicode를 보여준다."""
    print("\n" + "=" * 60)
    print("7. 문자열 인코딩 (Unicode & bytes)")
    print("=" * 60)

    korean: str = "안녕하세요"
    emoji: str = "🐍🎉"
    print(f"korean = {korean!r}, len = {len(korean)}")  # → korean = '안녕하세요', len = 5
    print(f"emoji = {emoji!r}, len = {len(emoji)}")  # → emoji = '🐍🎉', len = 2

    utf8_bytes: bytes = korean.encode("utf-8")
    print(f"\nUTF-8: {utf8_bytes}, len = {len(utf8_bytes)}")  # → UTF-8: b'\xec\x95\x88\xeb\x85\x95\xed\x95\x98\xec\x84\xb8\xec\x9a\x94', len = 15

    decoded: str = utf8_bytes.decode("utf-8")
    print(f"디코딩: {decoded}")  # → 디코딩: 안녕하세요

    print(f"\nUnicode 코드포인트:")
    print(f"  ord('A') = {ord('A')} (U+{ord('A'):04X})")  # →   ord('A') = 65 (U+0041)
    print(f"  ord('가') = {ord('가')} (U+{ord('가'):04X})")  # →   ord('가') = 44032 (U+AC00)
    print(f"  chr(65) = {chr(65)!r}")  # →   chr(65) = 'A'
    print(f"  chr(44032) = {chr(44032)!r}")  # →   chr(44032) = '가'


def demonstrate_advanced_formatting() -> None:
    """고급 포매팅 기법을 보여준다."""
    print("\n" + "=" * 60)
    print("8. 고급 포매팅 기법")
    print("=" * 60)

    # str.format() 방식 (레거시)
    print("str.format():")
    print("  '{} + {} = {}'.format(1, 2, 3) → " + "{} + {} = {}".format(1, 2, 3))  # → '{} + {} = {}'.format(1, 2, 3) → 1 + 2 = 3
    print("  '{name}'.format(name='Py') → " + "{name}".format(name="Py"))  # → '{name}'.format(name='Py') → Py

    # % 포매팅 (C 스타일, 레거시)
    print(f"\n% 포매팅: {'%s는 %d살' % ('Alice', 30)}")  # → % 포매팅: Alice는 30살

    # Template strings (보안이 중요한 경우)
    tmpl: Template = Template("$who likes $what")
    result: str = tmpl.substitute(who="Alice", what="Python")
    print(f"\nTemplate: {result!r}")  # → Template: 'Alice likes Python'


if __name__ == "__main__":
    demonstrate_string_creation()
    demonstrate_fstring()
    demonstrate_indexing_slicing()
    demonstrate_string_methods()
    demonstrate_immutability()
    demonstrate_raw_strings()
    demonstrate_encoding()
    demonstrate_advanced_formatting()

    print("\n" + "=" * 60)
    print("✅ 020_strings.py 학습 완료!")
    print("=" * 60)
