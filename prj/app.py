import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff


st.title("통계자료로 보는 한국의 어두운 전망")
st.title("(2010년 - 2022년)")
years = np.arange(2011,2023)
year = st.selectbox(
    '연도를 선택하세요',
    years)

st.write('You selected:', year)

chart = ['학생','폐교']
option = st.selectbox(
    '차트를 선택하세요',
    chart)

st.write('You selected:', option)



def display_student_data(year):
    students_df = pd.read_csv("prj/학생수.csv", index_col=0)
    area_number = len(students_df['지역'].unique()[1:])
    not_all_area = students_df[students_df['지역'] != '전국']
    sorted_area = not_all_area[['지역','학생(명)']]
    all_area = students_df[students_df['지역'] == '전국']
    sorted_area['전체평균'] = round(all_area['학생(명)'] / area_number).astype(int)
    set_index_area = sorted_area.reset_index()
    set_index_area.set_index('지역', inplace=True)
    data_year = set_index_area[set_index_area['연도'] == year]
    fig = ff.create_table(data_year, height_constant=60)


    # Add graph data
    team = data_year.index
    each_area_count = data_year['학생(명)']
    average_count = data_year['전체평균']
    trace1 = go.Bar(x=team, y=each_area_count, xaxis='x2', yaxis='y2',
                    marker=dict(color='#0099FF'),
                    name='학생(명)')
    trace2 = go.Bar(x=team, y=average_count, xaxis='x2', yaxis='y2',
                    marker=dict(color='#404040'),
                    name='평균 학생 (명)')
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
    fig.layout.yaxis2.update({'title': 'Goals'})
    # Update the margins to add a title and see graph x-labels.
    fig.layout.margin.update({'t':75, 'l':50})
    fig.layout.update({'title': f'{year}년도의 지역당 전체 학생 수'})
    # Update the height because adding a graph vertically will interact with
    # the plot height calculated for the table
    fig.layout.update({'height':800})
    # Plot!
    st.plotly_chart(fig, use_container_width=True)



def display_closed_school_data(year):
    close_school_df = pd.read_csv("prj/학교.csv", index_col=0)
    area_number = len(close_school_df['지역'].unique()[1:])
    not_all_area = close_school_df[close_school_df['지역'] != '전국']
    sorted_area = not_all_area[['지역','당년(개)']]
    all_area = close_school_df[close_school_df['지역'] == '전국']
    sorted_area['전체평균'] = round(all_area['당년(개)'] / area_number).astype(int)
    set_index_area = sorted_area.reset_index()
    set_index_area.set_index('지역', inplace=True)
    data_year = set_index_area[set_index_area['연도'] == year]


    # 차트 만들기
    fig = ff.create_table(data_year, height_constant=60)
    # Add graph data
    team = data_year.index
    each_area_count = data_year['당년(개)']
    average_count = data_year['전체평균']

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
    fig.layout.update({'title': f'{year}년도의 학교 폐교율'})

    # Update the height because adding a graph vertically will interact with
    # the plot height calculated for the table
    fig.layout.update({'height':800})
    # Plot!
    st.plotly_chart(fig, use_container_width=True)

if option == "학생":
    display_student_data(year)
else:
    display_closed_school_data(year)