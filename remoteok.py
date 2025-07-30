import requests
import json
from bs4 import BeautifulSoup

def scrape_remoteok_jobs():
    url = "https://remoteok.com/remote-python-jobs"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # First try the API endpoint
        api_url = "https://remoteok.com/api"
        params = {'tags': 'python'}
        response = requests.get(api_url, params=params, headers=headers, timeout=10)
        
        jobs = []
        
        # If API fails, fall back to HTML scraping
        if response.status_code != 200 or not response.text.strip():
            print("API failed, falling back to HTML scraping...")
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            job_rows = soup.find_all('tr', class_='job')[:5]  # Limit to 5 jobs
            
            for row in job_rows:
                try:
                    title = row.find('h2', itemprop='title').text.strip()
                    company = row.find('h3', itemprop='name').text.strip()
                    location = "Remote"
                    job_url = "https://remoteok.com" + row.find('a', class_='preventLink')['href']
                    
                    # Extract tags/tech stack
                    tags = [tag.text.strip() for tag in row.find_all('td', class_='tags')]
                    tech_stack = ", ".join(tags) if tags else "Not specified"
                    
                    jobs.append({
                        "title": title,
                        "job_type": "Internship" if "intern" in title.lower() else "Job",
                        "company": company,
                        "location": location,
                        "work_mode": "Remote",
                        "salary": "Not disclosed",
                        "tech_stack": tech_stack,
                        "apply_link": job_url
                    })
                except Exception as e:
                    print(f"Error parsing job listing: {e}")
                    continue
        else:
        
            try:
                
                json_str = response.text.strip()
                if json_str.startswith('[') and json_str.endswith(']'):
                    data = json.loads(json_str)
                else:
                    data = []
                
                for job in data[:5]:  
                    if isinstance(job, dict):
                        title = job.get('position', 'N/A').strip()
                        company = job.get('company', 'N/A').strip()
                        location = job.get('location', 'Remote').strip()
                        job_url = f"https://remoteok.com{job.get('url', '')}" if job.get('url', '').startswith('/') else job.get('url', '')
                        
                        jobs.append({
                            "title": title,
                            "job_type": "Internship" if "intern" in title.lower() else "Job",
                            "company": company,
                            "location": location,
                            "work_mode": "Remote",
                            "salary": job.get('salary', 'Not disclosed'),
                            "tech_stack": ", ".join(job.get('tags', [])) if job.get('tags') else "Not specified",
                            "apply_link": job_url
                        })
            except json.JSONDecodeError:
                print("Failed to parse API response as JSON")
                return []

        return jobs

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

if __name__ == "__main__":
    jobs = scrape_remoteok_jobs()
    for idx, job in enumerate(jobs, 1):
        print(f"{idx}. {job['title']} ({job['job_type']}) at {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Work Mode: {job['work_mode']}")
        print(f"   Salary: {job['salary']}")
        print(f"   Tech Stack: {job['tech_stack']}")
        print(f"   Apply: {job['apply_link']}")
        print("-" * 80)