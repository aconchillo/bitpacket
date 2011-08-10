.. BitPacket documentation master file, created by
   sphinx-quickstart on Tue Dec 22 19:38:18 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to BitPacket's documentation!
=====================================

BitPacket_ is a Python module that provides a simple objected-oriented
representation of data structures. The main purpose is to provide an
easy and extensible interface for building and parsing these structures,
such as network packages.

These are the main features of BitPacket:

- Data can be packed/unpacked to/from bytes.
- Works with single bit fields.
- Provides and extensible framework to customize data representation.
- Allows meta-fields, that is, fields that depend on other fields.

.. _BitPacket: http://www.nongnu.org/bitpacket/

Manual
======

.. toctree::
   :numbered:
   :maxdepth: 4

   intro
   concepts
   fields-base
   fields
   containers
   writers

API reference
=============

.. toctree::

   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

