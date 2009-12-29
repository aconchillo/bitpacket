Introduction
============

Download
--------

BitPacket_ is maintained in Savannah_. Savannah is the central point
for development, maintenance and distribution of official `GNU
software`_ (and other non-GNU software, like BitPacket).

You can dowlonad the latest BitPacket release from the website_, or
alternativelly, you can also clone the Mercurial_ BitPacket
repository_.

::

    hg clone http://hg.savannah.gnu.org/hgweb/bitpacket/

.. _Savannah: http://savnnah.gnu.org
.. _GNU software: http://www.gnu.org/gnu/thegnuproject.html
.. _Mercurial: http://mercurial.selenic.com
.. _repository: http://hg.savannah.gnu.org/hgweb/bitpacket/
.. _website: http://www.nongnu.org/bitpacket/


Build and install
-----------------

BitPacket is distributed as a distutils_ module, so the usual commands
for building and installing distutils modules can be used.

Once the BitPacket tarball is decompressed, you can build BitPacket as
a non-root user:

::

    python setup.py build

If the built was successful, you can then install it, as root, with
the following command:

::

    python setup.py install

.. _distutils: http://docs.python.org/distutils/

Now, you can use BitPacket in your application:

::

    from BitPacket import *


History
-------

The first version of BitPacket was released in 2007.

The validation guys, from the project I was working on, were building
a test enviroment to validate the DMU software (the Data Management
Unit payload software for the `LISA Pathfinder`_ satellite). All the
software involved a lot of packet management and they started by
accessing packet fields with indexes. This was very error prone, hard
to maitain, hard to read and understand and some more bad things. So,
I start digging through the web for something that could help us, but
I only found the struct_ module. The struct module is great, but it
does not solve the indexing problem. However, one is able to recover a
32-bit integer or float value without the need to access all four
bytes and build the value. Also, it does not solve the problem of bit
fields. Therefore, I wanted something easier to maitain, extend and
read and also able to work with bits.

Then, I found the BitVector_ class, which was able to work with bits
given a byte array, so I built BitPacket in top of it. Initially,
BitPacket consisted on three classes: BitField (for single bit
fields), BitStructure (a BitField itself, to build packets as a
sequence BitFields) and BitVariableStructure (something like a meta
BitStructure).

At the end of 2009, a refactoring of the test environtment was
necessary, and I knew BitPacket was very slow. This was because of the
BitVector class, as the main purpose of this class is not speed but
managing bits. Between 2007 and 2009, I discovered a great Python
library for building and parsing packets, construct_. construct is
great, it is a very complete and powerful library for working with
packets in a declarative way. The problem was that we had a lot of
code that could be reused written with BitPacket, so construct was not
an option.

Finally, I decided I needed to refactor BitPacket, while learning more
in the path, and create a small library, much simpler than struct but
much more powerful and fast than the old BitPacket, and this how
BitPacket 1.0.0 was born.


.. _BitPacket: http://www.nongnu.org/bitpacket/
.. _BitVector: http://cobweb.ecn.purdue.edu/~kak/dist/
.. _construct: http://construct.wikispaces.com/
.. _LISA Pathfinder: http://www.esa.int/esaSC/120397_index_0_m.html
.. _struct: http://docs.python.org/library/struct.html

