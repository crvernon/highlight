[![build](https://github.com/crvernon/highlight/actions/workflows/build.yml/badge.svg)](https://github.com/crvernon/highlight/actions/workflows/build.yml)
[![DOI](https://zenodo.org/badge/632456925.svg)](https://zenodo.org/doi/10.5281/zenodo.13750915)


## highlight

#### Generate publication highlights using AI

### Setting Up OpenAI API Key

To use the OpenAI API, you need to set up an API key and set it as an environment variable.

1. Obtain your OpenAI API key from the [OpenAI website](https://platform.openai.com/api-keys).

2. Set the API key as an environment variable:
    - On Windows:
        ```bash
        set OPENAI_API_KEY=your_api_key_here
        ```
    - On macOS and Linux:
        ```bash
        export OPENAI_API_KEY=your_api_key_here
        ```

Replace `your_api_key_here` with your actual OpenAI API key.

### Installation

#### Clone this repository
Navigate to the directory you want to store this repo in and run:

```bash
git clone https://github.com/crvernon/highlight.git
```

To install this Python package in a virtual environment, you can use either pip or Anaconda.

#### Using pip

1. Create a virtual environment:
    ```bash
    python -m venv highlight_env
    ```

2. Activate the virtual environment:
    - On Windows:
        ```bash
        highlight_env\Scripts\activate
        ```
    - On macOS and Linux:
        ```bash
        source highlight_env/bin/activate
        ```

3. Install the package from the cloned `highlight` directory:
    ```bash
    pip install .
    ```

#### Using Anaconda

1. Create a virtual environment:
    ```bash
    conda create --name highlight_env python=3.9
    ```

2. Activate the virtual environment:
    ```bash
    conda activate highlight_env
    ```

3. Install the package from the cloned `highlight` directory:
    ```bash
    pip install .
    ```

### Running the App

To run the app using Streamlit, follow these steps:

1. Ensure your virtual environment is activated.

2. Run the Streamlit app from the `highlight` directory:
    ```bash
    streamlit run app.py
    ```
