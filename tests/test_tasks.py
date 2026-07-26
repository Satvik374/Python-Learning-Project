import unittest

from tasks import TASKS, CodeTask, run_code_task


class TestTasks(unittest.TestCase):
    def test_has_code_and_quiz_tasks(self):
        has_code = any(isinstance(t, CodeTask) for t in TASKS)
        has_quiz = any(not isinstance(t, CodeTask) for t in TASKS)
        self.assertTrue(has_code)
        self.assertTrue(has_quiz)

    def test_code_tasks_solutions(self):
        solutions = {
            "c_add": """
""" +
"""

def add(a, b):
    return a + b
""",
            "c_even": """
""" +
"""

def is_even(n):
    return n % 2 == 0
""",
            "c_vowels": """
""" +
"""

def count_vowels(text):
    vowels = set('aeiou')
    count = 0
    for ch in text.lower():
        if ch in vowels:
            count += 1
    return count
""",
            "c_fact": """
""" +
"""

def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result
""",
        }

        for task in TASKS:
            if not isinstance(task, CodeTask):
                continue
            code = solutions.get(task.id)
            self.assertIsNotNone(code, msg=f"Missing solution for {task.id}")
            result = run_code_task(code, task)
            self.assertTrue(result["passed"], msg=f"Failed tests for {task.id}")


if __name__ == "__main__":
    unittest.main()
