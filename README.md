# python-address-scraper

### Project Objective

- Create a program that extracts all valid addresses on each page of a website.
- Extract the data in the following format: country, region, city, postcode, road, and road numbers.

### Tech Stack

- Python (Beautiful Soup, Deepparse)
- MySQL

### Description

1. The program will first process the given file and return a list of domains. The list of domains will be sent in batches to the following function. Multithreading will be used to increase processing speed.
2. For each domain, the program will attempt to get its sitemap in order to find all of its pages. If the program cannot find the sitemap, it will return the root domain. 
3. The program will then use Beautiful Soup for each of the returned pages for HTML parsing. 
4. Once the HTML is parsed, the program will attempt to find address keywords. 
5. If there is a matching keyword in our text, the program will start looking for the address string via Regex. 
6. If address strings are found, they will be parsed via Deepparse.
7. Finally, results will be sent to the database.

### Improvements

- Using a service such as Google Address Validation API to check if the extracted addresses are valid as well as to determine country based on the extracted address.
- Using intermediate tables in order to increase the program’s performance.
- Using a different pretrained model such as fastText for higher address parsing precision.
