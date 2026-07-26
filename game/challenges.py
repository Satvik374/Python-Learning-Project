from dataclasses import dataclass
from typing import Callable, Optional, List, Dict, Any, Tuple

Validator = Callable[[str], Tuple[bool, str]]


@dataclass
class Challenge:
    id: str
    title: str
    category: str
    kind: str
    prompt: str
    options: Optional[List[str]] = None
    answer: Optional[str] = None
    validator: Optional[Validator] = None
    func_name: Optional[str] = None
    test_cases: Optional[List[Dict[str, Any]]] = None
    points: int = 10
    hint: Optional[str] = None


def int_answer(expected: int) -> Validator:
    def _v(text: str) -> Tuple[bool, str]:
        try:
            value = int(text.strip())
        except ValueError:
            return False, "Please enter an integer."
        if value == expected:
            return True, "Correct!"
        return False, f"Expected {expected}."
    return _v


def bool_answer(expected: bool) -> Validator:
    def _v(text: str) -> Tuple[bool, str]:
        value = text.strip().lower()
        if value in ("true", "t", "1", "yes", "y"):
            actual = True
        elif value in ("false", "f", "0", "no", "n"):
            actual = False
        else:
            return False, "Please answer True or False."
        if actual == expected:
            return True, "Correct!"
        return False, f"Expected {expected}."
    return _v


def get_challenges() -> List[Challenge]:
    return [
        Challenge(
            id="B1",
            title="Type of 3.14",
            category="Basics",
            kind="mcq",
            prompt="What is the type of the literal 3.14?",
            options=["int", "float", "str", "bool"],
            answer="B",
            hint="A decimal point makes it a float.",
        ),
        Challenge(
            id="B2",
            title="Length of a String",
            category="Basics",
            kind="input",
            prompt='What is the result of len("hello")?',
            validator=int_answer(5),
            hint="Count the letters.",
        ),
        Challenge(
            id="B3",
            title="Integer Division",
            category="Basics",
            kind="input",
            prompt="What is the result of 7 // 2?",
            validator=int_answer(3),
            hint="Integer division drops the remainder.",
        ),
        Challenge(
            id="B4",
            title="Boolean Logic",
            category="Basics",
            kind="mcq",
            prompt="What does not (True and False) evaluate to?",
            options=["True", "False"],
            answer="A",
            hint="True and False is False, then not flips it.",
        ),
        Challenge(
            id="B5",
            title="String Concatenation",
            category="Basics",
            kind="input",
            prompt='What is the result of "Py" + "thon"? ',
            answer="Python",
            hint="String concatenation glues them together.",
        ),
        Challenge(
            id="C1",
            title="And Operator",
            category="Control Flow",
            kind="input",
            prompt="x = 5, y = 2. What is the result of x > y and y > 0? (True/False)",
            validator=bool_answer(True),
            hint="Both comparisons must be True.",
        ),
        Challenge(
            id="C2",
            title="Sum 1..5",
            category="Control Flow",
            kind="input",
            prompt="What is the sum of the numbers 1 through 5?",
            validator=int_answer(15),
            hint="1 + 2 + 3 + 4 + 5",
        ),
        Challenge(
            id="C3",
            title="Range Loop",
            category="Control Flow",
            kind="input",
            prompt="How many times does this loop run? for i in range(4):",
            validator=int_answer(4),
            hint="range(4) produces 0, 1, 2, 3",
        ),
        Challenge(
            id="D1",
            title="List Indexing",
            category="Data Structures",
            kind="input",
            prompt="nums = [10, 20, 30]. What is nums[-1]?",
            validator=int_answer(30),
            hint="Negative index -1 means the last item.",
        ),
        Challenge(
            id="D2",
            title="Dict Lookup",
            category="Data Structures",
            kind="input",
            prompt='data = {"a": 1, "b": 2}. What is data["b"]? ',
            validator=int_answer(2),
            hint="Look up the value by its key.",
        ),
        Challenge(
            id="D3",
            title="Mutable Type",
            category="Data Structures",
            kind="mcq",
            prompt="Which of these is mutable (can be changed)?",
            options=["list", "tuple", "str", "int"],
            answer="A",
            hint="Lists can be changed in place.",
        ),
        Challenge(
            id="D4",
            title="Set Property",
            category="Data Structures",
            kind="mcq",
            prompt="Which statement about sets is true?",
            options=[
                "Sets keep duplicates",
                "Sets preserve order",
                "Sets store unique items",
                "Sets allow indexing",
            ],
            answer="C",
            hint="Sets are for unique items.",
        ),
        Challenge(
            id="F1",
            title="Function Call",
            category="Functions",
            kind="input",
            prompt="def add(a, b): return a + b. What is add(2, 3)?",
            validator=int_answer(5),
            hint="Just add them.",
        ),
        Challenge(
            id="F2",
            title="Length of a List",
            category="Functions",
            kind="input",
            prompt="What is len([1, 2, 3, 4])?",
            validator=int_answer(4),
            hint="Count the items.",
        ),
        Challenge(
            id="P1",
            title="Add Two Numbers",
            category="Code Quests",
            kind="code",
            prompt="Write add(a, b) that returns the sum of a and b. Example: add(2, 3) -> 5.",
            func_name="add",
            test_cases=[
                {"args": [2, 3], "expected": 5},
                {"args": [-1, 1], "expected": 0},
            ],
            points=20,
            hint="Use the + operator.",
        ),
        Challenge(
            id="P2",
            title="Even or Odd",
            category="Code Quests",
            kind="code",
            prompt="Write is_even(n) that returns True when n is even, False otherwise.",
            func_name="is_even",
            test_cases=[
                {"args": [4], "expected": True},
                {"args": [5], "expected": False},
                {"args": [0], "expected": True},
            ],
            points=20,
            hint="Use n % 2 == 0.",
        ),
        Challenge(
            id="P3",
            title="Reverse a String",
            category="Code Quests",
            kind="code",
            prompt='Write reverse_string(s) that returns the reversed string. Example: "abc" -> "cba".',
            func_name="reverse_string",
            test_cases=[
                {"args": ["Python"], "expected": "nohtyP"},
                {"args": [""], "expected": ""},
            ],
            points=20,
            hint="Slicing with [::-1] can reverse a string.",
        ),
        Challenge(
            id="P4",
            title="Count Vowels",
            category="Code Quests",
            kind="code",
            prompt="Write count_vowels(s) that counts vowels (a, e, i, o, u), case-insensitive.",
            func_name="count_vowels",
            test_cases=[
                {"args": ["hello"], "expected": 2},
                {"args": ["Sky"], "expected": 0},
                {"args": ["AEIOU"], "expected": 5},
            ],
            points=20,
            hint="Lowercase the string and count letters in 'aeiou'.",
        ),
        Challenge(
            id="P5",
            title="FizzBuzz",
            category="Code Quests",
            kind="code",
            prompt=(
                "Write fizzbuzz(n) that returns a list of strings from 1..n. "
                "Use 'Fizz' for multiples of 3, 'Buzz' for multiples of 5, "
                "and 'FizzBuzz' for multiples of both."
            ),
            func_name="fizzbuzz",
            test_cases=[
                {"args": [5], "expected": ["1", "2", "Fizz", "4", "Buzz"]},
                {"args": [1], "expected": ["1"]},
            ],
            points=20,
            hint="Check 15 first, then 3 and 5.",
        ),
        Challenge(
            id="P6",
            title="Word Count",
            category="Code Quests",
            kind="code",
            prompt="Write word_count(text) that returns a dict of lowercase word counts using simple whitespace split.",
            func_name="word_count",
            test_cases=[
                {"args": ["Red red blue"], "expected": {"red": 2, "blue": 1}},
                {"args": ["One"], "expected": {"one": 1}},
            ],
            points=20,
            hint="Use text.lower().split() and count in a dict.",
        ),
    ]
