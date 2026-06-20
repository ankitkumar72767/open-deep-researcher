from functools import partial
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from tavily import TavilyClient

from state import AgentState
from planner_agent import planner_node
from searcher_agent import searcher_node
from writer_agent import writer_node


def build_graph(openai_api_key, tavily_api_key):

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=openai_api_key,
        temperature=0.5,
        max_tokens=1500
    )

    tavily = TavilyClient(api_key=tavily_api_key)

    p_node = partial(planner_node, llm=llm)
    s_node = partial(searcher_node, tavily_client=tavily)
    w_node = partial(writer_node, llm=llm)

    workflow = StateGraph(AgentState)

    workflow.add_node("planner", p_node)
    workflow.add_node("searcher", s_node)
    workflow.add_node("writer", w_node)

    workflow.set_entry_point("planner")

    workflow.add_edge("planner", "searcher")
    workflow.add_edge("searcher", "writer")
    workflow.add_edge("writer", END)

    return workflow.compile()
