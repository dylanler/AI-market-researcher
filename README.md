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

- Youtube Smart Q&A:

Input the URL of a Youtube video and a question.  Click 'Submit' and the app will search through the video captions to find an answer from the video.

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
- pytube
- youtube_transcript_api
- chromadb
- tiktoken

You can install these packages using pip:

```bash
pip install gradio bs4 openai requests pandas langchain youtube_transcript_api pytube chromadb tiktoken
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


### AI Market Researcher

#### Input a product you want to research about and the location you would like to launch the product.

<img width="826" alt="ai-research1" src="https://github.com/dylanler/AI-market-researcher/assets/9219358/e1c82afe-dc36-4da1-95eb-5bfd70347ddb">

#### Wait for about 50-70 seconds and the AI researcher will provide you 4 outputs:

1. Competitors
- <img width="386" alt="ai-competitor" src="https://github.com/dylanler/AI-market-researcher/assets/9219358/50898b3a-dbd0-485e-8605-e10d30a98089">
2. Competitor analysis
- <img width="358" alt="ai-comp2" src="https://github.com/dylanler/AI-market-researcher/assets/9219358/8d009d2c-2add-4105-9c76-266363b8aac4">
3. Creative Insights
- <img width="353" alt="creative-insights" src="https://github.com/dylanler/AI-market-researcher/assets/9219358/6eaa6902-3a0a-4094-a868-425cab030b6c">
4. Business Plan
- <img width="352" alt="strat" src="https://github.com/dylanler/AI-market-researcher/assets/9219358/71343ce1-adc3-441f-abcd-dffd56b2c864">
5. Location strategy & rationale
- <img width="352" alt="location-rationale" src="https://github.com/dylanler/AI-market-researcher/assets/9219358/2cb8bdd3-575a-4a82-85bb-2af8aec2b77e">

### Youtube Smart Q&A

### Find a Youtube video url and input it in the text box. Ask your question in the question text box.

<img width="285" alt="samplevideo" src="https://github.com/dylanler/AI-market-researcher/assets/9219358/01e24da5-1ce8-48ce-95cf-0e6a9f36c211">

- Youtube URL: https://www.youtube.com/watch?v=f20wXjWHh2o

#### Sample Question 1

<img width="943" alt="ans1" src="https://github.com/dylanler/AI-market-researcher/assets/9219358/f66ec787-3110-4a0b-a465-3322fceea8c9">

#### Sample Question 2

<img width="944" alt="ans2" src="https://github.com/dylanler/AI-market-researcher/assets/9219358/de5780e0-a587-426b-bece-14a7bd1467bc">

---------------------------------------------------------------------------------------------

## Deploying the App using Amazon Web Services (AWS)
Amazon Web Services (AWS) offers a variety of services for deploying applications, including EC2 for running virtual servers, EBS for block storage, and Elastic Beanstalk for deploying and scaling web applications and services developed with various languages. Here, we'll use Elastic Beanstalk to deploy our Gradio app.

## Pre-requisites
AWS Account: Before you begin, you need to have an AWS account. If you do not have one, you can create one here.

AWS CLI: You will also need the AWS CLI (Command Line Interface) installed on your local machine. You can download it here.

AWS Elastic Beanstalk CLI (EB CLI): This is a command-line interface for Elastic Beanstalk to deploy and manage applications. Install it following these instructions.

Docker: As Gradio apps run in a Docker container, you need Docker installed on your machine. Get Docker here.

## Steps to Deploy
Prepare your application

Your application should have a Dockerfile for running the application in a Docker container, and a requirements.txt file listing all the Python dependencies.

Here's an example of a Dockerfile:

```sql
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860
CMD [ "python", "app.py" ]
```

## Initialize the Elastic Beanstalk application

Navigate to your application's root directory in the terminal and run:

```bash
eb init -p docker
```
This will create a new Elastic Beanstalk Docker application.

## Create an environment and deploy the application

Now you can create an Elastic Beanstalk environment and deploy your application to it by running:

```bash
eb create gradio-app-env
```
Replace gradio-app-env with the name you want for your Elastic Beanstalk environment.

## Open the application in a web browser

After your application is deployed, you can open it in a web browser using:

```bash
eb open
```
Please note that deploying applications on AWS may incur charges. Make sure to terminate resources after use if you want to avoid continuous charges.

## Cleaning Up
To avoid incurring future charges, you can delete the resources you created for this app by terminating the Elastic Beanstalk environment:

```bash
eb terminate gradio-app-env
```
Remember to replace gradio-app-env with the name of your Elastic Beanstalk environment.

You can also delete the application:

```bash
eb delete-app gradio-app
```
Again, replace gradio-app with the name of your Elastic Beanstalk application.

For further details, refer to the official AWS Elastic Beanstalk Developer Guide.


