.. BitPacket documentation master file, created by
   sphinx-quickstart on Tue Dec 22 19:38:18 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to BitPacket's documentation!
=====================================

BitPacket_ is a Python module that provides a simple objected-oriented
representation of packets. The main purpose is to provide an easy and
extensible interface for building and parsing packets.

These are the main features of BitPacket:

- Packets can be packed/unpacked to/from bytes.
- Allows meta-fields, that is, fields that depend on other fields.
- A packet can have single bit fields.

.. _BitPacket: http://www.nongnu.org/bitpacket/

Manual
======

.. toctree::
   :numbered:
   :maxdepth: 4

   intro
   concepts
   fields-base
   fields-numeric
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

