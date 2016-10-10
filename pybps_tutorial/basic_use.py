import sys
import pybps

if __name__ == '__main__':

    args = sys.argv[1:]
    if not args:
        print "usage: pybs.py [--ncore ncore] [--stopwatch] <proj_dir>";
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
	
    print 'dir:', args[0]
	
	#proj_dir = os.path.abspath(args[0])
	
	# Check project folder for valid simulation project and
	# prepare simulation jobs
    #job_list = check_prep(proj_dir)
	
    # Run simulation jobs in parallel subprocesses
    #run_job_parallel(job_list, ncore, stopwatch)
    #run_job(job_list[0])