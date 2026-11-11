"""공통 입력 처리 함수 모음.

KeyboardInterrupt / EOFError 는 일부러 잡지 않고 위로 전달한다.
(최상위 QuizGame.run 에서 저장 후 안전하게 종료)
"""


def read_text(prompt):
    """빈 입력이 아닌 문자열을 받을 때까지 반복한다. 앞뒤 공백은 제거."""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("⚠️ 빈 입력입니다. 내용을 입력하세요.")


def read_int(prompt, low, high):
    """low~high 범위의 정수를 받을 때까지 반복한다."""
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("⚠️ 빈 입력입니다. 숫자를 입력하세요.")
            continue
        try:
            number = int(raw)
        except ValueError:
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        if not low <= number <= high:
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        return number
