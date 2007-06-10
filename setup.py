
from distutils.core import setup

setup(name = 'BitPacket',
      version = '0.1.0',
      author = 'Aleix Conchillo Flaque',
      author_email = 'aleix@member.fsf.org',
      license = 'GPL',
      maintainer = 'Aleix Conchillo Flaque',
      maintainer_email='aleix@member.fsf.org',
      url='http://hacks-galore.org/aleix/BitPacket',
      requires = ['BitVector'],
      packages = ['BitPacket'],
      py_modules = ['BitPacket.BitStructure', 'BitPacket.BitField',
                    'BitPacket.Common'],
      description='A Python representation for bit field structures',
      long_description=
      '''
      This module presents an objected oriented representation for bit
      field structures.
      ''')
