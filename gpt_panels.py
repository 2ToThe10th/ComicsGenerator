import openai
import re
from typing import List, Dict


def parse_comics(generated_text: str, panels: int) -> List[Dict[str, str]]:
    """
    Parsing the output of the GPT3 generated text
    """
    generated_text = generated_text.replace('\n', ' ').strip()
    generated_text = re.split(r"Panel|Person", generated_text)
    generated_text = [x for x in generated_text if x != '']
    if len(generated_text) != 2 * panels:
        raise ValueError("Number of panels is not sufficient")

    result = []
    for i in range(0, len(generated_text), 2):
        panel = generated_text[i].split(':')[1].strip()
        if panel[0] == '\'' or panel[0] == '\"':
            panel = panel[1:-1]

        phrase = generated_text[i + 1].split(':')[1].strip()
        if phrase[0] == '\'' or phrase[0] == '\"':
            phrase = phrase[1:-1]

        result.append({"panel": panel, "phrase": phrase})

    return result


def generate_comics_text(topic: str, panels: int) -> List[Dict[str, str]]:
    """Generating the description and phrases for each panel"""
    requested_text = f"""
    Create me a comics about {topic} .The comics consists of {panels} panels.
    Each panel consists of exactly one replica. The dialogue is between 2 people
    
    The comics must look like this:
    
    Panel N: "Describing what is happening in the picture"
    Person 1(or 2): "What the person is saying"
    ...
    """
    response = None
    while True:
        try:
            response = openai.Completion.create(engine="text-davinci-003", prompt=requested_text, temperature=0.6, max_tokens=4097 - len(requested_text))
            chatgpt_story = response.choices[0].text
            print(chatgpt_story)
            return parse_comics(chatgpt_story, panels)
        except Exception as e:
            if response is not None and len(response.choices) > 0:
                print(response.choices[0].text)
            print(e)
            print("Not parsed data from chat gpt. Get next")
