from functools import partial
from langgraph.graph import StateGraph, END

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

from tavily import TavilyClient

from reviewer_agent import reviewer_node
from graph_agent import graph_node

from state import AgentState
from planner_agent import planner_node
from searcher_agent import searcher_node
from writer_agent import writer_node


# ==================================
# MULTI LLM SUPPORT
# ==================================

def get_llm(
    selected_provider,
    google_api_key,
    groq_api_key,
    openrouter_api_key
):

    if selected_provider == "Google Gemini":

        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=google_api_key,
            temperature=0.5
        )

    elif selected_provider == "Groq":

        return ChatGroq(
            groq_api_key=groq_api_key,
            model_name="llama-3.3-70b-versatile",
            temperature=0.5
        )

    elif selected_provider == "OpenRouter":

        return ChatOpenAI(
            api_key=openrouter_api_key,
            base_url="https://openrouter.ai/api/v1",
            model="deepseek/deepseek-chat",
            temperature=0.5
        )

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=google_api_key,
        temperature=0.5
    )


# ==================================
# BUILD GRAPH
# ==================================

def build_graph(
    google_api_key,
    tavily_api_key,
    groq_api_key,
    openrouter_api_key,
    selected_provider
):

    llm = get_llm(
        selected_provider,
        google_api_key,
        groq_api_key,
        openrouter_api_key
    )

    tavily = TavilyClient(
        api_key=tavily_api_key
    )

    p_node = partial(
        planner_node,
        llm=llm
    )

    s_node = partial(
        searcher_node,
        tavily_client=tavily
    )

    w_node = partial(
        writer_node,
        llm=llm
    )

    r_node = partial(
        reviewer_node,
        llm=llm
    )

    g_node = graph_node

    workflow = StateGraph(
        AgentState
    )

    # =====================
    # NODES
    # =====================

    workflow.add_node(
        "planner",
        p_node
    )

    workflow.add_node(
        "searcher",
        s_node
    )

    workflow.add_node(
        "writer",
        w_node
    )

    workflow.add_node(
        "reviewer",
        r_node
    )

    workflow.add_node(
        "graph",
        g_node
    )

    # =====================
    # ENTRY POINT
    # =====================

    workflow.set_entry_point(
        "planner"
    )

    # =====================
    # FLOW
    # =====================

    workflow.add_edge(
        "planner",
        "searcher"
    )

    workflow.add_edge(
        "searcher",
        "writer"
    )

    workflow.add_edge(
        "writer",
        "reviewer"
    )

    workflow.add_edge(
        "reviewer",
        "graph"
    )

    workflow.add_edge(
        "graph",
        END
    )

    return workflow.compile()
