
from distutils.core import setup

setup(name = 'BitPacket',
      version = '0.1',
      author = 'Aleix Conchillo Flaque',
      author_email = 'aleix@member.fsf.org',
      license = 'GPL',
      maintainer = 'Aleix Conchillo Flaque',
      maintainer_email='aleix@member.fsf.org',
      url='http://hacks-galore.org/aleix/BitPacket',
      requires = ['BitVector'],
      py_modules = ['BitStructure', 'BitField', 'Common'],
      description='A Python representation for binary packets',
      long_description=
      '''
      This class presents a pure-Python memory efficient packed
      representation for bit arrays.
      ''')
