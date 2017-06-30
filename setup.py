from setuptools import setup, find_packages

setup(
    name = 'pybps',
    version = '0.2.5',
    description = 'A parametric simulation manager for building performance simulation projects',
    long_description = open('README.rst').read(),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering',
    ],
    keywords = 'building performance simulation parametric TRNSYS DAYSIM',
    url = 'http://github.com/dtavan/pybps',
    author = 'Damien Tavan',
    author_email = 'damien.tavan@gmail.com',
    license = 'BSD',
    packages = find_packages(),
    package_data = {'':['*.ini']},
    install_requires = ['pandas'],
    scripts = ['bin/run-pybps.py','bin/pybps_daysim-exe.bat'],
)
