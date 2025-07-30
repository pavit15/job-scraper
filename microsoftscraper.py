import requests
import json
from datetime import datetime

CONTINENT_MAPPING = {
    "US": "North America", "USA": "North America", "United States": "North America",
    "CA": "North America", "Canada": "North America", "MX": "North America", "Mexico": "North America",
    "GB": "Europe", "UK": "Europe", "United Kingdom": "Europe", "DE": "Europe", "Germany": "Europe",
    "FR": "Europe", "France": "Europe", "ES": "Europe", "Spain": "Europe", "IT": "Europe", "Italy": "Europe",
    "IN": "Asia", "India": "Asia", "CN": "Asia", "China": "Asia", "JP": "Asia", "Japan": "Asia",
    "SG": "Asia", "Singapore": "Asia", "AU": "Australia", "Australia": "Australia"
}

def get_continent(country):
    return CONTINENT_MAPPING.get(country, "Not specified")

def parse_location(location_str):
    if not location_str or not isinstance(location_str, str):
        return ("Not specified", "Not specified", "Not specified")
    location_str = location_str.strip()
    if location_str.lower() in ["remote", "hybrid"]:
        return (location_str, "Not specified", "Not specified")
    parts = [p.strip() for p in location_str.split(",")]
    if len(parts) >= 2:
        city = parts[0]
        country = parts[-1]
        return (city, country, get_continent(country))
    elif parts:
        return ("Not specified", parts[0], get_continent(parts[0]))
    return ("Not specified", "Not specified", "Not specified")

def determine_work_mode(description, title, location_str):
    text = f"{title or ''} {description or ''} {location_str or ''}".lower()
    if "remote" in text:
        return "Remote"
    elif "hybrid" in text:
        return "Hybrid"
    elif "work from home" in text or "wfh" in text:
        return "Work from Home"
    elif "on-site" in text or "onsite" in text:
        return "On-site"
    else:
        return "Not specified"

def extract_tech_stack(description, title):
    tech_keywords = [
        "python", "java", "c#", "javascript", "typescript",
        "azure", "aws", "gcp", "sql", "nosql",
        "docker", "kubernetes", "machine learning", "ai",
        "react", "angular", "node.js"
    ]
    found_tech = []
    text = f"{title or ''} {description}".lower()
    for tech in tech_keywords:
        if tech in text and tech.capitalize() not in found_tech:
            found_tech.append(tech.capitalize())
    return found_tech if found_tech else ["Not specified"]

def fetch_microsoft_jobs(keywords=None, location=None, limit=10):
    base_url = "https://gcsservices.careers.microsoft.com/search/api/v1/search"
    params = {"pg": 1, "ps": limit}
    if keywords: params["q"] = keywords
    if location: params["lc"] = location
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        jobs = data.get("operationResult", {}).get("result", {}).get("jobs", [])
        if not jobs:
            print("No jobs found in API response")
            return []
        detailed_jobs = []
        for job in jobs:
            properties = job.get("properties", {})
            title = job.get("title", "Not specified")
            location_str = properties.get("location", "Not specified")
            description = properties.get("description", "")
            city, country, continent = parse_location(location_str)
            detailed_jobs.append({
                "job_title": title,
                "job_type": "Internship" if "intern" in title.lower() else "Job",
                "location": {
                    "city": city,
                    "country": country,
                    "continent": continent
                },
                "work_mode": determine_work_mode(description, title, location_str),
                "salary": "Not disclosed",  # Microsoft typically doesn't disclose salaries in API
                "tech_stack": extract_tech_stack(description, title),
                "apply_link": f"https://jobs.careers.microsoft.com/global/en/job/{job.get('jobId', '')}"
            })
        return detailed_jobs
    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    jobs = fetch_microsoft_jobs(limit=5)
    for idx, job in enumerate(jobs, 1):
        print(f"{idx}. {job['job_title']} ({job['job_type']})")
        print(f"   Location: {job['location']['city']}, {job['location']['country']} ({job['location']['continent']})")
        print(f"   Work Mode: {job['work_mode']}")
        print(f"   Salary: {job['salary']}")
        print(f"   Tech Stack: {', '.join(job['tech_stack'])}")
        print(f"   Apply: {job['apply_link']}")
        print("-" * 80)