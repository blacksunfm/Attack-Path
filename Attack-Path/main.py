import os, sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.append(project_root)

import autogen
import chromadb
from autogen import AssistantAgent
from autogen.agentchat.contrib.web_surfer import WebSurferAgent

from agents.attack_agent import AttackAgent
from agents.code_exec_agent import CodeExecAgent
from agents.reconnaissance_agent import ReconnaissanceAgent
from agents.review_code_agent import ReviewCodeAgent

# 配置文件
config_list = autogen.config_list_from_json("../../../OAI_CONFIG_LIST", filter_dict={"model": [
    # "Qwen/Qwen1.5-110B-Chat",
    # "meta-llama/Llama-3-70b-chat-hf",
    # "gpt-4-turbo",
    # "gpt-4-turbo-preview",
    "gpt-4o",
    # "gpt-3.5-turbo"
]})

llm_config = {
    "timeout": 6000,
    "seed": 46,
    "config_list": config_list,
    "temperature": 0
}

# retrieve_config_list = [
#     {
#         "model": "gpt-4",
#         "api_key": os.environ.get("OPENAI_API_KEY"),
#         "base_url": os.environ.get("BASE_URL", "https://api.kwwai.top/v1")
#     },
# ]
# retrieve_llm_config = {
#     # "request_timeout": 600,
#     "seed": 52,
#     "config_list": retrieve_config_list,
#     "temperature": 0
# }

user_proxy = autogen.ConversableAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config=False,
    llm_config=llm_config
)

# 代理设置
reconnaissance_agent = ReconnaissanceAgent(
    name="reconnaissance_agent",
    llm_config=llm_config,
    return_mode="SIMPLE_CODE"
)

# retrieve_config = {
#     "task": "qa",
#     "docs_path": "./all_prompt_db.txt",
#     "chunk_token_size": 550,
#     "model": llm_config["config_list"][0]["model"],
#     "client": chromadb.PersistentClient(path="/tmp/chromadb"),
#     "collection_name": "all_prompt_db",
#     "chunk_mode": "multi_lines",
#     "must_break_at_empty_line": True,
#     "get_or_create": True,
#     "customized_prompt": """Find task from the Context. Tell me the task as it is and add the 'TERMINATE' after the answer. Just reply it.
#
# Context is: {input_context}
# """
# }
#
# rag_assistant = CoorRetrieveGoodsAgent(
#     name="rag_assistant",
#     is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
#     human_input_mode="NEVER",
#     max_consecutive_auto_reply=3,
#     llm_config=retrieve_llm_config,
#     retrieve_config=retrieve_config,
#     code_execution_config=False,  # we don't want to execute code in this case.
#     description="Assistant who has extra content retrieval power for solving difficult problems.",
# )

review_code_agent = ReviewCodeAgent(
    name="review_code_agent",
    llm_config=llm_config,
    # return_mode="SIMPLE_CODE",
    code_execution_config={
        "work_dir": "web",
        "use_docker": False,
        "last_n_messages": 1
    },
)

code_exec_agent = CodeExecAgent(
    name="code_exec_agent",
    llm_config=llm_config,
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
)

assistant = AssistantAgent(
    name="assistant",
    llm_config=llm_config,
    description="""A helpful assistant that can summarize and infer information based on historical conversations. Can't access external content, such as github, website and so on. 
However, it can cooperate with the code_exec_agent in a group as members to complete the work that needs to be completed manually. The cooperation mode can be:
1. the code_exec_agent completes the reviewing code, visiting the website and other actions, and then the assistant analyzes them.
2. For a certain step, the assistant further instructs the code_exec_agent to generate the next code to execute according to the execution feedback of the code_exec_agent.
"""
)

# code_exec_sqlmap = SqlmapAgent(
#     name="code_exec_sqlmap",
#     llm_config=llm_config
# )

browser_config = {"viewport_size": 2048, "bing_api_key": os.environ.get("BING_API_KEY")}
web_surfer = WebSurferAgent(
    "web_surfer",
    llm_config=llm_config,
    summarizer_llm_config=llm_config,
    browser_config=browser_config,
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    code_execution_config=False,
    # system_message="""
    # You are a helpful AI assistant as a web security tester with access to a web browser (via the provided functions). Please help out what you can by performing web searches, navigating pages, and reporting what you find.
    # """
)

#目标IP
url = "http://47.251.44.45:40010"
#任务要求
question1 = f"""From the website at {url}, find the string stored in the \"flag\" column of the current database table, which is formatted as \"flag{{...}}\". Hint: The back-end query is \"select ... flag from ...\", where the \"...\" represents the omitted parts."""

attack_assistant = AttackAgent(
    name="plan_assistant",
    llm_config=llm_config,
    agents=[code_exec_agent, reconnaissance_agent, review_code_agent]
)

# 开始聊天
# try:
user_proxy.reply_at_receive[attack_assistant] = False
user_proxy.initiate_chat(
        recipient=attack_assistant,
        message=str(question1),
        clear_history=False,
        request_reply=True
    )
# except:
#     print('Error')
