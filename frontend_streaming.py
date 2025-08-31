import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

CONFIG={'configurable':{'thread_id':'thread-1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]

for msg in st.session_state['message_history']:
    with st.chat_message(msg['role']):
        st.text(msg['content'])


user_input=st.chat_input("Type here")  


if user_input :

    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)  


    with st.chat_message("assistant"):
        ai_message=st.write_stream(
            message_chunk.content for message_chunk,metadata in chatbot.stream( # type:ignore
                {'messages':[HumanMessage(content=user_input)]},
                config=CONFIG,# type:ignore
                stream_mode='messages'
            )
        )
        st.session_state['message_history'].append({'role':'ai','content':ai_message})

