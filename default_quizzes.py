"""기본 퀴즈 데이터 (주제: 파이썬 & Git 기초)."""
from quiz import Quiz


def create_default_quizzes():
    return [
        Quiz("Python의 창시자는?", ["Guido van Rossum", "Linus Torvalds", "Bjarne Stroustrup", "James Gosling"], 1),
        Quiz("리스트에 요소를 맨 뒤에 추가하는 메서드는?", ["add()", "append()", "insert()", "push()"], 2),
        Quiz("다음 중 변경 불가능한(immutable) 자료형은?", ["list", "dict", "tuple", "set"], 3),
        Quiz("Git에서 변경 사항을 저장소에 기록하는 명령어는?", ["git push", "git add", "git pull", "git commit"], 4),
        Quiz("파이썬에서 클래스의 생성자 역할을 하는 메서드는?", ["__init__", "__new_obj__", "__start__", "__main__"], 1),
        Quiz("Git에서 원격 저장소를 로컬로 복제하는 명령어는?", ["git init", "git clone", "git fetch", "git merge"], 2),
    ]
