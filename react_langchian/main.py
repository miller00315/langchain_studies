from typing import List, Union
from dotenv import load_dotenv, find_dotenv
from langchain.agents import tool, Tool
from langchain_core.agents import AgentAction, AgentFinish
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.prompts import PromptTemplate
from langchain.tools.render import render_text_description
from langchain_openai import ChatOpenAI

load_dotenv(dotenv_path=find_dotenv())


@tool
def get_text_length(text: str) -> int:
    """Returns the length of the text by characters"""

    print(f"Get_text_length enter with {text=}")

    text = text.strip("'\n").strip('"')

    return len(text)

def find_tool_by_name(tools: List[Tool], tool_name: str) -> Tool:
    result = list(filter(lambda x: x.name == tool_name, tools))
    
    if result:
        return result[0]
    else:
        raise ValueError(f'Tool with name {tool_name} not found')


if __name__ == "__main__":
    print("Hello langchian")

    tools: list[tool] = [get_text_length]

    template = """
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
    
    Begin!
    
    Question: {input}\
    Thought:
    """

    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )

    llm = ChatOpenAI(temperature=0, stop_sequences=['\nObservation'])

    agent = {'input': lambda x: x['input']} | prompt | llm | ReActSingleInputOutputParser()

    agent_step: Union[AgentAction, AgentFinish] = agent.invoke({'input': 'What the length of "DOG" in chanracters?'})

    if isinstance(agent_step, AgentAction):
        tool_name = agent_step.tool
        
        tool_to_use = find_tool_by_name(tools, tool_name)

        tool_input = agent_step.tool_input

        observation = tool_to_use.func(str(tool_input))

        print(observation)







