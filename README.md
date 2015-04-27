hk-news-scrapper
==========

A scrapper of Hong Kong news.  It is a spin-off from [the backend of NewsDiff HK](https://github.com/code4hk/Newsdiff-Backend).

Dev Environment Setup
---------------------

Install mongodb and start it up:

    $mongod --dbpath <path to ur dev db>

To create a virtual environment and install the dependencies:

    $ virtualenv -p python3 newsdiff
    $ source newsdiff/bin/activate
    $ pip3 install -r requirements.txt

To run the scraper:
	
	$ python3 main.py &

To track the log:

	$ tail news_diff.log -f

To deactivate the virtual environment after use:

    $ deactivate
   
