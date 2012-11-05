
from setuptools import setup, find_packages

setup(name = 'BitPacket',
      version = '1.0.0',
      author = 'Aleix Conchillo Flaque',
      author_email = 'aconchillo@gmail.com',
      license = 'GPLv3',
      maintainer = 'Aleix Conchillo Flaque',
      maintainer_email='aconchillo@gmail.com',
      url='http://www.nongnu.org/bitpacket',
      requires = [],
      package_dir = {'': 'src'},
      packages = find_packages('src'),
      description = 'A Python object-oriented representation for data structures',
      long_description =
      '''
      BitPacket is a Python module that provides a simple
      objected-oriented representation for data structures. The main
      purpose is to provide an easy and extensible interface for
      building and parsing these structures (e.g. network packets).

      These are the main features of BitPacket:

        * Byte-oriented with support for bit fields.

        * Same BitPacket definition can be used for packing and
          unpacking data.

        * Comes with an extensible framework to customize BitPackets
          representation (e.g. text tables, Gtk widgets).
      ''',
      classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Software Development :: Libraries :: Python Modules'
        ]
      )
