import requests
from bs4 import BeautifulSoup
import random
from fake_useragent import UserAgent

def scrape_linkedin_jobs():
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    params = {
        'keywords': 'software',
        'location': 'remote',
        'start': 0,
        'f_TPR': 'r86400'  
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        job_cards = soup.find_all('div', class_='base-card')[:5]  # Limit to 5 jobs
        jobs = []
        for card in job_cards:
            title = card.find('h3', class_='base-search-card__title').text.strip()
            company = card.find('h4', class_='base-search-card__subtitle').text.strip()
            location = card.find('span', class_='job-search-card__location').text.strip()
            job_url = card.find('a', class_='base-card__full-link')['href'].split('?')[0]
            job_type = "Internship" if "intern" in title.lower() else "Job"
            jobs.append({
                "title": title,
                "job_type": job_type,
                "company": company,
                "location": location,
                "work_mode": "Remote" if "remote" in location.lower() else "Not specified",
                "salary": "Not disclosed",
                "tech_stack": "Not specified",  
                "apply_link": job_url
            })
        return jobs
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    jobs = scrape_linkedin_jobs()
    for idx, job in enumerate(jobs, 1):
        print(f"{idx}. {job['title']} ({job['job_type']}) at {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Work Mode: {job['work_mode']}")
        print(f"   Salary: {job['salary']}")
        print(f"   Tech Stack: {job['tech_stack']}")
        print(f"   Apply: {job['apply_link']}")
        print("-" * 80)