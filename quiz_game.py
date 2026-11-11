from input_utils import read_int


class QuizGame:
    """게임 전체를 관리하는 클래스."""

    def __init__(self):
        self.running = True

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

    def run(self):
        try:
            while self.running:
                self.show_menu()
                choice = read_int("선택: ", 1, 5)
                if choice == 5:
                    print("👋 게임을 종료합니다.")
                    self.running = False
                else:
                    print("🚧 아직 구현되지 않은 기능입니다.\n")
        except (KeyboardInterrupt, EOFError):
            print("\n\n⚠️ 입력이 중단되었습니다. 안전하게 종료합니다.")
