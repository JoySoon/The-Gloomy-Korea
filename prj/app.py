import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff


st.title("통계자료로 보는 한국의 어두운 전망")
st.title("(2010년 - 2022년)")
year = np.arange(2011,2023)
option = st.selectbox(
    '연도를 선택하세요',
    year)

st.write('You selected:', option)



# def view_year(i):
  

# 데이터 커스터마이징징
close_school_df = pd.read_csv("prj/학교.csv", index_col=0)
area_number = len(close_school_df['지역'].unique()[1:])
not_all_area = close_school_df[close_school_df['지역'] != '전국']
sorted_area = not_all_area[['지역','당년(개)']]
all_area = close_school_df[close_school_df['지역'] == '전국']
sorted_area['전체평균'] = round(all_area['당년(개)'] / area_number).astype(int)
set_index_area = sorted_area.reset_index()
set_index_area.set_index('지역')

data_2022 = set_index_area[set_index_area['날짜'] == 2022]


# 차트 만들기기
fig = ff.create_table(data_2022, height_constant=60)
# Add graph data
team = data_2022['지역']
each_area_count = data_2022['당년(개)']
average_count = data_2022['전체평균']

trace1 = go.Bar(x=team, y=each_area_count, xaxis='x2', yaxis='y2',
                marker=dict(color='#0099ff'),
                name='Each area')
trace2 = go.Bar(x=team, y=average_count, xaxis='x2', yaxis='y2',
                marker=dict(color='#404040'),
                name='Total Average')

# Add trace data to figure
fig.add_traces([trace1, trace2])

# initialize xaxis2 and yaxis2
fig['layout']['xaxis2'] = {}
fig['layout']['yaxis2'] = {}

# Edit layout for subplots
fig.layout.yaxis.update({'domain': [0, .45]})
fig.layout.yaxis2.update({'domain': [.6, 1]})

# The graph's yaxis2 MUST BE anchored to the graph's xaxis2 and vice versa
fig.layout.yaxis2.update({'anchor': 'x2'})
fig.layout.xaxis2.update({'anchor': 'y2'})
fig.layout.yaxis2.update({'title': '폐교 학교 수'})

# Update the margins to add a title and see graph x-labels.
fig.layout.margin.update({'t':75, 'l':50})
fig.layout.update({'title': '2022 학교 폐교율'})

# Update the height because adding a graph vertically will interact with
# the plot height calculated for the table
fig.layout.update({'height':800})


st.plotly_chart(fig, use_container_width=True)