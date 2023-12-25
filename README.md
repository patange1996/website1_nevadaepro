# website1_nevadaepro
Module used: Selenium, scrapy, pandas

There are two spiders that you need to run in order to get the data.
1. nevadaepro_2: nevadaepro.py
2. nevadaepro_download_files: nevadaepro_download_files.py

You need to run as scrapy. Go to the main directory and run two commands:
scrapy crawl nevadaepro_2 -o final.json
scrapy crawl nevadaepro_download_files

Note: The first spider nevadapro_2 will scrape the data specified in the dict or json format.
Note: The second spider nevadaepro_download_files will download the attachments from the each url and store it in the downloaded_files in the homedirectory
Note: The first spder and second spider share a common database named database.csv where all the url's of the form reside. 
