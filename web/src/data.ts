export type QuizTask = {
  id: string;
  title: string;
  type: "quiz";
  question: string;
  options: string[];
  correctIndex: number;
  explanation: string;
};

export type CodeTest = {
  input: string;
  expected: string;
};

export type CodeTask = {
  id: string;
  title: string;
  type: "code";
  prompt: string;
  starterCode: string;
  tests: CodeTest[];
};

export type Task = QuizTask | CodeTask;

export const tasks: Task[] = [
  {
    id: "q_vars",
    title: "Variables",
    type: "quiz",
    question: "Which line assigns the value 5 to a variable named x?",
    options: ["x == 5", "x = 5", "5 = x", "x := 5"],
    correctIndex: 1,
    explanation: "Use = to assign values. == checks equality."
  },
  {
    id: "c_add",
    title: "Add Two Numbers",
    type: "code",
    prompt: "Write a function add(a, b) that returns the sum of a and b.",
    starterCode: "def add(a, b):\n    # TODO: return the sum\n    pass\n",
    tests: [
      { input: "add(2, 3)", expected: "5" },
      { input: "add(-1, 1)", expected: "0" },
      { input: "add(0, 0)", expected: "0" }
    ]
  },
  {
    id: "q_lists",
    title: "Lists",
    type: "quiz",
    question: "What is the value of nums[0] if nums = [10, 20, 30]?",
    options: ["10", "20", "30", "0"],
    correctIndex: 0,
    explanation: "List indexing starts at 0."
  },
  {
    id: "c_even",
    title: "Is Even",
    type: "code",
    prompt: "Write a function is_even(n) that returns True if n is even, else False.",
    starterCode: "def is_even(n):\n    # TODO: return True if n is even\n    pass\n",
    tests: [
      { input: "is_even(2)", expected: "True" },
      { input: "is_even(7)", expected: "False" },
      { input: "is_even(0)", expected: "True" }
    ]
  },
  {
    id: "q_len",
    title: "Length",
    type: "quiz",
    question: "What does len([1, 2, 3, 4]) return?",
    options: ["3", "4", "5", "Error"],
    correctIndex: 1,
    explanation: "len returns the number of items in a sequence."
  },
  {
    id: "c_vowels",
    title: "Count Vowels",
    type: "code",
    prompt: "Write a function count_vowels(text) that counts a, e, i, o, u in a string.",
    starterCode: "def count_vowels(text):\n    # TODO: return the number of vowels in text\n    pass\n",
    tests: [
      { input: "count_vowels(\"hello\")", expected: "2" },
      { input: "count_vowels(\"rhythm\")", expected: "0" },
      { input: "count_vowels(\"AEIOU\")", expected: "5" }
    ]
  },
  {
    id: "q_func",
    title: "Functions",
    type: "quiz",
    question: "Which keyword is used to define a function in Python?",
    options: ["func", "define", "def", "lambda"],
    correctIndex: 2,
    explanation: "The def keyword starts a function definition."
  },
  {
    id: "c_fact",
    title: "Factorial",
    type: "code",
    prompt: "Write a function factorial(n) that returns n! (the product of 1..n).",
    starterCode: "def factorial(n):\n    # TODO: compute factorial using a loop\n    pass\n",
    tests: [
      { input: "factorial(0)", expected: "1" },
      { input: "factorial(1)", expected: "1" },
      { input: "factorial(5)", expected: "120" }
    ]
  }
];
