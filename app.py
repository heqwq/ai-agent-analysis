import streamlit as st
import os
import glob
from agent import agent

st.title("🛡️ 智能时序数据异常检测系统")
st.write("上传你的数据，AI 会自动帮你查重、找异常并生成图表。")

# 上传文件组件
uploaded_file = st.file_uploader("请上传 CSV 文件 (建议包含数值列)", type="csv")

if uploaded_file is not None:
    # 保存文件到本地
    temp_path = "temp_data.csv"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("文件上传成功！")

    # 用户输入框
    user_input = st.text_input("请告诉我你想做什么：", value="帮我检测一下这份数据有没有重复或异常，并画个图。")

    if st.button("开始分析"):
        with st.spinner("AI 正在分析和计算中，请稍候..."):
            try:
                # 调用 Agent
                response = agent.invoke({
                    "messages": [{"role": "user", "content": f"文件路径是 '{temp_path}'。任务：{user_input}"}]
                })

                # 打印文字报告
                st.markdown("### 🤖 AI 诊断报告")
                st.info(response["messages"][-1].content)

                # 找到最新图片展示
                list_of_files = glob.glob('plot_*.png')
                if list_of_files:
                    latest_file = max(list_of_files, key=os.path.getctime)
                    st.markdown("### 📊 可视化图表")
                    st.image(latest_file, use_container_width=True)

            except Exception as e:
                st.error(f"运行出错了：{str(e)}")