=====
PyBPS
=====

.. image:: https://img.shields.io/badge/python-2.7,_3.5-blue.svg

PyBPS is a simulation manager that provides a framework for running parametric simulation jobs in an efficient way.
It includes modules to:

* **Pre-process parametric simulation jobs** (prepare simulation input files with a specific set of parameters)

* **Run simulation jobs in parallel**, making the most of available processors to run the parametric jobs faster

* **Post-process simulation jobs**, by extracting results directly from simulation output files

* **Store simulation parameters and results** in an SQlite database and a set of CSV files for subsequent analysis

* **Produce a simulation run summary**, including execution times of all simulated jobs, warnings and errors.

The package uses ``pandas`` DataFrames to handle data, which opens a lot of possibilities in terms of data analysis.
Users can therefore leverage all of the power of the ``pandas`` package to analyze simulation results.
Using ``pandas`` also makes it very straightforward to plot results using the ``matplotlib`` package.


Installation
============

To install PyBPS, use pip::

    $ pip install pybps

If you have an earlier version of PyBPS already installed that you want to upgrade, just use::

    $ pip install pybps --upgrade

This will also upgrade PyBPS dependencies.

Additionally, you will need to install ``jupyter notebook`` and ``matplotlib`` to view and run the tutorial notebook::

    $ pip install jupyter matplotlib


Configuration
=============

Prior to using PyBPS, you first have to configure simulation tools options in the ``config.ini`` file located at the root of the ``pybps`` directory (usually ``C:\Python27\Lib\site-packages\pybps``).

Alternatively, you can also include a ``config.ini`` file in your project directory with a project specific configuration. PyBPS will override default configuration settings whenever a custom ``config.ini`` file is found in the project directory.

Currently, PyBPS works on Windows with the following building performance simulation tools:

* `TRNSYS v17 <http://trnsys.com>`_

* `DAYSIM v3.1b <http://daysim.ning.com>`_

Most of the configuration options should be left to their default value. However, the user should revise the following options:

Simulation tool installation directory
--------------------------------------
::

    [TRNSYS]
    Install_Dir = C:\TRNSYS17  # Default installation directory for TRNSYS v17

    [DAYSIM]
    Install_Dir = C:\DAYSIM   # Default installation directory for DAYSIM

**IMPORTANT:** If your DAYSIM install directory is different from the one above, you will also have to modify the ``DAYSIMPATH`` in the batch script ``pybps_daysim-exe.bat`` found in ``C:\Python27\Scripts``

Simulation result file extensions
----------------------------------

Simulation result files are files that might require post-processing and that will be exported to CSV and/or SQlite database.
::

    [TRNSYS]
    ResultFile_Extensions = .out, .month  # Default extensions for TRNSYS output files

    [DAYSIM]
    ResultFile_Extensions = .el.htm, .DA  # Default extensions for DAYSIM output files

In the current version of PyBPS, when working with TRNSYS, for the simulation results to be parsed automatically you must output monthly integrated results with a ``Type46``. All the results should go to a unique output file.
Future version of PyBPS will support additional TRNSYS output formats.

Simulation log file extensions
-------------------------------

Log files are files that are just kept for reference.
::

    [TRNSYS]
    LogFile_Extensions = .log  # Default extensions for TRNSYS log files

    [DAYSIM]
    LogFile_Extensions = _active.intgain.csv  # Default extensions for DAYSIM log files

Actually, DAYSIM does not produce log files, but since this field can't be left empty, just put here the extensions of files that won't need post-processing.

Template files search string
----------------------------

Used to identify which files are templates, that is, files containing parameter search strings to be replaced by real values.
Template filenames should contain the specified string.
::

    TemplateFile_SearchString = _Template   # Example: Model_Template.dck

Parameter sample files search string
------------------------------------

Used to identify which file contains the parameter sample, that is, file containing real values for all parameters found in template files.
Sample filenames should contain the specified string.
::

    SampleFile_SearchString = _Samples   # Example: Model_Sample.csv


Prerequisites
=============

In addition to the necessary configuration options commented above, there is a set of prerequisites to ensure PyBPS can work properly with your building simulation project.

Template Files
--------------

Template files have to be properly identified by putting the search string specified in ``config.ini`` in their filename.
For example, the template file for the ``3Dbuilding.dck`` project would be ``3Dbuilding_Template.dck``.

To properly work as a template file, it should contain parameter search strings in place of actual parameters that should be replaced by PyBPS in each simulation job.
**It is a requirement of PyBPS that all parameter search strings should be strings of characters with a leading $ sign.**
Valid parameter search strings would look like::

    $ORIENTATION  # Valid search string for ORIENTATION parameter
    $HEAT_SETPOINT # Valid search string for HEAT_SETPOINT parameter

Sample File
-----------

For every single parameter search string defined in the template files, there should be a corresponding column with values in the sample file.

Sample files should always be CSV files and be properly identified by putting the search string specified in ``config.ini`` in their filename.
For example, the sample file for the ``3Dbuilding.dck`` project would be ``3Dbuilding_Sample.csv`` and would contain the following information::

    ORIENTATION,HEAT_SETPOINT
    0,20
    0,21
    180,20
    180,21
    ...


Usage
=====

Shell Script
------------

The simplest way to start using PyBPS is by way of the shell script.

Just open a command line window and call ``run-pybps.py`` followed by the path to the BPS project directory. It should look like this::

    $ run-pybps.py C:\My_BPS_Project\

The script accepts optional arguments to control the number of local threads/processors to be used in simulation run and to calculate to total execution time.
For example, calling the script with the following arguments will limit to 2 threads/processors and returns the batch execution run time::

    $ run-pybps.py --ncore 2 --stopwatch C:\My_BPS_Project\


Package
-------

If you are already proficient with Python programming, you can get more control over the simulation workflow by directly using the methods of the ``PyBPS`` package in your own script.
The best way to start is probably by having a look at the ``run-pybps.py`` script mentioned above.
Anyway, here is a quick guide to the main methods and functions contained in the ``PyBPS`` package.

To get started, it is necessary to import the ``BPSProject`` class definition::

    From pybps import BPSProject

An instance of the ``BPSProject`` class should then be created, giving the path to the simulation project directory as an argument::

    path_to_bps_project = 'C:\BPS_PROJECT'
    bpsproj = BPSProject(path_to_bps_project)

During the instance creation process, the given directory is analyzed and all of the information necessary to run the simulation jobs is stored in the new instance: paths to simulation input files, details about simulation tool to be used, parameter sample, etc...
Once the new instance has been created, class methods can be used to manage the parametric simulation jobs.
For example, simulation jobs identified from the parameter sample can (and should) be added using the following method::

	  bpsproj.add_jobs()

This step creates instances of a ``BPSJob`` class for each one of the identified simulation jobs.
Additional functions can be written by the user to modify the parameter sample prior to adding jobs to the simulation project.
For example, it is possible to have several simulation input files listed in the project directory and select a different input file in each job based on specific parameter values.

A particular job can be manage using the following methods::

	  bpsproj.jobs[0].prepare()    # Copy all simulation files to a temp directory where the first job will be run
	  bpsproj.jobs[0].preprocess() # Create simulation input files with set of parameters for first job
	  bpsproj.jobs[0].run()        # Run the first job
	  bpsproj.jobs[0].close()      # Copy result and log files to results dir, get job run summary and delete temp dir

The decision of which result and log files should be copied to the *Results* directory depends on the files extensions specified in the *ResultFile_Extensions* and *LogFile_Extensions* keywords of the ``config.ini`` file.

In general, it is more common to run all simulation jobs at once.
Calling the ``run`` method without arguments launches simulation jobs in parallel using all available processors::

	  bpsproj.run()

You can also limit the number of threads/processors used to prevent PyBPS from eating up all of the available computing resources::

	  bpsproj.run(ncore=2)   # limits the current run to 2 threads/processors

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
