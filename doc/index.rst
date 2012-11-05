Welcome to BitPacket
====================

BitPacket is a Python module that provides a simple objected-oriented
representation for data structures. The main purpose is to provide an
easy and extensible interface for building and parsing these structures
(e.g. network packets).

These are the main features of BitPacket:

- Byte-oriented with support for bit fields.
- Same BitPacket definition can be used for packing and unpacking data.
- Comes with an extensible framework to customize BitPackets
  representation (e.g. text tables, Gtk widgets).

If you don't like BitPacket, you might want to check construct_, another
python library to perform the same task in a completely different way.

.. _construct: http://construct.wikispaces.com/


Documentation
-------------

The documentation is still a work in progress, but it's almost
complete. Browse the manual_ online or download the PDF_.

.. _manual: manual.html
.. _PDF: BitPacket.pdf


Download
--------

BitPacket will be freely available for download under the terms of the
GNU General Public License version 3 (GPLv3).

*There is no public release yet.*

Start playing with BitPacket by cloning the git repository:

::

  $ git clone git://git.sv.nongnu.org/bitpacket.git

Or, if you only have HTTP access:

::

  $ git clone http://git.sv.nongnu.org/r/bitpacket.git

You can also browse it online_ if you prefer.

.. _online: http://github.com/aconchillo/bitpacket/
