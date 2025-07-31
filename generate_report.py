import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

# Step 1: Load your API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file!")

# Step 2: Configure Gemini with the 2.0 Flash model
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash-001")  # THIS is the free tier model id

# Step 3: Read your student CSV
df = pd.read_csv('students.csv')

# Step 3.5: Create output folder if it doesn't exist
output_folder = "generated_reports"
os.makedirs(output_folder, exist_ok=True)

# Step 4: For each student, create a report
for idx, row in df.iterrows():
    name = f"{row['gender'].capitalize()} Student {idx+1}"
    math = row['math score']
    reading = row['reading score']
    writing = row['writing score']
    prompt = (
        f"You are a learning expert. Write a 1-page report for this student:\n"
        f"Description: {name}\n"
        f"Scores: Math: {math}, Reading: {reading}, Writing: {writing}\n\n"
        "Highlight their strengths, suggest specific improvements per subject, and finish with a motivational message."
    )

    # Gemini 2.0 Flash supports text generation with .generate_content
    response = model.generate_content(prompt)
    report = response.text

    # Save inside the generated_reports folder
    filename = f"{name.replace(' ', '_')}_report.txt"
    filepath = os.path.join(output_folder, filename)
    with open(filepath, 'w', encoding='utf-8') as out:
        out.write(report)

print(f"Reports generated and saved inside '{output_folder}' folder!")
