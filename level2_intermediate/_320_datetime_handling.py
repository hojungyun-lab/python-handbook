"""
_320_datetime_handling.py — 날짜/시간 처리

이 모듈에서 다루는 내용:
  1. datetime, date, time 기본
  2. timedelta (시간 연산)
  3. timezone과 zoneinfo
  4. 포맷팅과 파싱
  5. ISO 8601 표준
  6. 실용적인 날짜 패턴

실행 방법:
    poetry run python 2_intermediate/_320_datetime_handling.py
"""

import calendar
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo


def demonstrate_datetime_basics() -> None:
    """datetime, date, time 기본을 보여준다."""
    print("=" * 60)
    print("1. datetime, date, time 기본")
    print("=" * 60)

    # datetime — 날짜 + 시간
    now: datetime = datetime.now()
    print(f"datetime.now() = {now}")
    print(f"  year={now.year}, month={now.month}, day={now.day}")
    print(f"  hour={now.hour}, minute={now.minute}, second={now.second}")

    # 직접 생성
    dt: datetime = datetime(2025, 12, 25, 14, 30, 0)
    print(f"\ndatetime(2025,12,25,14,30) = {dt}")  # → datetime(2025,12,25,14,30) = 2025-12-25 14:30:00

    # date — 날짜만
    today: date = date.today()
    print(f"\ndate.today() = {today}")

    birthday: date = date(1990, 5, 15)
    print(f"birthday = {birthday}")
    print(f"  weekday = {birthday.weekday()} (0=월~6=일)")
    print(f"  isoweekday = {birthday.isoweekday()} (1=월~7=일)")

    # time — 시간만
    t: time = time(14, 30, 45)
    print(f"\ntime(14,30,45) = {t}")  # → time(14,30,45) = 14:30:45


def demonstrate_timedelta() -> None:
    """timedelta를 보여준다."""
    print("\n" + "=" * 60)
    print("2. timedelta (시간 연산)")
    print("=" * 60)

    now: datetime = datetime.now()

    # 시간 덧셈/뺄셈
    tomorrow: datetime = now + timedelta(days=1)
    next_week: datetime = now + timedelta(weeks=1)
    two_hours_ago: datetime = now - timedelta(hours=2)

    print(f"현재: {now.strftime('%Y-%m-%d %H:%M')}")
    print(f"내일: {tomorrow.strftime('%Y-%m-%d %H:%M')}")
    print(f"다음주: {next_week.strftime('%Y-%m-%d %H:%M')}")
    print(f"2시간 전: {two_hours_ago.strftime('%H:%M')}")

    # 날짜 차이
    d1: date = date(2025, 1, 1)
    d2: date = date(2025, 12, 31)
    diff: timedelta = d2 - d1
    print(f"\n{d1} ~ {d2} 차이:")
    print(f"  {diff.days}일")  # →   364일
    print(f"  총 초: {diff.total_seconds():,.0f}")  # →   총 초: 31,449,600

    # timedelta 연산
    one_day: timedelta = timedelta(days=1)
    one_hour: timedelta = timedelta(hours=1)
    print(f"\ntimedelta 산술:")
    print(f"  1일 + 1시간 = {one_day + one_hour}")  # →   1일 + 1시간 = 1 day, 1:00:00
    print(f"  3일 * 2 = {timedelta(days=3) * 2}")  # →   3일 * 2 = 6 days, 0:00:00
    print(f"  5일 // 2 = {timedelta(days=5) // 2}")  # →   5일 // 2 = 2 days, 12:00:00


def demonstrate_timezone() -> None:
    """timezone과 zoneinfo를 보여준다."""
    print("\n" + "=" * 60)
    print("3. timezone과 zoneinfo")
    print("=" * 60)

    # naive vs aware datetime
    naive: datetime = datetime.now()
    aware: datetime = datetime.now(timezone.utc)
    print(f"naive (tzinfo=None): {naive}")
    print(f"aware (UTC):         {aware}")

    # zoneinfo (Python 3.9+) — IANA 시간대
    kst: ZoneInfo = ZoneInfo("Asia/Seoul")
    est: ZoneInfo = ZoneInfo("America/New_York")
    utc: ZoneInfo = ZoneInfo("UTC")

    now_kst: datetime = datetime.now(kst)
    now_est: datetime = datetime.now(est)
    now_utc: datetime = datetime.now(utc)

    print(f"\n현재 시각 (시간대별):")
    print(f"  서울 (KST): {now_kst.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"  뉴욕 (EST): {now_est.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"  UTC:        {now_utc.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    # 시간대 변환
    meeting_utc: datetime = datetime(2025, 6, 15, 9, 0, tzinfo=utc)
    meeting_kst: datetime = meeting_utc.astimezone(kst)
    meeting_est: datetime = meeting_utc.astimezone(est)

    print(f"\n회의 시간 변환 (UTC 09:00):")
    print(f"  서울: {meeting_kst.strftime('%H:%M %Z')}")
    print(f"  뉴욕: {meeting_est.strftime('%H:%M %Z')}")

    # UTC 오프셋
    print(f"\n오프셋:")
    print(f"  KST: {now_kst.utcoffset()}")
    print(f"  EST: {now_est.utcoffset()}")


def demonstrate_formatting_parsing() -> None:
    """포맷팅과 파싱을 보여준다."""
    print("\n" + "=" * 60)
    print("4. 포맷팅과 파싱")
    print("=" * 60)

    now: datetime = datetime.now()

    # strftime — datetime → 문자열
    formats: list[tuple[str, str]] = [
        ("%Y-%m-%d", "ISO 날짜"),
        ("%Y/%m/%d %H:%M:%S", "일반 형식"),
        ("%Y년 %m월 %d일", "한국어"),
        ("%A, %B %d, %Y", "영어 전체"),
        ("%I:%M %p", "12시간"),
    ]
    print("strftime (포맷팅):")
    for fmt, desc in formats:
        print(f"  {desc:<12}: {now.strftime(fmt)}")

    # strptime — 문자열 → datetime
    date_strings: list[tuple[str, str]] = [
        ("2025-06-15", "%Y-%m-%d"),
        ("15/06/2025 14:30", "%d/%m/%Y %H:%M"),
        ("Jun 15, 2025", "%b %d, %Y"),
    ]
    print(f"\nstrptime (파싱):")
    for s, fmt in date_strings:
        parsed: datetime = datetime.strptime(s, fmt)
        print(f"  {s!r} → {parsed}")

    # 포맷 코드 참조
    print(f"\n📌 주요 포맷 코드:")
    print(f"  %Y: 4자리 연도  %m: 월(01-12)  %d: 일(01-31)")
    print(f"  %H: 시(00-23)   %M: 분(00-59)  %S: 초(00-59)")
    print(f"  %A: 요일 전체   %B: 월 전체    %p: AM/PM")


def demonstrate_iso8601() -> None:
    """ISO 8601 표준을 보여준다."""
    print("\n" + "=" * 60)
    print("5. ISO 8601 표준")
    print("=" * 60)

    # isoformat
    now: datetime = datetime.now(timezone.utc)
    print(f"isoformat: {now.isoformat()}")

    # fromisoformat (Python 3.7+)
    iso_strings: list[str] = [
        "2025-06-15",
        "2025-06-15T14:30:00",
        "2025-06-15T14:30:00+09:00",
        "2025-06-15T05:30:00Z",  # Python 3.11+
    ]
    print(f"\nfromisoformat:")
    for s in iso_strings:
        try:
            dt: datetime | date = datetime.fromisoformat(s)
            print(f"  {s} → {dt}")
        except ValueError as e:
            print(f"  {s} → 에러: {e}")

    # timestamp → datetime
    ts: float = datetime.now().timestamp()
    from_ts: datetime = datetime.fromtimestamp(ts)
    from_ts_utc: datetime = datetime.fromtimestamp(ts, tz=timezone.utc)
    print(f"\ntimestamp: {ts}")
    print(f"  로컬: {from_ts}")
    print(f"  UTC:  {from_ts_utc}")


def demonstrate_practical_patterns() -> None:
    """실용적인 날짜 패턴을 보여준다."""
    print("\n" + "=" * 60)
    print("6. 실용적인 패턴")
    print("=" * 60)

    # 날짜 범위 생성
    def date_range(
        start: date,
        end: date,
        step: timedelta = timedelta(days=1),
    ) -> list[date]:
        """날짜 범위를 생성한다."""
        dates: list[date] = []
        current: date = start
        while current <= end:
            dates.append(current)
            current += step
        return dates

    dates: list[date] = date_range(
        date(2025, 1, 1), date(2025, 1, 7)
    )
    print(f"날짜 범위: {[d.isoformat() for d in dates]}")

    # 월의 마지막 날
    def last_day_of_month(year: int, month: int) -> int:
        """월의 마지막 날을 반환한다."""
        _, last = calendar.monthrange(year, month)
        return last

    print(f"\n월의 마지막 날:")
    for m in [1, 2, 6, 12]:
        print(f"  2025-{m:02d}: {last_day_of_month(2025, m)}일")

    # 나이 계산
    def calculate_age(birthdate: date) -> int:
        """나이를 계산한다."""
        today: date = date.today()
        age: int = today.year - birthdate.year
        if (today.month, today.day) < (birthdate.month, birthdate.day):
            age -= 1
        return age

    print(f"\n나이 계산:")
    print(f"  2000-01-01 → {calculate_age(date(2000, 1, 1))}세")

    # 비즈니스 일수 계산
    def business_days(start: date, end: date) -> int:
        """영업일 수를 계산한다."""
        days: int = 0
        current: date = start
        while current <= end:
            if current.weekday() < 5:  # 월~금
                days += 1
            current += timedelta(days=1)
        return days

    bd: int = business_days(date(2025, 1, 1), date(2025, 1, 31))
    print(f"\n2025년 1월 영업일 수: {bd}일")  # → 2025년 1월 영업일 수: 23일

    print(f"\n📌 날짜/시간 모범 사례:")
    print(f"  ✅ 항상 timezone-aware datetime 사용")
    print(f"  ✅ 저장/전송 시 UTC 기준 → 표시 시 로컬 변환")
    print(f"  ✅ ISO 8601 형식 사용")
    print(f"  ❌ naive datetime으로 시간대 계산")


if __name__ == "__main__":
    demonstrate_datetime_basics()
    demonstrate_timedelta()
    demonstrate_timezone()
    demonstrate_formatting_parsing()
    demonstrate_iso8601()
    demonstrate_practical_patterns()

    print("\n" + "=" * 60)
    print("✅ _320_datetime_handling.py 학습 완료!")
    print("=" * 60)
