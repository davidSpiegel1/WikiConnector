# Wiki Connector
Desktop application that involves connecting to various packaged APIs called _connectors_. These connectors store and deliver information to the user.

## Table Of Contents
1. [Installation](#installation)
2. [How It Works](#hiw)
1. [Updates](#subparagraph1)


## Installation
Clone the most recent version. Run the ``Main.py`` file within the ``src`` directory.

## How It Works
* Makes API calls that are dependent on the _connector_ that is being used.
* Utilizes a CSV file to aggregate data treated as a temporary database.
* Queries this file using a query language developed by myself.

## Updates
* added a query editor to the application
* Made the readme
* Changed to PyQt5 gui lib. Also added bash-like features to query language.
* Added an 'App' layer that has applications like terminal and settings. Also, have started on building connector layer.