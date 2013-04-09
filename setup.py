from distutils.core import setup

setup(
    name='pybps',
    version='0.1.0',
    description='A parametric simulation manager for building performance simulation projects',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Operating System :: Microsoft :: Windows',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering',
    ],
    keywords='building performance simulation parametric TRNSYS DAYSIM',
    url='http://github.com/aiguasol/pybps',
    author='Damien Tavan',
    author_email='damien.tavan@aiguasol.coop',
    license='BSD',
    packages=['pybps','pybps.preprocess','pybps.postprocess'],
    package_data={'pybps': ['config.ini']},
    install_requires=[
        "pandas",
    ],
)