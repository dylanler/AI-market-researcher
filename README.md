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

Installation
This project requires Python 3.6+ and the following packages:

- gradio
- bs4
- openai
- requests
- pandas
- langchain

You can install these packages using pip:
