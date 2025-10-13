
.. _usage-cli:

============
Command Line
============

Installing memory.fm gives you access to a command line tool 
``memoryfm``. 
You can use it to manage your Last.fm scrobble data and Spotify listening data.

.. note::
   Support for Apple Music exports is also planned. Check issue tracker for updates.


Using the commands
------------------

Some commands have subcommands with their own options. For instance, you can
import your `Last.fm <https://www.last.fm.com>`_ data obtained from 
`lastfmstats <https://www.lastfmstats.com>`_ like this:

.. sourcecode:: shell

   $ memoryfm import lastfmstats ~/Downloads/lastfmstats-siddhant.json
   Imported and saved to /home/siddhant/.local/share/memoryfm/imports/siddhant

Similarly, you can import spotify listening history like this:

.. sourcecode:: shell

   $ memoryfm import spotify ~/Downloads/my_spotify_data.zip --username sid-spotify
   Imported and saved to /home/siddhant/.local/share/memoryfm/imports/sid-spotify

.. note::
   You can have multiple imports, with the caveat that each username may only 
   have one import.

To see all import usernames, use the ``list`` command.

.. sourcecode:: shell

   $ memoryfm list
   Scrobble Logs:
   ['siddhant', 'sid-spotify']

Printing scrobbles/listens and top charts is very simple. First you use the 
``load`` command to load one of your imports.

.. sourcecode:: shell

   $ memoryfm load sid-spotify
   Loaded: sid-spotify

Now you can print your latest listens using the ``print`` command.

.. sourcecode:: shell

   $ memoryfm print --max-length 5
   ScrobbleLog for username: sid-spotify
   From 2025-06-03 21:33 to 2025-09-14 02:31

   | Timestamp        | Track           | Artist            | Album              | Duration   |
   |:-----------------|:----------------|:------------------|:-------------------|:-----------|
   | 2025-09-14 02:31 | Floating in the | Frightened Rabbit | The Midnight Organ | 00:04:14   |
   |                  | Forth           |                   | Fight              |            |
   | 2025-09-14 02:27 | Floating in the | Frightened Rabbit | The Midnight Organ | 00:04:14   |
   |                  | Forth           |                   | Fight              |            |
   | 2025-09-14 02:23 | Floating in the | Frightened Rabbit | The Midnight Organ | 00:04:14   |
   |                  | Forth           |                   | Fight              |            |
   Showing newest 3 out of 3121 listens

If you want to see which import is  loaded right now, you can use the 
``loaded`` command.

.. sourcecode:: shell
   
   $ memoryfm loaded
   Loaded import: sid-spotify

The command ``top`` can be used to see your top tracks/artists/albums.

.. sourcecode:: shell

   $ memoryfm top albums --n 5 --last month
   | Album                       |   Scrobbles |
   |:----------------------------|------------:|
   | The Midnight Organ Fight    |          31 |
   | Come In                     |          29 |
   | Songs About Leaving         |          16 |
   | 69 Love Songs               |           7 |
   | XO                          |           5 |

Finally, if you want to delete an import, you may use the ``import delete`` command.

.. sourcecode:: shell

   $ memoryfm import delete sid-spotify
   Are you sure you want to delete import sid-spotify? (Y/n):Y
   Import deleted: sid-spotify

To see what commands, subcommands, and options are available, use the 
``--help`` flag.

.. sourcecode:: shell

   $ memoryfm import --help
   Usage: memoryfm top [OPTIONS] KIND:{tracks|artists|albums}

   Print top n tracks/artists/albums. Optionally filter by dates or 
   timeperiod.

   Arguments 
    *    kind      KIND:{tracks|artists|albums}  [required]
   
   Options
    --import-name        TEXT
    --n                  INTEGER  [default: 10]
    --from-date          TEXT
    --to-date            TEXT
    --last               TEXT     Time period for the chart. Either (positive)
                                  integer number of days, or one of: week,
                                  month, year.
    --help                        Show this message and exit.              



Autocompletion
--------------

If you use bash, zsh, or fish, you can enable autocompletion with the 
``--install-completion`` flag.

.. sourcecode:: shell

   $ memoryfm --install-completion


Obtaining the scrobble/listening data
-------------------------------------

Last.fm
~~~~~~~

1. Visit `lastfmstats.com <https://lastfmstats.com>`_.
2. Put your Last.fm username. It might take a while as your scrobbles load.
3. Once scrobbles are loaded, choose JSON or CSV to export your data. 
   
**Small Tip:** Also click on the Browser button beside JSON to save your data in 
the browser. This way, the next time you want to export, only the new scrobbles
would need to be loaded.

Spotify
~~~~~~~

1. Go to `<https://www.spotify.com/us/account/privacy>`_ . You will need to login 
   with your Spotify account.
2. Request to get the extended listening history. It might take a few days 
   (2-3 days usually).
3. You will receive an email at the address used by your Spotify account.
4. Download the attached zip file (`my_spotify_data.zip`).
