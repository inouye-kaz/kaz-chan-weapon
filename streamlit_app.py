
import streamlit as st
import pandas as pd
import subprocess
import os

st.title("kaz-chan weapon - X全投稿CSVダウンローダー")
username = st.text_input("取得したいユーザー名を入力してください（@なし）")

if st.button("取得開始") and username:
    with st.spinner("ツイート取得中...（少々お待ちください）"):
        filename = f"{username}_tweets.json"
        cmd = f"snscrape --jsonl --max-results 3200 twitter-user {username} > {filename}"
        subprocess.run(cmd, shell=True)

        tweets = []
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                tweet = eval(line)
                tweets.append({
                    "日時": tweet["date"],
                    "本文": tweet["content"]
                })

        df = pd.DataFrame(tweets)
        csv = df.to_csv(index=False)
        st.success(f"{len(df)}件のツイートを取得しました。")
        st.download_button("CSVをダウンロード", csv, file_name=f"{username}_tweets.csv", mime="text/csv")
        os.remove(filename)
