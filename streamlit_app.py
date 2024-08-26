import streamlit as st

if 'messages' not in st.session_state:
    st.session_state.messages = [] 

if 'username' not in st.session_state:
    st.session_state.username =""
    st.session_state.ready = False
    st.session_state.hist=False


if not st.session_state.ready:
    st.title("채팅방 로그인")
    st.write("채팅방에 로그인하기 위해서는 이름을 입력해주세요")
    username_input = st.text_input("이름을 입력하세요:", st.session_state.username)
    
    if st.button("입력"):
        username_input = username_input.strip()
        if username_input:
            st.session_state.username = username_input
            st.session_state.ready =True
            st.write(f"안녕하세요, {st.session_state.username}!")
            st.rerun()
        else :
            st.error("이름은 공백일 수 없습니다")
    
else :
    st.title(f"채팅방에 오신걸 환영합니다. {st.session_state.username}님!")
    if st.session_state.messages and  st.session_state.hist:
        for messages in st.session_state.messages:
            st.write(messages)
        st.session_state.hist=False
    message = st.chat_input("채팅을 입력하세여")
    
    if message == "나가기":
        st.write(f"{st.session_state.username}님이 퇴장하셨습니다")
        st.session_state.ready=False
        st.rerun()
    if message :
        if message.split(" ")[0] == "@이름변경":
            ### name 빈칸 처리 ###
            _list=message.split(" ")
            user_ms=" ".join(_list[1:])
            ##### 빈칸 처리 끝 ###

            username1=st.session_state.username
            #user_ms=message.split(" ")[1]
            st.session_state.messages.append(f"{username1}님이 {user_ms}로 변경되었습니다.")
            st.session_state.username=user_ms   #message.split(" ")[1]
            history=st.session_state.messages
            st.session_state.hist=True
            st.rerun()
        else:    
           st.session_state.messages.append(f"{st.session_state.username} : {message}") 
           if st.session_state.messages:
                for messages in st.session_state.messages:
                    st.write(messages)
                    #with open("./history.tmp") as f:
                    #    f.write(messages)
