from typing import List, Union
from dotenv import load_dotenv, find_dotenv
from langchain.agents import tool, Tool
from langchain_core.agents import AgentAction, AgentFinish
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.prompts import PromptTemplate
from langchain.tools.render import render_text_description
from langchain_openai import ChatOpenAI
from langchain.agents.format_scratchpad import format_log_to_str

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
        raise ValueError(f"Tool with name {tool_name} not found")


if __name__ == "__main__":
    intermediate_steps = []

    print("Hello langchian")

    tools: list[tool] = [get_text_length]

    template = """
    Answer the following questions as best you can. You have access to the following tools:
    
    {tools}
    
    Use the following format:

    ** DOnt send obesetion and final answer at the same time**
    
    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the result
 
    
    Begin!
    
    Question: {input}
    Thought: {agent_scratchpad}
    """

    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )

    llm = ChatOpenAI(temperature=0, stop_sequences=["\nObservation"], model='gpt-4o')

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_log_to_str(x["agent_scratchpad"]),
        }
        | prompt
        | llm
        | ReActSingleInputOutputParser()
    )

    agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
        {
            "input": 'What the length of the text ANIMAL?',
            "agent_scratchpad": intermediate_steps,
        }
    )

    if isinstance(agent_step, AgentAction):
        tool_name = agent_step.tool

        tool_to_use = find_tool_by_name(tools, tool_name)

        tool_input = agent_step.tool_input

        print(tool_input)

        observation = tool_to_use.func(str(tool_input))

        print(f"{observation}")

        intermediate_steps.append((agent_step, str(observation)))

    print(intermediate_steps)

    agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
        {
            "input": 'What the length of the text ANIMAL?',
            "agent_scratchpad": intermediate_steps,
        }
    )

    print(agent_step)
