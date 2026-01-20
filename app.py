import streamlit as st
import preprocessor
st.sidebar.title("Whatsapp chat analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    
    df=preprocessor.preprocess(data)
    st.dataframe(df)
    user_list=df['sender'].unique().tolist()
    user_list.sort()
    # user_list.remove("group_notification")
    user_list.insert(0,"overall")
    st.sidebar.selectbox("show analysis wrt user",user_list)
    if st.sidebar.button("show analysis"):
        pass