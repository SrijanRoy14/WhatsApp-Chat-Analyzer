import streamlit as st
import preprocessor as pre
import helper
import matplotlib.pyplot as plt
import pandas as pd
st.sidebar.title("WhatsApp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data= bytes_data.decode("utf-8")
    df=pre.preprocess(data)
    
    st.header("The Whatsapp chat")
    st.dataframe(df)

    #fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)
    num_messages,words,num_media_msg,num_links=helper.fetch_stats(selected_user,df)

    if st.sidebar.button("Show Analysis"):
        
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.subheader(num_messages)
        with col2:
            st.header("Total words")
            st.subheader(words)
        with col3:
            st.header("Total media shared")
            st.subheader(num_media_msg)
        with col4:
            st.header("Links shared")
            st.subheader(num_links)
        
        #find the busiest user in the group
        st.header("The most busiest users were!")
        if selected_user=='Overall':
            #st.title('Most active user')
            x,new_df=helper.fetch_most_busy_user(df)
            img=pd.DataFrame(x).reset_index().rename(
                columns={'index':'name','user':'messages'})
           
            col1,col2=st.columns(2)

            with col1:
                st.bar_chart(data=img,x="name",y="messages")

                
                
                
            with col2:
                st.dataframe(new_df)
        
        st.header("What did you guys most talk about")
        #wordcloud
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.header("The buzz words!")
        #most_common_words
        most_commondf= helper.most_commwords(selected_user,df)
        st.dataframe(most_commondf,width=600)

        st.header("The busiest months")
        #timeline
        timeline=helper.monthly_timeline(selected_user,df)
        st.line_chart(timeline,x='time',y='message',)