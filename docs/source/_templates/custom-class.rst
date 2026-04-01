{{ fullname | escape | underline }}

.. currentmodule:: {{ module }}

.. sqla-model:: ~{{ fullname }}

~~~~~~~~~~~~~~
Relationships
~~~~~~~~~~~~~~

.. autoclass:: {{ fullname }}
   :noindex:
   :members:
   :exclude-members: id, username, tz, timestamp, track, artist, album, user_id