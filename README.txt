Testing crawler.py

Setup:
	1) Ensure you have the following installed on your machine
		- Python 2.7.9 ( https://www.python.org/downloads/release/python-279/ )
		- Bottle ( http://bottlepy.org/docs/dev/index.html )
		- Beautiful Soup ( http://www.crummy.com/software/BeautifulSoup/bs4/doc/ )

	2) Ensure the following files are in the same folder
		- crawler.py
		- urls.txt
		- test.py
		- testtemp0.tpl
		- testtemp1.tpl
		- testtemp2.tpl
		- testtemp3.tpl
		- crawler_test.py

	3) Navigate to the folder in the previous step using the terminal

Testing:
	1) In terminal, run test.py
		$ python test.py

	2) In new terminal, run crawler_test.py
		$ python crawler_test.py

	   If you can not open a new terminal, go back to step 1 and run test.py in the background and then run crawler_test.py
	   	$ python test.py &
	   	$ bg
	   	$ python crawler.py
