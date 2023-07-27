import io
import os

from docxtpl import DocxTemplate
import openai
from pptx import Presentation
import streamlit as st

import highlight as hlt
import prompts


def generate_content(container,
                     content,
                     prompt_name="title",
                     result_title="Title Result:",
                     max_tokens=50,
                     temperature=0.0,
                     box_height=200,
                     additional_content=None,
                     max_word_count=100,
                     min_word_count=75,
                     model="gpt-4"):

    response = prompts.generate_prompt(content=content,
                                       prompt_name=prompt_name,
                                       temperature=temperature,
                                       max_tokens=max_tokens,
                                       additional_content=additional_content)
    container.markdown(result_title)

    word_count = len(response.split())

    if word_count > max_word_count:

        # construct word count reduction prompt
        reduction_prompt = prompts.prompt_queue["reduce_wordcount"].format(min_word_count, max_word_count, response)

        messages = [{"role": "system",
                     "content": prompts.prompt_queue["system"]},
                    {"role": "user",
                     "content": reduction_prompt}]

        reduced_response = openai.ChatCompletion.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=messages)

        response = reduced_response["choices"][0]["message"]["content"]

    container.text_area(label=result_title,
                        value=response,
                        label_visibility="collapsed",
                        height=box_height)

    st.write(f"Word count:  {len(response.split())}")

    return response


if "reduce_document" not in st.session_state:
    st.session_state.reduce_document = False

if "content_dict" not in st.session_state:
    st.session_state.content_dict = {}

if "max_allowable_tokens" not in st.session_state:
    st.session_state.max_allowable_tokens = 8192

# parameters for word document
if "title_response" not in st.session_state:
    st.session_state.title_response = None

if "subtitle_response" not in st.session_state:
    st.session_state.subtitle_response = None

if "photo" not in st.session_state:
    st.session_state.photo = None

if "photo_link" not in st.session_state:
    st.session_state.photo_link = None

if "photo_site_name" not in st.session_state:
    st.session_state.photo_site_name = None

if "image_caption" not in st.session_state:
    st.session_state.image_caption = None

if "science_response" not in st.session_state:
    st.session_state.science_response = None

if "impact_response" not in st.session_state:
    st.session_state.impact_response = None

if "summary_response" not in st.session_state:
    st.session_state.summary_response = None

if "funding" not in st.session_state:
    st.session_state.funding = None

if "citation" not in st.session_state:
    st.session_state.citation = None

if "related_links" not in st.session_state:
    st.session_state.related_links = None

# additional word doc content that is not in the template
if "figure_response" not in st.session_state:
    st.session_state.figure_response = None

if "caption_response" not in st.session_state:
    st.session_state.caption_response = None

if "output_file" not in st.session_state:
    st.session_state.output_file = None

# parameters for the ppt slide
if "objective_response" not in st.session_state:
    st.session_state.objective_response = None

if "approach_response" not in st.session_state:
    st.session_state.approach_response = None

if "ppt_impact_response" not in st.session_state:
    st.session_state.ppt_impact_response = None


# Force responsive layout for columns also on mobile
st.write(
    """<style>
    [data-testid="column"] {
        width: calc(50% - 1rem);
        flex: 1 1 calc(50% - 1rem);
        min-width: calc(50% - 1rem);
    }
    </style>""",
    unsafe_allow_html=True,
)

# Render streamlit page
st.title("Research Highlight Generator")

st.markdown(
    "This app uses OpenAI's GPT-4 to generated formatted research highlight content from an input file."
)

st.markdown("#### Input your OpenAI API Key")
st.markdown("Your account needs to be approved for GPT-4 use.")

example_api_key_length = 51
api_key = st.text_input(
    label="Enter your OpenAI API Key",
    placeholder="*"*example_api_key_length,
    type="password")

# set api key
openai.api_key = os.getenv("OPENAI_API_KEY") # api_key

st.markdown("#### Load file to process:")
uploaded_file = st.file_uploader(
    label="### Select PDF or text file to upload",
    type=["pdf", "txt"],
    help="Select PDF or text file to upload",
)

if uploaded_file is not None:

    if uploaded_file.type == "text/plain":
        content_dict = hlt.read_text(uploaded_file)

    elif uploaded_file.type == "application/pdf":
        content_dict = hlt.read_pdf(uploaded_file)

    st.session_state.output_file = uploaded_file.name

    st.code(f"""File specs:\n
    - Number of pages:  {content_dict['n_pages']}
    - Number of characters:  {content_dict['n_characters']}
    - Number of words: {content_dict['n_words']}
    - Number of tokens: {content_dict['n_tokens']}
    """)

    if content_dict['n_tokens'] > st.session_state.max_allowable_tokens:
        msg = f"""
    The number of tokens in your document exceeds the maximum allowable tokens for GPT-4.
    This will cause your queries to fail.
    The queries account for the number of tokens in a prompt + the number of tokens in your document.
    
    Maximum allowable token count from GPT-4: {st.session_state.max_allowable_tokens}
    
    Your documents token count: {content_dict['n_tokens']}
    
    Token deficit: {content_dict['n_tokens'] - st.session_state.max_allowable_tokens}
    """
        st.error(msg, icon="🚨")

        st.session_state.reduce_document = st.radio(
            """Would you like me to attempt to reduce the size of 
        your document by keeping only relevant information? 
        If so, I will give you a file to download with the content 
        so you only have to do this once.
        If you choose to go through with this, it may take a while
        to process, usually on the order of 15 minutes for a 20K token
        document.
        Alternatively, you can copy and paste the contents that you
        know are of interest into a text file and upload that
        instead.
    
        """,
            ("Yes", "No"),
        )

    # word document content
    st.markdown('# ')
    st.markdown("### Content to fill in Word document template:")

    # title section
    title_container = st.container()
    title_container.markdown("##### Generate title from text content")
    title_container.markdown("Set desired temperature:")

    # title slider
    title_temperature = title_container.slider("Title Temperature",
                                               0.0,
                                               1.0,
                                               0.2,
                                               label_visibility="collapsed")

    # build container content
    if title_container.button('Generate Title'):

        st.session_state.title_response = generate_content(
            container=title_container,
            content=content_dict["content"],
            prompt_name="title",
            result_title="Title Result:",
            max_tokens=50,
            temperature=title_temperature,
            box_height=50
        )

    else:
        if st.session_state.title_response is not None:
            title_container.markdown("Title Result:")
            title_container.text_area(label="Title Result:",
                                      value=st.session_state.title_response,
                                      label_visibility="collapsed",
                                      height=50)

    # subtitle section
    subtitle_container = st.container()
    subtitle_container.markdown("##### Generate subtitle from text content")
    subtitle_container.markdown("Set desired temperature:")

    # subtitle slider
    subtitle_temperature = subtitle_container.slider("Subtitle Temperature",
                                                     0.0,
                                                     1.0,
                                                     0.5,
                                                     label_visibility="collapsed")

    # build container content
    if subtitle_container.button('Generate Subtitle'):

        if st.session_state.title_response is None:
            st.write("Please generate a Title first.  Subtitle generation considers the title response.")
        else:

            st.session_state.subtitle_response = generate_content(
                container=subtitle_container,
                content=content_dict["content"],
                prompt_name="subtitle",
                result_title="Subtitle Result:",
                max_tokens=100,
                temperature=subtitle_temperature,
                box_height=50,
                additional_content=st.session_state.title_response,
                max_word_count=100,
                min_word_count=75
            )

    else:
        if st.session_state.subtitle_response is not None:
            subtitle_container.markdown("Subtitle Result:")
            subtitle_container.text_area(label="Subtitle Result:",
                                         value=st.session_state.subtitle_response,
                                         label_visibility="collapsed",
                                         height=50)

    # science section
    science_container = st.container()
    science_container.markdown("##### Generate science summary from text content")
    science_container.markdown("Set desired temperature:")

    # slider
    science_temperature = science_container.slider("Science Summary Temperature",
                                                   0.0,
                                                   1.0,
                                                   0.3,
                                                   label_visibility="collapsed")

    # build container content
    if science_container.button('Generate Science Summary'):
        st.session_state.science_response = generate_content(
            container=science_container,
            content=content_dict["content"],
            prompt_name="science",
            result_title="Science Summary Result:",
            max_tokens=200,
            temperature=science_temperature,
            box_height=250,
            max_word_count=100,
            min_word_count=75
        )

    else:
        if st.session_state.science_response is not None:
            science_container.markdown("Science Summary Result:")
            science_container.text_area(label="Science Summary Result:",
                                        value=st.session_state.science_response,
                                        label_visibility="collapsed",
                                        height=250)

    # impact section
    impact_container = st.container()
    impact_container.markdown("##### Generate impact summary from text content")
    impact_container.markdown("Set desired temperature:")

    # slider
    impact_temperature = impact_container.slider("Impact Summary Temperature",
                                                   0.0,
                                                   1.0,
                                                   0.0,
                                                   label_visibility="collapsed")

    # build container content
    if impact_container.button('Generate Impact Summary'):
        st.session_state.impact_response = generate_content(
            container=impact_container,
            content=content_dict["content"],
            prompt_name="impact",
            result_title="Impact Summary Result:",
            max_tokens=700,
            temperature=impact_temperature,
            box_height=250,
            max_word_count=100,
            min_word_count=75
        )

    else:
        if st.session_state.impact_response is not None:
            impact_container.markdown("Impact Summary Result:")
            impact_container.text_area(label="Impact Summary Result:",
                                        value=st.session_state.impact_response,
                                        label_visibility="collapsed",
                                        height=250)

    # general summary section
    summary_container = st.container()
    summary_container.markdown("##### Generate general summary from text content")
    summary_container.markdown("Set desired temperature:")

    # slider
    summary_temperature = summary_container.slider("General Summary Temperature",
                                                   0.0,
                                                   1.0,
                                                   0.3,
                                                   label_visibility="collapsed")

    # build container content
    if summary_container.button('Generate General Summary'):
        st.session_state.summary_response = generate_content(
            container=summary_container,
            content=content_dict["content"],
            prompt_name="summary",
            result_title="General Summary Result:",
            max_tokens=700,
            temperature=summary_temperature,
            box_height=400,
            max_word_count=200,
            min_word_count=100
        )

    else:
        if st.session_state.summary_response is not None:
            summary_container.markdown("General Summary Result:")
            summary_container.text_area(label="General Summary Result:",
                                        value=st.session_state.summary_response,
                                        label_visibility="collapsed",
                                        height=400)

    # figure recommendations section
    figure_container = st.container()
    figure_container.markdown("##### Generate figure recommendations from the general summary")
    figure_container.markdown("Set desired temperature:")

    # slider
    figure_temperature = figure_container.slider("Figure Recommendations Temperature",
                                                 0.0,
                                                 1.0,
                                                 0.9,
                                                 label_visibility="collapsed")

    # build container content
    if figure_container.button('Generate Figure Recommendations'):

        if st.session_state.summary_response is None:
            st.write("Please generate a general summary first.")
        else:
            st.session_state.figure_response = generate_content(
                container=figure_container,
                content=st.session_state.summary_response,
                prompt_name="figure",
                result_title="Figure Recommendations Result:",
                max_tokens=200,
                temperature=figure_temperature,
                box_height=200
            )

    else:
        if st.session_state.figure_response is not None:
            figure_container.markdown("Figure Recommendations Result:")
            figure_container.text_area(label="Figure Recommendations Result:",
                                       value=st.session_state.figure_response,
                                       label_visibility="collapsed",
                                       height=200)

    export_container = st.container()
    export_container.markdown("##### Export Word document with new content when ready")

    # template parameters
    word_parameters = {
        'title': st.session_state.title_response,
        'subtitle': st.session_state.subtitle_response,
        'photo': st.session_state.photo,
        'photo_link': st.session_state.photo_link,
        'photo_site_name': st.session_state.photo_site_name,
        'image_caption': st.session_state.image_caption,
        'science': st.session_state.science_response,
        'impact': st.session_state.impact_response,
        'summary': st.session_state.summary_response,
        'funding': st.session_state.funding,
        'citation': st.session_state.citation,
        'related_links': st.session_state.related_links
    }

    # template word document
    template = DocxTemplate("data/highlight_template.docx")
    template.render(word_parameters)
    bio = io.BytesIO()
    template.save(bio)
    if template:
        export_container.download_button(
            label="Export Word Document",
            data=bio.getvalue(),
            file_name="modified_template.docx",
            mime="docx"
        )

    # power point slide content
    st.markdown('# ')
    st.markdown("### Content to fill in PowerPoint template template:")

    # objective section
    objective_container = st.container()
    objective_container.markdown("##### Generate objective summary from text content")
    objective_container.markdown("Set desired temperature:")

    # slider
    objective_temperature = objective_container.slider("Objective Temperature",
                                                   0.0,
                                                   1.0,
                                                   0.3,
                                                   label_visibility="collapsed")

    # build container content
    if objective_container.button('Generate Objective'):
        st.session_state.objective_response = generate_content(
            container=objective_container,
            content=content_dict["content"],
            prompt_name="objective",
            result_title="Objective Result:",
            max_tokens=300,
            temperature=objective_temperature,
            box_height=250
        )

    else:
        if st.session_state.objective_response is not None:
            objective_container.markdown("Objective Result:")
            objective_container.text_area(label="Objective Result:",
                                        value=st.session_state.objective_response,
                                        label_visibility="collapsed",
                                        height=250)

    # approach section
    approach_container = st.container()
    approach_container.markdown("##### Generate approach summary from text content")
    approach_container.markdown("Set desired temperature:")

    # slider
    approach_temperature = approach_container.slider("Approach Temperature",
                                                   0.0,
                                                   1.0,
                                                   0.1,
                                                   label_visibility="collapsed")

    # build container content
    if approach_container.button('Generate Approach'):
        st.session_state.approach_response = generate_content(
            container=approach_container,
            content=content_dict["content"],
            prompt_name="approach",
            result_title="Approach Result:",
            max_tokens=300,
            temperature=approach_temperature,
            box_height=250,
            additional_content=st.session_state.objective_response
        )

    else:
        if st.session_state.approach_response is not None:
            approach_container.markdown("Approach Result:")
            approach_container.text_area(label="Approach Result:",
                                        value=st.session_state.approach_response,
                                        label_visibility="collapsed",
                                        height=250)

    # power point impact section
    ppt_impact_container = st.container()
    ppt_impact_container.markdown("##### Generate impact points from text content")
    ppt_impact_container.markdown("Set desired temperature:")

    # slider
    ppt_impact_temperature = ppt_impact_container.slider("Impact Points Temperature",
                                                   0.0,
                                                   1.0,
                                                   0.1,
                                                   label_visibility="collapsed")

    # build container content
    if ppt_impact_container.button('Generate Impact Points'):
        st.session_state.ppt_impact_response = generate_content(
            container=ppt_impact_container,
            content=content_dict["content"],
            prompt_name="ppt_impact",
            result_title="Impact Points Result:",
            max_tokens=300,
            temperature=ppt_impact_temperature,
            box_height=250
        )

    else:
        if st.session_state.ppt_impact_response is not None:
            ppt_impact_container.markdown("Impact Points Result:")
            ppt_impact_container.text_area(label="Impact Points Result:",
                                        value=st.session_state.ppt_impact_response,
                                        label_visibility="collapsed",
                                        height=250)

    ppt_export_container = st.container()
    ppt_export_container.markdown("##### Export PowerPoint document with new content when ready")

    # template PPTX document
    ppt_template = Presentation("data/highlight_template.pptx")
    slide = ppt_template.slides[0]
    content_shapes = [i for i in slide.shapes if i.has_text_frame]
    objective_block = content_shapes[0]
    title_block = content_shapes[1]
    reference_block = content_shapes[2]
    caption_block = content_shapes[3]
    approach_block = content_shapes[4]
    impact_block = content_shapes[5]

    bio = io.BytesIO()
    ppt_template.save(bio)

    if ppt_export_container:

        objective_block.text = st.session_state.objective_response
        title_block.text = st.session_state.title_response
        reference_block.text = "fill in"
        caption_block.text = "fill in"
        approach_block.text = st.session_state.approach_response
        impact_block.text = st.session_state.impact_response

        export_container.download_button(
            label="Export PowerPoint Document",
            data=bio.getvalue(),
            file_name="modified_template.pptx",
            mime="pptx"
        )