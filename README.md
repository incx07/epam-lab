# Myshows App

[![build](https://github.com/incx07/epam-lab/actions/workflows/build-docker.yml/badge.svg)](https://github.com/incx07/epam-lab/actions/workflows/build-docker.yml/) [![Coverage Status](https://coveralls.io/repos/github/incx07/epam-lab/badge.svg?branch=develop)](https://coveralls.io/github/incx07/epam-lab?branch=develop)

## Description

“MyShows App” is web-application which allows users to show information about TV series. Information is reading from base of myshows.me (API based on [JSON-RPC](https://api.myshows.me/shared/doc/)).
  
Users can:
* Search and view detail information about any TV series;
* Add TV series to their own watch lists (“Going to watch” and “Watched all”);
* Delete records from list “Going to watch”;
* Set the rating for the series from list “Watched all”.
  
Information about users and added series is stored in a separate database.

See [documentation](https://github.com/incx07/epam-lab/blob/step12/documentation/Software%20Requirements%20Specification.md) for more information.

## Installation

#### 1. Install Docker

Before installation the application you must download and install Docker. Refer to the following [link](https://docs.docker.com/get-docker/) and choose the best installation path for you.

#### 2. Clone repository from GitHub

Change the current working directory to the location where you want the cloned directory.

Type the following command:

    $ git clone https://github.com/incx07/epam-lab/

Press Enter to create your local clone.

## Run project

You must go to the working directory of project (where is docker-compose.yml). 

Then type the following command:

    $ docker-compose up --build

Press Enter to run project.

## Use project

The following addresses will be available after launch:

For the Web service:

* http://127.0.0.1:8000/api/ (provides access to the database)
* http://127.0.0.1:8000/api/auth/ (provides authentication system by djoser library)

For the Web application:

* http://127.0.0.1:8000/ (provides the user interface)
