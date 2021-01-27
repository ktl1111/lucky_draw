# lucky_draw
A lucky draw program for company year-end party

## Setting up
* Install modules

		pip install Django
		pip install pandas 
		pip install xlwt
		pip install xlsxwriter 
		pip install playsound 
		pip install pyglet
		pip install Pillow 

* Add in people to lucky/app/static/app/PEOPLE_LIST.txt as one column 
* Add in prizes to lucky/app/static/app/PRIZE_LIST.txt as one column 
* **DO NOT include new line at the end of the rows**

## Notes
The winsound module can only run on Windows

## Run server
``python manage.py runserver``
