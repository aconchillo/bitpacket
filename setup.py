
from distutils.core import setup

setup(name = 'BitPacket',
      version = '1.0.0',
      author = 'Aleix Conchillo Flaque',
      author_email = 'aconchillo@gmail.com',
      license = 'GPL',
      maintainer = 'Aleix Conchillo Flaque',
      maintainer_email='aconchillo@gmail.com',
      url='http://www.nongnu.org/bitpacket',
      requires = [],
      packages = ['BitPacket', 'BitPacket.utils'],
      package_dir = {'BitPacket': 'src',
                     'BitPacket.utils': 'src/utils'},
      description = 'A Python object-oriented representation of packets',
      long_description =
      '''
      BitPacket is a Python module that provides a simple
      objected-oriented representation of packets. The main purpose is
      to provide an easy and extensible interface for building and
      parsing packets.

      These are the main features of BitPacket:

        * Packets can be packed/unpacked to/from bytes.
        * Allows meta-fields, that is, fields that depend on other fields.
        * A packet can have single bit fields.
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
