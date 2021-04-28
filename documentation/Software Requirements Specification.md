## Introduction

There is my training Django-project for EPAM.

______________

## Overall Description

“MyShows App” is web-application which allows users to show information about TV series. Information is generated from base of myshows.me (API based on [JSON-RPC](https://api.myshows.me/shared/doc/)).
  
Users can:
* Search and view detail information about any TV series;
* Add TV series to their own watch lists (“Going to watch”, “Watched all”);
* Delete the records from list “Going to watch”;
* Set the rating for the series from list “Watched all”.
  
Information about users and added series is stored in a separate database.
______________

## System features

### Search and view detail information about TV series

The mode is designed to search TV series and view detail information about the series selected by the user.
  
Main scenario:
* User enters the name of the series in search box and presses button “Search”;
* Application displays a list of series found in the database of myshows.me.

<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/003.JPG" alt="Picture 01" width="800"/>

* User chooses wanted series (all names are clickable).
* Application displays detailed information about the series (includes the name of the series, poster, description, current status, country of production, number of seasons, rating on kinopoisk.ru and imdb.com).

<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/004.JPG" alt="Picture 02" width="800"/>