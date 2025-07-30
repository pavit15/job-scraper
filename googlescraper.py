import requests
import re

TECH_KEYWORDS = [
    "Python", "Java", "C++", "C#", "Go", "JavaScript", "TypeScript", "React", "Angular",
    "Node.js", "Django", "Flask", "Spring", "Kotlin", "Swift", "AWS", "Azure", "GCP",
    "Docker", "Kubernetes", "SQL", "NoSQL", "MongoDB", "PostgreSQL", "Git", "Linux"
]

CONTINENT_MAP = {
    "India": "Asia", "United States": "North America", "Germany": "Europe",
    "United Kingdom": "Europe", "Canada": "North America", "Australia": "Oceania"
}

def extract_tech_stack(text):
    if not text:
        return "Not specified"
    found = set()
    for keyword in TECH_KEYWORDS:
        if re.search(rf"\b{re.escape(keyword)}\b", text, re.IGNORECASE):
            found.add(keyword)
    return ", ".join(sorted(found)) if found else "Not specified"

def scrape_google_jobs():
    url = "https://careers.google.com/api/v3/search/?q=software&location=India"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        jobs = data.get("jobs", [])[:5]  # Limit to 5 jobs
        formatted_jobs = []
        for job in jobs:
            title = job.get("title", "Unknown")
            job_url = job.get("applyUrl", "https://careers.google.com/")
            job_location = job.get("locations", [{}])[0].get("display", "Unknown, Unknown")
            desc = job.get("description", "")
            quals = job.get("qualifications", "")
            parts = [p.strip() for p in job_location.split(",")]
            city = parts[0] if len(parts) > 0 else "Unknown"
            country = parts[-1] if len(parts) > 1 else "Unknown"
            continent = CONTINENT_MAP.get(country, "Unknown")
            formatted_jobs.append({
                "title": title,
                "job_type": "Internship" if "intern" in title.lower() else "Job",
                "location": f"{city}, {country} ({continent})",
                "work_mode": "Hybrid",  # Google often uses hybrid
                "salary": "Not disclosed",
                "tech_stack": extract_tech_stack(desc + "\n" + quals),
                "apply_link": job_url
            })
        return formatted_jobs
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    jobs = scrape_google_jobs()
    for idx, job in enumerate(jobs, 1):
        print(f"{idx}. {job['title']} ({job['job_type']})")
        print(f"   Location: {job['location']}")
        print(f"   Work Mode: {job['work_mode']}")
        print(f"   Salary: {job['salary']}")
        print(f"   Tech Stack: {job['tech_stack']}")
        print(f"   Apply: {job['apply_link']}")
        print("-" * 80)