import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import io
import zipfile
import streamlit as st

@st.cache_resource
def fetch_and_clean_data():
     with zipfile.ZipFile("merged_df.zip", 'r') as zip_file:
        csv_data = zip_file.read("merged_df.csv")
        csv_string = csv_data.decode('utf-8')
        csv_io = io.StringIO(csv_string)
    return pd.read_csv(csv_io)


class Utils:

    def __init__(self):
        self.merged_df = fetch_and_clean_data()
    
    def fig1(self, start, stop):
        activities = ["Sports", "PersonalCare", "Socializing", "Eating", "CareGiving", "Travel", "Shopping",
                      "Housework", "Calls", "Work"]
        data = self.merged_df[
            ['tucaseid', 'tuactivity_n', 'tustarttim', 'tustoptime', 'activity_name', 'has_children_under_18']]

        filtered_df = data[(data['tustarttim'] >= start) & (data['tustoptime'] <= stop)]

        # Change dtype of a column
        children_mapping = {0: 'No',
                            1: 'Yes'}
        filtered_df['has_children_under_18'] = filtered_df['has_children_under_18'].map(children_mapping)
        fig = px.histogram(filtered_df, x='activity_name', color='has_children_under_18', barmode='group',
                           color_discrete_sequence={0: '#FF9B01', 1: '#6177F1'},
                           category_orders={'activity_name': activities},
                           labels={'has_children_under_18': 'Have children under 18'},
                           log_y=True
                           ).update_xaxes(categoryorder="total descending")
        fig.update_traces(texttemplate='%{y}', textposition='outside', textfont=dict(size=14))

        # Remove y-axis labels
        fig.update_layout(yaxis=dict(title='', showticklabels=False))
        fig.update_layout(legend=dict(title='Has Children Under 18',
                                      yanchor='top',
                                      y=0.99,
                                      xanchor='left',
                                      x=0.99,
                                      font_size=20,
                                      title_font_size=24
                                      ))
        return fig

    def fig2(self, start, stop, activity):

        data2 = self.merged_df[['tucaseid', 'activity_name', 'tustarttim', 'tustoptime', 'gestfips']]

        filtered_df = data2[(data2['tustarttim'] >= start) & (data2['tustoptime'] <= stop) & (
            data2['activity_name'] == activity)]

        state_counts = filtered_df.groupby('gestfips').size().reset_index(name='count')
        total_counts = self.merged_df.groupby(['gestfips']).size().reset_index(name='total_in_state')

        new_df = state_counts.merge(total_counts, left_on='gestfips', right_on='gestfips', how='left')
        new_df['normalized_count'] = round(new_df['count'] / new_df['total_in_state'], 4)
        rows_count = len(filtered_df)

        fig = px.choropleth(data_frame=new_df, locationmode='USA-states', locations='gestfips',
                            labels={'normalized_count': 'Normalized Count'},
                            scope='usa', color='normalized_count',
                            color_continuous_scale='Blues',
                            hover_data=['count', 'normalized_count', 'gestfips'])
        fig.update_layout(geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='rgba(0,0,0,0)'), height=700, width=1300)
        fig.update_traces(
            hovertemplate='<b>State FIPS code: %{customdata[2]}</b><br>'
                          '<b>Number of people: %{customdata[0]}</b><br>'
                          '<b>Proportion of state population: %{customdata[1]}</b><br>'
                          ,
            hoverlabel=dict(
                font=dict(size=20)  # Set the desired font size for the hover text
            )
        )
        return rows_count, state_counts, fig

    def fig3(self, time, activity):

        data3 = self.merged_df[['tucaseid', 'activity_name', 'tustarttim', 'tustoptime','teage','tesex']]

        # Filter dataframe based on start and stop time, and activity
        df = data3[(data3['tustarttim'] <= time) & (data3['tustoptime'] >= time) & data3['activity_name'].isin(
            activity)]

        # Create age groups
        bins = [0, 18, 30, 45, 60, 75, np.inf]
        names = ['<18', '18-30', '30-45', '45-60', '60-75', '75+']

        df['age_group'] = pd.cut(df['teage'], bins, labels=names)

        # Group data by sex, age group and activity and count the records
        group = df.groupby(['tesex', 'age_group', 'activity_name']).size().reset_index(name='count')

        # Get unique labels and add them to the nodes list
        sex_labels = sorted(group['tesex'].apply(lambda x: 'Male' if x == 1 else 'Female').unique().tolist(), reverse=True)
        age_labels = sorted(group['age_group'].unique().tolist())
        activity_labels = group['activity_name'].unique().tolist()

        labels = sex_labels + age_labels + activity_labels

        male_color = '#66B2FF'
        female_color = '#FFA2A2'

        # Create source, target, value and color lists
        source = []
        target = []
        value = []
        color = []

        # Loop over each record and add to source, target, value and color lists
        total_records = 0
        max_count = group['count'].max()
        for i, row in group.iterrows():
            if row['count'] < 0.1*max_count:
                continue
            source.append(labels.index('Male' if row['tesex'] == 1 else 'Female'))
            target.append(labels.index(row['age_group']))
            value.append(row['count'])
            color.append(male_color if row['tesex'] == 1 else female_color)

            source.append(labels.index(row['age_group']))
            target.append(labels.index(row['activity_name']))
            value.append(row['count'])
            color.append(male_color if row['tesex'] == 1 else female_color)
            total_records += row['count']

        # Create Sankey diagram
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=50,
                thickness=5,
                line=dict(color="black", width=0.1),
                label=labels,
                color="black",
            ),
            link=dict(
                source=source,
                target=target,
                value=value,
                color=color,
                line=dict(color='black', width=0.5),


            )
        )])

        fig.update_layout(height=1000, font_size=40)
        fig.update_traces(textfont_color='black', selector=dict(type='sankey'))
        fig.update_traces(
            # hovertemplate='<b>Number of people: %{customdata[0]}</b><br>Proportion of state population: %{customdata[1]}',
            hoverlabel=dict(
                font=dict(size=30)  # Set the desired font size for the hover text
            )
        )

        return total_records, fig
