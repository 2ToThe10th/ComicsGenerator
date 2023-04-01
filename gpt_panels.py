import openai
from typing import List, Dict


def parse_comics(generated_text: str, panels: int) -> List[Dict[str, str]]:
    generated_text = generated_text.strip().split('\n')
    phrases = [x for x in generated_text if x != '']
    result = []
    for i in range(0, len(phrases), 2):
        panel = phrases[i]
        replica = phrases[i + 1]
        result.append({"panel": panel, "replica": replica})
    return result


def generate_comics(topic: str, panels: int) -> List[Dict[str, str]]:
    requested_text = f"""
    Create me a comics about {topic} that consists of {panels} panels.
    Each panel consists of exactly one replica. The dialogue is between 2 people
    
    The comics must look like this:
    
    Panel N: "Describing what is happening in the picture"
    Person 1(or 2): "What the person is saying"
    ...
    """
    while True:
        try:
            response = openai.Completion.create(engine="text-davinci-003", prompt=requested_text, temperature=0.6, max_tokens=500)
            return parse_comics(response.choices[0].text, panels)
        except Exception:
            print("Not parsed data from chat gpt. Get next")
