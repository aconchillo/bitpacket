
from distutils.core import setup

setup(name = 'BitPacket',
      version = '0.2.0',
      author = 'Aleix Conchillo Flaque',
      author_email = 'aleix@member.fsf.org',
      license = 'GPL',
      maintainer = 'Aleix Conchillo Flaque',
      maintainer_email='aleix@member.fsf.org',
      url='http://hacks-galore.org/aleix/BitPacket',
      requires = [],
      packages = ['BitPacket'],
      package_dir = {'BitPacket': 'src'},
      description = 'A Python representation for bit field structures',
      long_description =
      '''
      This module presents an objected-oriented representation for bit
      field structures.
      ''',
      classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Software Development :: Libraries :: Python Modules'
        ]
      )
