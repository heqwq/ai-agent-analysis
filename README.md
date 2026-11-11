智能时序数据异常检测系统 (Intelligent Time-Series Anomaly Detection Agent)

这是一个基于大语言模型（LLM）与 Agent 架构的智能数据分析 MVP（最小可行性产品）。
用户无需编写任何代码，只需上传 CSV 数据并输入自然语言指令，系统即可自动调度底层算法进行异常检测，并生成带图表的可视化诊断报告。

核心痛点与解决方案
痛点：传统业务人员不懂 Python，无法快速排查海量设备时序数据的异常；而直接使用网页端大模型（如 ChatGPT），大模型存在“数学计算幻觉”，且上传原始表格存在数据泄露风险。
解决方案：构建 **Agent (智能体) 架构**。让大模型（DeepSeek）只做“大脑”负责理解意图和调度，底层使用纯 Python (Pandas + 3σ算法) 做“手脚”负责精准计算与画图。

核心特性
Function Calling (工具调用)**：将底层的 Python 算法封装为 `Tools`，大模型能自主决定调用哪个工具。
三层解耦架构：前端视图层、Agent 决策层、Tool 执行层完全分离，符合企业级工程设计。
数据安全隔离：原始 CSV 数据仅在本地由 Pandas 处理，**仅将计算后的文本结论（脱敏特征）传给云端大模型 API**，极大降低隐私泄露风险。
极速前端搭建：使用 Streamlit 快速实现文件上传、指令输入与 Markdown 报告渲染。

## 🛠️ 技术栈
AI 框架：LangChain
大语言模：DeepSeek API (OpenAI 兼容接口)
数据处理与算法：Pandas, NumPy, 3σ 统计原则 (拉依达准则)
数据可视化：Matplotlib
前端框架：Streamlit
环境与安全：Python-dotenv (环境变量保护 API Key)

系统架构设计
本项目采用模块化设计，包含三个核心文件：
1. `app.py` (前端视图层)：负责文件上传（流处理）、用户交互输入、渲染 AI 生成的 Markdown 报告与异常检测图表。
2. `agent.py` (智能调度层)：配置大模型，注入 `System Prompt`，挂载工具库，实现基于自然语言的任务规划。
3. `tools.py` (底层执行层)：封装 `detect_anomaly`（数据去重与异常检测）和 `plot_anomalies`（生成带红点标注的折线图）等工具函数。

> 业务流程：用户上传数据 -> 前端保存至本地 -> 大模型解析意图 -> 调度 Tools 进行 Pandas 运算 -> 返回结论给大模型 -> 大模型生成诊断报告与图表。

📸 效果展示
*(将你的项目截图或录屏 GIF 放在这里，非常重要！)*
<img width="936" height="582" alt="image" src="https://github.com/user-attachments/assets/3875e133-2208-4aca-a1f5-67e6b684957c" />

<img width="1107" height="757" alt="image" src="https://github.com/user-attachments/assets/1bf8ce3a-0119-48fe-b00c-ebb6ed21ffff" />


快速开始

环境准备
确保已安装 Python 3.9+，并安装依赖：
```bash
pip install streamlit langchain langchain-openai pandas matplotlib python-dotenv
配置
DEEPSEEK_API_KEY=sk-你的真实API_KEY
DEEPSEEK_API_BASE=https://api.deepseek.com（若是有本地大模型可采用本地模型，更安全）
启动
streamlit run app.py
