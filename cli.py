from argparse import ArgumentParser

from macropad import MacroPad

parser = ArgumentParser(description="This is the cli part of hot_macropad")


subparsers = parser.add_subparsers(dest="subcommand")

listen_parser = subparsers.add_parser("listen")
run_parser = subparsers.add_parser("run")
configure_parser = subparsers.add_parser("configure")

listen_parser.add_argument("-d", "--device", type=str, required=True, help="Device interface path")

configure_parser.add_argument("-o", "--output-file", type=str,
                              help="Output file for configuration. If not specified, the output will be printed to STDOUT")
configure_parser.add_argument("-d", "--device", type=str, required=True, help="Device interface path")

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

elif args.subcommand == "configure":
    mp = MacroPad(device_path=args.device)
    mp.prepare_config_with_listen(args.output_file)
elif args.subcommand == "run":
    mp = MacroPad(device_path=args.device, locked=args.start_locked)
    mp.initialize_actions(args.config_file)
    try:
        mp.main_loop()
    except KeyboardInterrupt:
        pass

