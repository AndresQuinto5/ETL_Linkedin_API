import http.client
import json
import urllib.parse
import pandas as pd
from tabulate import tabulate
from datetime import datetime, timedelta
import pytz
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use the API key
api_key = os.getenv('LINKEDIN_API_KEY')

def search_linkedin_jobs(api_key, search_term, location_id):
    conn = http.client.HTTPSConnection("linkedin-data-scraper.p.rapidapi.com")
    
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "linkedin-data-scraper.p.rapidapi.com"
    }
    
    encoded_term = urllib.parse.quote(search_term)
    query_params = {
        "query": encoded_term,
        "page": "1",
        "searchLocationId": location_id,
        "sortBy": "DD",
    }
    query_string = urllib.parse.urlencode(query_params)
    
    try:
        conn.request("GET", f"/search_jobs?{query_string}", headers=headers)
        res = conn.getresponse()
        data = res.read()
        
        if res.status == 200:
            jobs_data = json.loads(data.decode("utf-8"))
            
            # Save full API response to a JSON file
            with open("full_api_response.json", "w") as f:
                json.dump(jobs_data, f, indent=2)
            
            print("Full API response saved to 'full_api_response.json'")
            
            if jobs_data.get('success') and isinstance(jobs_data.get('response'), dict):
                all_jobs = jobs_data['response'].get('jobs', [])
                if all_jobs:
                    print(f"Retrieved {len(all_jobs)} jobs for '{search_term}'")
                    return all_jobs, True
                else:
                    print(f"No jobs found for '{search_term}'")
            else:
                print(f"Unexpected response structure for '{search_term}'")
        else:
            print(f"Error searching for '{search_term}': HTTP {res.status}: {res.reason}")
    except Exception as e:
        print(f"An error occurred while searching for '{search_term}': {str(e)}")
    
    return [], False

def main():
    api_key = os.getenv('LINKEDIN_API_KEY')
    
    search_terms = [
        "datos",
        "dataanalyst",
        "datascientist",
        "dataengineer",
        "businessintelligence",
        "bigdata",
        "analistadatos",
        "cientificodatos",
        "ingenierodatos"
    ]
    
    location_id = "105967320"  # Guatemala
    
    all_jobs = []
    
    for term in search_terms:
        jobs, success = search_linkedin_jobs(api_key, term, location_id)
        if success:
            all_jobs.extend(jobs)
    
    if not all_jobs:
        print("No jobs were retrieved. Exiting.")
        return

    # Create a DataFrame from the jobs data
    df = pd.DataFrame(all_jobs)
    
    # Filter for jobs in Guatemala
    df = df[df['formattedLocation'].str.contains('Guatemala', case=False, na=False)]
    
    # Remove duplicate job listings
    df = df.drop_duplicates(subset=['title', 'companyName', 'formattedLocation'])
    
    # Convert 'listedAt' to datetime and filter for last 2 months
    df['listedAt'] = pd.to_datetime(df['listedAt'])
    two_months_ago = datetime.now(pytz.UTC) - timedelta(days=60)
    df = df[df['listedAt'] > two_months_ago]

    # Save the filtered DataFrame to CSV
    df.to_csv("linkedin_jobs_last_2_months.csv", index=False)

    # Save the DataFrame to CSV and JSON files
    df.to_csv("linkedin_jobs.csv", index=False)
    df.to_json("linkedin_jobs.json", orient="records", indent=2)
    
    # Display a table of the results
    print("\nJob Search Results:")
    print(f"Columns in the DataFrame: {df.columns.tolist()}")
    if set(['title', 'companyName', 'formattedLocation', 'jobPostingUrl']).issubset(df.columns):
        if not df.empty:
            print(tabulate(df[['title', 'companyName', 'formattedLocation', 'jobPostingUrl']], headers='keys', tablefmt='pretty', maxcolwidths=[30, 20, 20, 50]))
        else:
            print("No jobs found in Guatemala.")
    else:
        print("Unable to display results table. Some expected columns are missing.")
        print("First few rows of the DataFrame:")
        print(df.head().to_string())
    
    print(f"\nTotal jobs found in Guatemala: {len(df)}")
    print("Full results saved to 'linkedin_jobs.csv' and 'linkedin_jobs.json'")
    print("Full API response saved to 'full_api_response.json'")
    print("Jobs from the last 2 months saved to 'linkedin_jobs_last_2_months.csv'")

if __name__ == "__main__":
    main()
