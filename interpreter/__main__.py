from interpreter.cli import parse_args, run_main_loop


def main():
    args = parse_args()
    run_main_loop(args)


if __name__ == "__main__":
    main()