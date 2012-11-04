Introduction
============

Download
--------

BitPacket_ is maintained in Savannah_ (and mirrored in
github_). Savannah is the central point for development, maintenance and
distribution of official `GNU software`_ (and other non-GNU software,
like BitPacket).

You can download the latest BitPacket release from the project's
website_, or alternatively, you can also clone the source repository.

::

    git clone git://git.sv.gnu.org/bitpacket.git

Or, if you are behind a firewall, you might use the HTTP version:

::

    git clone http://git.savannah.gnu.org/r/bitpacket.git


.. _Savannah: https://savannah.nongnu.org/projects/bitpacket
.. _github: http://github.com/aconchillo/bitpacket/
.. _GNU software: http://www.gnu.org/gnu/thegnuproject.html
.. _website: http://www.nongnu.org/bitpacket/


Build and install
-----------------

BitPacket is distributed as a Distribute_ (setuptools) module, so the
usual commands for building and installing setuptools modules can be
used. However, this means that you need setuptools installed in your
system.

Once the BitPacket tarball is decompressed, you can build BitPacket as
a non-root user:

::

    python setup.py build

If the built is successful, you can then install it, as root, with the
following command:

::

    python setup.py install

.. _Distribute: http://packages.python.org/distribute/setuptools.html

Usage
-----

Using BitPacket in your application is straightforward. You only need
to add the following import in your Python scripts:

::

    from BitPacket import *


History
-------

The first version of BitPacket was released in 2007.

The validation guys from the project I was working on were building a
test environment to validate a software which involved a lot of network
packet management. They started by accessing packet fields with
indexes. This was very error prone, hard to maintain, hard to read and
hard to understand. So, I start digging through the web for something
that could help us, but I only found the struct_ module. However, it
does not solve the indexing problem neither it supports bit fields.

Then, I found the BitVector_ class which was able to work with bits
given a byte array, and I built BitPacket in top of it. Initially,
BitPacket consisted on three classes: BitField (for single bit
fields), BitStructure (a BitField itself, to build packets as a
sequence BitFields) and BitVariableStructure (something like a meta
BitStructure).

At the end of 2009, a refactoring of the test environment was
necessary, and I knew BitPacket was very slow and hard to
extend. Between 2007 and 2009, I discovered a great Python library for
building and parsing packets, construct_. construct is great and
performs its jobs very well. It is a very complete and powerful
library for working with packets in a declarative way. The problem was
that we had a lot of code that need to be reused written with
BitPacket, so construct was not an option.

Finally, I decided I needed to refactor BitPacket, while learning more
in the path, and create a small library, much simpler than struct and
much more powerful and fast than the old BitPacket. This is how
BitPacket 1.0.0 was born.

.. _BitPacket: http://www.nongnu.org/bitpacket/
.. _BitVector: http://cobweb.ecn.purdue.edu/~kak/dist/
.. _construct: http://construct.wikispaces.com/
.. _LISA Pathfinder: http://www.esa.int/esaSC/120397_index_0_m.html
.. _struct: http://docs.python.org/library/struct.html
