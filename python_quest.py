import tkinter as tk
from tkinter import ttk

from tasks import TASKS, CodeTask, QuizTask, run_code_task


SCORE_PER_TASK = 10

COLORS = {
    "bg": "#F6F3EE",
    "sidebar_bg": "#1F2A37",
    "sidebar_fg": "#E5E7EB",
    "card_bg": "#FFFFFF",
    "text": "#1F2937",
    "muted": "#6B7280",
    "accent": "#0E7490",
    "accent_dark": "#0A5E75",
    "success": "#1E7F3F",
    "warning": "#B45309",
    "danger": "#B91C1C",
    "divider": "#E5E7EB",
    "code_bg": "#FBFAF8",
}


class PythonQuestApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Python Quest")
        self.geometry("1080x720")
        self.minsize(980, 640)
        self.configure(bg=COLORS["bg"])

        self.tasks = TASKS
        self.current_index = 0
        self.completed_correct = set()
        self.score = 0

        self._setup_style()
        self._build_ui()
        self._load_task(0)

    def _setup_style(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")

        default_font = ("Segoe UI", 10)
        title_font = ("Segoe UI", 16, "bold")
        subtitle_font = ("Segoe UI", 10)
        card_title_font = ("Segoe UI", 14, "bold")

        style.configure("TFrame", background=COLORS["bg"])
        style.configure("App.TFrame", background=COLORS["bg"])
        style.configure("Header.TFrame", background=COLORS["bg"])

        style.configure("Sidebar.TFrame", background=COLORS["sidebar_bg"])
        style.configure("SidebarTitle.TLabel", background=COLORS["sidebar_bg"], foreground=COLORS["sidebar_fg"], font=title_font)
        style.configure("SidebarText.TLabel", background=COLORS["sidebar_bg"], foreground=COLORS["sidebar_fg"], font=subtitle_font)
        style.configure("SidebarMuted.TLabel", background=COLORS["sidebar_bg"], foreground="#9CA3AF", font=subtitle_font)

        style.configure("Card.TFrame", background=COLORS["card_bg"], relief="flat")
        style.configure("CardTitle.TLabel", background=COLORS["card_bg"], foreground=COLORS["text"], font=card_title_font)
        style.configure("CardBody.TLabel", background=COLORS["card_bg"], foreground=COLORS["text"], font=default_font)
        style.configure("Muted.TLabel", background=COLORS["card_bg"], foreground=COLORS["muted"], font=default_font)

        style.configure("Pill.TLabel", background=COLORS["accent"], foreground="#FFFFFF", font=("Segoe UI", 9, "bold"), padding=(10, 4))

        style.configure("TButton", font=("Segoe UI", 10), padding=(12, 6))
        style.map("TButton", background=[("active", "#E5E7EB")])

        style.configure("Accent.TButton", background=COLORS["accent"], foreground="#FFFFFF", font=("Segoe UI", 10, "bold"))
        style.map(
            "Accent.TButton",
            background=[("active", COLORS["accent_dark"]), ("disabled", "#94A3B8")],
            foreground=[("disabled", "#F8FAFC")],
        )

        style.configure("Status.TLabel", background=COLORS["card_bg"], foreground=COLORS["muted"], font=default_font)

    def _build_ui(self) -> None:
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        container = ttk.Frame(self, style="App.TFrame", padding=16)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(1, weight=1)
        container.rowconfigure(0, weight=1)

        sidebar = ttk.Frame(container, style="Sidebar.TFrame", padding=16)
        sidebar.grid(row=0, column=0, sticky="nsw", padx=(0, 16))
        sidebar.rowconfigure(2, weight=1)

        title = ttk.Label(sidebar, text="Python Quest", style="SidebarTitle.TLabel")
        title.grid(row=0, column=0, sticky="w")
        subtitle = ttk.Label(sidebar, text="Beginner Track", style="SidebarMuted.TLabel")
        subtitle.grid(row=1, column=0, sticky="w", pady=(2, 12))

        self.task_list = tk.Listbox(
            sidebar,
            height=24,
            width=28,
            bg=COLORS["sidebar_bg"],
            fg=COLORS["sidebar_fg"],
            selectbackground=COLORS["accent"],
            selectforeground="#FFFFFF",
            highlightthickness=0,
            bd=0,
            activestyle="none",
            font=("Segoe UI", 10),
        )
        self.task_list.grid(row=2, column=0, sticky="nsew")
        for i, task in enumerate(self.tasks, start=1):
            kind = "Quiz" if isinstance(task, QuizTask) else "Code"
            self.task_list.insert(tk.END, f"{i}. {kind}: {task.title}")
        self.task_list.bind("<<ListboxSelect>>", self._on_list_select)

        sidebar_divider = ttk.Separator(sidebar, orient="horizontal")
        sidebar_divider.grid(row=3, column=0, sticky="ew", pady=(12, 8))

        self.progress_var = tk.StringVar(value="Score: 0 | Completed: 0/0")
        progress = ttk.Label(sidebar, textvariable=self.progress_var, style="SidebarText.TLabel")
        progress.grid(row=4, column=0, sticky="w")

        self.main = ttk.Frame(container, style="App.TFrame")
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.columnconfigure(0, weight=1)
        self.main.rowconfigure(1, weight=1)

        header = ttk.Frame(self.main, style="Header.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        header.columnconfigure(0, weight=1)

        header_title = ttk.Label(header, text="Welcome to Python Quest", font=("Segoe UI", 18, "bold"), background=COLORS["bg"], foreground=COLORS["text"])
        header_title.grid(row=0, column=0, sticky="w")
        header_subtitle = ttk.Label(header, text="Learn core Python skills through quick quizzes and coding missions.", font=("Segoe UI", 10), background=COLORS["bg"], foreground=COLORS["muted"])
        header_subtitle.grid(row=1, column=0, sticky="w", pady=(2, 0))

        self.header_pill = ttk.Label(header, text="Score 0", style="Pill.TLabel")
        self.header_pill.grid(row=0, column=1, rowspan=2, sticky="e")

        self.card = ttk.Frame(self.main, style="Card.TFrame", padding=18)
        self.card.grid(row=1, column=0, sticky="nsew")
        self.card.columnconfigure(0, weight=1)

        self.content = ttk.Frame(self.card, style="Card.TFrame")
        self.content.grid(row=0, column=0, sticky="nsew")
        self.content.columnconfigure(0, weight=1)

        nav = ttk.Frame(self.main, style="App.TFrame")
        nav.grid(row=2, column=0, sticky="ew", pady=(12, 0))
        nav.columnconfigure(1, weight=1)

        self.status_var = tk.StringVar(value="Ready for your next challenge.")
        status = ttk.Label(nav, textvariable=self.status_var, style="Status.TLabel")
        status.grid(row=0, column=0, sticky="w")

        self.prev_button = ttk.Button(nav, text="Previous", command=self._go_prev)
        self.prev_button.grid(row=0, column=2, sticky="e", padx=(0, 8))

        self.next_button = ttk.Button(nav, text="Next", command=self._go_next, style="Accent.TButton")
        self.next_button.grid(row=0, column=3, sticky="e")

    def _update_progress(self) -> None:
        total = len(self.tasks)
        done = len(self.completed_correct)
        self.progress_var.set(f"Score: {self.score} | Completed: {done}/{total}")
        self.header_pill.configure(text=f"Score {self.score}")

    def _clear_content(self) -> None:
        for child in self.content.winfo_children():
            child.destroy()

    def _set_feedback(self, message: str, kind: str = "info") -> None:
        color_map = {
            "info": COLORS["muted"],
            "success": COLORS["success"],
            "warning": COLORS["warning"],
            "danger": COLORS["danger"],
        }
        color = color_map.get(kind, COLORS["muted"])
        self.feedback_var.set(message)
        if self.feedback_label is not None:
            self.feedback_label.configure(foreground=color)

    def _load_task(self, index: int) -> None:
        if index < 0 or index >= len(self.tasks):
            return
        self.current_index = index
        self.task_list.selection_clear(0, tk.END)
        self.task_list.selection_set(index)
        self.task_list.activate(index)

        self._clear_content()
        task = self.tasks[index]

        title = ttk.Label(self.content, text=f"{index + 1}. {task.title}", style="CardTitle.TLabel")
        title.grid(row=0, column=0, sticky="w")

        kind = "Quiz" if isinstance(task, QuizTask) else "Code"
        meta = ttk.Label(self.content, text=f"{kind} Challenge", style="Muted.TLabel")
        meta.grid(row=1, column=0, sticky="w", pady=(2, 12))

        if isinstance(task, QuizTask):
            self._show_quiz(task)
        else:
            self._show_code(task)

        self.status_var.set("Working on a quiz." if isinstance(task, QuizTask) else "Working on a coding challenge.")
        self._update_progress()

    def _show_quiz(self, task: QuizTask) -> None:
        prompt = ttk.Label(self.content, text=task.question, style="CardBody.TLabel", wraplength=720, justify="left")
        prompt.grid(row=2, column=0, sticky="w", pady=(0, 8))

        self.quiz_var = tk.IntVar(value=-1)
        for i, option in enumerate(task.options):
            rb = ttk.Radiobutton(self.content, text=option, variable=self.quiz_var, value=i)
            rb.grid(row=3 + i, column=0, sticky="w", pady=4)

        self.feedback_var = tk.StringVar(value="")
        self.feedback_label = ttk.Label(self.content, textvariable=self.feedback_var, style="CardBody.TLabel", wraplength=720, justify="left")
        self.feedback_label.grid(row=3 + len(task.options), column=0, sticky="w", pady=(12, 8))

        check = ttk.Button(self.content, text="Check Answer", command=self._check_quiz, style="Accent.TButton")
        check.grid(row=4 + len(task.options), column=0, sticky="w")

    def _show_code(self, task: CodeTask) -> None:
        prompt = ttk.Label(self.content, text=task.prompt, style="CardBody.TLabel", wraplength=760, justify="left")
        prompt.grid(row=2, column=0, sticky="w", pady=(0, 8))

        self.code_editor = tk.Text(
            self.content,
            height=14,
            width=90,
            font=("Consolas", 11),
            bg=COLORS["code_bg"],
            fg=COLORS["text"],
            insertbackground=COLORS["accent"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=COLORS["divider"],
            highlightcolor=COLORS["accent"],
        )
        self.code_editor.grid(row=3, column=0, sticky="nsew", pady=(0, 12))
        self.code_editor.insert("1.0", task.starter_code)

        self.feedback_var = tk.StringVar(value="")
        self.feedback_label = ttk.Label(self.content, textvariable=self.feedback_var, style="CardBody.TLabel", wraplength=720, justify="left")
        self.feedback_label.grid(row=4, column=0, sticky="w", pady=(0, 8))

        self.results_box = tk.Text(
            self.content,
            height=6,
            width=90,
            font=("Consolas", 10),
            bg="#F9FAFB",
            fg=COLORS["text"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=COLORS["divider"],
            highlightcolor=COLORS["accent"],
        )
        self.results_box.grid(row=5, column=0, sticky="nsew")
        self.results_box.configure(state="disabled")

        check = ttk.Button(self.content, text="Run Tests", command=self._check_code, style="Accent.TButton")
        check.grid(row=6, column=0, sticky="w", pady=(10, 0))

    def _check_quiz(self) -> None:
        task = self.tasks[self.current_index]
        if not isinstance(task, QuizTask):
            return
        choice = self.quiz_var.get()
        if choice == -1:
            self._set_feedback("Pick an option first.", "warning")
            return

        if choice == task.correct_index:
            self._set_feedback(f"Correct! {task.explanation}", "success")
            self._mark_complete(task.id)
        else:
            self._set_feedback("Not quite. Try again.", "danger")

    def _check_code(self) -> None:
        task = self.tasks[self.current_index]
        if not isinstance(task, CodeTask):
            return

        code = self.code_editor.get("1.0", tk.END)
        result = run_code_task(code, task)

        self.results_box.configure(state="normal")
        self.results_box.delete("1.0", tk.END)

        if result["error"]:
            self._set_feedback(result["error"], "danger")
        else:
            lines = []
            for test in result["results"]:
                status = "PASS" if test["ok"] else "FAIL"
                lines.append(f"{status} - {test['name']}: {test['message']}")
            self.results_box.insert("1.0", "\n".join(lines))
            if result["passed"]:
                self._set_feedback("Great job! All tests passed.", "success")
            else:
                self._set_feedback("Keep going, fix the failing tests.", "warning")

        self.results_box.configure(state="disabled")

        if result["passed"]:
            self._mark_complete(task.id)

    def _mark_complete(self, task_id: str) -> None:
        if task_id in self.completed_correct:
            return
        self.completed_correct.add(task_id)
        self.score += SCORE_PER_TASK
        self._update_progress()

    def _go_next(self) -> None:
        if self.current_index + 1 < len(self.tasks):
            self._load_task(self.current_index + 1)

    def _go_prev(self) -> None:
        if self.current_index - 1 >= 0:
            self._load_task(self.current_index - 1)

    def _on_list_select(self, event) -> None:
        selection = self.task_list.curselection()
        if not selection:
            return
        self._load_task(selection[0])


if __name__ == "__main__":
    app = PythonQuestApp()
    app.mainloop()
