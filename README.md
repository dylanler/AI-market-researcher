# AI Market Researcher & SEO Keyword Extractor
A multi-tabbed Gradio application that leverages the power of AI to provide detailed market research and SEO keyword extraction.

## Description
This application has two main functionalities:

AI Market Researcher: Given a product and a location, the AI Analyst researches nearby competitors, formulates a business plan to differentiate your product from competitors, and recommends a strategic location for your business.

SEO Keyword Extractor: Given a URL and a number of desired keywords, the SEO Manager extracts valuable key phrases from the website text that are highly beneficial for SEO purposes. The output is provided as a downloadable CSV file.

## How It Works

- AI Market Researcher:

Input your product and location in the textboxes. Click on 'Submit' to get the analysis. The AI uses the Google Maps API to fetch information about competitors in the specified location and then formulates a strategy.

- SEO Keyword Extractor:

Input the URL of a webpage and the number of keywords you want to extract. Click on 'Submit' to get a CSV file containing the SEO keywords.

## Live Demo
URL: https://huggingface.co/spaces/django-ochain/AI-market-researcher

## Installation
This project requires Python 3.6+ and the following packages:

- gradio
- bs4
- openai
- requests
- pandas
- langchain

You can install these packages using pip:

```bash
pip install gradio bs4 openai requests pandas langchain
```

You also need to have API keys for Google Maps and OpenAI, which should be set as environment variables. In a Unix-like OS, you can do this by adding these lines to your shell profile file (.bashrc, .zshrc, etc.):

```bash
export OPENAI_API_KEY="your_openai_key"
export GOOGLE_MAPS_API="your_google_maps_key"```
```

## Usage
Clone this repository.

1. Make sure you have all the required packages installed and API keys set up.
2. Run python app.py (or however you named the Python file containing this Gradio app).
3. Open the link shown in the terminal to interact with the application.
4. Please note: The actual Python filename and instructions may vary based on your specific setup and the name you give to the Python file.

## How to Use

### SEO Keyword Extractor

1. Insert URL and pick the number of SEO keywords you want extracted from the web page.

<img width="835" alt="seo_ss" src="https://github.com/dylanler/AI-market-researcher/assets/9219358/7e6bde25-e0ca-40dc-b5dc-b8ea2f0984e7">

2. Download a list of keywords as a csv file.

<img width="212" alt="csv--ss" src="https://github.com/dylanler/AI-market-researcher/assets/9219358/70166536-d45b-4c3a-a9e3-0625546c0149">
