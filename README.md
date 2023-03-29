A work in progress, this project started as a solution the Codewars problem "Break the Pieces" without using numpy/array processing libraries.
The goal of the problem is to identify and reproduce the "smallest pieces" of an image represented by rows of the characters '+', '-', '|', ' '; more detail and examples at https://www.codewars.com/kata/527fde8d24b9309d9b000c4e
I have tried to approach it using topological methods, as the problem is asking for the minimal generating set (ignoring basepoint) of the fundamental group of the planar graph "G" represented by the text input (\pi_1(G))
With the initial problem solved, I now plan to add more functionality to the compute_generator and grid modules, so that they may be applied to similar problems, for instance, finding the largest set of (not necessarily simple) cycles in the graph that contain a given cycle as a subcycle or in their interiors.

Written in Python 3.8.
The simple_generators program can be run from command line, passing a text file containing one line (with newline chars) per graph to process.
