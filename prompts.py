
import highlight as hlt


example_text_one = """Multisector Dynamics: Advancing the Science of Complex Adaptive Human-Earth Systems.  The field of MultiSector Dynamics (MSD) explores the dynamics and co-evolutionary pathways of human and Earth systems with a focus on critical goods, services, and amenities delivered to people through interdependent sectors. This commentary lays out core definitions and concepts, identifies MSD science questions in the context of the current state of knowledge, and describes ongoing activities to expand capacities for open science, leverage revolutions in data and computing, and grow and diversify the MSD workforce. Central to our vision is the ambition of advancing the next generation of complex adaptive human-Earth systems science to better address interconnected risks, increase resilience, and improve sustainability. This will require convergent research and the integration of ideas and methods from multiple disciplines. Understanding the tradeoffs, synergies, and complexities that exist in coupled human-Earth systems is particularly important in the context of energy transitions and increased future shocks."""
example_text_two = """The Role of Regional Connections in Planning for Future Power System Operations Under Climate Extremes.  Identifying the sensitivity of future power systems to climate extremes must consider the concurrent effects of changing climate and evolving power systems. We investigated the sensitivity of a Western U.S. power system to isolated and combined heat and drought when it has low (5%) and moderate (31%) variable renewable energy shares, representing historic and future systems. We used an electricity operational model combined with a model of historically extreme drought (for hydropower and freshwater-reliant thermoelectric generators) over the Western U.S. and a synthetic, regionally extreme heat event in Southern California (for thermoelectric generators and electricity load). We found that the drought has the highest impact on summertime production cost (+10% to +12%), while temperature-based deratings have minimal effect (at most +1%). The Southern California heat wave scenario impacting load increases summertime regional net imports to Southern California by 10–14%, while the drought decreases them by 6–12%. Combined heat and drought conditions have a moderate effect on imports to Southern California (−2%) in the historic system and a stronger effect (+8%) in the future system. Southern California dependence on other regions decreases in the summertime with the moderate increase in variable renewable energy (−34% imports), but hourly peak regional imports are maintained under those infrastructure changes. By combining synthetic and historically driven conditions to test two infrastructures, we consolidate the importance of considering compounded heat wave and drought in planning studies and suggest that region-to-region energy transfers during peak periods are key to optimal operations under climate extremes."""
system_scope = """You are a technical science editor.  You are constructing high impact highlight content from recent publications."""

max_allowable_tokens = 8192

prompt_queue = {
    "title": """Generate a title for the highlight that should pique the interest of the reader while also being somewhat descriptive. 
    - Output as one short sentence. 
    - The output sentence must have a maximum length of 10 words.
    - The title should be different than the paper title and be understandable to a general audience.
    
    TEXT: {0}
    RESPONSE: Setting the Stage for the Future of MultiSector Dynamics Research
    ###
    TEXT: {1}
    RESPONSE: U.S. Land Use Dataset for Renewable and Non-Renewable Energy Production 
    ### 
    TEXT: {2}
    RESPONSE:
    """,

    "subtitle": """Provide a short subtitle.
    - Use no more than 155 characters with spaces.
    - The goal for the subtitle is to provide further information that will encourage people to read more.  
    - Do not produce sentances that are colon separated. 
    
    TEXT: {0}
    RESPONSE: The combined impact of heat waves and drought on the Western U.S. significantly affects energy production costs and interregional transfers during peak hours.
    ###
    TEXT: {1}
    RESPONSE: A high-resolution geospatial dataset to enable comparative land use studies of energy technologies. 
    ### 
    TEXT: {2}
    RESPONSE:
    """,

    "science": """Describe the scientific results for a non-expert, non-scientist audience.
    - Should answer what the big challenge in this field of science is that the research addresses.
    - Should state what the key finding is.
    - Should explain the science, not the process.
    - Use a minimum of 75 words and a maximum of 100 words. 
    - The paragraph should be understandable to a high school senior or college freshman. 
    - Use short sentences and succinct words. 
    - Avoid technical terms if possible; if necessary, define them. 
    - Provide the necessary context so someone can have a very basic understanding of what you did. 
    - Start with things the reader already knows and move on to more complex ideas. 
    
    TEXT: {0}
    RESPONSE: MultiSector Dynamics (MSD) is a scientific field that studies the co-evolution of human and Earth systems. Example research areas include sustainability, climate change risks, and energy system transitions. In this commentary we provide definitions for core concepts and themes in the field. We also describe important science questions, ongoing activities, and provide a vision for the field moving forward. A key part of the future vision is the goal to facilitate a diverse, transdisciplinary workforce and to leverage open science to tackle MSD problems.
    ###
    TEXT: {1}
    RESPONSE: This study investigates the importance of the interactions between climate change and energy system transitions for power system planning and operations. The research examines the individual and combined impacts of a Southern California heat wave and a Western U.S. drought on the historical (5% renewables) and a projected future Western U.S. power system (31% renewables). The key findings are that drought has a higher impact on energy production costs than the heat wave, the cost increases for the combined events are similar to the drought scenario alone, and interregional transfers during peak demand hours are complex and highly sensitive to extreme events and the generation mix.
    ###
    TEXT: {2}
    RESPONSE:
    """,

    "impact": """Describe the impact of the research to a non-expert, non-scientist audience. The response should consider the following:
    - Should answer why the findings presented are important, i.e., what problem the research is trying to solve.
    - Should answer if the finding is the first of its kind.
    - Should answer what was innovative or distinct about the research.
    - Should answer what the research enables other scientists in your field to do next.
    - The paragraph should be understandable to a high school senior or college freshman. 
    - Use short sentences and short words. 
    - Avoid technical terms if possible; if necessary, define them. 
    - Include other scientific fields potentially impacted. 
    - Do not use "Recent research" or similar statements to start the first sentence.  
    - In general, the response should speak about the research as "this study", not "a recent study".
    - Use 75 to 100 words.
    
    TEXT: {0}
    RESPONSE:
        """,

    "summary": """Generate a summary of the current research text.  Consider the following context:
    - Should relay key findings and value.
    - The summary should be still accessible to the non-specialist but may be more technical if necessary. 
    - As a point of style, we usually do not mention the name of the institution. 
    - If there is a DOE Office of Science user facility involved, such as NERSC, you can mention the user facility. 
    - Should be 1 or 2 paragraphs detailing the research.
    - Use no more than 200 words.
    
    TEXT: {0}
    RESPONSE:
    """,

    "figure": """Generate a list of 5 search strings for use in the website https://www.pexels.com/ that would be representative of an aspect of the following research statement:

    ###
    PROMPT: {0}
    RESPONSE:
    """,

    "caption": """Generate a caption for a photograph describing an aspect of the research. The caption should be greater than 200 characters and less than 255 character long.

    ###
    PROMPT: {0}
    RESPONSE:
    """,

    "objective": """Generate 1 sentence stating the core purpose of the study. Use active verbs for the start of each point. 
    - Use present tense.
    - Do not include methodology related to stastistical, technological, and theory based

    TEXT: {0}
    RESPONSE: Defines key terms and concepts for the field of MultiSector Dynamics and identifies important science questions driving the field forward.
    ###
    TEXT: {1}
    RESPONSE: Understand the effects of temperature and drought extremes on the Western U.S. power grid, while taking into account the increasing penetration of variable renewable energy sources, using a high-resolution operational power system model.
    ### 
    TEXT: {2}
    RESPONSE:
    """,

    "approach": """Clearly and concisely state in 2-3 short points how this work accomplished the stated objective from a methodolgocial perspecive. 
    - Do not restate the objective or include results.
    - Only include methodology including but not limited to: statistical, technological, and theory based approaches. 
    - Here is the objective statement: {2} 
    - Use a different action verb to start sentences than what is used to begin the objective statement.
    - Use active verbs for the start of each point.  
    - Use present tense.

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

    TEXT: {0}
    RESPONSE:
    """
}


def generate_prompt(content: str,
                    prompt_name: str = "title",
                    max_tokens: int = 50,
                    temperature: float = 0.0,
                    additional_content: str = None) -> str:

    if prompt_name in ("title", "subtitle", "science", "objective"):
        prompt = prompt_queue[prompt_name].format(example_text_one, example_text_two, content)

    elif prompt_name in ("approach"):
        if additional_content is None:
            additional_content = content
        prompt = prompt_queue[prompt_name].format(example_text_two, content, additional_content)

    elif prompt_name in ("figure", "caption", "impact", "summary", "ppt_impact"):
        prompt = prompt_queue[prompt_name].format(content)

    return hlt.generate_content(system_scope=system_scope,
                                prompt=prompt,
                                max_tokens=max_tokens,
                                temperature=temperature,
                                max_allowable_tokens=max_allowable_tokens)


