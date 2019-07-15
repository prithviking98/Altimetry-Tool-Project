This is an altimetry tool made by Prithvi Raj Nair and Abhiroop Bhattacharjee of 
BITS Pilani (summer 2018) under the guidance of Dr. S.P. Aggarwal (Head, WRD)

================================================= OVERVIEW ======================================================

the following is a brief description of what all it does.

1) the python scripts main.py, downlaod.py and process.py present in code/webGUI/
are the scripts used for the automation of the process of checking for new satellite
data, downlaoding if new file is available and processing it to get the altitude for the desired locations 
( We added as many locations as possible where the satellite tracks intersect with water bodies which are wide enough) 
[instructions to run it are given further below]

2) We have made a Django web app for the website [instructions to locally host the website on this computer given futher below]. 
It has the following three views

  a) addLoc - this view was made for our backend internal use to ease the process of finding locations where the satellite track 
intersects with waterbodies and to add those locations to the data base 
(IMPORTANT NOTE: If the web app is ever going to be publicly hosted, then this view should not be made public as obviously public 
should not be allowed to add locations arbitrarily).
  If you ever have to add locations (in India you won't need to, we have made an exhaustive search for suitable locations for 
Jason 2 and Jason 3) then just locally host the web app and add the desired location (very simple to use, when you open the 
webpage it will be self explanatory)

  b) plotter - This view is where user can see virtual gauges, search for locations, and click on the points to get plots of 
elevation vs time (instructions on use of this webpage are given as a helpbox on the webpage itself)

  c) plot views (plotMss/plotGeoid) - these views show the plots and tabular data when a point is clicked

================================VIRUTAL ENVIRONMENTS ==================================================================
you can read about creating virtual environments here https://docs.python.org/3/tutorial/venv.html

the required packages for running the software are present in app/code/webGUI/requirements.txt

=================================== HOW TO RUN THE AUTOMATIC DOWNLOAD SCRIPT ===========================================

1)open the folder Altimetry Tool project BITS Pilani (summer 2018)/app  in command prompt

2) activate the virtual environment by using the following command -
> source env/bin/activate

3) change into app/code/webGUI folder

4) run the main.py script using the following command-
> python main.py

done!

==HOW IT WORKS==
main.py checks for the existence of a new file for jason 2 or 3 at the following 
URLS:
https://data.nodc.noaa.gov/jason2/ogdr/ogdr/
https://data.nodc.noaa.gov/jason3/ogdr/ogdr/

The name of the last downloaded file is stored in app/data/last/JAx_last.txt .

So everytime the script is run, it starts of from where it left off the last time.
As long as the script is running, it will check for and download all the new files available until no more new files are available. 

The code is a continuous loop so it just keeps running and checking for new files
and downloads them as and when they appear.

If for some reason the downlaod is affected or computer is turned off then fear
not, just restart main.py as given in the instructions above and it will pick up where it left off.

download.py is in charge of downlaoding the netCDF files. Everytime a new netCDF file is downloaded, it overwrites the existing file 
so that the netCDF files don't clutter the computer. 

The process.py module processes each file and checks if any location in the database is available in that file. If yes it adds the 
corresponding elevation to the database. This is the only source of increasing data for this software so it requires very little space.


======================================== HOW TO LOCALLY HOST THE WEB APP ====================================================

1)open the folder Altimetry Tool project BITS Pilani (summer 2018)/app  in command prompt

2) activate the virtual environment by using the following command -
> source env/bin/activate

3) change into app/code/webGUI folder

4) run the Django local host server
> python manage.py runserver

after running this command keep this terminal window open when you want to access the webapp
(press ctrl + C to stop the server)

4) open your browser, the URL for the views are as given below
addLoc - http://127.0.0.1:8000/addLoc/
plotter- http://127.0.0.1:8000/plotter/
admin  - http://127.0.0.1:8000/admin/

ABOUT DJANGO ADMIN: django admin is just a page which allows you to manage the website database. It will show you all the tables 
present in the database and allow you to modify/add/delete data. 
(IMPORTANT NOTE: this view also shouldn't be hosted publicly)
the credentials for the admin super user for this web app are as given below
username: admin
password: adminpassword

================================================================================================================================

This is a brief README on how to run the code given with this tool. A more detailed description of the different functions used 
can be found in the final report we submitted in completion of this project. 
