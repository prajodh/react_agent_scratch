from dotenv import load_dotenv
from langchain.agents import tool
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools.render import render_text_description
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

@tool
def get_text_length(str):
    """
    return the length of text
    """
    return len(str)


if __name__ == "__main__":
    # print(get_text_length.invoke(input = {"str":"Hello World"}))
    tools = [get_text_length]

    prompt  ="""
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought:
    """
    prompt_template = PromptTemplate.from_template(template = prompt).partial(tools = render_text_description(tools), tool_names = ", ".join(x.name for x in tools))
    llm = ChatGoogleGenerativeAI(temperature=0, model="gemini-1.5-flash", stop = ["\nObservation"])
    agent = {"input": lambda x : x["input"]} | prompt_template | llm | StrOutputParser()
    agent_step = agent.invoke(input = {"input":"what is the text length of 'DOG' in characters"})
    print(agent_step)
