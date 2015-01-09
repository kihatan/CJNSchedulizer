Schedule Planning Website
=========================

This is our group's final project for EECS 183.  It is based off of the Schedule Planning Website offered through the class.  We wanted to make a website that would help us in our club, and this is what we thought would help us the most.

The point of this website is to help us organize our 50 - 60 members for our yearly gathering, Con Ja Nai.  At Con Ja Nai we have our members watch over materials such as PlayStation 3s and Projectors.  To help our members decide when they will be "on shift" we are making this site to show them their options and give them possible schedules they could sign up for based on their choices.  

To see our site in action, visit <a href="http://cjnschedulizer.herokuapp.com/" target="_blank"> cjnschedulizer.herokuapp.com </a> or download these packages and run them locally.

This database takes advantage of many of the features of Flask, as well as sqlalchemy, bootstrap, and javascript.  

Flask is used to let this website use Python script.  Our website takes advantage of a database to store information about different 'shows' that we are comparing.  Sqlalchemy is what we use to access this database and change cells inside of it.  We have used the base version of Bootstrap with some minor adjustments to make our website look more nice.  These include the nav-tabs feature as well as the buttons, panels, and columns that come along with it.  The fonts in our website are also the ones distributed with the Bootstrap distribution.  The website also takes advantage of many basic html elements such as tables, embeded videos, and viewing pdfs.

For practical use outside of simply our project, the included code could be useful for others planning on organizing staff for a large event.  The code in this project can be used with any database with the name of Shows and a similar setup:

  ID  |  NAME  |  TYPE  |  START  |  FINISH  |  LOCATION  |  PERSON1  |  PERSON2  |  LINK <br>
\-------------------------------------------------------------------------------------------

Where:<br>
ID:  The primary key of the database that lists the shows in order<br>
NAME:  The name of the show that the user will sign up for<br>
TYPE:  This became useless during development, but helps the user organize by event type<br>
START:  The start time of the event in minutes relative to 12AM (ex. 6:00 AM == 3600)<br>
FINISH:  The finish time of the event in minutes relative to 12AM<br>
LOCATION:  Where the event takes place<br>
PERSON1:  The first person signing up for a shift at the event<br>
PERSON2:  The second person signing up for a shift at the event<br>
LINK:  A YouTube link that will be navigated to in the embeded video when the link is clicked<br>

There is one MAJOR rule that needs to be followed in the original table for the application to work. PERSON1, PERSON2, and LINK need to be set to 'none' by default, otherwise the application will output that people are in those shifts and assign a dead link to the links.

The data in the table is used to fill in the spots in the table, so simply making a different database and uploading it will also change the options that appear online.  This site automatically understands and displays in groups items with the show types: Panel, Event, Show, Movie, and Table.

There are various expansions that could be made on this site.  Firstly, a page where administrators can go in and more easily change the data in the table would be nice.  For now, if a user inputs an innappropriate word as their name, the site administrator has to go in and change the database table to fix the error.  With the administrator page, this would be fixed.  Another extension would be to make all the data tables organizable by any of their factors.  For example, sorting by name or time could improve the user experience.  A final adjustment could be to adjust the site so that it looks good on all size monitors.  
