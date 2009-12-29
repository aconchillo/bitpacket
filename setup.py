
from distutils.core import setup

setup(name = 'BitPacket',
      version = '1.0.0',
      author = 'Aleix Conchillo Flaque',
      author_email = 'aleix@member.fsf.org',
      license = 'GPL',
      maintainer = 'Aleix Conchillo Flaque',
      maintainer_email='aleix@member.fsf.org',
      url='http://www.nongnu.org/bitpacket',
      requires = [],
      packages = ['BitPacket', 'BitPacket.utils'],
      package_dir = {'BitPacket': 'src',
                     'BitPacket.utils': 'src/utils'},
      description = 'A Python object-oriented representation of packets',
      long_description =
      '''
      This module provides a simple objected-oriented representation
      of packets. The main purpose is to provide an easy and
      extensible interface for building and parsing packets.
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
