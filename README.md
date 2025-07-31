# Job Scraper Codes
As a prerequisite to my Job Hunter project, I implemented these codes to scrape job listings from companies. 

Link to the Job Hunter project: https://github.com/pavit15/job-hunter

## Features
Scrapes job listings from Microsoft, LinkedIn, RemoteOK, Google, and Amazon

Extracts key information such as:

1. Job/Internship title

2. Job type (Job/Internship)

3. Location (city, country, continent)

4. Work mode (Remote/Hybrid/On-site)

5. Salary information (when available)

6. Tech stack requirements

7. Direct apply links

## Implemetation

To use these codes, clone the repository, install the requirements from requirements.txt, and you can individually run:

```bash
git clone https://github.com/pavit15/job-scraper-codes.git
cd job-scraper-codes
pip install -r requirements.txt
```
Then run the individual scripts:

```bash
python microsoftscraper.py
python linkedinscraper.py
python remoteok.py
python googlescraper.py
python amazonscraper.py
```
   
## Output 

Sample Output
```bash
1. Software Engineer (Job)
   Location: Redmond, United States (North America)
   Work Mode: Hybrid
   Salary: Not disclosed
   Tech Stack: Python, Java, Azure
   Apply: https://careers.microsoft.com/...
--------------------------------------------------
```

## Note

Some companies may block scrapers, so if you get empty results:

1. Try changing your IP (use a VPN)

2. Reduce request frequency

3. Check if the website structure has changed

4. Salary information is rarely available in public listings

5. For LinkedIn scraping, you may need to use rotating proxies

6. Implement delays between requests
