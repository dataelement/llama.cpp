from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_cohere import ChatCohere, create_cohere_react_agent
from langchain.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor

from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.agents import Tool
from langchain_experimental.utilities import PythonREPL
from langchain_core.tools import tool
import random


def test1():
    llm = ChatCohere()

    internet_search = TavilySearchResults(max_results=4)
    internet_search.name = "internet_search"
    internet_search.description = "Route a user query to the internet"

    prompt = ChatPromptTemplate.from_template("{input}")

    agent = create_cohere_react_agent(
        llm,
        [internet_search],
        prompt
    )

    agent_executor = AgentExecutor(agent=agent, tools=[internet_search], verbose=True)

    agent_executor.invoke({
        "input": "In what year was the company that was founded as Sound of Music added to the S&P 500?",
    })


def test2():
    # tool1
    internet_search = TavilySearchResults()
    internet_search.name = "internet_search"
    internet_search.description = "Returns a list of relevant document snippets for a textual query retrieved from the internet."


    class TavilySearchInput(BaseModel):
        query: str = Field(description="Query to search the internet with")
    internet_search.args_schema = TavilySearchInput

    # tool2
    python_repl = PythonREPL()
    python_tool = Tool(
        name="python_repl",
        description="Executes python code and returns the result. The code runs in a static sandbox without interactive mode, so print output or save output to a file.",
        func=python_repl.run,
    )
    python_tool.name = "python_interpreter"

    # from langchain_core.pydantic_v1 import BaseModel, Field
    class ToolInput(BaseModel):
        code: str = Field(description="Python code to execute.")

    python_tool.args_schema = ToolInput
        
    @tool
    def random_operation_tool(a: int, b: int):
        """Calculates a random operation between the inputs."""
        coin_toss = random.uniform(0, 1)
        return {'output': a*b}
    
        if coin_toss > 0.5:
            return {'output': a*b}
        else:
            return {'output': a+b}

    random_operation_tool.name = "random_operation" # use python case
    random_operation_tool.description = "Calculates a random operation between the inputs."

    class random_operation_inputs(BaseModel):
        a: int = Field(description="First input")
        b: int = Field(description="Second input")
    random_operation_tool.args_schema = random_operation_inputs
        

    # LLM
    llm = ChatCohere(model="command-r-plus", temperature=0.3)

    # Preamble
    preamble = """
You are an expert who answers the user's question with the most relevant datasource. You are equipped with an internet search tool and a special vectorstore of information about how to write good essays.
You also have a 'random_operation_tool' tool, you must use it to compute the random operation between two numbers.
"""

    # Prompt template
    prompt = ChatPromptTemplate.from_template("{input}")

    # Create the ReAct agent
    agent = create_cohere_react_agent(
        llm=llm,
        tools=[internet_search, python_tool, random_operation_tool],
        prompt=prompt,
    )

    agent_executor = AgentExecutor(agent=agent, tools=[internet_search, python_tool, random_operation_tool], verbose=True)


    # response = agent_executor.invoke({
    #    "input": "Calculate the result of the random operation of 10 and 20. Then find a few fun facts about that number, as well as its prime factors.",
    #    "preamble": preamble,
    # })

    # response['output']

    response = agent_executor.invoke({
         "input": "Hey how are you?",
         "preamble": preamble,
    })

    response['output']

    # note that the modle can directly answer!
     

test2()