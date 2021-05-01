## Introduction

There is my training Django-project for EPAM.

______________

## Overall Description

“MyShows App” is web-application which allows users to show information about TV series. Information is generated from base of myshows.me (API based on [JSON-RPC](https://api.myshows.me/shared/doc/)).
  
Users can:
* Search and view detail information about any TV series;
* Add TV series to their own watch lists (“Going to watch” and “Watched all”);
* Delete records from list “Going to watch”;
* Set the rating for the series from list “Watched all”.
  
Information about users and added series is stored in a separate database.
______________

## System features

### 1. Search and view detail information about TV series

The mode is designed to search a TV series and view detail information about a series selected by user.
  
Main scenario:
* User enters the name of the series in search box and presses the “Search” button;
* Application displays a list of series found in the database of myshows.me;

<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/003.JPG" alt="Picture 01" width="800"/>

* User chooses wanted series (all names are clickable);
* Application displays detailed information about the series (includes the name of the series, poster, description, current status, country of production, number of seasons, rating on kinopoisk.ru and imdb.com).

<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/004.JPG" alt="Picture 02" width="800"/>
  
### 2. Adding TV series to own watch lists

If user logs into the app, he can add the series to his own lists (two buttons are available: "Going to watch" and "Watched all"):

<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/005.JPG" alt="Picture 03" width="800"/>
  
Main scenario (when user clicks the "Going to watch" button):
* The series is added to the "Going to watch" list (available on the main page);
* The "Going to watch" button becomes unavailable (disappears);
* On the page of the series appears the inscription "I am going to watch this show!".

<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/006.JPG" alt="Picture 04" width="800"/>

Main scenario (when user clicks the "Watched all" button):
* The series is added to the "Watched all" list (available on the main page);
* If the series was previously added to the "Going to watch" list - it is removed from there;
* Buttons "Watched all" and "Going to watch" become unavailable (disappear);
* On the page of the series appears the inscription "I fully watched this show!".

<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/007.JPG" alt="Picture 05" width="800"/>
  
### 3. View of the main page

If user is not logged into the application - he has access only to search and view information about the series:

<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/002.JPG" alt="Picture 06" width="800"/>

If user has logged into the application - on the main page he has access to 2 columns with lists of TV series: "Going to watch" and "Watched all". In each column the maximum number of records is 5. If the number of added series is more than 5, pagination buttons become available. 
  
User can remove records from the "Going to watch" list (by clicking on the "cross" button). For a series from the "Watched all" list, user can rate it (by clicking the "Change" button).

<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/008.JPG" alt="Picture 07" width="800"/>

### 4. Delete records from the “Going to watch” list

Main scenario:
* user clicks the "cross" button in the "Going to watch" column;
* The series is removed from the list;
* On the page of the series, the "Going to watch" button becomes available (user can add the series back). 

### 5. Set rating for the series from the “Watched all” list

* User clicks the "Change" button in the "Watched all" column;
* In the drop-down list, user selects a rating in the range from 1 to 5 (by default the series has no rating);
* User clicks the "Save" button;
* The selected rating is saved;
* User can change the rating by clicking on the "Change" button.

<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/013.JPG" alt="Picture 07" width="400"/>
  
<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/012.JPG" alt="Picture 07" width="400"/>