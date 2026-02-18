"""
_330_regular_expressions.py — 정규 표현식 (Regular Expressions)

이 모듈에서 다루는 내용:
  1. re 모듈 기본 (match, search, findall)
  2. 패턴 문법 (메타문자, 수량자)
  3. 그룹과 캡처
  4. sub (치환)
  5. lookahead / lookbehind
  6. re.compile과 실용 패턴

실행 방법:
    poetry run python 2_intermediate/_330_regular_expressions.py
"""

import re


def demonstrate_basics() -> None:
    """re 모듈 기본을 보여준다."""
    print("=" * 60)
    print("1. re 모듈 기본")
    print("=" * 60)

    text: str = "Python 3.13 is released in 2024"

    # match — 문자열 시작에서 매칭
    m: re.Match[str] | None = re.match(r"Python", text)
    print(f"match('Python'): {m.group() if m else None}")  # → match('Python'): Python

    m2: re.Match[str] | None = re.match(r"3.13", text)
    print(f"match('3.13'): {m2}")  # → match('3.13'): None

    # search — 어디서든 매칭
    s: re.Match[str] | None = re.search(r"3\.13", text)
    print(f"\nsearch('3.13'): {s.group() if s else None}")
    if s:
        print(f"  위치: {s.start()}-{s.end()}")

    # findall — 모든 매칭
    numbers: list[str] = re.findall(r"\d+", text)
    print(f"\nfindall(숫자): {numbers}")  # → findall(숫자): ['3', '13', '2024']

    # finditer — 매치 객체 이터레이터
    print(f"finditer:")
    for m in re.finditer(r"\d+", text):
        print(f"  {m.group()!r} at {m.start()}-{m.end()}")


def demonstrate_pattern_syntax() -> None:
    """패턴 문법을 보여준다."""
    print("\n" + "=" * 60)
    print("2. 패턴 문법")
    print("=" * 60)

    # 메타문자
    print("메타문자:")
    patterns: list[tuple[str, str, str]] = [
        (r".", "a1b2", "임의의 한 문자"),
        (r"\d", "abc123", "숫자"),
        (r"\D", "abc123", "비숫자"),
        (r"\w", "hello world!", "단어 문자 [a-zA-Z0-9_]"),
        (r"\W", "hello world!", "비단어 문자"),
        (r"\s", "hello world", "공백 문자"),
        (r"\S", "hello world", "비공백 문자"),
    ]
    for pat, text, desc in patterns:
        matches: list[str] = re.findall(pat, text)
        print(f"  {pat:<4} ({desc:<20}): {matches}")

    # 수량자
    text: str = "aabbbcccc"
    print(f"\n수량자 ('{text}'):")
    quantifiers: list[tuple[str, str]] = [
        (r"a{2}", "정확히 2개"),
        (r"b{2,3}", "2~3개"),
        (r"c{2,}", "2개 이상"),
        (r"c+", "1개 이상"),
        (r"c*", "0개 이상"),
        (r"c?", "0 또는 1개"),
    ]
    for pat, desc in quantifiers:
        matches = re.findall(pat, text)
        print(f"  {pat:<8} ({desc:<10}): {matches}")

    # 탐욕적 vs 게으른
    html: str = "<b>bold</b> and <i>italic</i>"
    print(f"\n탐욕적 vs 게으른:")
    print(f"  텍스트: {html!r}")
    print(f"  <.*>  (탐욕): {re.findall(r'<.*>', html)}")
    print(f"  <.*?> (게으름): {re.findall(r'<.*?>', html)}")

    # 앵커
    print(f"\n앵커:")
    print(f"  ^Python: {re.findall(r'^Python', 'Python rocks')}")
    print(f"  rocks$:  {re.findall(r'rocks$', 'Python rocks')}")
    print(f"  \\bcat\\b: {re.findall(r'\\bcat\\b', 'cat catch caterpillar')}")


def demonstrate_groups() -> None:
    """그룹과 캡처를 보여준다."""
    print("\n" + "=" * 60)
    print("3. 그룹과 캡처")
    print("=" * 60)

    # 기본 그룹
    text: str = "2025-06-15"
    m: re.Match[str] | None = re.match(
        r"(\d{4})-(\d{2})-(\d{2})", text
    )
    if m:
        print(f"그룹:")
        print(f"  전체: {m.group(0)}")
        print(f"  년:   {m.group(1)}")
        print(f"  월:   {m.group(2)}")
        print(f"  일:   {m.group(3)}")
        print(f"  groups(): {m.groups()}")

    # 이름 있는 그룹
    pattern: str = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
    m2: re.Match[str] | None = re.match(pattern, text)
    if m2:
        print(f"\n이름 있는 그룹:")
        print(f"  year:  {m2.group('year')}")
        print(f"  month: {m2.group('month')}")
        print(f"  groupdict(): {m2.groupdict()}")

    # 비캡처 그룹
    results: list[str] = re.findall(r"(?:https?://)?(\S+)", "https://example.com http://test.org")
    print(f"\n비캡처 그룹 (?:...): {results}")  # → 비캡처 그룹 (?:...): ['example.com', 'test.org']

    # 역참조
    doubles: list[str] = re.findall(r"(\w)\1", "aabbccdefgg")
    print(f"\n역참조 (연속 같은 문자): {doubles}")  # → 역참조 (연속 같은 문자): ['a', 'b', 'c', 'g']

    # or 패턴
    fruits: list[str] = re.findall(
        r"apple|banana|cherry", "I like apple and cherry"
    )
    print(f"OR 패턴: {fruits}")  # → OR 패턴: ['apple', 'cherry']


def demonstrate_sub() -> None:
    """sub (치환)을 보여준다."""
    print("\n" + "=" * 60)
    print("4. sub (치환)")
    print("=" * 60)

    # 기본 치환
    text: str = "Hello World Hello Python"
    result: str = re.sub(r"Hello", "Hi", text)
    print(f"기본: {result!r}")  # → 기본: 'Hi World Hi Python'

    # 횟수 제한
    result2: str = re.sub(r"Hello", "Hi", text, count=1)
    print(f"count=1: {result2!r}")  # → count=1: 'Hi World Hello Python'

    # 역참조 사용
    date_text: str = "2025-06-15 and 2024-12-25"
    result3: str = re.sub(
        r"(\d{4})-(\d{2})-(\d{2})",
        r"\2/\3/\1",  # MM/DD/YYYY
        date_text,
    )
    print(f"\n형식 변환: {result3!r}")  # → 형식 변환: '06/15/2025 and 12/25/2024'

    # 함수로 치환
    def double_number(match: re.Match[str]) -> str:
        return str(int(match.group()) * 2)

    text2: str = "price: 100, qty: 50"
    result4: str = re.sub(r"\d+", double_number, text2)
    print(f"함수 치환: {result4!r}")  # → 함수 치환: 'price: 200, qty: 100'

    # subn — 치환 횟수 반환
    result5, count = re.subn(r"\d+", "X", "a1b2c3d4")
    print(f"\nsubn: {result5!r} ({count}번 치환)")  # → subn: 'aXbXcXdX' (4번 치환)

    # split
    parts: list[str] = re.split(r"[;,\s]+", "one, two;three  four")
    print(f"\nsplit (다중 구분자): {parts}")  # → split (다중 구분자): ['one', 'two', 'three', 'four']


def demonstrate_lookaround() -> None:
    """lookahead/lookbehind를 보여준다."""
    print("\n" + "=" * 60)
    print("5. lookahead / lookbehind")
    print("=" * 60)

    # Positive lookahead (?=...)
    # "뒤에 ...이 오는" 것만 매칭
    text: str = "100px 200em 300px 400%"
    px_values: list[str] = re.findall(r"\d+(?=px)", text)
    print(f"Positive lookahead (px 앞의 숫자): {px_values}")  # → ... ['100', '300']

    # Negative lookahead (?!...)
    non_px: list[str] = re.findall(r"\d+(?!px)\d*\w+", text)
    print(f"Negative lookahead (px 아닌): {non_px}")

    # Positive lookbehind (?<=...)
    prices: str = "$100 €200 $300"
    dollar: list[str] = re.findall(r"(?<=\$)\d+", prices)
    print(f"\nPositive lookbehind ($ 뒤 숫자): {dollar}")  # → ... ['100', '300']

    # Negative lookbehind (?<!...)
    non_dollar: list[str] = re.findall(r"(?<!\$)\d+", prices)
    print(f"Negative lookbehind ($ 아닌 뒤 숫자): {non_dollar}")

    # 비밀번호 검증
    def validate_password(pw: str) -> bool:
        """비밀번호를 검증한다."""
        pattern: str = (
            r"^"
            r"(?=.*[A-Z])"      # 대문자 포함
            r"(?=.*[a-z])"      # 소문자 포함
            r"(?=.*\d)"         # 숫자 포함
            r"(?=.*[!@#$%])"    # 특수문자 포함
            r".{8,}"            # 8자 이상
            r"$"
        )
        return bool(re.match(pattern, pw))

    passwords: list[str] = ["Abc12345!", "abc12345", "Abcdefgh", "Ab1!"]
    print(f"\n비밀번호 검증:")
    for pw in passwords:
        print(f"  {pw:<12} → {'✅' if validate_password(pw) else '❌'}")


def demonstrate_compile_patterns() -> None:
    """re.compile과 실용 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("6. re.compile과 실용 패턴")
    print("=" * 60)

    # re.compile — 패턴 재사용
    email_pattern: re.Pattern[str] = re.compile(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        re.IGNORECASE,
    )

    text: str = "Contact: alice@example.com or bob@test.org"
    emails: list[str] = email_pattern.findall(text)
    print(f"이메일 추출: {emails}")  # → 이메일 추출: ['alice@example.com', 'bob@test.org']

    # 플래그
    print(f"\n플래그:")
    print(f"  re.IGNORECASE (re.I): 대소문자 무시")
    print(f"  re.MULTILINE (re.M):  ^$가 각 줄에 적용")
    print(f"  re.DOTALL (re.S):     .이 \\n도 매칭")
    print(f"  re.VERBOSE (re.X):    주석과 공백 허용")

    # VERBOSE 예시
    phone_pattern: re.Pattern[str] = re.compile(r"""
        (\d{3})     # 지역 번호
        [-.\s]?     # 구분자 (선택)
        (\d{3,4})   # 중간 번호
        [-.\s]?     # 구분자 (선택)
        (\d{4})     # 끝 번호
    """, re.VERBOSE)

    phones: str = "010-1234-5678, 02.987.6543, 031 555 1234"
    matches: list[tuple[str, ...]] = phone_pattern.findall(phones)
    print(f"\n전화번호 추출: {matches}")

    # URL 추출
    url_pattern: re.Pattern[str] = re.compile(
        r"https?://[^\s<>\"']+"
    )
    html_text: str = 'Visit <a href="https://python.org">Python</a> or http://example.com'
    urls: list[str] = url_pattern.findall(html_text)
    # href 뒤에 "가 포함될 수 있으므로 정리
    urls = [u.rstrip('">') for u in urls]
    print(f"URL 추출: {urls}")

    # IP 주소
    ip_pattern: re.Pattern[str] = re.compile(
        r"\b(\d{1,3}\.){3}\d{1,3}\b"
    )
    log: str = "Access from 192.168.1.1 and 10.0.0.255"
    ips: list[str] = [m.group() for m in ip_pattern.finditer(log)]
    print(f"IP 추출: {ips}")  # → IP 추출: ['192.168.1.1', '10.0.0.255']

    print(f"\n📌 정규 표현식 모범 사례:")
    print(f"  ✅ r'' raw string 사용")
    print(f"  ✅ 재사용 → re.compile()")
    print(f"  ✅ 복잡한 패턴 → re.VERBOSE")
    print(f"  ❌ HTML/XML 파싱에 사용 (→ 전용 파서 사용)")
    print(f"  💡 난독화 방지: 주석 달기!")


if __name__ == "__main__":
    demonstrate_basics()
    demonstrate_pattern_syntax()
    demonstrate_groups()
    demonstrate_sub()
    demonstrate_lookaround()
    demonstrate_compile_patterns()

    print("\n" + "=" * 60)
    print("✅ _330_regular_expressions.py 학습 완료!")
    print("=" * 60)
