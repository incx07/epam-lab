## Introduction

There is my training Django-project for EPAM.

______________

## Overall Description

“MyShows App” is web-application which allows users to show information about TV series. Information is reading from base of myshows.me (API based on [JSON-RPC](https://api.myshows.me/shared/doc/)).
  
Users can:
* Search and view detail information about any TV series;
* Add TV series to their own watch lists (“Going to watch” and “Watched all”);
* Delete records from list “Going to watch”;
* Set the rating for the series from list “Watched all”.
  
Information about users and added series is stored in a separate database.
______________

## System features

### 1. View of the main page

At the top of the main page, a horizontal navigation bar is available to the user, which includes the following components: 
* the application name "MyShows App" (user can always return to the main page by clicking on it);
* search box and the “Search” button (used to search serials);
* the “Login / Registration” button (used to register and authorize user).

If user is not logged into the application - he has access only to search and view information about the series:

<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/002.JPG" alt="Picture 01" width="800"/>

If user has logged into the application - on the main page he has access to 2 columns with lists of TV series: "Going to watch" and "Watched all". In each column the maximum number of records is 5. If the number of added series is more than 5, pagination buttons become available. 
  
User can remove records from the "Going to watch" list (by clicking on the "cross" button). For a series from the "Watched all" list, user can rate it (by clicking the "Change" button).

<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/008.JPG" alt="Picture 02" width="800"/>

### 2. Search and view detail information about TV series

The mode is designed to search a TV series and view detail information about a series selected by user.
  
Main scenario:
* User enters the name of the series in search box and presses the “Search” button;
* Application displays a list of series found in the database of myshows.me;

<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/003.JPG" alt="Picture 03" width="800"/>

* User chooses wanted series by clicking (all names are clickable);
* Application displays detail information about the series (included the name of the series, poster, description, current status, show period, TV channel, country of production, number of seasons, rating on kinopoisk.ru and imdb.com).

<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/004.JPG" alt="Picture 04" width="800"/>

### 3. User registration (login) 

To register (login) in the application, user must click the “Login / Registration” button in the upper right corner of the page. 
  
After clicking, the user sees the login page:

<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/014.JPG" alt="Picture 05" width="800"/>

If user has an account, to login he needs to enter username, password and press the "login" button. After successful authorization, user will be redirected to the main page.
  
If the user does not remember his password, he can click on the "Forgot your password?" button, then enter the user’s registered email address and click the "Reset password" button. 
  
<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/015.JPG" alt="Picture 06" width="800"/>

After it, user will see the message: "We've emailed you instructions for setting your password. If they haven't arrived in a few minutes, check your spam folder."
 
Allows users to reset their password by generating a one-time use link that can be used to reset the password, and sending that link to the email. If the email address provided does not exist in the system, this view won’t send an email, but the user won’t receive any error message either. This information leaking to potential attackers prevents. 

If user is not registered in the application, he needs to click the "Registration?" button on the login page. After clicking, the user sees the register page:

<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/016.JPG" alt="Picture 06" width="800"/>

The page contains fields for entering a username, entering and confirming a password, and requirements for a username and password.

If user enters an invalid name, he will see the messages: "Enter a valid username. This value may contain only letters, numbers, and @ /. / + / - / _ characters" or "A user with that username already exists".
  
If user enters an incorrect password (password confirmation), he may see the following messages "This password is too short. It must contain at least 8 characters.", "This password is too common.", "This password is entirely numeric.", "The two password fields didn't match." (depending on the reason).
  
### 4. Adding TV series to own watch lists

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
  
### 5. Delete records from the “Going to watch” list

Main scenario:
* user clicks the "cross" button in the "Going to watch" column;
* The series is removed from the list;
* On the page of the series, the "Going to watch" button becomes available (user can add the series back). 

### 6. Set rating for the series from the “Watched all” list

* User clicks the "Change" button in the "Watched all" column;
* In the drop-down list, user selects a rating in the range from 1 to 5 (by default the series has no rating);
* User clicks the "Save" button;
* The selected rating is saved;
* User can change the rating by clicking on the "Change" button.

<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/013.JPG" alt="Picture 07" width="400"/>
  
<img src="https://github.com/incx07/epam-lab/blob/develop/documentation/images/012.JPG" alt="Picture 07" width="400"/>