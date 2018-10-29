#!/usr/bin/env python

"""Create puzzle from input image.

This module loads image and creates puzzle by dividing image
into square pieces and then shuffles pieces to produce random puzzle.

Note that created puzzle size may differ from original image size
depending on given piece size.

"""

import argparse
import os.path
import numpy as np
import cv2

from gaps import image_helpers

MIN_PIECE_SIZE = 28
MAX_PIECE_SIZE = 128
DEFAULT_PIECE_SIZE = 28

COLOR_STRING = {
    "ERROR": "\033[31m[ERROR]\033[0m {0}",
    "SUCCESS": "\033[32m[SUCCESS]\033[0m {0}"
}


def create_puzzle(image_path, output_path, piece_size):
    """Creates jigsaw puzzle from input image"""
    image = cv2.imread(image_path)
    pieces, rows, columns = image_helpers.flatten_image_stripe(image, piece_size)

    # Randomize pieces in order to make puzzle
    np.random.shuffle(pieces)

    # Create puzzle by stacking pieces
    puzzle = image_helpers.assemble_image(pieces, rows, columns)

    cv2.imwrite(output_path, puzzle)
    print_messages(["Puzzle created with {} pieces".format(len(pieces))])


def print_messages(messages, level="SUCCESS"):
    """Prints given messages as colored strings"""
    print
    for message in messages:
        print(COLOR_STRING[level].format(message))


def validate_arguments(args):
    """Validates input arguments required to create puzzle"""
    errors = []

    if not os.path.isfile(args.source):
        errors.append("Image does not exist.")

    if args.size < MIN_PIECE_SIZE:
        errors.append("Minimum piece size is {0} px.".format(MIN_PIECE_SIZE))

    if args.size > MAX_PIECE_SIZE:
        errors.append("Maximum piece size is {0} px.".format(MAX_PIECE_SIZE))

    if len(errors) > 0:
        print_messages(errors, level="ERROR")
        exit()


def parse_arguments():
    """Parses input arguments required to create puzzle"""
    description = ("Create puzzle pieces from input image by random shuffling.\n"
                   "Maximum possible rectangle is cropped from original image.")

    piece_size_help = ("Side of puzzle piece.\n"
                       "Default: {0} px\n"
                       "Min:     {1} px\n"
                       "Max:     {2} px\n").format(DEFAULT_PIECE_SIZE,
                                                   MIN_PIECE_SIZE,
                                                   MAX_PIECE_SIZE)

    parser = argparse.ArgumentParser(description=description,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("source", type=str, help="Path to the input file.")
    parser.add_argument("--destination", type=str, default="./out.jpg",
                        help="Path to the output file.")
    parser.add_argument("--size", type=int, default=DEFAULT_PIECE_SIZE, help=piece_size_help)

    return parser.parse_args()

if __name__ == "__main__":
    ARGS = parse_arguments()
    validate_arguments(ARGS)
    create_puzzle(ARGS.source, ARGS.destination, ARGS.size)
