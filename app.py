import os
from bs4 import BeautifulSoup
import gradio as gr
import openai
import requests
from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain
from langchain.agents import load_tools, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.llms import OpenAI
from collections import Counter
import pandas as pd
from langchain.document_loaders import TextLoader, YoutubeLoader
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.indexes import VectorstoreIndexCreator


OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
GOOGLE_MAPS_API = os.environ['GOOGLE_MAPS_API']

#### TAB 1 ####

def get_location_data(search_term, location):
    # First, we get the latitude and longitude coordinates of the location
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": location,
        "key": GOOGLE_MAPS_API
    }
    response = requests.get(url, params=params)
    location_data = response.json()["results"][0]["geometry"]["location"]
    
    # Next, we use the Places API nearbysearch endpoint to find places matching the search term
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{location_data['lat']},{location_data['lng']}",
        "radius": "10000", # 10km radius
        #"type": search_term,
        "keyword" : search_term,
        "key": GOOGLE_MAPS_API
    }
    response = requests.get(url, params=params)
    results = response.json()["results"]
    
    # We only want the first 5 results
    results = results[:5]
    
    # For each result, we get the place details to retrieve the description and top reviews
    locations = []
    for result in results:
        place_id = result["place_id"]
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            "place_id": place_id,
            "fields": "name,formatted_address,formatted_phone_number,rating,review",
            "key": GOOGLE_MAPS_API
        }
        response = requests.get(url, params=params)
        place_details = response.json()["result"]
        
        # Create a dictionary representing the location and add it to the list
        location_dict = {
            "name": place_details["name"],
            "address": place_details["formatted_address"],
            #"phone_number": place_details.get("formatted_phone_number", "N/A"),
            #"rating": place_details.get("rating", "N/A"),
            "reviews": []
        }
        
        # Add the top 3 reviews to the dictionary
        reviews = place_details.get("reviews", [])
        for review in reviews[:3]:
            review_dict = {
                #"author": review["author_name"],
                #"rating": review["rating"],
                "text": review["text"],
                #"time": review["relative_time_description"]
            }
            location_dict["reviews"].append(review_dict)
        
        locations.append(location_dict)
    
    return locations

# Define the function to be used in the Gradio app
def find_competitors(product, location):
    locations = get_location_data(product, location)
    if len(locations) == 0:
        return f"No competitors found for {product} in {location}."
    
    output_str = f"Top competitors for {product} in {location}:"
    for i, loc in enumerate(locations):
        output_str += f"\n{i+1}. {loc['name']}"
        output_str += f"\nAddress: {loc['address']}"
        #output_str += f"\nPhone number: {loc['phone_number']}"
        #output_str += f"\nRating: {loc['rating']}"
        output_str += f"\nTop 3 reviews:"
        for review in loc['reviews']:
            output_str += f"\n- {review['text']}"
            #output_str += f"\n  Author: {review['author']}"
            #output_str += f"\n  Rating: {review['rating']}"
            #output_str += f"\n  Time: {review['time']}"
            
    output_str2 = f"Top competitors for {product} in {location}:"
    for i, loc in enumerate(locations):
        output_str2 += f"\n{i+1}. {loc['name']}"
        output_str2 += f"\nAddress: {loc['address']}"
    
    #return output_str

    prompt_input = '''
    You are an expert management consultant that rivals the best of Mckinsey, Bain, BCG.
    The client wants to sell {} in {}.
    {}
    Provide an analysis of the following:
    - From the competition and reviews about its products and come up with creative insights to recommend the client execute as part of a differentiating business strategy.
    - From there, think step by step, explain 5 strategies in bullet points of a creative and effective business plan.
    - Suggest a location for the client and explain the rationale of this locatioin.
    - Let us think step by step.
    '''.format(product, location, output_str)
   
    template = '''
    {history}
    {human_input}
    '''
    prompt = PromptTemplate(
        input_variables=["history", "human_input"], 
        template=template
    )

    chatgpt_chain = LLMChain(
        llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5,openai_api_key=OPENAI_API_KEY), 
        prompt=prompt, 
        verbose=True, 
        memory=ConversationBufferWindowMemory(k=10),
    )

    output = output_str2 + "\n\n" + chatgpt_chain.predict(human_input=prompt_input)
    
    return(output)

# Create the Gradio app interface
inputs = [
    gr.inputs.Textbox(label="Product to research"),
    gr.inputs.Textbox(label="Location")
]


output = gr.outputs.Textbox(label="AI Analysis")

iface1 = gr.Interface(fn=find_competitors, inputs=inputs, outputs=output, title="Market Research AI", 
             description="Input a product and a location.  The AI analyst will help you research nearby competitors, formulate a business plan to differentiate you from your competitors, and recommend a strategic location for your business.")

#### TAB 2 ####

template2 = '''
{history}
{human_input}
'''
prompt2 = PromptTemplate(
    input_variables=["history", "human_input"], 
    template=template2
)

chatgpt_chain = LLMChain(
    llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.5,openai_api_key=OPENAI_API_KEY), 
    prompt=prompt2, 
    verbose=True, 
    memory=ConversationBufferWindowMemory(k=10),
)

# Scrape the URL
def scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.extract()

    return soup.get_text()

# Extract keywords
def extract_keywords(prompt_input, num_keywords):
    
    output= chatgpt_chain.predict(human_input=prompt_input)
    output_parser = CommaSeparatedListOutputParser()
    ret_list = output_parser.parse(output)
    
    return ret_list

# Define the function to be used in Gradio
def keywords_from_url(url, num_keywords):
    url_text = scrape(url)
    prompt_input2 = '''
You are an expert SEO optimized, consultant and manager.

Here is the text from a website:

{}

From the text above, extract {} SEO keyphrase that are highly valueble in terms of SEO purpose.

Your response should be a list of comma separated values, eg: `foo, bar, baz
'''.format(url_text, num_keywords)
    
    keywords = extract_keywords(prompt_input2, num_keywords)

    df = pd.DataFrame(keywords, columns=["Keyword"])
    df.index.name = "Rank"
    df.index += 1
    df.to_csv('keywords.csv')
    
    return "keywords.csv"



iface2 = gr.Interface(
    fn=keywords_from_url,
    inputs=[gr.inputs.Textbox(label="URL"), gr.inputs.Slider(minimum=1, maximum=50, step=1, default=10, label="Number of SEO Keywords")],
    outputs=gr.outputs.File(label="Download CSV File"),
    title="SEO Keyword Extractor",
    description="Enter a URL and the number of keywords you want to extract from that page. The output will be a CSV file containing the SEO keywords."
)


#### TAB 3 ####



previous_youtube_url = None
index = None

def get_video_id(url):
    video_id = None
    if 'youtu.be' in url:
        video_id = url.split('/')[-1]
    else:
        video_id = url.split('watch?v=')[-1]
    return video_id

def get_captions(url):
    try:
        video_id = get_video_id(url)
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en'])
        captions = transcript.fetch()

        formatted_captions = ''
        for caption in captions:
            formatted_captions += caption['text'] + ' '

        return formatted_captions

    except Exception as e:
        print(e)
        return "Error. Could not fetch captions."



def answer_question(youtube_url, user_question):
    # You can implement your logic here to process the video, transcribe it, and answer the user question.
    # For now, let's return the user question as output.
    global previous_youtube_url
    global index

    query = '''
    You are an expert researcher that can answer any questions from a given text.  Here is the question:
    {}
    '''.format(str(user_question))

    if previous_youtube_url == youtube_url:
        #index = VectorstoreIndexCreator().from_loaders([loader])
        #query = user_question
        answer = index.query(llm=OpenAI(model="text-davinci-003"), question = query)
    else:
        f= open("temp.txt","w+")
        f.write(get_captions(youtube_url))
        f.close() 
        loader = TextLoader("temp.txt")
    
        index = VectorstoreIndexCreator().from_loaders([loader])
        os.remove("temp.txt")

        #query = user_question
        answer = index.query(llm=OpenAI(model="text-davinci-003"), question = query)

    return answer

iface3 = gr.Interface(
    fn=answer_question,
    inputs=[
        gr.Textbox(lines=1, placeholder="Enter YouTube URL here..."),
        gr.Textbox(lines=1, placeholder="Enter your question here...")
    ],
    outputs=gr.Textbox(),
    title="YouTube Smart Q & A",
    description="Enter a YouTube URL & a question and the app will find the answer from the video captions."
)



#tab1 = gr.Tab("AI Market Research", inputs=iface1.inputs, outputs=iface1.outputs)
#tab2 = gr.Tab("SEO Keyword Extractor", inputs=iface2.inputs, outputs=iface2.outputs)

demo = gr.TabbedInterface([iface2, iface1, iface3], ["SEO Keyword Extractor", "AI Market Researcher","YouTube Smart Q & A"])
demo.launch()
