import argparse

from .engine import run_game, list_challenges, play_specific, reset_progress


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Python Learning Quest - a terminal learning game."
    )
    parser.add_argument("--list", action="store_true", help="List all challenges.")
    parser.add_argument("--challenge", help="Play a specific challenge by id.")
    parser.add_argument("--reset", action="store_true", help="Reset progress.")
    args = parser.parse_args()

    if args.reset:
        reset_progress()
        print("Progress reset.")
        return
    if args.list:
        list_challenges()
        return
    if args.challenge:
        play_specific(args.challenge)
        return

    run_game()


if __name__ == "__main__":
    main()
