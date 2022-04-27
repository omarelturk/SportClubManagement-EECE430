# SportClubManagement-EECE430

## Django SportsClub Management System
## Steps to Run the Project 

**Step 1 - Django Environment Preparation (If you don't already have a django Virtual Environment)** 
``` 
The following steps are provided by Professor Ali Moukalled
Steps to install Django2.0.1 with Python3.6.4 on windows 64bits
C:\>pip3 install virtualenvwrapper-win
C:\>mkvirtualenv my_env		//you can replace my_env with any name

This will create an environment to run Django. You can run the following DOS commands on the environment:
1.	workon: lists available virtual environment , because you can run many mkvirtualenv
2.	workon env_name:  to activate specific environment
3.	deactivate: to exit the virtual environment
4.	rmvirtualenv env_name: to remove specific environment

C:\>workon my_env
(my_env) C:\>pip3 install django			//to install Django in the virtual env.

``` 
**Step 2 - Clone the repository** 
``` 
(my_env) C:\>git clone https://github.com/omarelturk/SportClubManagement-EECE430.git
(my_env) C:\>cd SportClubManagement-EECE430
(my_env) C:\SportClubManagement-EECE430>cd scms
``` 
**Step 3 - Running the project** 
Make sure you are working on my_env & correct path
First, Install the required python libraries as follows: 
``` 
(my_env) C:\scms>pip install netifaces pillow requests django-crispy-forms
``` 

SETUP is done … let’s see if it works
``` 
(my_env) C:\scms>python manage.py runserver 0.0.0.0:8000 
``` 
Few lines will be displayed and a message showing you how to quit
Leave this DOS session running (minimize the screen if you like) and,
Open any browser and type the following URL: 
Your_computer_ip_address:8000
Example 127.0.0.1:8000
Or localhost:8000 (localhost instead of ip_address)

Click on the link provided, it will direct you to the django application 

*Navigate through the web application and enjoy its features ツ* 
