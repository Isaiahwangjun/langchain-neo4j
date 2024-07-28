import pandas as pd

df = pd.read_csv('new_data/BasicInfo.csv', encoding='utf-8')
df['url'] = df['人名ID'].apply(
    lambda x: f'https://nmtl.daoyidh.com/zh-tw/main/writerintro?personId={x}')

df.to_csv('new_data/BasicInfo_url.csv', encoding='utf-8-sig', index=False)
print("odne")
