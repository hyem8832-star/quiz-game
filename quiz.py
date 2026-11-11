class Quiz:
    """객관식 퀴즈 1개를 표현한다. 정답은 1~4 번호로 관리한다."""

    CHOICE_COUNT = 4

    def __init__(self, question, choices, answer):
        if len(choices) != self.CHOICE_COUNT:
            raise ValueError("선택지는 4개여야 합니다.")
        if not isinstance(answer, int) or isinstance(answer, bool) \
                or not 1 <= answer <= self.CHOICE_COUNT:
            raise ValueError("정답은 1~4 사이의 정수여야 합니다.")
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제가 비어 있습니다.")
        self.question = question
        self.choices = [str(c) for c in choices]
        self.answer = answer

    def display(self, number=None):
        """문제와 선택지를 출력한다."""
        if number is not None:
            print(f"[문제 {number}]")
        print(self.question)
        print()
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")
        print()

    def is_correct(self, user_answer):
        """사용자가 고른 번호가 정답인지 확인한다."""
        return user_answer == self.answer

    def to_dict(self):
        return {"question": self.question, "choices": self.choices, "answer": self.answer}

    @classmethod
    def from_dict(cls, data):
        """dict -> Quiz. 형식이 틀리면 ValueError/KeyError/TypeError 발생."""
        return cls(data["question"], data["choices"], data["answer"])
