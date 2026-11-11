from default_quizzes import create_default_quizzes
from input_utils import read_int, read_text
from quiz import Quiz


class QuizGame:
    """게임 전체를 관리하는 클래스."""

    def __init__(self):
        self.running = True
        self.quizzes = create_default_quizzes()
        self.best_score = None  # 최고 점수(정답 수)
        self.best_total = 0     # 최고 점수를 낸 판의 문제 수

    def show_menu(self):
        print("=" * 40)
        print("        🎯 나만의 퀴즈 게임 🎯")
        print("=" * 40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 40)

    def play_quiz(self):
        """저장된 퀴즈를 모두 출제하고 결과를 보여준다."""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.\n")
            return
        total = len(self.quizzes)
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)\n")
        correct = 0
        for number, quiz in enumerate(self.quizzes, start=1):
            print("-" * 40)
            quiz.display(number)
            answer = read_int("정답 입력: ", 1, Quiz.CHOICE_COUNT)
            if quiz.is_correct(answer):
                print("✅ 정답입니다!\n")
                correct += 1
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.\n")
        self.show_result(correct, total)

    def add_quiz(self):
        """사용자에게 문제/선택지 4개/정답 번호를 입력받아 퀴즈를 추가한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.\n")
        question = read_text("문제를 입력하세요: ")
        choices = [read_text(f"선택지 {i}: ") for i in range(1, Quiz.CHOICE_COUNT + 1)]
        answer = read_int(f"정답 번호 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT)
        self.quizzes.append(Quiz(question, choices, answer))
        print("\n✅ 퀴즈가 추가되었습니다!\n")

    def list_quizzes(self):
        """등록된 퀴즈의 문제 목록을 보여준다."""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.\n")
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)\n")
        print("-" * 40)
        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"[{i}] {quiz.question}")
        print("-" * 40 + "\n")

    @staticmethod
    def calc_score(correct, total):
        """정답 수를 100점 만점 점수로 환산한다."""
        return round(correct / total * 100) if total else 0

    def update_best_score(self, correct, total):
        """기존 최고 점수보다 높으면 갱신하고 True 를 반환한다."""
        if self.best_score is None or \
                self.calc_score(correct, total) > self.calc_score(self.best_score, self.best_total):
            self.best_score = correct
            self.best_total = total
            return True
        return False

    def show_best_score(self):
        if self.best_score is None:
            print("⚠️ 아직 퀴즈를 푼 기록이 없습니다.\n")
            return
        score = self.calc_score(self.best_score, self.best_total)
        print(f"\n🏆 최고 점수: {score}점 ({self.best_total}문제 중 {self.best_score}문제 정답)\n")

    def show_result(self, correct, total):
        score = self.calc_score(correct, total)
        is_new_best = self.update_best_score(correct, total)
        print("=" * 40)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if is_new_best:
            print("🎉 새로운 최고 점수입니다!")
        print("=" * 40 + "\n")

    def run(self):
        try:
            while self.running:
                self.show_menu()
                choice = read_int("선택: ", 1, 5)
                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.list_quizzes()
                elif choice == 4:
                    self.show_best_score()
                elif choice == 5:
                    print("👋 게임을 종료합니다.")
                    self.running = False
                else:
                    print("🚧 아직 구현되지 않은 기능입니다.\n")
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 입력이 중단되었습니다. 안전하게 종료합니다.")
