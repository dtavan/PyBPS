"""

"""

import sys
import os
import argparse

from pybps import BPSProject


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Run PyBPS parametric simulation manager.')

    parser.add_argument('model_path', help='path to folder containing model')
    parser.add_argument('--ncore', default=-1, type=int, help='Number of local cores used for parallel simulations (default: -1 to use all local cores)')
    parser.add_argument('--stopwatch', action='store_true', help='Enables stopwatch to return total simulation run time.')

    args = parser.parse_args()

    print(args)

    model_path = os.path.abspath(args.model_path)

	# Creatw new instance of BPSProject class to hold all of the info
	# about simulation project
    module = BPSProject(model_path)

    # Add simulation jobs to BPSProject instance
    module.add_jobs()

    # Run simulation jobs
    module.run(args.ncore, args.stopwatch)

    # Get jobs list, results and run summary into pandas DataFrames
    module.jobs2df()
    module.results2df()
    module.runsum2df()

    # Save jobs list, results and run summary DataFrames into sqlite database
    module.save2db()

    # Save jobs list, results and run summary DataFrames into csv files
    module.save2csv()

    # Save jobs list, results and run summary DataFrames into pickled files
    module.save2pkl()

    print("\nResults saved to following output files, located in '_pybps_results' directory:")
    print("- " + module.db_name)
    print("- " + module.jobs_fname + ".csv/.pkl")
    print("- " + module.results_fname + ".csv/.pkl")
    print("- " + module.runsum_fname + ".csv/.pkl")
