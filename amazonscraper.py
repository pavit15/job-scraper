import requests

def scrape_amazon_jobs():
    url = "https://www.amazon.jobs/en/search.json?base_query=software&loc_query=India"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        jobs = data.get("jobs", [])[:5]  
        formatted_jobs = []
        for job in jobs:
            title = job.get("title", "N/A")
            location = job.get("location", "N/A")
            job_url = "https://www.amazon.jobs" + job.get("job_path", "")
            formatted_jobs.append({
                "title": title,
                "job_type": "Internship" if "intern" in title.lower() else "Job",
                "location": location,
                "work_mode": "Hybrid", 
                "salary": "Not disclosed",
                "tech_stack": "Not specified",  
                "apply_link": job_url
            })
        return formatted_jobs
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    jobs = scrape_amazon_jobs()
    for idx, job in enumerate(jobs, 1):
        print(f"{idx}. {job['title']} ({job['job_type']})")
        print(f"   Location: {job['location']}")
        print(f"   Work Mode: {job['work_mode']}")
        print(f"   Salary: {job['salary']}")
        print(f"   Tech Stack: {job['tech_stack']}")
        print(f"   Apply: {job['apply_link']}")
        print("-" * 80)