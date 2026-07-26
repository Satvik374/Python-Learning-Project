from dataclasses import dataclass
from typing import List, Tuple, Any, Dict


@dataclass
class CodeTask:
    id: str
    title: str
    prompt: str
    starter_code: str
    function_name: str
    tests: List[Tuple[tuple, Any]]


@dataclass
class QuizTask:
    id: str
    title: str
    question: str
    options: List[str]
    correct_index: int
    explanation: str


TASKS = [
    QuizTask(
        id="q_vars",
        title="Variables",
        question="Which line assigns the value 5 to a variable named x?",
        options=[
            "x == 5",
            "x = 5",
            "5 = x",
            "x := 5"
        ],
        correct_index=1,
        explanation="Use = to assign values. == checks equality."
    ),
    CodeTask(
        id="c_add",
        title="Add Two Numbers",
        prompt="Write a function add(a, b) that returns the sum of a and b.",
        starter_code=(
            "def add(a, b):\n"
            "    # TODO: return the sum\n"
            "    pass\n"
        ),
        function_name="add",
        tests=[
            ((2, 3), 5),
            ((-1, 1), 0),
            ((0, 0), 0)
        ]
    ),
    QuizTask(
        id="q_lists",
        title="Lists",
        question="What is the value of nums[0] if nums = [10, 20, 30]?",
        options=["10", "20", "30", "0"],
        correct_index=0,
        explanation="List indexing starts at 0."
    ),
    CodeTask(
        id="c_even",
        title="Is Even",
        prompt="Write a function is_even(n) that returns True if n is even, else False.",
        starter_code=(
            "def is_even(n):\n"
            "    # TODO: return True if n is even\n"
            "    pass\n"
        ),
        function_name="is_even",
        tests=[
            ((2,), True),
            ((7,), False),
            ((0,), True)
        ]
    ),
    QuizTask(
        id="q_len",
        title="Length",
        question="What does len([1, 2, 3, 4]) return?",
        options=["3", "4", "5", "Error"],
        correct_index=1,
        explanation="len returns the number of items in a sequence."
    ),
    CodeTask(
        id="c_vowels",
        title="Count Vowels",
        prompt="Write a function count_vowels(text) that counts a, e, i, o, u in a string.",
        starter_code=(
            "def count_vowels(text):\n"
            "    # TODO: return the number of vowels in text\n"
            "    pass\n"
        ),
        function_name="count_vowels",
        tests=[
            (("hello",), 2),
            (("rhythm",), 0),
            (("AEIOU",), 5)
        ]
    ),
    QuizTask(
        id="q_func",
        title="Functions",
        question="Which keyword is used to define a function in Python?",
        options=["func", "define", "def", "lambda"],
        correct_index=2,
        explanation="The def keyword starts a function definition."
    ),
    CodeTask(
        id="c_fact",
        title="Factorial",
        prompt=(
            "Write a function factorial(n) that returns n! (the product of 1..n).\n"
            "Assume n is a non-negative integer."
        ),
        starter_code=(
            "def factorial(n):\n"
            "    # TODO: compute factorial using a loop\n"
            "    pass\n"
        ),
        function_name="factorial",
        tests=[
            ((0,), 1),
            ((1,), 1),
            ((5,), 120)
        ]
    )
]


def run_code_task(code: str, task: CodeTask) -> Dict[str, Any]:
    safe_builtins = {
        "abs": abs,
        "len": len,
        "range": range,
        "str": str,
        "int": int,
        "float": float,
        "list": list,
        "dict": dict,
        "set": set,
        "tuple": tuple,
        "enumerate": enumerate,
        "sum": sum,
        "min": min,
        "max": max,
        "print": print,
    }

    globals_dict: Dict[str, Any] = {"__builtins__": safe_builtins}
    locals_dict: Dict[str, Any] = {}

    try:
        exec(code, globals_dict, locals_dict)
    except Exception as exc:
        return {
            "passed": False,
            "results": [],
            "error": f"Code error: {exc}"
        }

    func = locals_dict.get(task.function_name) or globals_dict.get(task.function_name)
    if not callable(func):
        return {
            "passed": False,
            "results": [],
            "error": f"Function '{task.function_name}' was not found."
        }

    results = []
    for i, (args, expected) in enumerate(task.tests, start=1):
        try:
            actual = func(*args)
            ok = actual == expected
            message = f"Expected {expected}, got {actual}"
        except Exception as exc:
            ok = False
            message = f"Error: {exc}"

        results.append({
            "name": f"Test {i}",
            "ok": ok,
            "message": message
        })

    passed = all(r["ok"] for r in results)
    return {
        "passed": passed,
        "results": results,
        "error": ""
    }
