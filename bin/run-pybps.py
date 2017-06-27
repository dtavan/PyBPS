"""

"""

import sys
import os

from pybps import BPSProject


if __name__ == '__main__':

    args = sys.argv[1:]
    if not args:
        print "usage: run-pybps.py [--ncore ncore] [--stopwatch] <projdir_path>";
        sys.exit(1)

    # ncore and stopwatch are either set from command line
    # or left as the empty string.
    # The args array is left just containing the dirs.
    ncore = 'max'
    if args[0] == '--ncore':
        ncore = int(args[1])
        del args[0:2]

    stopwatch = False
    if args[0] == '--stopwatch':
        stopwatch = True
        del args[0:1]

    if len(args) == 0:
        print "error: must specify one project directory"
        sys.exit(1)


    projdir_path = os.path.abspath(args[0])

	# Creatw new instance of BPSProject class to hold all of the info
	# about simulation project
    module = BPSProject(projdir_path)

    # Add simulation jobs to BPSProject instance
    module.add_jobs()

    # Run simulation jobs
    module.run(ncore, stopwatch)

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
