from openai import OpenAI

client = OpenAI(api_key='org-T0Sr0k3a6m78av0QtSd0Pt5g')

response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="Hello world! This is a streaming test.",
)

response.stream_to_file("output.mp3")