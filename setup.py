#!/usr/bin/env python

import os
import os.path
import subprocess

from setuptools import setup
from setuptools.command.sdist import sdist as _sdist

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def subprocess_check_output(*popenargs, **kwargs):
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')

    process = subprocess.Popen(stdout=subprocess.PIPE, stderr=subprocess.STDOUT, *popenargs, **kwargs)
    stdout, stderr = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = ' '.join(*popenargs)
        raise Exception("'%s' failed(%d): %s" % (cmd, retcode, stderr))
    return (stdout, stderr, retcode)

pkg_version = "master"

def modify_specfile():
    cmd = (' sed -e "s/@VERSION@/%s/g" < python-psphere.spec.in ' % pkg_version) + " > python-psphere.spec"
    print cmd
    os.system(cmd)

class sdist(_sdist):
    """ custom sdist command to prepare python-psphere.spec file """
    def run(self):
        modify_specfile()
        _sdist.run(self)

setup(name="python-psphere",
      version=pkg_version,
      description="vSphere SDK for Python",
      long_description=read("README.rst"),
      author="Jonathan Kinred",
      author_email="jonathan.kinred@gmail.com",
      url="https://github.com/jkinred/psphere",
      packages=["psphere"],
      package_data={"psphere": ["wsdl/*"]},
      install_requires=["suds", "PyYAML"],
      keywords=["vsphere", "vmware"],
      classifiers=["Development Status :: 4 - Beta",
                   "License :: OSI Approved :: Apache Software License"],
      cmdclass = {'sdist': sdist}
     )

