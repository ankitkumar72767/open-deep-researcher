from typing import TypedDict, List


class AgentState(TypedDict):

    topic: str

    chat_history: str

    summary_length: str

    search_mode: str

    research_plan: List[str]

    search_results: str

    final_report: str

    review_feedback: str

    graph_keywords: List[str]
