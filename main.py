import sys

from quiz_game import QuizGame


def setup_console():
    """콘솔 인코딩이 이모지를 표현하지 못해도 프로그램이 죽지 않도록 한다."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(errors="replace")
        except (AttributeError, ValueError):
            pass


def main():
    setup_console()
    QuizGame().run()


if __name__ == "__main__":
    main()
