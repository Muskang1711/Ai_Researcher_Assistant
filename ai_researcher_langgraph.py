from typing import Annotated, Literal
from typing_extensions import TypedDict
from dotenv import load_dotenv
from langgraph.graph.message import add_messages
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Step 1: Define State
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Step 2: Define Tools
from arxiv_tool import arxiv_search
from write_pdf import render_latex_pdf
from read_pdf import read_pdf
from langgraph.prebuilt import ToolNode

tools = [arxiv_search, read_pdf, render_latex_pdf]
tool_node = ToolNode(tools)

# Step 3: Define Model
from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(model="gemini-1.5-flash").bind_tools(tools)

# Step 4: Define Workflow Nodes
from langgraph.graph import START, StateGraph
from langgraph.constants import END
def call_model(state: State):
    logger.debug("=== [Agent Node] ===")
    logger.debug(f"Incoming state messages: {state['messages']}")

    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}

def should_continue(state: State) -> Literal["tools", "END"]:
    messages = state["messages"]
    last_message = messages[-1]

    logger.debug("=== [should_continue] ===")
    last_message = state["messages"][-1]
    logger.debug(f"Last message: {last_message}")

    if getattr(last_message, "tool_calls", None):  # safer than last_message.tool_call
        return "tools"
    logger.debug("Decision: → END")
    return "END"

# Step 5: Define Graph Workflow
workflow = StateGraph(State)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "END": END,
    },
)
workflow.add_edge("tools", "agent")

# Initial system prompt
INITIAL_PROMPT = """
You are an expert researcher in the fields of physics, mathematics,
computer science, quantitative biology, quantitative finance, statistics,
electrical engineering and systems science, and economics.

You are going to analyze recent research papers in one of these fields in
order to identify promising new research directions and then write a new
research paper. For research information or getting papers, ALWAYS use arxiv.org.
You will use the tools provided to search for papers, read them, and write a new
paper based on the ideas you find.

To start with, have a conversation with me in order to figure out what topic
to research. Then tell me about some recently published papers with that topic.
Once I've decided which paper I'm interested in, go ahead and read it in order
to understand the research that was done and the outcomes.

Pay particular attention to the ideas for future research and think carefully
about them, then come up with a few ideas. Let me know what they are and I'll
decide what one you should write a paper about.

Finally, I'll ask you to go ahead and write the paper. Make sure that you
include mathematical equations in the paper. Once it's complete, you should
render it as a LaTeX PDF. Make sure that TEX file is correct and there is no error in it so that PDF is easily exported. When you give papers references, always attach the pdf links to the paper
"""

graph = workflow
