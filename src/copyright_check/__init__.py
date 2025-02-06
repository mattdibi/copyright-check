import yaml
import argparse
import datetime
import logging
import os
import re
import magic

from enum import Enum

from difflib import ndiff

from comment_parser import comment_parser

logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGES = {
    'java': 'text/x-java',
    'xml': 'text/xml',
    'c': 'text/x-c'
}

class Error(Enum):
    HEADER_MISSING = 1
    HEADER_INCORRECT = 2
    YEAR_INCORRECT = 3

ERROR_MESSAGES = {
    Error.HEADER_MISSING: "header missing",
    Error.HEADER_INCORRECT: "header incorrect or missing",
    Error.YEAR_INCORRECT: "year incorrect or missing"
}


class CheckResult:
    def __init__(self, error, diff):
        self.error = error
        self.diff = diff

    def is_valid(self):
        return self.error is None

    def __str__(self):
        return "FAIL - (reson: {})".format(ERROR_MESSAGES[self.error]) if self.error else "OK"


def check_header(filename, template, mime_type, bypass_year=False):
    logger.debug("Checking file: {}".format(filename))

    # Get regex from template
    regex = re.escape(template)
    regex = regex.replace(r"\{years\}", r"(\d{4}|\d{4}, \d{4})")
    regex = regex.replace(r"\{holder\}", r"[\w\s\.]+")

    comments = comment_parser.extract_comments(filename, mime=mime_type)
    if comments is None or len(comments) == 0:
        return CheckResult(Error.HEADER_MISSING, None)
    header_comment = comments[0] # First comment is the header

    # Check copyright
    if not re.search(re.compile(regex), header_comment.text()):
        # Print diff for debugging
        template_lines = template.splitlines(True)
        diff_header_comment_lines = header_comment.text().splitlines(True)[:len(template_lines)]
        diff = ndiff(template_lines, diff_header_comment_lines)

        return CheckResult(Error.HEADER_INCORRECT, "".join(diff))

    # Check year
    year = datetime.datetime.now().year
    if not bypass_year and not str(year) in header_comment.text():
        return CheckResult(Error.YEAR_INCORRECT, None)

    return CheckResult(None, None)


def load_configuration(config_file_path):
    loaded_templates = {
        'text/x-java': None,
        'text/xml': None,
        'text/x-c': None
    }

    # Parse config
    if not os.path.isfile(config_file_path):
        logger.error("Config file not found: {}".format(config_file_path))
        return None

    config = None
    with open(config_file_path, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logger.error("Error parsing config file: {}".format(exc))
            return None

    for language in SUPPORTED_LANGUAGES:
        config_entry = "template_" + language
        config_mime_type = SUPPORTED_LANGUAGES[language]

        if config_entry not in config:
            loaded_templates[config_mime_type] = None
            continue

        loaded_templates[config_mime_type] = config[config_entry].strip()

    return {
        'bypass_year_check': config['bypass_year_check'],
        'templates': loaded_templates,
        'ignore_files': config['ignore']
    }


def build_parser():
    parser = argparse.ArgumentParser(
            prog="copyright-check",
            description='Check copyright headers',
            epilog="Example usage: copyright-check -c config.yaml $(git diff --name-only) **/*.java")

    parser.add_argument(
            '-d', '--debug',
            help="Print debug information",
            action="store_const", dest="loglevel", const=logging.DEBUG,
            default=logging.INFO, required=False)

    parser.add_argument(
            '-c', '--config',
            help='set path to the config yaml file',
            default='check_copyright_config.yaml', required=True)

    parser.add_argument(
            'filenames',
            nargs='+',
            help='file(s) to check',
            metavar='file')

    return parser


def main():
    # Parse command line arguments
    args = build_parser().parse_args()

    # Log some information
    logging.basicConfig(level=args.loglevel, format="[%(levelname)-5s] %(message)s")
    logger.info("Starting Kura projects copyright checker...")
    logger.debug("Arguments: {}".format(args))
    logger.info("Current working directory: {}".format(os.getcwd()))

    # Parse config
    config = load_configuration(args.config)
    if config is None:
        logger.error("Error loading configuration at path: {}".format(args.config))
        exit(1)

    # Check files
    incorrect_files = []

    for filename in args.filenames:
        if not os.path.isfile(filename):
            logger.error("File not found: {}".format(filename))
            continue

        # Retrieve mime type
        mime_type = magic.Magic(mime=True).from_file(filename)
        if mime_type not in config["templates"] or not config["templates"][mime_type]:
            logger.debug("Unsupported file type({}): {}".format(mime_type, filename))
            continue

        result = check_header(filename, config["templates"][mime_type], mime_type, config["bypass_year_check"])

        if not result.is_valid():
            incorrect_files.append(filename)

        if result.diff:
            logger.debug("Issues for \"{}\":\n{}\n".format(filename, result.diff))

        logger.info("{} - {}".format(filename, result))

    if incorrect_files:
        logger.error("Incorrect files: {}".format(incorrect_files))
        exit(1)

if __name__ == '__main__':
    main()
