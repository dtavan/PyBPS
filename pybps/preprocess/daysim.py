"""
A set of functions required to pre-process DAYSIM simulation input files
"""

# Common imports
import os
import re

# Custom imports
from pybps import util

# Handle Python 2/3 compatibility
from six.moves import configparser
import six

if six.PY2:
  ConfigParser = configparser.SafeConfigParser
else:
  ConfigParser = configparser.ConfigParser


def rotate_scene(model_abspath):
    """Rotate Radiance geometry in Daysim project"""

	# Get information from config file
    conf = SafeConfigParser()
    conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
        '..\config.ini')
    conf.read(conf_file)
    bin_dir = os.path.abspath(conf.get('DAYSIM', 'Bin_Dir'))
    rotatescene_path = os.path.join(bin_dir, 'rotate_scene.exe')

    # Call rotate_scene program
    cmd = [rotatescene_path, model_abspath]
    util.run_cmd(cmd)

    # Rename rotated .rad and .pts files
    work_dir = os.path.dirname(model_abspath)
    for root, dirs, files in os.walk(work_dir):
        for fname in files:
            if fname.endswith('rotated.rad') or fname.endswith('rotated.pts'):
                old = os.path.join(root, fname)
                new = os.path.join(root, fname[:-12])
                # Try to rename filename
                # Remove new_fname if already exists because os.rename can't
                # overwrite existing files on Windows
                try:
                    os.rename(old, new)
                except WindowsError:
                    os.remove(new)
                    os.rename(old, new)


def radfiles2daysim(model_abspath):
    """Call radfiles2daysim program to convert source rad file to
    daysim material and geometry rad files"""

	# Get information from config file
    conf = SafeConfigParser()
    conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
        '..\config.ini')
    conf.read(conf_file)
    bin_dir = os.path.abspath(conf.get('DAYSIM', 'Bin_Dir'))
    radfiles2daysim_path = os.path.join(bin_dir, 'radfiles2daysim.exe')

    # Call radfiles2daysim program
    cmd = [radfiles2daysim_path, model_abspath, '-g', '-m', '-d']
    util.run_cmd(cmd)
