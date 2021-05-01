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

### 1. Search and view detail information about TV series

The mode is designed to search TV series and view detail information about the series selected by the user.
  
Main scenario:
* User enters the name of the series in search box and presses button “Search”;
* Application displays a list of series found in the database of myshows.me;

<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/003.JPG" alt="Picture 01" width="800"/>

* User chooses wanted series (all names are clickable);
* Application displays detailed information about the series (includes the name of the series, poster, description, current status, country of production, number of seasons, rating on kinopoisk.ru and imdb.com).

<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/004.JPG" alt="Picture 02" width="800"/>
  
### 2. Adding TV series to own watch lists

If user logs into the app, he can add the series to his own lists (two buttons are available: "Going to watch" and "Watched all"):

<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/005.JPG" alt="Picture 03" width="800"/>
  
Main scenario (when user clicks button "Going to watch"):
* The series is added to the "Going to watch" list (available on the main page);
* The "Going to watch" button becomes unavailable (disappears);
* On the page of the series appears the inscription "I am going to watch this show!".

<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/006.JPG" alt="Picture 04" width="800"/>

Main scenario (when user clicks button "Watched all"):
* The series is added to the "Watched all" list (available on the main page);
* If the series was previously added to the "Going to watch" list - it is removed from there;
* Buttons "Watched all" and "Going to watch" become unavailable (disappear);
* On the page of the series appears the inscription "I fully watched this show!".

<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/007.JPG" alt="Picture 05" width="800"/>