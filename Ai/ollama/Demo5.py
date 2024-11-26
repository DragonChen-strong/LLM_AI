import streamlit as st
import ollama

model_list=ollama.list()  #获取可用的模型列表


#st.session_state 是 Streamlit 提供的一个全局状态管理器，用于在不同页面和会话之间共享数据
if "model_name" not in st.session_state:
    st.session_state["model_name"] = "qwen2.5:1.5b"

if "messages" not in st.session_state:
    st.session_state.messages = []


st.title("金豆科技")


#自己添加
with st.sidebar:
    st.subheader("Settings")

    option=st.selectbox("select a model",[model['name'] for model in model_list['models']])
    st.write('You selected',option)
    st.session_state["model_name"] = option


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder=st.empty()
        full_response=""
    try:
        for chunk in ollama.chat(
            model=st.session_state["model_name"],
            messages=[
                {'role':m['role'],"content":m['content']} for m in st.session_state["messages"]
            ],
            stream=True,
        ):
            if 'messages' in chunk :
                content=chunk['messages'].get('content',"")
                if content:
                    full_response++content
                    message_placeholder.markdown(full_response)
        message_placeholder.markdown(full_response)
    except Exception as e:
        st.error(f"An error occurred: {e}")
    st.session_state.messages.append({"role": "assistant", "content": full_response})