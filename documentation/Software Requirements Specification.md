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

The mode is designed to search TV series and view detail information about the series selected by the user.
  
Main scenario:
* User enters the name of the series in search box and presses button “Search”;
* Application displays a list of series found in the database of myshows.me.

![alt-текст](https://github.com/incx07/epam-lab/blob/develop/documentation/images/003.JPG "Picture 01")
