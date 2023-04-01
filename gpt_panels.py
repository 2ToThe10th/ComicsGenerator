import openai
from typing import List, Dict

openai.api_key = "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"



def generate_comics(topic : str, panels : int) -> List[Dict[str, str]]:
    reqested_text = f"""
    Create me a comics about {topic} that consists of {panels} panels.
    Each panel consists of exactly one replica. The dialogue is between 2 people
    
    The comics must look like this:
    
    Panel N: "Describing what is happening in the picture"
    Person 1(or 2): "What the person is saying"
    ...
    """

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=reqested_text,
        temperature=0.6,
        max_tokens=1000
    )
    # print(response)
    print(response.choices[0].text)



generate_comics("the putin in ukraine", 8)




