import argparse
import logging
import os

logger = logging.getLogger(__name__)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
            prog="copyright-check",
            description='Check copyright headers',
            epilog="Example usage: copyright-check -c config.yaml $(git diff --name-only)")
    parser.add_argument(
            '-d', '--debug',
            help="Print debug information",
            action="store_const", dest="loglevel", const=logging.DEBUG,
            default=logging.INFO, required=False)

    parser.add_argument(
            '-c', '--config',
            help='set path to the config yaml file',
            default='check_copyright_config.yaml')

    parser.add_argument(
            'filenames',
            nargs='+',
            help='file(s) to check',
            metavar='file')

    args = parser.parse_args()

    # Log some information
    logging.basicConfig(level=args.loglevel, format="[%(levelname)-5s] %(message)s")
    logger.info("Starting Kura projects metadata generator...")
    logger.debug("Arguments: {}".format(args))
    logger.info("Current working directory: {}".format(os.getcwd()))


if __name__ == '__main__':
    main()
