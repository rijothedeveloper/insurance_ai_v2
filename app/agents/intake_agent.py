from openai import OpenAI
import os

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def run_intake_agent(claim):
    prompt = f"""
    Analyse this insurance claim.
    
    Claim:
    {claim}
    
    Return:
    - completeness score
    - missing fields
    - summary
    """
    
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content