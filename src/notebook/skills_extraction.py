import spacy
from spacy.matcher import Matcher
from PyPDF2 import PdfReader
import csv

# Load the Spacy English model
nlp = spacy.load('en_core_web_sm')

# Read skills from CSV file
skills_file_path = '/Users/mac/Documents/Job-Recommendation-System/Job-Recommendation-System/src/notebook/skills.csv'
with open(skills_file_path, 'r') as file:
    csv_reader = csv.reader(file)
    skills = [row for row in csv_reader]

# Create pattern dictionaries from skills
skill_patterns = [[{'LOWER': skill}] for skill in skills[0]]

# Create a Matcher object
matcher = Matcher(nlp.vocab)

# Add skill patterns to the matcher
for pattern in skill_patterns:
    matcher.add('Skills', [pattern])

# Function to extract skills from text
def extract_skills(text):
    doc = nlp(text)
    matches = matcher(doc)
    skills = set()
    for match_id, start, end in matches:
        skill = doc[start:end].text
        skills.add(skill)
    return skills

# Function to extract text from PDF
def extract_text_from_pdf(file_content):
    pdf_reader = PdfReader(file_content)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def skills_extractor(uploaded_file):
    # Extract text from PDF
    resume_text = extract_text_from_pdf(uploaded_file)

    # Extract skills from resume text
    skills = list(extract_skills(resume_text))
    return skills
