import streamlit as st
import ollama
import fitz

model_list=ollama.list()  #获取可用的模型列表



if "model_name" not in st.session_state:
    st.session_state["model_name"] = "codegemma" #进行初始化模型

if "messages" not in st.session_state:
    st.session_state.messages = []


st.title("金豆科技")


#设置左侧功能
with st.sidebar:
    st.subheader("选择创建实现体")

    #选择创建的功能
    mode=st.radio("选择功能",("代码生成","与PDF对话","知识库学习"))

    if mode == "代码生成":
        st.subheader("选择模型")
        option=st.selectbox("选择模型",[model['name'] for model in model_list["models"] if "code" in model['name'].lower()])
        st.write("您选择的模型：",option)
        st.session_state["model_name"]=option


if mode == "代码生成":
    prompt=st.text_area("描述您想要生成的代码", "例如：写一个Python函数计算斐波那契数列")
    if st.button("生成代码"):
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt, unsafe_allow_html=True)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                for chunk in ollama.chat(
                        model=st.session_state["model_name"],
                        messages=[{'role': m['role'], "content": m['content']} for m in st.session_state["messages"]],
                        stream=True,
                ):
                    if 'message' in chunk and 'content' in chunk['message']:
                        full_response += (chunk['message']['content'] or "")
                        message_placeholder.markdown(full_response + "")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})


    # 与PDF文件进行对话功能
elif mode == "Chat with PDF":
        uploaded_pdf = st.file_uploader("上传PDF", type="pdf")
        if uploaded_pdf:
            # 读取PDF内容
            doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
            if uploaded_pdf:
                #读取PDF内容
                doc=fitz.open(uploaded_pdf.read(),filetype="pdf")
            pdf_text = ""
            for page in doc:
                pdf_text += page.get_text()

            st.write("提取的PDF内容")
            st.text_area("PDF Content", pdf_text, height=300)

            # 输入与PDF对话的内容
            prompt = st.text_area("提问与PDF相关的问题")
            if st.button("提问"):
                if prompt:
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    with st.chat_message("user"):
                        st.markdown(prompt)

                    # 将PDF内容和用户问题一并发送给模型
                    context = pdf_text[:1000]  # 只传递PDF的前1000个字符作为上下文
                    full_prompt = f"基于以下PDF内容，回答问题：{context}\n\n问题: {prompt}"

                    with st.chat_message("assistant"):
                        message_placeholder = st.empty()
                        full_response = ""
                        for chunk in ollama.chat(
                                model=st.session_state["model_name"],
                                messages=[{'role': 'user', 'content': full_prompt}],
                                stream=True,
                        ):
                            if 'message' in chunk and 'content' in chunk['message']:
                                full_response += (chunk['message']['content'] or "")
                                message_placeholder.markdown(full_response + "")
                        message_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})

# 知识库学习功能
elif mode == "知识库学习":
    # 提供一个文本框用于用户输入学习内容
    knowledge_input = st.text_area("输入学习内容", "在这里输入需要学习的知识点。")
    if st.button("学习"):
        if knowledge_input:
            st.session_state.messages.append({"role": "user", "content": knowledge_input})
            with st.chat_message("user"):
                st.markdown(knowledge_input)

            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                for chunk in ollama.chat(
                        model=st.session_state["model_name"],
                        messages=[{'role': m['role'], "content": m['content']} for m in st.session_state["messages"]],
                        stream=True,
                ):
                    if 'message' in chunk and 'content' in chunk['message']:
                        full_response += (chunk['message']['content'] or "")
                        message_placeholder.markdown(full_response + "")
                message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})