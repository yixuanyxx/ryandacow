from backend.shared.llm_clients import get_apim_client

client = get_apim_client()

response = client.chat.completions.create(
    model="gpt-5-mini",
    messages=[
        {"role": "system", "content": "You are PORTalGPT, PSA's internal co-pilot."},
        {"role": "user", "content": "Which expressway connects Jurong East to Tampines?"}
    ]
)

print(response.choices[0].message.content)