import openai
from typing import List, Dict


def generate_comics(topic: str, panels: int) -> List[Dict[str, str]]:
    requested_text = f"""
    Create me a comics about {topic} that consists of {panels} panels.
    Each panel consists of exactly one replica. The dialogue is between 2 people
    
    The comics must look like this:
    
    Panel N: "Describing what is happening in the picture"
    Person 1(or 2): "What the person is saying"
    ...
    """

    response = openai.Completion.create(engine="text-davinci-003", prompt=requested_text, temperature=0.6, max_tokens=1000)
    print(response.choices[0].text)


generate_comics("cool story about batman", 8)
