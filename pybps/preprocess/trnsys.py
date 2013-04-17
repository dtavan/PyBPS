"""
A set of functions required to pre-process TRNSYS simulation input files
"""

import os
import re
from ConfigParser import SafeConfigParser

from pybps import util


def gen_type56(model_abspath, select='all'):
    """Generates Type56 matrices and idf files"""
	
	# Get information from config file
    conf = SafeConfigParser()
    conf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
        '..\config.ini')
    conf.read(conf_file)
    trnbuild_path = os.path.abspath(conf.get('TRNSYS', 'TRNBuild_Path'))
    trnsidf_path = os.path.abspath(conf.get('TRNSYS', 'trnsIDF_Path'))

    # Get b17 file path from deck file
    pattern = re.compile(r'ASSIGN "(.*b17)"')
    with open(model_abspath, 'rU') as m_f:
        temp = m_f.read()
        match = pattern.search(temp)
        # TRNBUILD is only called if Type56 is found in deck file.
        if match:
            b17_relpath = match.group(1)
            b17_abspath = os.path.join(os.path.dirname(model_abspath), b17_relpath)
            # Generate shading/insolation matrix
            if select == 'all' or select == 'matrices' or select == 'masks':
                cmd = [trnbuild_path, b17_abspath, '/N', '/masks']
                util.run_cmd(cmd)
            # Generate view factor matrix
            if select == 'all' or select == 'matrices' or select == 'vfm':					
                cmd = [trnbuild_path, b17_abspath, '/N', '/vfm']
                util.run_cmd(cmd)
            # Generate trnsys3D idf file, to view geometry in Sketchup
            if select == 'all' or select == 'idf':				
                cmd = [trnsidf_path, b17_abspath]
                util.run_cmd(cmd)

