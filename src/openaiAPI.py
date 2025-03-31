from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_test_from_notes(notes: list[str], numOfQuestions: int) -> list[dict]:
  combined_notes = "\n".join(notes)

  prompt = f"""
  Based on the following notes, generate {numOfQuestions} questions and answers in JSON format. Each item should look like: {{"question": "...", "answer": "..."}}
  Your response as a WHOLE should be parsable JSON.
  Notes:
  {combined_notes}
  """

  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=1500,
    n=1,
    stop=None,
    temperature=0.7,
  )

  content = response.choices[0].message.content

  try:
    import json
    return json.loads(content)
  except Exception as e:
    print(f"Error parsing JSON: {e}")
    print(f"Response content: {content}")
    return ["chatGPT was unable to give a response in parsable JSON format."]
  
def generate_summary_from_notes(notes: list[str]) -> str:
  combined_notes = "\n".join(notes)

  prompt = f"""
  Based on the following notes, generate a summary in JSON format. The summary should be concise and cover all the main points.
  Your response as a WHOLE should be parsable JSON.
  Notes:
  {combined_notes}
  """

  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=1500,
    n=1,
    stop=None,
    temperature=0.7,
  )

  content = response.choices[0].message.content

  try:
    import json
    return json.loads(content)
  except Exception as e:
    print(f"Error parsing JSON: {e}")
    print(f"Response content: {content}")
    return {}