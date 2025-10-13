
.. _quickstart.installation:

============
Installation
============

The package should soon be available on PyPI. For now, you can install 
directly from the repository with pip. 

.. sourcecode:: shell
   
   $ pip install "memory.fm @ git+https://github.com/shsiddhant/memory.fm.git"

`ScrobbleLog` dates are timezone aware. If you want your timezone to be automatically
found from your system, you need to install the package with the optional dependency 
group "timezone".

.. sourcecode:: shell

   $ pip install "memory.fm[timezone] @ git+https://github.com/shsiddhant/memory.fm.git"

.. note::
   You will need Python version 3.10 or above.

