import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
st.sidebar.title("Whatsapp chat analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    
    df=preprocessor.preprocess(data)
    # st.dataframe(df)
    user_list=df['sender'].unique().tolist()
    user_list.sort()
    # user_list.remove("group_notification")
    user_list.insert(0,"overall")
    selected=st.sidebar.selectbox("show analysis wrt user",user_list)
    if st.sidebar.button("show analysis"):
        num_msg,words,media,links= helper.fetch(selected,df)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.markdown("<h4 style='font-weight:400; font-size:20px;'>Total messages</h4>", unsafe_allow_html=True)

            st.title(num_msg)
        with col2:
            st.markdown("<h4 style='font-weight:400; font-size:20px;'>Total words</h4>", unsafe_allow_html=True)
            st.title(words)
        with col3:
            st.markdown("<h4 style='font-weight:400; font-size:20px;'>Total media</h4>", unsafe_allow_html=True)
            st.title(media)
        with col4:
             st.markdown("<h4 style='font-weight:400; font-size:20px;'>Total links</h4>", unsafe_allow_html=True)
             st.title(links)
        if selected=='overall':
            st.title("Most busy user")
            x,df1=helper.busy(df)
            fig,ax=plt.subplots()

            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(df1)
        st.title('Wordcloud')
        df2=helper.word(selected,df)
        fig,ax=plt.subplots()
        ax.imshow(df2)
        st.pyplot(fig)

        df4=helper.common(selected,df)
        st.title("Most common words")
        st.dataframe(df4)

        emojjidf=helper.emojihelper(selected,df)
        st.title("Emoji analysis")
        col1,col2=st.columns(2)
        with col1:

          st.dataframe(emojjidf)
        with col2:
            if emojjidf.empty:
              st.write("No emojis used by this user")
            else:
             fig,ax=plt.subplots()
             ax.pie(emojjidf['count'].head(),labels=emojjidf['emoji'].head(),autopct="%0.2f")
             st.pyplot(fig)

        st.title("monthly timeline")
        timeline,time=helper.month(selected,df)
        fig,ax=plt.subplots()
        ax.plot(time,timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        st.title("Activity map")
        col1,col2=st.columns(2)
        with col1:
            st.header("Most busy day")
            busy=helper.day(selected,df)
            fig,ax=plt.subplots()
            ax.plot(busy.index,busy.values)
            st.pyplot(fig)
        with col2:
            st.header("Most busy month")
            busy1=helper.month_activity(selected,df)
            fig,ax=plt.subplots()
            ax.plot(busy1.index,busy1.values)
            st.pyplot(fig)

        