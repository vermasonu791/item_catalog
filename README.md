## Item Catalog Web App
This web app is a project for the Udacity.

## About
This project is a web application utilizing the Flask framework which accesses a SQL database that populates categories and their items. OAuth2 provides authentication for further CRUD functionality on the application. Currently OAuth2 is implemented for Google Accounts.

## For run that web app Install 
1.Vagrant
2.Virtual box
3.Clone Udacity vagrant folder

## How to Install
1. Install Vagrant & VirtualBox
2. Clone the Udacity Vagrantfile
3. Go to Vagrant directory and either clone this repo or download and place zip here
3. Launch the Vagrant VM (`vagrant up`) in terminal
4. Log into Vagrant VM (`vagrant ssh`) in terminal
5. Navigate to `cd/vagrant` as instructed in terminal
6. Go item_catalog directory use cd item_catalog
7. Setup application database python3 database_setup.py in terminal`
8. Insert data `use python3 gamedata.py`
9. Run application using project.py`
10. Access the application locally using http://localhost:5000 in browser


## Using Google Login
To get the Google login working there are a few additional steps:

1. Go to [Google Dev Console](https://console.developers.google.com)
2. Sign up or Login if prompted
3. Go to Credentials
4. Select Create Crendentials > OAuth Client ID
5. Select Web application
6. Enter name 'Item_Catalog'
7. Authorized JavaScript origins = 'http://localhost:5000'
8. Authorized redirect URIs = 'http://localhost:5000/login' && 'http://localhost:5000/gconnect'
9. Select Create
10. Copy the Client ID and paste it into the `data-clientid` in login.html
11. On the Dev Console Select Download JSON
12. Rename JSON file to client_secrets.json
13. Place JSON file in item-catalog directory 
14. Run application using `python project.py`

