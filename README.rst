**********
FlashLight
**********
The Visualization Tool For Your NeuralNetwork
--------------------------------------

.. image:: https://travis-ci.org/dlguys/flashlight.svg?branch=master
   :target: https://travis-ci.org/dlguys/flashlight
.. image:: https://api.codeclimate.com/v1/badges/54045484eb16f44c7c2f/maintainability
   :target: https://codeclimate.com/github/dlguys/flashlight/maintainability
   :alt: Maintainability
.. image:: https://api.codeclimate.com/v1/badges/54045484eb16f44c7c2f/test_coverage
   :target: https://codeclimate.com/github/dlguys/flashlight/test_coverage
   :alt: Test Coverage
.. image:: https://readthedocs.org/projects/flashlight/badge/?version=latest
   :target: http://flashlight.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

FlashLight is built to make model interpretation easy. Rather than just being a visualization tool we wanted to make a playground for researchers and developers to debug the neural network and playe around with the graph. FlashLight currently supports only PyTorch model visualization but we are tyring to make it compatible with GLUON and TensorFlow eager.

Usage
=====
FlashLight has very intuitive and non-exhaustive list of APIs available. The FlashLight object creation expects the user to pass the neural net instance

>>> import FlashLight
>>> net = NeuralNet()
>>> viz = FlashLight(net)

Calling the functional APIs saves the data to the FlashLight home folder which is by default ``$USERHOME/.flashlight``
FlashLight installation creates the command line interface which also to call the FlashLight server. FlashLight server collects the data from FlashLight home folder and serves in the browser.

Installation
============
FlashLight uses `sanic`_ as backend server. Sanic is dependant on python ``async`` and ``await`` and hence won't work with versions < python 3.5

If your code base is python 3.5+,
--------------------------------
Everything works fine by installing FlashLight from pip. This will give you access to importable FlashLight package and command line interface that instantiates the Sanic server
``pip install flashlight``

If your code base is using python version < 3.5,
-----------------------------------------------
In this case, you are in bit trouble. We have created a separate FlashLight client for you to import in your script but FlashLight server still have to be with python3.5+, that means, you'll end up installing ``flashlight-client`` in your environment that uses older version of python and you need to create an environement with new version of python for running the FlashLight server. We really wanted to help you and hence we had created docker image also for you. Step for people who uses older version of python will be updated once we have a beta release.


.. _sanic: https://github.com/channelcat/sanic

Full Documentation is available in `readthedocs`_ 

.. _readthedocs: http://flashlight.readthedocs.io/