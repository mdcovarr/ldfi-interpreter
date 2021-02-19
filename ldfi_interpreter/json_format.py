"""
    Utility to format json output from Go tests
"""
import argparse
import sys
import json
from subprocess import check_call, CalledProcessError


def handle_arguments():
    """
        Set script arguments

        Parameters:
        None

        Returns:
        parser (ArgumentParser object): parser for CLI
    """
    parser = argparse.ArgumentParser(description="Json pretty print tests")

    parser.add_argument("-i", "--input", dest="input_file",
                        help="input json file to reformat")
    parser.add_argument("-o", "--output", dest="output_file",
                        help="input json file to reformat")

    return parser


def main():
    """
        Main Entrance
    """
    parser = handle_arguments()
    args = parser.parse_args()

    if not args.input_file:
        parser.print_help()
        sys.exit(1)

    if not args.output_file:
        args.output_file = args.input_file

    input_file = open(args.input_file, "r")
    data = json.load(input_file)
    input_file.close()

    # Delete output file if exists
    try:
        command = "rm -f {outfile}".format(outfile=args.output_file)
        check_call(command, shell=True)
    except CalledProcessError:
        print("Issue removing {outfile}. Exiting...".format(outfile=args.output_file))
        sys.exit(1)

    out_file = open(args.output_file, "w+")
    out_file.write(json.dumps(data, indent=4, sort_keys=True))
    out_file.close()


if __name__ == "__main__":
    main()
