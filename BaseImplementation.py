from crewai import Agent, LLM, Task, Crew, Process
from crewai_tools import PDFSearchTool
import os
from crewai_tools import FileWriterTool
#from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

file_writer = FileWriterTool()

# Environment Setup
os.environ["OPENAI_API_KEY"] = "dummy_key"

# PDF Tool Setup

pdf_rag = PDFSearchTool(
    pdf="Learning\prompthacking.pdf",
    config=dict(
        llm=dict(
            provider="ollama", # or google, openai, anthropic, llama2, ...
            config=dict(
                 model="llama3.1",
                temperature=0.5,
                # top_p=1,
                 # stream=true,
            ),
     ),
    embedder = dict(
            provider="ollama", # or openai, ollama, ...
            config=dict(
                model="mxbai-embed-large",
                # task_type="retrieval_document",
                # title="Embeddings",
            )
    )
    #embeddings = OllamaEmbeddings(model="mxbai-embed-large", base_url="http://localhost:11434")
)
)


# LLM Setup
llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434"
)

# Agent Setup
base_agent = Agent(
    role="Senior Research Paper Summarizer",
    goal="Provide Summary of the research paper uploaded",
    backstory="You have been known for providing the best summary without losing any major details while keeping it concise.",
    tools=[pdf_rag],
    llm=llm,
    custom_prompt="""
You are an agent assisting with research paper summarization. Always follow this format when reasoning:
Thought: Describe your reasoning.
Action: [The action to take, such as tool usage.]
Action Input: [The input for the action, formatted as a dictionary.]
Observation: [The result of the action.]

If you cannot use a tool, provide the final answer:
Thought: Reasoning about why you cannot proceed with tools.
Final Answer: [Your complete response based on the information available.]

Important:
- Use each tool only once unless explicitly instructed to reuse it.
- Ensure proper formatting to avoid invalid outputs.
"""
)

l1_agent = Agent(
    role="Senior Research Paper Summary Formatter",
    goal="Format the summary provided by the base_agent",
    backstory="You are best at formatting the input for the readers to have a easy reading",
    llm=llm,
    custom_prompt="""
You are an agent assisting with research paper summary formatting. Always follow this format when reasoning:
Thought: Describe your reasoning.
Action: [The action to take, such as tool usage.]
Action Input: [The input for the action, formatted as a dictionary.]
Observation: [The result of the action.]

If you cannot use a tool, provide the final answer:
Thought: Reasoning about why you cannot proceed with tools.
Final Answer: [Your complete response based on the information available.]

Important:
- Use each tool only once unless explicitly instructed to reuse it.
- Ensure proper formatting to avoid invalid outputs.
"""
)


# Task Setup
base_task = Task(
    description="Summarize the research paper PDF in the most concise form without losing any details. The summary should highlight all the important points, and if possible mention the links for important resources. Also, ignore parts of the pdf that contains names of the author and other things that might not be necessary for the summary.",
    agent=base_agent,
    expected_output="brief summary of the research paper",
    tools=[pdf_rag]
)

l1_task = Task(
    description="Format the research paper summary without losing any details. The formatting will be for markdown file. Format in such a way, the reader will find it helpful in reading and understanding the content.",
    agent=l1_agent,
    expected_output="Formatting of the input text in markdown format",
    output_file="summary.md"
)
# Crew Execution
crew = Crew(
    agents=[base_agent, l1_agent],
    tasks=[base_task, l1_task],
    process=Process.sequential,
    verbose=True
)

# Inside your task execution block
try:
    result = crew.kickoff()
    print("Crew Result:", result)

    # Task Output
    task_output = base_task.output
    print("Task Output:", task_output)

except Exception as e:
    print(f"Error during execution: {e}")
    if hasattr(e, 'llm_output'):
        print("LLM Output that caused the error:", e.llm_output)
