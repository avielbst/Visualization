import datetime
from utils import *
import streamlit as st


st.set_page_config(page_title="visualization project", layout='wide')
header = st.container()
fig1 = st.container()
fig2 = st.container()
fig3 = st.container()

util = Utils()

st.markdown("""
    <style>
    .desc {
        font-size:22px;
        color: #626862;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .warn {
        font-size:22px;
        color: #FF0000;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

with header:
    title = 'How Americans Spend Their Time'

    project_description = """
    In this project we provide visualization tools that might help to analyze Americans' time investment<br> Goals are
    to understand what activities are most common and how different demographic/economic factors might affect them.
    <br><br>
    Our data is based on "Americans Time Usage Survey" (ATUS) organization which includes around 3 million records
     of different people
    around the united states and how they invest their time on a daily basis.<br><br>
    """

    st.markdown(f"<h1 style='text-align: center; color: black; font-size: 60px;'>{title}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #626862; font-size: 30px;'>{project_description}</h3>",
                unsafe_allow_html=True)

with fig1:
    st.markdown(f"<h3 style='color: black; font-size: 40px;'>Popular Activities - Children a Factor?</h3>",
                unsafe_allow_html=True)

    st.markdown(f'<p class="desc">Bar plot showing how many Americans do each of the activities in the chosen'
                ' time range.<br>'
                'Each activity counts the number of Americans with:<br>'
                '1. Young children (<18)<br>'
                '2. No children (or children that are >18)<br>'
                'This might help to better understand if'
                ' children are a factor that affects time usage among Americans<br><br>'
                'Please choose time range below:</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        start = st.time_input('Start Time', datetime.time(8, 00))
    with col2:
        stop = st.time_input('Stop Time', datetime.time(9, 15))

    start = str(start)
    stop = str(stop)

    figure1 = util.fig1(start, stop)
    figure1.update_layout(
        xaxis=dict(
            title=dict(
                text='Activity',  # Set the desired x-axis title
                font=dict(size=30)  # Set the desired font size for the x-axis title
            ),
            tickfont=dict(
                size=20  # Set the desired font size for the x-axis ticks
            )
        ),
        yaxis=dict(
            title=dict(
                text='Number (Log Scaled)',  # Set the desired y-axis title
                font=dict(size=30)  # Set the desired font size for the y-axis title
            ),
            tickfont=dict(
                size=20  # Set the desired font size for the y-axis ticks
            )
        ),
        legend=dict(
            font=dict(
                size=22  # Set the desired font size for the legend labels
            ),
            title_font_size=24

        )

    )
    st.plotly_chart(figure1, use_container_width=True)

with fig2:
    st.markdown(f"<h3 style='color: black; font-size: 40px;'>Activity Popularity By Geographical Location</h3>", unsafe_allow_html=True)
    st.markdown('<p class="desc">The map shows the amount of Americans that do the specified activity in'
                ' different geographical locations (states) based on the chosen time range.<br>'
                'Choosing time and activity will make the map focus on relevant data.<br><br>'
                'Numbers represent the proportion of people in the specified state of total people participated in'
                ' this survey from this state.</p>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])

    with col2:
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.markdown('<p class="desc">Please choose desired time range and activity below:</p>', unsafe_allow_html=True)
        col21, col22 = st.columns(2)

        with col21:
            start2 = st.time_input('Start time', datetime.time(8, 45), key='fig2_start')
        with col22:
            stop2 = st.time_input('End time', datetime.time(9, 45), key='fig2_stop')
        start2 = str(start2)
        stop2 = str(stop2)
        activity = st.selectbox(
            'Select activity',
            ("Sports", "PersonalCare", "Socializing", "Eating", "CareGiving", "Travel", "Shopping",
             "Housework", "Calls", "Work"))
    with col1:
        rows_count, count_per_state, figure2 = util.fig2(start2, stop2, activity)
        figure2.update_layout(
            coloraxis_colorbar=dict(
                title='Proportion',
                thicknessmode="pixels",
                thickness=20,
                lenmode="pixels",
                len=300,
                ticks="outside",
                title_font_size=24,
                tickfont=dict(size=20)  # Set the desired font size for the color legend
            ),
            annotations=[
                dict(
                    text=f'Total number of Americans in specified time frame: {rows_count}',
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=1,
                    showarrow=False,
                    font=dict(size=22)
                )
            ]



        )
        st.plotly_chart(figure2, use_container_width=True)

with fig3:
    st.markdown(f"<h3 style='color: black; font-size: 40px;'>Activity Popularity Flow</h3>",
                unsafe_allow_html=True)
    st.markdown("<p class=desc>"
                "A flow showing how sex and age affect the popularity of different activities. The flow (left to right) consists of 3"
                " layers where each layer represent a split in data.<br>"
                "Left layer representing split based on gender - blue for male and pink for female.<br>"
                "Middle layer splits data based on age.<br>"
                "The size of each link is bigger as the number of people it represents is higher<br>"
                "The flow might be a bit complicated at first, but can be used to understand which activities are more popular than others "
                "and define the its population.<br>"
                "Based on chosen time and activities the flow will focus on relevant data<br><br>"
                "Please choose time and up to 2 activities on the filter panel on the right."
                "</p>", unsafe_allow_html=True)
    st.markdown("<p class=warn>"
                "Note: After 2 activities are chosen, any additional choices will be ignored!!"
                "</p>", unsafe_allow_html=True)
    col31, col32 = st.columns([9, 1])
    with col32:
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        time = st.time_input('Choose time', datetime.time(8, 45), key='fig3_time')
        time = str(time)

        activities = ("Sports", "PersonalCare", "Socializing", "Eating", "CareGiving", "Travel",
                      "Shopping", "Housework", "Calls", "Work")
        cb_sports = st.checkbox("Sports", value=True)
        cb_PersonalCare = st.checkbox("PersonalCare")
        cb_Socializing = st.checkbox("Socializing")
        cb_Eating = st.checkbox("Eating", value=True)
        cb_CareGiving = st.checkbox("CareGiving")
        cb_Travel = st.checkbox("Travel")
        cb_Shopping = st.checkbox("Shopping")
        cb_Housework = st.checkbox("Housework")
        cb_Calls = st.checkbox("Calls")
        cb_Work = st.checkbox("Work")

        cb_acts = []
        for activity, value in zip(activities,
                                   [cb_sports, cb_PersonalCare, cb_Socializing, cb_Eating, cb_CareGiving, cb_Travel,
                                    cb_Shopping, cb_Housework, cb_Calls, cb_Work]):
            if value and len(cb_acts) < 2:
                cb_acts.append(activity)

    with col31:
        total_records, figure3 = util.fig3(time, cb_acts)
        figure3.update_layout(
            annotations=[
                dict(
                    text=f'Total number of Americans in specified time frame: {total_records}',
                    xref='paper',
                    yref='paper',
                    x=0.5,
                    y=1.1,
                    showarrow=False,
                    font=dict(size=22)
                )
            ]
        )
        st.plotly_chart(figure3, use_container_width=True)
