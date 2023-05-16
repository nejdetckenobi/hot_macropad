from argparse import ArgumentParser
import os
import sys
from time import sleep

print(__file__)
sys.path.append(os.path.abspath(__file__))


def run_cli(args):
    from macropad import MacroPadRunner
    mp = MacroPadRunner(device_path=args.device,
                        locked=args.start_locked,
                        start_page_name=args.page,
                        action_page_output_file=args.page_output)
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
run_parser.add_argument("-w", "--wait", action="store_true",
                        help="Waits for the device")
run_parser.add_argument("-p", "--page", type=str, required=True,
                        help="Initial action page name")
run_parser.add_argument("--no-restart", action="store_true",
                        help="No restart")
run_parser.add_argument("--page-output", type=str,
                        help="The file that contains the current action page name")

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
        if args.wait:
            while not os.path.exists(args.device):
                print('.', end='')
                sys.stdout.flush()
                sleep(1)

        run_cli(args)
