#!/usr/bin/env python

"""Solves given jigsaw puzzle

This module loads puzzle and initializes genetic algorithm with
given number of generations and population. At the end, solution image is displayed.

"""

import argparse
import matplotlib.pyplot as plt
import cv2
from time import time
from gaps.genetic_algorithm_stripe import GeneticAlgorithm
from gaps.size_detector import SizeDetector
from gaps.plot import Plot

GENERATIONS = 30
POPULATION = 1000


def show_image(img, title):
    if not args.verbose:
        Plot(img, title)
    plt.show()


def parse_arguments():
    """Parses input arguments required to solve puzzle"""
    parser = argparse.ArgumentParser(description="A Genetic based solver for jigsaw puzzles")
    parser.add_argument("--image", type=str, default="out.jpg", help="Input image.")
    parser.add_argument("--generations", type=int, default=GENERATIONS, help="Num of generations.")
    parser.add_argument("--population", type=int, default=POPULATION, help="Size of population.")
    parser.add_argument("--size", type=int, help="Single piece size in pixels.")
    parser.add_argument("--verbose", action="store_true", help="Show best individual after each generation.")
    parser.add_argument("--save", action="store_true", help="Save puzzle result as image.")
    parser.add_argument("-n", type=int, default=0)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    image = cv2.imread(args.image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    if args.n > 0:
        width = image.shape[1]
        piece_size = int(width / args.n)
    else:
        if args.size is not None:
            piece_size = args.size
        else:
            detector = SizeDetector(image)
            piece_size = detector.detect_piece_size()

    print("\n=== Population:  {}".format(args.population))
    print("=== Generations: {}".format(args.generations))
    print("=== Piece size:  {} px".format(piece_size))

    # Let the games begin! And may the odds be in your favor!
    start = time()
    algorithm = GeneticAlgorithm(image, piece_size, args.population, args.generations)
    solution = algorithm.start_evolution(args.verbose)
    end = time()

    print("\n=== Done in {0:.3f} s".format(end - start))

    solution_image = solution.to_image()
    solution_image_name = "results/" + args.image.split("/")[1].split(".")[0] + "_" + str(args.n) + "_GA_sol.png"

    if args.save:
        cv2.imwrite(solution_image_name, solution_image)
        print("=== Result saved as '{}'".format(solution_image_name))

    print("=== Close figure to exit")
    # show_image(solution_image, "Solution")
