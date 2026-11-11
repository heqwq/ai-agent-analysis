import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from tools import get_data_info, detect_anomaly, plot_anomalies

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
base_url = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")

# 1. 配置大模型
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=api_key,
    base_url=base_url
)

# 2. 告诉大模型工作流程（这里修改了提示词，让它明白现在是统计学分析）
system_prompt = """你是一个专业的数据分析师。请严格按以下步骤工作：
1. 收到文件路径后，必须先调用 get_data_info 查看数据有哪些列。
2. 根据用户的要求，选择一个数值类型的列进行分析。
3. 调用 detect_anomaly 工具进行检测（它会查重并使用3σ原则找异常）。
4. 调用 plot_anomalies 工具生成带红点的图表。
5. 最后用自然语言向用户汇报你的诊断报告。"""

# 3. 组装 Agent
tools = [get_data_info, detect_anomaly, plot_anomalies]

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
)