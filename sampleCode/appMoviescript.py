from typing import List
from rich.pretty import pprint
from pydantic import BaseModel, Field
from agno.agent import Agent, RunResponse
from agno.models.openai import OpenAIChat
from agno.models.groq import Groq
import streamlit as st


import os

from dotenv import load_dotenv

load_dotenv()

theModel="llama3-8b-8192"

class MovieScript(BaseModel):
    setting: str = Field(..., description="Provide a nice setting for a blockbuster movie.")
    ending: str = Field(..., description="Ending of the movie. If not available, provide a happy ending.")
    genre: str = Field(
        ..., description="Genre of the movie. If not available, select action, thriller or romantic comedy."
    )
    name: str = Field(..., description="Give a name to this movie")
    characters: List[str] = Field(..., description="Name of characters for this movie.")
    storyline: str = Field(..., description="3 sentence storyline for the movie. Make it exciting!")
    year: str = Field(..., description="The year this script takes place in")

json_mode_agent= Agent(
    model=Groq(id=theModel),
    #model=OpenAIChat(id="gpt-4o"),
    description="You write movie scripts.",
    response_model=MovieScript,
)

structured_output_agent= Agent(
    #model=OpenAIChat(id="gpt-4o"),
    model=Groq(id=theModel),
    description="You write movie scripts",
    response_model=MovieScript,
    structured_outputs=True,
)

#Streamlit
st.set_page_config("Movie Script Creater",layout="wide")

st.header("Movie Script Creator")

theTopic= st.chat_input("Import city for the setting")


with st.sidebar:
    st.write("Where droplists shall be")

if theTopic:

    with st.spinner("Thinking..."):
        json_mode_response: RunResponse = json_mode_agent.run(theTopic)
        structured_output_response: RunResponse = structured_output_agent.run(theTopic)
        st.markdown(structured_output_response.content.setting)
        st.markdown(f"Year: {structured_output_response.content.year}")
        st.markdown(f"Storyline: {structured_output_response.content.storyline}")
