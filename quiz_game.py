import json
from pathlib import Path

from default_quizzes import create_default_quizzes
from input_utils import read_int, read_text
from quiz import Quiz


STATE_FILE = Path(__file__).resolve().parent / "state.json"


class QuizGame:
    """게임 전체를 관리하는 클래스."""

    def __init__(self, state_file=STATE_FILE):
        self.state_file = Path(state_file)
        self.running = True
        self.quizzes = create_default_quizzes()
        self.best_score = None  # 최고 점수(정답 수)
        self.best_total = 0     # 최고 점수를 낸 판의 문제 수
        self.load_message = self.load_state()

    def load_state(self):
        """state.json 을 읽어 상태를 복원한다. 사용자에게 보여줄 안내 문구를 반환한다.

        - 파일이 없으면 기본 퀴즈를 그대로 사용
        - 손상/오류가 있으면 안내 후 기본 데이터로 초기화하고 다시 저장
        """
        if not self.state_file.exists():
            return "🆕 저장된 데이터가 없어 기본 퀴즈로 시작합니다."
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            best_score = data.get("best_score")
            best_total = data.get("best_total", 0)
            if best_score is not None:
                if not (isinstance(best_score, int) and isinstance(best_total, int)
                        and 0 <= best_score <= best_total and best_total > 0):
                    raise ValueError("최고 점수 값이 올바르지 않습니다.")
        except OSError as e:
            return f"⚠️ 파일을 읽을 수 없어 기본 데이터로 시작합니다. ({e})"
        except (ValueError, KeyError, TypeError, AttributeError):
            # json.JSONDecodeError 는 ValueError 의 하위 클래스
            self.quizzes = create_default_quizzes()
            self.best_score, self.best_total = None, 0
            self.save_state()
            return "⚠️ 저장 파일이 손상되어 기본 데이터로 초기화했습니다."
        self.quizzes = quizzes
        self.best_score = best_score
        self.best_total = best_total if best_score is not None else 0
        score_text = "없음" if best_score is None else f"{self.calc_score(best_score, best_total)}점"
        return f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(quizzes)}개, 최고점수 {score_text})"

    def save_state(self):
        """현재 상태를 state.json 에 UTF-8 로 저장한다. 성공 여부를 반환한다."""
        data = {
            "quizzes": [q.to_dict() for q in self.quizzes],
            "best_score": self.best_score,
            "best_total": self.best_total,
        }
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except OSError as e:
            print(f"⚠️ 저장에 실패했습니다: {e}")
            return False

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
        self.save_state()
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
        if is_new_best:
            self.save_state()

    def run(self):
        print(self.load_message + "\n")
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
                    self.save_state()
                    print("👋 게임을 종료합니다.")
                    self.running = False
                else:
                    print("🚧 아직 구현되지 않은 기능입니다.\n")
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 입력이 중단되었습니다. 저장 후 안전하게 종료합니다.")
            self.save_state()
