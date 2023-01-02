from argparse import ArgumentParser
from watchfiles import run_process


def run_cli(args):
    from macropad import MacroPadRunner
    mp = MacroPadRunner(device_path=args.device, locked=args.start_locked)
    mp.initialize_actions(args.config_file)
    try:
        mp.main_loop()
    except KeyboardInterrupt:
        pass


parser = ArgumentParser(description="This is the cli part of hot_macropad")


subparsers = parser.add_subparsers(dest="subcommand")

listen_parser = subparsers.add_parser("listen")
run_parser = subparsers.add_parser("run")
configure_parser = subparsers.add_parser("configure")

listen_parser.add_argument("-d", "--device", type=str, required=True, help="Device interface path")

configure_parser.add_argument("-o", "--output-file", type=str,
                              help="Output file for configuration. If not specified, the output will be printed to STDOUT")
configure_parser.add_argument("-d", "--device", type=str, required=True,
                              help="Device interface path")
configure_parser.add_argument("-c", "--page-count", type=int, default=1,
                              help="Decides how many pages should be created for configuration")
# configure_parser.add_argument("-a", "--add-page", action="store_true",
#                               help="Add a new page to the existing action pages file.")
run_parser.add_argument("-d", "--device", type=str, required=True,
                        help="Device interface path")
run_parser.add_argument("-c", "--config-file", type=str, required=True,
                        help="Action pages path")
run_parser.add_argument("-l", "--start-locked", action="store_true",
                        help="Start keypad software as locked. Be sure your first action page contains a PadLocker")

args = parser.parse_args()

if __name__ == '__main__':
    if args.subcommand == "listen":
        from macropad import MacroPadListener
        mp = MacroPadListener(device_path=args.device)
        try:
            mp.echo()
        except KeyboardInterrupt:
            pass

    elif args.subcommand == "configure":
        from macropad import MacroPadConfigurer
        mp = MacroPadConfigurer(device_path=args.device)
        mp.prepare_config_with_listen(args.output_file, page_count=args.page_count)

    elif args.subcommand == "run":
        run_process(args.config_file, target=run_cli, args=(args,))
