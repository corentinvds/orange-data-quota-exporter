import logging
from argparse import ArgumentParser
from datetime import datetime

from datamonitoring.metrics import start_metric_server
from datamonitoring.processor import print_usages

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

LOGGER = logging.getLogger(__name__)


def main():
    try:
        script_start = datetime.now()
        logging.basicConfig(format=LOG_FORMAT, level=logging.INFO)
        arg_parser = ArgumentParser()
        arg_parser.add_argument("--user", "-u", help=u"Orange user", required=True)
        arg_parser.add_argument("--password", "-p", help=u"Orange password", required=True)
        arg_parser.add_argument("--number", "-n", help=u"Phone number", required=False, action="append")
        arg_parser.add_argument("--port", help=u"Server port, required to enable server mode", type=int,
                                required=False)
        args = arg_parser.parse_args()

        LOGGER.info(f"Started with args {args}")

        if args.port:
            start_metric_server(args.port, args.user, args.password, args.number)
        else:
            print_usages(args.user, args.password, args.number)

        script_end = datetime.now()
        LOGGER.info("END ({})".format(script_end - script_start))
    except Exception as e:
        LOGGER.exception("FATAL ERROR: {}".format(e))
        raise


if __name__ == "__main__":
    main()
