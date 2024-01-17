
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

import highlight as hlt



def build_prompt_template():
    """ """
    system_message = """
    You are a technical science editor.
    You are constructing high-impact highlight content from scientific journal articles.
    You should always respond with the most relevant content.
    You should only respond with a response to the request.
    You should never ask any questions.
    Do not answer questions that are not about the specific journal article you have been provided.
    Given a request, you should respond with the most relevant summary of the content below:\n
    {context}
    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_message)
    human_message_prompt = HumanMessagePromptTemplate.from_template("{question}")
    return ChatPromptTemplate.from_messages(
        [
            system_message_prompt,
            human_message_prompt,
        ]
    )

prompt_dict = {

    "title": """
    ### INSTRUCTION ###
    Create a captivating and concise title for the provided text, adhering to these guidelines:

    - Avoid using colons in the title.
    - The title should be engaging and slightly descriptive, sparking curiosity in potential readers.
    - It must be clear and easily understood by a broad audience.
    - Refrain from beginning with phrases like "unraveling" or "unlocking the secrets."
    - Limit the title to a single sentence, not exceeding 10 words.
    - Return the title only.
    - Exclude words such as "revolutionizing" or "unraveling."

    Remember, do not use colons in the title and do not exceed 10 words.

    ### EXAMPLE ###
    Unraveling the Complex Web of Urban Land Teleconnections

    """,

    "subtitle": """
    ### INSTRUCTION ###
    Create a subtitle for the provided text, adhering to these guidelines:

    - Keep the subtitle within a limit of 155 characters, spaces included.
    - Absolutely no colons are to be included in the subtitle.
    - It should complement and connect to the given title (enclosed in single backticks `{title}`), without directly repeating any part of it.
    - The subtitle needs to add intriguing details that encourage the audience to learn more about the research topic.
    - Only the subtitle should be provided as the output.

    Remember, do not use colons and keep the number of characters including spaces limited to 155.

    ### EXAMPLE ###
    Delving Deeper into the Complex Interactions Between Urban and Rural Areas and Their Consequential Effects on Land Development

    """,

    "science": """
    Explain the scientific findings in a simple and relatable manner for the provided text, adhering to these guidelines:

    - You must not generate a response that is greater than 100 words.
    - Highlight the main challenge this scientific field faces, which the research aims to address.
    - Clearly state the primary discovery.
    - Focus on the scientific concepts rather than the research methodology.
    - Ensure the language is clear and accessible to high school seniors or college freshmen.
    - Use straightforward, brief sentences with clear language.
    - Avoid or explain any technical jargon in layman's terms.
    - Provide enough background for a basic understanding of the research.
    - Begin with familiar concepts and gradually introduce more complex ideas.
    - Use the present tense for your description.
    - Write as if you, the researcher, are explaining your own work.
    - Keep the description to one paragraph, with a word count between 75 to 100 words.
    - Return only the explanatory paragraph.

    Remember, you must at all cost limit your response to no more than 100 words.

    """,

    "impact": """
    Convey the significance of the research findings for a non-specialist audience for the provided text, adhering to these guidelines:

    - You must not generate a response that is greater than 100 words.
    - Clarify the relevance of the findings, specifically addressing the problem the research seeks to resolve.
    - Indicate whether this discovery is a first in its field.
    - Highlight what sets this research apart in terms of innovation.
    - Explain how this research paves the way for future scientific endeavors in the same field.
    - Mention any other scientific disciplines that could be influenced by these findings.
    - Keep the language simple enough for understanding by a high school senior or college freshman.
    - Use concise sentences with straightforward wording.
    - Minimize the use of technical jargon, and if necessary, provide clear definitions.
    - Employ the present tense in your description.
    - Write from the perspective of the researchers, using the first person to discuss the work.
    - Ensure the description is at least 75 words but does not exceed 100 words.

    Remember, you must at all cost limit your response to no more than 100 words.

    """,

    "summary": """
    Create a succinct overview of the research described for the provided text, adhering to these guidelines:

    - You must not generate a response that is greater than 200 words.
    - Highlight the principal findings and their significance.
    - While the summary should be understandable to those outside the field, it can include some technical details where necessary.
    - Avoid naming specific institutions, except for mentioning user facilities like NERSC or if they are part of the United States Department of Energy Office of Science.
    - Provide a detailed account of the research in one or two paragraphs.
    - Use the present tense for your summary.
    - Narrate from the perspective of the researchers involved, using first person to discuss the work.

    Remember, you must at all cost limit your response to no more than 200 words.

    """,

}









# open example reduced content text
with open("data/example_text_one.txt") as get:
    example_text = get.read()

example_text_one = """Multisector Dynamics: Advancing the Science of Complex Adaptive Human-Earth Systems.  The field of MultiSector Dynamics (MSD) explores the dynamics and co-evolutionary pathways of human and Earth systems with a focus on critical goods, services, and amenities delivered to people through interdependent sectors. This commentary lays out core definitions and concepts, identifies MSD science questions in the context of the current state of knowledge, and describes ongoing activities to expand capacities for open science, leverage revolutions in data and computing, and grow and diversify the MSD workforce. Central to our vision is the ambition of advancing the next generation of complex adaptive human-Earth systems science to better address interconnected risks, increase resilience, and improve sustainability. This will require convergent research and the integration of ideas and methods from multiple disciplines. Understanding the tradeoffs, synergies, and complexities that exist in coupled human-Earth systems is particularly important in the context of energy transitions and increased future shocks."""
example_text_two = """The Role of Regional Connections in Planning for Future Power System Operations Under Climate Extremes.  Identifying the sensitivity of future power systems to climate extremes must consider the concurrent effects of changing climate and evolving power systems. We investigated the sensitivity of a Western U.S. power system to isolated and combined heat and drought when it has low (5%) and moderate (31%) variable renewable energy shares, representing historic and future systems. We used an electricity operational model combined with a model of historically extreme drought (for hydropower and freshwater-reliant thermoelectric generators) over the Western U.S. and a synthetic, regionally extreme heat event in Southern California (for thermoelectric generators and electricity load). We found that the drought has the highest impact on summertime production cost (+10% to +12%), while temperature-based deratings have minimal effect (at most +1%). The Southern California heat wave scenario impacting load increases summertime regional net imports to Southern California by 10–14%, while the drought decreases them by 6–12%. Combined heat and drought conditions have a moderate effect on imports to Southern California (−2%) in the historic system and a stronger effect (+8%) in the future system. Southern California dependence on other regions decreases in the summertime with the moderate increase in variable renewable energy (−34% imports), but hourly peak regional imports are maintained under those infrastructure changes. By combining synthetic and historically driven conditions to test two infrastructures, we consolidate the importance of considering compounded heat wave and drought in planning studies and suggest that region-to-region energy transfers during peak periods are key to optimal operations under climate extremes."""
system_scope = """You are a technical science editor.  You are constructing high impact highlight content from recent publications."""

max_allowable_tokens = 150000

_prompt_queue = {
    "system": """You are a technical science editor.  You are constructing high impact highlight content from recent publications.""",

    "title": """
    Generate a title for the text delimited by triple backticks. 
    
    The title should meet the following criteria:
    - No colons are allowed in the output.
    - Should pique the interest of the reader while still being somewhat descriptive.
    - Be understandable to a general audience.
    - Do not use the intro "unraveling" or "unlocking the secrets"
    - Should be only once sentence.
    - Should have a maximum length of 10 words.
    - Return only the title.
    - Do not use words like "revolutionizing" or "unraveling"
    
    The following is an example to use for formatting only.  Do not use it in the response.  \
    The example is delimited by three pound signs.
    ###
    Unraveling the Complex Web of Urban Land Teleconnections
    ###

    The following is the input text delimited by triple backticks.  Do not use colons in the response.
    ```{0}```
    """,

    "subtitle": """
    Generate a subtitle for the text delimited by triple backticks.
    
    The subtitle should meet the following criteria:
    - Strictly do not allow colons in the response text.
    - Be an extension of and related to, but not directly quote, this title delimited by single backticks `{1}`
    - Provide information that will make the audience want to find out more about the research.
    - Do not use more than 155 characters including spaces.
    - Return only the subtitle.
    
    The following is an example to use for formatting only.  Do not use it in the response.  \
    The example is delimited by three pound signs.
    ###
    Exploring the Intricate Dynamics of Urban-Rural Relationships and Their Impact on Land Use Change
    ###

    The following is the input text delimited by triple backticks.  Do not use colons in the response.
    ```{0}```
    """,

    "science": """
    Describe the scientific results for a non-expert, non-scientist audience for the text delimited by triple backticks.
    
    The description should meet the following criteria:
    - Answer what the big challenge in this field of science is that the research addresses.
    - State what the key finding is.
    - Explain the science, not the process.
    - Be understandable to a high school senior or college freshman.
    - Use short sentences and succinct words.
    - Avoid technical terms if possible.  If technical terms are necessary, define them.
    - Provide the necessary context so someone can have a very basic understanding of what you did. 
    - Start with topics that the reader already may know and move on to more complex ideas.
    - Use present tense.
    - In general, the description should speak about the research or researchers in first person.
    - Use a minimum of 75 words and a maximum of 100 words. 
    - Produce only one paragraph.
    - Return only the description.
    
    Finally, do not exceed 100 words in the response.
    
    ```{0}```
    """,

    "impact": """
    Describe the impact of the research to a non-expert, non-scientist audience for the text delimited by triple backticks.
    
    The description should meet the following criteria:
    - Answer why the findings presented are important, i.e., what problem the research is trying to solve.
    - Answer if the finding is the first of its kind.
    - Answer what was innovative or distinct about the research.
    - Answer what the research enables other scientists in your field to do next.
    - Include other scientific fields potentially impacted. 
    - Be understandable to a high school senior or college freshman. 
    - Use short sentences and succinct words.
    - Avoid technical terms if possible.  If technical terms are necessary, define them.
    - Use present tense.
    - In general, the description should speak about the research or researchers in first person.
    - Use a minimum of 75 words and a maximum of 100 words. 
    
    Finally, do not exceed 100 words in the response.


    ```{0}```
    """,

    "summary": """
    Generate a summary of the current research represented in the text delimited by triple backticks.
    
    The summary should meet the following criteria:
    - Should relay key findings and value.
    - The summary should be still accessible to the non-specialist but may be more technical if necessary. 
    - Do not mention the names of institutions. 
    - If there is a United States Department of Energy Office of Science user facility involved, such as NERSC, you can mention the user facility. 
    - Should be 1 or 2 paragraphs detailing the research.
    - Use present tense.
    - In general, the description should speak about the research or researchers in first person.
    - Use no more than 200 words.
    - Return only the summary.
    
    Finally, do not exceed 200 words in the response.

    
    ```{0}```
    """,

    "figure": """
    Generate a list of 5 search strings for use in the website that hosts free stock photos  \
    (e.g., https://www.pexels.com/) that would be representative of an aspect of the following research statement \
    delimited by triple backticks.  

    ```{0}```
    """,

    "caption": """
    Generate a caption for a photograph describing an aspect of the research for the text delimited by triple backticks.
    
    The caption should meet the following criteria:
    - The caption should be greater than 200 characters and less than 255 character long.

    ```{0}```
    """,

    "objective": """
    Generate one sentence stating the core purpose of the study.

    The sentence should meet the following criteria:
    - Use active verbs for the start of each point.
    - Use present tense.
    - Do not include methodology related to statistical, technological, and theory based
    - Return only the summary.

    The following are example responses separated by three pound signs from input text.  The example section starts \
    with two pound signs and ends with four pound signs:
    ##
    TEXT: {0}
    RESPONSE: Defines key terms and concepts for the field of MultiSector Dynamics and identifies important science questions driving the field forward.
    ###
    TEXT: {1}
    RESPONSE: Understand the effects of temperature and drought extremes on the Western U.S. power grid, while taking into account the increasing penetration of variable renewable energy sources, using a high-resolution operational power system model.
    ####

    Here is the input text delimited by triple backticks:
    ```{2}```
    """,

    "approach": """Clearly and concisely state in 2-3 short points how this work accomplished the stated objective from a methodolgocial perspecive. 
    - Do not restate the objective or include results.
    - Only include methodology including but not limited to: statistical, technological, and theory based approaches. 
    - Here is the objective statement: {2} 
    - Use a different action verb to start sentences than what is used to begin the objective statement.
    - Use active verbs for the start of each point.  
    - Use present tense.
    - Format the results as a hyphen-separated list.

    TEXT: {0}
    RESPONSE:
    - Evaluate contemporary and hypothesized Western U.S. infrastructures with variable renewable generation shares for sensitivity to drought and Southern California heat wave scenarios on generation and load.
    - Use a stochastic temperature simulation combined with spatially resolved historical drought as a toolset to incorporate other grid stressors in high-resolution power system models, leading to improved sensitivity analyses not limited by the current ability of climate models to capture extreme conditions.
    ### 
    TEXT: {1}
    RESPONSE:
    """,

    "ppt_impact": """Clearly and concisely state in 3 points the key results and outcomes from this research. 
    - State what the results indicate.
    - Include results that may be considered profound or surprising.
    - Each point should be 1 concise sentence.
    - Use present tense.
    - Format the results as a hyphen-separated list.

    TEXT: {0}
    RESPONSE:
    """,

    "reduce_wordcount": """Reduce the current text to be greater than {0} words and less than or equal to {1} words.  \
    The following is the text delimited by triple backquotes:
     
     ```{2}```
    """,

    "figure_caption": """Summarize the key findings of the paper as a figure caption.
    - Limit the response to 25 words.
    
    TEXT: {0}
    RESPONSE:
    """,

    "figure_choice": """What figure best represents the high impact content that can be easily understood by a non-technical, non-scientifc audience.
    Limit the response to:
    1. The figure name as it is written in the text,
    2. An explanation of why it was chosen,
    3. What the figure is about as a figure caption in less than 50 words. Use the figure name in the caption.  Start this point with the phrase "CAPTION:  "
        
    TEXT: {0}
    RESPONSE:
    """,

    "citation": """Generate the citation for this publication.
    
    And use the formatting provided in the following:
    Hadjimichael, A., J. Yoon, P. Reed, N. Voisin, W. Xu. 2023. “Exploring the Consistency of Water Scarcity Inferences between Large-Scale Hydrologic and Node-Based Water System Model Representations of the Upper Colorado River Basin,” J. Water Resour. Plann. Manage., 149(2): 04022081. DOI: 10.1061/JWRMD5.WRENG-5522
    """,
}


# def generate_prompt(content: str,
#                     prompt_name: str = "title",
#                     max_tokens: int = 50,
#                     temperature: float = 0.0,
#                     additional_content: str = None,
#                     model: str = "gpt-4") -> str:

#     if prompt_name in ("objective",):
#         prompt = prompt_queue[prompt_name].format(example_text_one, example_text_two, content)

#     elif prompt_name in ("approach",):
#         if additional_content is None:
#             additional_content = content
#         prompt = prompt_queue[prompt_name].format(example_text_two, content, additional_content)

#     elif prompt_name in ("subtitle",):
#         if additional_content is None:
#             additional_content = content
#         prompt = prompt_queue[prompt_name].format(content, additional_content)

#     elif prompt_name in ("figure", "caption", "impact", "summary", "ppt_impact", "title", "science", "figure_caption", "figure_choice", "citation"):
#         prompt = prompt_queue[prompt_name].format(content)

#     return hlt.generate_content(system_scope=system_scope,
#                                 prompt=prompt,
#                                 max_tokens=max_tokens,
#                                 temperature=temperature,
#                                 max_allowable_tokens=max_allowable_tokens,
#                                 model=model)


