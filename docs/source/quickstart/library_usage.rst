
.. _quickstart.usage.library:

.. currentmodule:: memoryfm

=============
Library Usage
=============


The library has two object classes:

1. Scrobble : Represents a single scrobbles/listen.
2. ScrobbleLog : Represents a sequence/log of scrobbles/listens.

Read and Parse
--------------

You can use :func:`from_lastfmstats` to read JSON/CSV downloads from
`lastfmstats <https://lastfmstats.com>`_ to create a ``ScrobbleLog`` instance.
Optionally, you can set a timezone using IANA strings.

.. ipython:: :okexcept:
   
   In [1]: import memoryfm as mfm
   
   In [2]: sclog = mfm.from_lastfmstats("lastfmstats-demo.csv", file_type="csv", tz="Asia/Kolkata")


.. seealso::
   See :func:`from_lastfm_api` to read scrobbling history using last.fm API, and :func:`from_spotify` and :func:`from_spotify_zip` for reading Spotify listening history.


Head and Tail
--------------

Like pandas DataFrames, memory.fm ScrobbleLog also have analogous
methods: :func:`ScrobbleLog.head` and :func:`ScrobbleLog.tail`. 

If no argument is passed, the first (``head``) or last (``tail``) 5 
scrobbles are extracted.

.. ipython::

   In [3]: print(sclog.tail())
   | Timestamp        | Track         | Artist      | Album             |
   |:-----------------|:--------------|:------------|:------------------|
   | 2025-09-13 12:48 | Wishes        | Beach House | Bloom             |
   | 2025-09-13 12:53 | Superstar     | Beach House | Once Twice Melody |
   | 2025-09-13 13:01 | New Romance   | Beach House | Once Twice Melody |
   | 2025-09-13 13:05 | Days of Candy | Beach House | Depression Cherry |
   | 2025-09-13 13:12 | All the Years | Beach House | Devotion          |
   
   
Slicing
-------

If you are familiar with pandas, the slicing works exactly like ``pd.DataFrame.iloc``.
Like most slicing in Python, index starts with 0. The start bound is *included*,
while the end bound is *excluded*.

.. ipython::
   
   In [4]: print(sclog[6:9])
   | Timestamp        | Track            | Artist         | Album       |
   |:-----------------|:-----------------|:---------------|:------------|
   | 2025-09-12 04:37 | Porcelain Hands  | Weatherday     | Come In     |
   | 2025-09-12 22:53 | So You Are Tired | Sufjan Stevens | Javelin     |
   | 2025-09-12 22:58 | And So It Goes   | Billy Joel     | Storm Front |


When start or end is omitted, the the corresponding bound doesn't apply.
So if you omit end, all scrobbles from start are included.

.. ipython::
   
   In [5]: print(sclog[16:])
   | Timestamp        | Track         | Artist      | Album             |
   |:-----------------|:--------------|:------------|:------------------|
   | 2025-09-13 13:01 | New Romance   | Beach House | Once Twice Melody |
   | 2025-09-13 13:05 | Days of Candy | Beach House | Depression Cherry |
   | 2025-09-13 13:12 | All the Years | Beach House | Devotion          |


Filter by Dates
---------------

You can filter a ``ScrobbleLog`` by dates using the method 
:func:`ScrobbleLog.filter_by_date`. You may pass the time alongside the date. 
The end date is included by default.

.. ipython::

   In [6]: print(sclog.filter_by_date("2025-09-12 10 PM", end="2025-09-13 10:40 AM"))
   | Timestamp        | Track                | Artist              | Album            |
   |:-----------------|:---------------------|:--------------------|:-----------------|
   | 2025-09-12 22:53 | So You Are Tired     | Sufjan Stevens      | Javelin          |
   | 2025-09-12 22:58 | And So It Goes       | Billy Joel          | Storm Front      |
   | 2025-09-12 23:16 | I Know               | Fiona Apple         | When the Pawn... |
   | 2025-09-13 10:30 | Epitaph for My Heart | The Magnetic Fields | 69 Love Songs    |
   | 2025-09-13 10:36 | Epitaph for My Heart | The Magnetic Fields | 69 Love Songs    |


If you'd like to exclude the end date, pass ``include_end = False`` to the method.

.. ipython::
   

   In [7]: print(sclog.filter_by_date(start="2025-09-12 10 PM", end="2025-09-13", include_end = False))
   | Timestamp        | Track            | Artist         | Album            |
   |:-----------------|:-----------------|:---------------|:-----------------|
   | 2025-09-12 22:53 | So You Are Tired | Sufjan Stevens | Javelin          |
   | 2025-09-12 22:58 | And So It Goes   | Billy Joel     | Storm Front      |
   | 2025-09-12 23:16 | I Know           | Fiona Apple    | When the Pawn... |


Top Charts
----------

Using the method :func:`ScrobbleLog.top_charts`,  you can obtain top ``n`` 
tracks/artists/albums from a ``ScrobbleLog``. The method returns a pandas Series,
with name: ``Scrobbles``. 


.. ipython::
  
   In [8]: print(sclog.top_charts(kind="album").to_markdown())
   | Album             |   Scrobbles |
   |:------------------|------------:|
   | Come In           |           7 |
   | 69 Love Songs     |           4 |
   | Once Twice Melody |           2 |
