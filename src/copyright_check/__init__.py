import argparse
import datetime
import logging
import os
import re
import textwrap

from difflib import ndiff

from comment_parser import comment_parser

logger = logging.getLogger(__name__)

def main():
    # Parse command line arguments
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
            default='check_copyright_config.yaml')

    # TODO: Move this in the configuration file not in CLI
    parser.add_argument(
            '--bypass_year',
            help='bypass check on the years in the header',
            action="store_true",
            default=False, required=False)

    parser.add_argument(
            'filenames',
            nargs='+',
            help='file(s) to check',
            metavar='file')

    args = parser.parse_args()

    # Log some information
    logging.basicConfig(level=args.loglevel, format="[%(levelname)-5s] %(message)s")
    logger.info("Starting Kura projects copyright checker...")
    logger.debug("Arguments: {}".format(args))
    logger.info("Current working directory: {}".format(os.getcwd()))

    # Parse config
    # TODO

    # Check files
    template = textwrap.dedent('''\
******************************************************************************
 * Copyright (c) {years} {holder} and/or its affiliates and others
 *
 * This program and the accompanying materials are made
 * available under the terms of the Eclipse Public License 2.0
 * which is available at https://www.eclipse.org/legal/epl-2.0/
 *
 * SPDX-License-Identifier: EPL-2.0
 *
 * Contributors:
''')

    year = datetime.datetime.now().year

    regex = re.escape(template)
    regex = regex.replace(r"\{years\}", r"(\d{4}|\d{4}, \d{4})")
    regex = regex.replace(r"\{holder\}", r"[\w\s\.]+")

    incorrect_files = []

    for filename in args.filenames:
        logger.debug("Checking file: {}".format(filename))
        comments = comment_parser.extract_comments(filename, mime="text/x-java-source")
        if comments is None or len(comments) == 0:
            logger.error("{} - FAIL (reason: header missing)".format(filename))
            incorrect_files.append(filename)
            continue
        header_comment = comments[0] # First comment is the header

        # Check copyright
        if not re.search(re.compile(regex), header_comment.text()):
            logger.error("{} - FAIL (reason: header incorrect or missing)".format(filename))

            # Print diff for debugging
            template_lines = template.splitlines()
            diff_header_comment_lines = header_comment.text().splitlines()[:len(template_lines)]
            diff = ndiff(template.splitlines(), diff_header_comment_lines)
            logger.debug("Issues for \"{}\":\n{}".format(filename, "\n".join(diff)))

            incorrect_files.append(filename)
            continue

        # Check year
        if not args.bypass_year and not str(year) in header_comment.text():
            logger.error("{} - FAIL (reason: copyright year incorrect or missing)".format(filename))
            incorrect_files.append(filename)
            continue

        logger.info("{} - OK".format(filename))

    if incorrect_files:
        logger.error("Incorrect files: {}".format(incorrect_files))
        exit(1)

if __name__ == '__main__':
    main()
