import pandas as pd

df = pd.read_csv('data/Article.csv', encoding='utf-8')
df['url'] = df['srcID'].apply(
    lambda x: f'https://nmtl2.daoyidh.com/zh-tw/main/articleInfo?artId={x}')

df.to_csv('data/Article_url.csv', encoding='utf-8-sig', index=False)
