import pandas as pd
import webbrowser
import os

# Load the filtered job data
df_relevant = pd.read_csv('job_matches.csv')

# Load all job data
df_all = pd.read_csv('linkedin_jobs_last_2_months.csv')

# Create HTML content
html_content = """
<html>
<head>
    <title>Job Listings</title>
    <style>
        body { font-family: Arial, sans-serif; }
        table {
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 30px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        h1, h2 { color: #333; }
    </style>
</head>
<body>
    <h1>Job Listings</h1>
    
    <h2>Relevant Job Listings</h2>
    <table>
        <tr>
            <th>Title</th>
            <th>Company</th>
            <th>Location</th>
            <th>Listed At</th>
            <th>Skills Match</th>
            <th>Link</th>
        </tr>
"""

for _, row in df_relevant.iterrows():
    html_content += f"""
        <tr>
            <td>{row['title']}</td>
            <td>{row['companyName']}</td>
            <td>{row['formattedLocation']}</td>
            <td>{row['listedAt']}</td>
            <td>{row['Skills Match']}%</td>
            <td><a href="{row['jobPostingUrl']}" target="_blank">View Job</a></td>
        </tr>
    """

html_content += """
    </table>
    
    <h2>All Job Listings</h2>
    <table>
        <tr>
            <th>Title</th>
            <th>Company</th>
            <th>Location</th>
            <th>Listed At</th>
            <th>Link</th>
        </tr>
"""

for _, row in df_all.iterrows():
    html_content += f"""
        <tr>
            <td>{row['title']}</td>
            <td>{row['companyName']}</td>
            <td>{row['formattedLocation']}</td>
            <td>{row['listedAt']}</td>
            <td><a href="{row['jobPostingUrl']}" target="_blank">View Job</a></td>
        </tr>
    """

html_content += """
    </table>
</body>
</html>
"""

# Write HTML content to a file
with open('all_job_listings.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

# Open the HTML file in the default web browser
webbrowser.open('file://' + os.path.realpath('all_job_listings.html'))

print("Job listings HTML file created and opened in your default web browser.")