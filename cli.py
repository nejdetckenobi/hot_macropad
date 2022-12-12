from argparse import ArgumentParser

from macropad import MacroPad

parser = ArgumentParser(description="This is the cli part of hot_macropad")


subparsers = parser.add_subparsers(dest="subcommand")

listen_parser = subparsers.add_parser("listen")
run_parser = subparsers.add_parser("run")


listen_parser.add_argument("-d", "--device", type=str, required=True, help="Device interface path")
run_parser.add_argument("-d", "--device", type=str, required=True, help="Device interface path")
run_parser.add_argument("-c", "--config-file", type=str, required=True, help="Action pages path")
run_parser.add_argument("-l", "--start-locked", action="store_true")

args = parser.parse_args()


if args.subcommand == "listen":
    mp = MacroPad(device_path=args.device)
    try:
        mp.echo()
    except KeyboardInterrupt:
        pass

elif args.subcommand == "run":
    mp = MacroPad(device_path=args.device, locked=args.start_locked)
    mp.initialize_actions(args.config_file)
    try:
        mp.main_loop()
    except KeyboardInterrupt:
        pass
