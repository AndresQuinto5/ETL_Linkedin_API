import pandas as pd
import re
from collections import Counter

# Load your resume skills (in both English and Spanish)
your_skills = [
    'Python', 'R', 'PostgreSQL', 'Git', 'TensorFlow', 'PyTorch', 'Matplotlib',
    'Seaborn', 'Plotly', 'ETL', 'Data Analysis', 'Machine Learning',
    'Data Visualization', 'Web Development', 'React', 'JavaScript',
    'Problem Solving', 'Leadership', 'Team Management', 'Time Management',
    'Adaptability', 'Communication',
    # Spanish translations
    'Análisis de Datos', 'Aprendizaje Automático', 'Visualización de Datos',
    'Desarrollo Web', 'Resolución de Problemas', 'Liderazgo', 'Gestión de Equipos',
    'Gestión del Tiempo', 'Adaptabilidad', 'Comunicación'
]

# Define relevant job terms (in both English and Spanish)
relevant_terms = [
    'data', 'datos', 'analyst', 'analista', 'scientist', 'científico',
    'engineer', 'ingeniero', 'machine learning', 'aprendizaje automático',
    'AI', 'IA', 'inteligencia artificial', 'business intelligence', 'BI',
    'database', 'base de datos', 'programming', 'programación',
    'software', 'developer', 'desarrollador', 'web', 'full stack',
    'frontend', 'backend', 'ETL', 'big data', 'analytics', 'analítica',
    'data science', 'ciencia de datos', 'data engineer', 'ingeniero de datos',
    'business analyst', 'analista de negocios', 'data architect', 'arquitecto de datos',
    'machine learning engineer', 'ingeniero de aprendizaje automático',
    'data visualization', 'visualización de datos', 'statistician', 'estadístico',
    'quantitative analyst', 'analista cuantitativo', 'data mining', 'minería de datos',
    'predictive modeling', 'modelado predictivo', 'NLP', 'procesamiento de lenguaje natural',
    'deep learning', 'aprendizaje profundo', 'artificial intelligence', 'inteligencia artificial',
    'data warehouse', 'almacén de datos', 'business intelligence', 'inteligencia de negocios',
    'data governance', 'gobernanza de datos', 'data quality', 'calidad de datos',
    'data strategy', 'estrategia de datos', 'data analytics', 'análisis de datos'
]

# Load the LinkedIn jobs data
df = pd.read_csv('linkedin_jobs_last_2_months.csv')

def is_relevant_job(job_title, job_description):
    combined_text = (job_title + ' ' + job_description).lower()
    return any(term.lower() in combined_text for term in relevant_terms)

def calculate_skills_match(job_description, your_skills):
    job_description_lower = job_description.lower()
    skill_count = sum(1 for skill in your_skills if re.search(r'\b' + re.escape(skill.lower()) + r'\b', job_description_lower))
    match_percentage = (skill_count / len(your_skills)) * 100
    matched_skills = [skill for skill in your_skills if re.search(r'\b' + re.escape(skill.lower()) + r'\b', job_description_lower)]
    return round(match_percentage, 2), matched_skills

# Filter relevant jobs
df['is_relevant'] = df.apply(lambda row: is_relevant_job(row['title'], row['jobDescription']), axis=1)
df_relevant = df[df['is_relevant']]

# Apply the skills match calculation to each relevant job
df_relevant['Skills Match'], df_relevant['Matched Skills'] = zip(*df_relevant['jobDescription'].apply(lambda x: calculate_skills_match(x, your_skills)))

# Additional relevance check based on job title
def is_title_relevant(title):
    title_lower = title.lower()
    return any(term.lower() in title_lower for term in relevant_terms)

df_relevant = df_relevant[df_relevant['title'].apply(is_title_relevant)]

# Select relevant columns and sort by skills match
df_filtered = df_relevant[['title', 'companyName', 'formattedLocation', 'listedAt', 'Skills Match', 'Matched Skills', 'jobPostingUrl']]
df_filtered = df_filtered.sort_values('Skills Match', ascending=False)

# Save to CSV
df_filtered.to_csv('job_matches.csv', index=False)

print("Job matches saved to job_matches.csv")

# Print top 10 job matches
print("\nTop 10 Job Matches:")
for _, row in df_filtered.head(10).iterrows():
    print(f"{row['title']} at {row['companyName']} - {row['Skills Match']}% match")
    print(f"Matched Skills: {', '.join(row['Matched Skills'])}")
    print(f"Link: {row['jobPostingUrl']}\n")

# Analyze most in-demand skills
all_matched_skills = [skill for skills in df_filtered['Matched Skills'] for skill in skills]
skill_demand = Counter(all_matched_skills)

print("\nMost In-Demand Skills:")
for skill, count in skill_demand.most_common(10):
    print(f"{skill}: {count} occurrences")