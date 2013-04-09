=====
PyBPS
=====

PyBPS is a parametric simulation manager, mainly for the `TRNSYS <http://trnsys.com>`_ and `DAYSIM <http://daysim.ning.com>`_ simulation tools, although its features can easily be extended to other text-based input tools.
It provides a framework for running parametric simulation jobs and includes modules to:

* Pre-process parametric simulation jobs (prepare simulation input files with a specific set of paramaters)

* Run simulation jobs in parallel, making the most of available processors to run the parametric job faster

* Post-process simulation jobs, by extracting results directly from TRNSYS and DAYSIM output files

* Store simulation parameters and results in an SQlite database and a set of CSV files for subsequent analysis

* Produce a simulation run summary, including execution times of all simulated jobs, warnings and errors.

The package uses ``pandas`` DataFrames to handle data, which opens a lot of possibilities in terms of data analysis. Users can therefore leverage all of the power of the ``pandas`` package to analyze simulation results.
Using ``pandas`` also makes it very straightforward to plot results using the ``matplotlib`` package.


Installation
============

To install PyBPS, use pip::

    pip install pybps
	
	
Configuration
=============

Prior to using PyBPS, you first have to configure simulation tools options in *pybps/config.ini*

Most of the configuration options should be left to their default value. However, the user should revise the following options:

* Simulation tool installation directory

    *Install_Dir = C:\TRNSYS*
	
* Extensions of simulation result files

    *ResultFile_Extensions = .out, .month*

* Extensions of simulation log files

    *LogFile_Extensions = .log*
	
* Search strings for template files (used to identify which files are templates; template filenames should contain the specified string)
	
    *TemplateFile_SearchString = _Template*

* Search strings for parameter sample files (used to identify which files are parameter samples; sample filenames should contain the specified string)	

    *SampleFile_SearchString = _Sample*

	
Usage
=====

To get started, it is necessary to import the ``BPSProject`` class definition::

    From pybps import BPSProject
	
An instance of the ``BPSProject`` class should then be created, giving the path to the simulation project directory as an argument::

    path_to_bps_project = 'C:\BPS_PROJECT'
    bpsproj = BPSProject(path_to_bps_project)
	
During the instance creation process, the given directory is analyzed and all of the information necessary to run the simulation jobs is stored in the new instance: paths to simulation input files, details about simulation tool to be used, parameter sample, etc...
Once the new instance has been created, class methods can be used to manage the parametric simulation jobs. 
For example, simulation jobs identified from the parameter sample can be added using the following method::

	bpsproj.addjobs()

This step creates instances of a ``BPSJob`` class for each one of the identified simulation jobs. 
Additional functions can be written by the user to modify the parameter sample prior to adding jobs to the simulation project. 
For example, it is possible to have several simulation input files listed in the project directory and select a different input file in each job based on specific parameter values.

A particular job can be manage using the following methods::

	bpsproj.jobs[0].prepare()    # Copy all simulation files to a temp directory where the first job will be run
	bpsproj.jobs[0].preprocess() # Create simulation input files with set of parameters for first job
	bpsproj.jobs[0].run()        # Run the first job
	bpsproj.jobs[0].close()      # Copy result and log files to results dir, get job run summary and delete temp dir
	
The decision of which result and log files should be copied to the *Results* directory depends on the files extensions specified in the *ResultFile_Extensions* and *LogFile_Extensions* keywords of the ``config.ini`` file.
	
In general, it is more common to want to run all simulation jobs at once. 
Calling the ``run`` method without arguments launches simulation jobs in parallel using all available processors::

	bpsproj.run()
	

When all simulation jobs have been run, all of the information related to the current simulation project (job parameters, results and run summaries) can be stored in ``pandas`` DataFrames::
	
	bpsproj.jobs2df()
	bpsproj.results2df()
	bpsproj.runsum2df()
	
Once our simulation project data is in DataFrames, it can be stored in an SQlite database and/or CSV files::

	bpsproj.save2db()
	bpsproj.save2csv()
	
	
License
=======

This software is licensed under the ``3-clause BSD license``. See the ``LICENSE`` file in the top distribution directory for the full license text.


Contributors
============

PyBPS is open to contributions! Feel free to fork `the repository <http://github.com/aiguasol/pybps>`_ on github to start making your changes.
