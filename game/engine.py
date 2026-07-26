import json
import importlib
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .challenges import Challenge, get_challenges

DATA_DIR = "data"
STATE_FILE = "progress.json"


def _data_dir() -> Path:
    return Path(__file__).resolve().parents[1] / DATA_DIR


def _state_path() -> Path:
    return _data_dir() / STATE_FILE


def default_state() -> Dict[str, Any]:
    return {"score": 0, "completed": []}


def load_state() -> Dict[str, Any]:
    path = _state_path()
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                return default_state()
            data.setdefault("score", 0)
            data.setdefault("completed", [])
            if not isinstance(data["completed"], list):
                data["completed"] = []
            return data
        except Exception:
            return default_state()
    return default_state()


def save_state(state: Dict[str, Any]) -> None:
    _data_dir().mkdir(parents=True, exist_ok=True)
    _state_path().write_text(json.dumps(state, indent=2), encoding="utf-8")


def reset_progress() -> None:
    path = _state_path()
    if path.exists():
        path.unlink()


def list_challenges() -> None:
    challenges = get_challenges()
    state = load_state()
    completed = set(state["completed"])
    print("Challenge List")
    print("-" * 60)
    for ch in challenges:
        status = "DONE" if ch.id in completed else "OPEN"
        print(f"{ch.id:>3} [{status}] {ch.title} - {ch.category} ({ch.points} pts)")
    print("-" * 60)
    print(f"Score: {state['score']}")


def run_game() -> None:
    challenges = get_challenges()
    state = load_state()
    print("Python Learning Quest")
    print("=" * 24)
    while True:
        print("")
        print("1. Continue")
        print("2. Choose challenge")
        print("3. List challenges")
        print("4. Reset progress")
        print("5. Exit")
        choice = input("Select an option: ").strip()
        if choice == "1":
            next_challenge = _next_incomplete(challenges, state)
            if not next_challenge:
                print("You cleared all challenges. Great job!")
                continue
            _play_challenge(next_challenge, state)
        elif choice == "2":
            _play_specific_prompt(challenges, state)
        elif choice == "3":
            list_challenges()
        elif choice == "4":
            confirm = input("Type RESET to confirm: ").strip()
            if confirm == "RESET":
                reset_progress()
                state = load_state()
                print("Progress reset.")
            else:
                print("Reset canceled.")
        elif choice == "5":
            print("See you next time.")
            break
        else:
            print("Please choose 1-5.")


def play_specific(challenge_id: str) -> None:
    challenges = get_challenges()
    state = load_state()
    challenge = _find_challenge(challenges, challenge_id)
    if not challenge:
        print(f"Challenge '{challenge_id}' not found.")
        return
    _play_challenge(challenge, state)


def _find_challenge(challenges: List[Challenge], challenge_id: str) -> Optional[Challenge]:
    for ch in challenges:
        if ch.id.lower() == challenge_id.lower():
            return ch
    return None


def _next_incomplete(challenges: List[Challenge], state: Dict[str, Any]) -> Optional[Challenge]:
    completed = set(state["completed"])
    for ch in challenges:
        if ch.id not in completed:
            return ch
    return None


def _play_specific_prompt(challenges: List[Challenge], state: Dict[str, Any]) -> None:
    list_challenges()
    choice = input("Enter a challenge id: ").strip()
    challenge = _find_challenge(challenges, choice)
    if not challenge:
        print("No such challenge.")
        return
    _play_challenge(challenge, state)


def _play_challenge(challenge: Challenge, state: Dict[str, Any]) -> None:
    print("")
    print(f"[{challenge.id}] {challenge.title}")
    print(f"Category: {challenge.category} | Points: {challenge.points}")
    print("-" * 60)

    if challenge.kind == "code":
        ok, msg = _run_code_challenge(challenge)
        if msg:
            print(msg)
        if ok:
            _mark_complete(challenge, state)
        return

    print(challenge.prompt)
    if challenge.kind == "mcq":
        _print_options(challenge)
    user_input = _prompt_answer(challenge)
    if user_input is None:
        print("Skipped.")
        return

    if challenge.kind == "mcq":
        ok, msg = _evaluate_mcq(challenge, user_input)
    elif challenge.kind == "input":
        ok, msg = _evaluate_input(challenge, user_input)
    else:
        ok, msg = False, "Unknown challenge type."

    print(msg)
    if ok:
        _mark_complete(challenge, state)


def _print_options(challenge: Challenge) -> None:
    if not challenge.options:
        return
    for idx, option in enumerate(challenge.options):
        letter = chr(ord("A") + idx)
        print(f"{letter}) {option}")


def _prompt_answer(challenge: Challenge) -> Optional[str]:
    while True:
        entry = input("Your answer (or 'hint' / 'skip'): ").strip()
        if entry.lower() in ("hint", "h", "?"):
            if challenge.hint:
                print(f"Hint: {challenge.hint}")
            else:
                print("No hint available.")
            continue
        if entry.lower() in ("skip", "s"):
            return None
        if entry == "":
            print("Please enter an answer or 'skip'.")
            continue
        return entry


def _evaluate_mcq(challenge: Challenge, user_input: str) -> Tuple[bool, str]:
    if not challenge.options or not challenge.answer:
        return False, "Challenge misconfigured."
    letters = [chr(ord("A") + i) for i in range(len(challenge.options))]
    answer_letter = challenge.answer.strip().upper()
    if answer_letter not in letters:
        return False, "Challenge misconfigured."

    normalized = user_input.strip().lower()
    if normalized in [l.lower() for l in letters]:
        chosen_text = challenge.options[letters.index(normalized.upper())]
    else:
        chosen_text = user_input

    correct_text = challenge.options[letters.index(answer_letter)]
    ok = chosen_text.strip().lower() == correct_text.strip().lower() or normalized == answer_letter.lower()
    if ok:
        return True, "Correct!"
    return False, f"Not quite. Correct answer: {answer_letter}) {correct_text}"


def _evaluate_input(challenge: Challenge, user_input: str) -> Tuple[bool, str]:
    if challenge.validator:
        return challenge.validator(user_input)
    if challenge.answer is None:
        return False, "Challenge misconfigured."
    expected = str(challenge.answer).strip()
    ok = user_input.strip().lower() == expected.lower()
    if ok:
        return True, "Correct!"
    return False, f"Expected: {expected}"


def _run_code_challenge(challenge: Challenge) -> Tuple[bool, str]:
    print(challenge.prompt)
    print("")
    print("Open game/player_solutions.py and implement the function.")
    print("Type 'run' to test, 'hint' for a hint, or 'skip' to go back.")
    while True:
        entry = input("> ").strip().lower()
        if entry in ("hint", "h", "?"):
            if challenge.hint:
                print(f"Hint: {challenge.hint}")
            else:
                print("No hint available.")
            continue
        if entry in ("skip", "s"):
            return False, "Skipped."
        if entry in ("", "run"):
            ok, msg = _evaluate_code(challenge)
            if ok:
                return True, msg
            print(msg)
            print("Fix your code and type 'run' again, or 'skip' to return.")
            continue
        print("Type 'run', 'hint', or 'skip'.")


def _evaluate_code(challenge: Challenge) -> Tuple[bool, str]:
    if not challenge.func_name:
        return False, "Challenge misconfigured."
    try:
        from . import player_solutions
        importlib.reload(player_solutions)
    except Exception as exc:
        return False, f"Could not import player_solutions: {exc}"

    func = getattr(player_solutions, challenge.func_name, None)
    if not callable(func):
        return False, f"Function '{challenge.func_name}' not found or not callable."

    cases = challenge.test_cases or []
    for case in cases:
        args = case.get("args", [])
        expected = case.get("expected")
        try:
            result = func(*args)
        except Exception as exc:
            return False, f"Function raised {type(exc).__name__}: {exc}"
        if result != expected:
            return False, f"For args {args} expected {expected} but got {result}"
    return True, "All tests passed!"


def _mark_complete(challenge: Challenge, state: Dict[str, Any]) -> None:
    if challenge.id in state["completed"]:
        print("Already completed. No extra points awarded.")
        return
    state["completed"].append(challenge.id)
    state["score"] += challenge.points
    save_state(state)
    print(f"+{challenge.points} points. Total: {state['score']}")
