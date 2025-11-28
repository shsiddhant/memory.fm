
.. _api.io:

============
Input/Output
============

.. currentmodule:: memoryfm

   
External Sources
~~~~~~~~~~~~~~~~

.. autosummary::
    :toctree: api/

    from_lastfm_api
    from_lastfmstats
    from_spotify
    from_spotify_zip

Canonical Sources
~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api/

   ScrobbleLog.from_json
   ScrobbleLog.from_parquet

Exports
~~~~~~~

.. autosummary::
   :toctree: api/

   ScrobbleLog.to_markdown


Canonical Exports
~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: api/

   ScrobbleLog.to_json
   ScrobbleLog.to_parquet
