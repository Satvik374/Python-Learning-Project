from __future__ import annotations

from flask import Flask, render_template, request, session

from tasks import TASKS, CodeTask, QuizTask, run_code_task


SCORE_PER_TASK = 10

app = Flask(__name__)
app.secret_key = "python-quest-secret"


def _ensure_progress() -> None:
    if "completed" not in session:
        session["completed"] = []
    if "score" not in session:
        session["score"] = 0


def _mark_complete(task_id: str) -> None:
    completed = set(session.get("completed", []))
    if task_id in completed:
        return
    completed.add(task_id)
    session["completed"] = list(completed)
    session["score"] = int(session.get("score", 0)) + SCORE_PER_TASK


@app.route("/", methods=["GET"])
def index():
    _ensure_progress()
    return task_view(0)


@app.route("/task/<int:index>", methods=["GET", "POST"])
def task_view(index: int):
    _ensure_progress()
    if index < 0 or index >= len(TASKS):
        index = 0

    task = TASKS[index]
    feedback = {"message": "", "kind": "info"}
    results = []
    code_value = task.starter_code if isinstance(task, CodeTask) else ""
    selected = -1

    if request.method == "POST":
        if isinstance(task, QuizTask) and "choice" in request.form:
            try:
                selected = int(request.form.get("choice", -1))
            except ValueError:
                selected = -1
            if selected == -1:
                feedback = {"message": "Pick an option first.", "kind": "warning"}
            elif selected == task.correct_index:
                feedback = {"message": f"Correct! {task.explanation}", "kind": "success"}
                _mark_complete(task.id)
            else:
                feedback = {"message": "Not quite. Try again.", "kind": "danger"}

        if isinstance(task, CodeTask) and "code" in request.form:
            code_value = request.form.get("code", "")
            result = run_code_task(code_value, task)
            if result["error"]:
                feedback = {"message": result["error"], "kind": "danger"}
            else:
                results = result["results"]
                if result["passed"]:
                    feedback = {"message": "Great job! All tests passed.", "kind": "success"}
                    _mark_complete(task.id)
                else:
                    feedback = {"message": "Keep going, fix the failing tests.", "kind": "warning"}

    completed = set(session.get("completed", []))
    score = int(session.get("score", 0))

    return render_template(
        "task.html",
        task=task,
        index=index,
        total=len(TASKS),
        score=score,
        completed_count=len(completed),
        tasks=TASKS,
        feedback=feedback,
        results=results,
        code_value=code_value,
        selected=selected,
    )


if __name__ == "__main__":
    app.run(debug=True)
