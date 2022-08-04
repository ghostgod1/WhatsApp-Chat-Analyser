import streamlit as st
import data_collecter, backend
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("Whatsapp Chat Analyser")

upload_file = st.sidebar.file_uploader("Choose a file")
if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = data_collecter.preprocess(data)
    st.dataframe(df)

    userlist = df['user'].unique().tolist()
    userlist.remove('group_notification')
    userlist.sort()
    userlist.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",userlist)

    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media_messages,num_links = backend.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Messages")
            st.title(num_media_messages)
        with col4:
            st.header("links Shared")
            st.title(num_links)

        st.title("Monthly Timeline")
        timeline = backend.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        st.title("Daily Timeline")
        daily_timeline = backend.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'])
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        st.title("Activity Map")
        col1,col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = backend.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = backend.month_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values)
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = backend.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

    if selected_user == 'Overall':
        st.title('Most Busy User')
        x, new_df = backend.most_busy_users(df)
        fig, ax = plt.subplots()
        
        col1,col2 = st.columns(2)

        with col1:
            ax.bar(x.index,x.values, color = 'red')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)

    st.title("WordCloud")
    df_wc = backend.create_wordcloud(selected_user,df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

    st.title("Most Common Words")
    most_common_df = backend.most_common_words(selected_user,df)
    fig,ax = plt.subplots()
    ax.barh(most_common_df[0],most_common_df[1])
    plt.xticks(rotation = 'vertical')
    st.pyplot(fig)


    emoji_df = backend.emoji_counter(selected_user,df)
    st.title("Emoji Analysis")

    col1,col2 = st.columns(2)

    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig,ax = plt.subplots()
        ax.bar(emoji_df[0].head(10), emoji_df[1].head(10))
        st.pyplot(fig)

