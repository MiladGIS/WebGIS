# Spatial Layers Management Website

This practice involves creating a website using Flask to manage spatial layers. The website provides users with the ability to access more information about their Points of Interest. 

## User Registration and Login

Users are required to create an account to utilize this service. The registration process involves collecting the user's unique username, first name, last name, and password. After registration, the user is logged into the site and redirected to the main page. The login page collects the user's username and password. It also includes a link to the registration page for new users.The main page is accessible to logged-in users. If a user who is not logged in tries to access this page, they are redirected to the login page. 

The main page features:
1. A full-page map created with Openlayers 3+.
2. An OSM layer as default.
3.  WMS layers that have been previously published in Geoserver and styled.
4. A section where users can toggle their layers on and off.
5. A feature that allows users to click on any point on the map and, using the Geocode API available on the OpenMapQuest site, obtain and display the address and postal code of that point in an Overlay on the map.
