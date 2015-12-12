# our created modules
from parser import BNParser, QueryParser
from bayesnet import BayesNet

# other modules
import argparse
import time
from pprint import pprint

parser = argparse.ArgumentParser(description='Probabilistic reasoner based on Bayesian networks.')
parser.add_argument('bayesnet', type=argparse.FileType('r'), help='an input file where the Bayesian network is defined')
parser.add_argument('query', type=argparse.FileType('r'), help='an input file where the query and evidence are defined')
parser.add_argument('--verbose', '-v', action='store_true', help='explain what is being done')
args = parser.parse_args()

if __name__ == "__main__":

    # measure time
    start_time_program = time.time()

    print('Parsing Bayesian network from ' + args.bayesnet.name + '... ', end = '')
    bnp = BNParser(args.bayesnet)
