#!/usr/bin/env python

# standard library imports
import os.path
import shutil
import subprocess
import sys

# third party related imports

# local library imports


def main(argv):

    cwd = os.path.abspath(os.path.dirname(__file__))
    pkg_dir = os.path.join(cwd, '..', 'serene_bardeen')
    config_file = os.path.join(pkg_dir, 'config.py')

    try:
        shutil.copy(os.path.join(pkg_dir, 'config_test.py'), config_file)
        subprocess.call(['nosetests'] + argv[1:])

    except subprocess.CalledProcessError:
        pass

    finally:
        os.path.exists(config_file) and os.unlink(config_file)


if __name__ == '__main__':

    main(sys.argv)
