import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


st.title("통계자료로 보는 한국의 어두운 전망")
st.title("(2010년 - 2022년)")


# chart_data = pd.DataFrame(
#     np.random.randn(20, 3),
#     columns=['a', 'b', 'c'])

# st.line_chart(chart_data)



marriage_df = pd.read_csv("prj/출생,결혼.csv", index_col=0)
students_df = pd.read_csv("prj/학생수.csv", index_col=0)
close_school_df = pd.read_csv("prj/학교.csv", index_col=0)
# # close_school_df
# # students_df
# # marriage_df

marriage_df.rename_axis("연도", axis='index', inplace=True) # 인덱스의 이름을 바꾸는것
m_p = marriage_df['항목'] == '결혼(건)'
df = marriage_df[m_p][['월','값']]
df_month = df.copy()
df_month['월'] = df_month['월'].str.replace('월', '').astype(int)
df_year = df_month.sort_values(['연도','월'], ascending=True).copy()
reset_df = df_year.reset_index()
reset_df = reset_df[['연도','값']]
m_sum_df = reset_df.groupby(by=['연도']).sum()

b_p = marriage_df['항목'] == '출생(명)'
df = marriage_df[b_p][['월','값']]
df_month = df.copy()
df_month['월'] = df_month['월'].str.replace('월', '').astype(int)
df_year = df_month.sort_values(['연도','월'], ascending=True).copy()
reset_df = df_year.reset_index()
b_sum_df = reset_df[['연도','값']]
b_sum_df = b_sum_df.groupby(by=['연도']).sum()


merged_df = pd.merge(m_sum_df, b_sum_df, on='연도', how='outer')
merged_df = merged_df.rename(columns={'값_x': '결혼(수)', '값_y': '출생(수)'})


st.line_chart(merged_df)


df_by_year = lambda year: reset_df.loc[reset_df['연도'] == year].copy()
month_and_year = lambda year: (df_by_year(year)['월'], df_by_year(year)['값'])

plt.figure(figsize=(10, 12))
draw_plot = lambda year: plt.plot(*month_and_year(year), '*:', label=f'{year}년')

n_sub_plot = [221,222,223,224]

def make_subplot(i,n):
  c_year = 2010+n
  plt.subplot(n_sub_plot[i//3])
  a_year = [v for v in reset_df['연도'].unique()]
  a_year.sort()
  if n == 9:
    y_data = [v for v in a_year[n:n+4]]
    plt.title(f'{c_year}년 부터 {c_year+3}년 까지 ')
  else: 
    y_data = [v for v in a_year[n:n+3]]
    plt.title(f'{c_year}년 부터 {c_year+2}년 까지')
  y_data.sort()
  for index in y_data:
    draw_plot(index)
  plt.xlabel('월')
  plt.ylabel('결혼 건수')
  plt.grid(True)
  plt.legend(loc=0)

for i in range(0,10,3):
  make_subplot(i,i)

plt.tight_layout() # 안 겹치게 레이아웃 조정
plt.show()