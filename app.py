import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
from streamlit_option_menu import option_menu

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocessor(df, region_df)

st.sidebar.markdown(
    "<h1 style='font-size:32px;'>Olympics Analysis</h1>",
    unsafe_allow_html=True
)
image_path = "https://raw.githubusercontent.com/rajnish-dubey/olympics-analysis/main/pictures/olympic-games.webp"
st.sidebar.image(image_path, use_column_width=True)
user_menu = option_menu(
    "Select an option",
    ["Medal Tally", "Country-wise Analysis", "Player-wise Analysis", "Overall Analysis"],
    icons=["trophy", "globe", "person", "bar-chart"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)

if user_menu == "Medal Tally":
    image_path = "https://raw.githubusercontent.com/rajnish-dubey/olympics-analysis/main/pictures/totcglightings570b.webp"
    st.image(image_path, use_column_width=True)
    st.sidebar.header("Medal Tally")
    year, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", year)
    selected_country = st.sidebar.selectbox("Select Country", country)
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    medal_tally['Year'] = medal_tally['Year'].astype(str)
    medal_tally.rename(columns={'region': 'Region'}, inplace=True)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.subheader("Overall Tally")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.subheader("Overall performance of " + selected_country + " in Olympics")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.subheader("Medal Tally in " + str(selected_year) + " Olympics")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.subheader(selected_country + " performance in " + str(selected_year) + " Olympics")

    st.dataframe(medal_tally, use_container_width=True)

if user_menu == "Overall Analysis":
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    image_path = "https://raw.githubusercontent.com/rajnish-dubey/olympics-analysis/main/pictures/PARIS-MEDALS-header.jpg"
    st.sidebar.image(image_path, use_column_width=True)
    edition = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    event = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.header("Top Statistic")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Editions")
        st.header(edition)
    with col2:
        st.subheader("Hosts")
        st.header(cities)
    with col3:
        st.subheader("Sports")
        st.header(sports)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Events")
        st.header(event)
    with col2:
        st.subheader("Nation")
        st.header(nations)
    with col3:
        st.subheader("Players")
        st.header(athletes)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Edition", y="region", color_discrete_sequence=["royalblue"])
    fig.update_layout(
        plot_bgcolor="#f0f0f0",
        paper_bgcolor="#ffffff",
        font=dict(color="#000000"),
        xaxis=dict(
            title=dict(
                font=dict(
                    color="black",
                    size=14,
                    family="Arial",
                    weight="bold"
                )
            ),
            tickfont=dict(
                color="black",
                size=12,
                weight="bold"
            )
        ),
        yaxis=dict(
            title=dict(
                font=dict(
                    color="black",
                    size=14,
                    family="Arial",
                    weight="bold"
                )
            ),
            tickfont=dict(
                color="black",
                size=12,
                weight="bold"
            )
        ),
        shapes=[
            dict(
                type='rect',
                xref='paper',
                yref='paper',
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(color='lightblue', width=2),
                fillcolor='rgba(255,255,255,0)',
            )
        ]
    )
    st.subheader("Participating nations over years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event", color_discrete_sequence=["royalblue"])
    fig.update_layout(
        plot_bgcolor="#f0f0f0",
        paper_bgcolor="#ffffff",
        font=dict(color="#000000"),
        xaxis=dict(
            title=dict(
                font=dict(
                    color="black",
                    size=14,
                    family="Arial",
                    weight="bold"
                )
            ),
            tickfont=dict(
                color="black",
                size=12,
                weight="bold"
            )
        ),
        yaxis=dict(
            title=dict(
                font=dict(
                    color="black",
                    size=14,
                    family="Arial",
                    weight="bold"
                )
            ),
            tickfont=dict(
                color="black",
                size=12,
                weight="bold"
            )
        ),
        shapes=[
            dict(
                type='rect',
                xref='paper',
                yref='paper',
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(color='lightblue', width=2),
                fillcolor='rgba(255,255,255,0)',
            )
        ]
    )
    st.subheader("Events over the years")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x="Edition", y="Name", color_discrete_sequence=["royalblue"])
    fig.update_layout(
        plot_bgcolor="#f0f0f0",
        paper_bgcolor="#ffffff",
        font=dict(color="#000000"),
        xaxis=dict(
            title=dict(
                font=dict(
                    color="black",
                    size=14,
                    family="Arial",
                    weight="bold"
                )
            ),
            tickfont=dict(
                color="black",
                size=12,
                weight="bold"
            )
        ),
        yaxis=dict(
            title=dict(
                font=dict(
                    color="black",
                    size=14,
                    family="Arial",
                    weight="bold"
                )
            ),
            tickfont=dict(
                color="black",
                size=12,
                weight="bold"
            )
        ),
        shapes=[
            dict(
                type='rect',
                xref='paper',
                yref='paper',
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(color='lightblue', width=2),
                fillcolor='rgba(255,255,255,0)',
            )
        ]
    )
    st.subheader("Players over the years")
    st.plotly_chart(fig)

    st.subheader("No. of Events over time (every sport)")
    fig, y = plt.subplots(figsize=(20, 20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
        annot=True)
    st.pyplot(fig)

    fig = helper.age_distribution(df)
    fig.update_layout(
        autosize=False,
        width=1000,
        height=600,
        plot_bgcolor='rgba(240, 240, 240, 0.8)',
        paper_bgcolor='rgba(255, 255, 255, 1)',
        font=dict(color="black"),
        xaxis=dict(
            title=dict(
                text="Age",
                font=dict(color="black", size=14, weight="bold")
            ),
            tickfont=dict(color="black", size=12, weight="bold")
        ),
        yaxis=dict(
            title=dict(
                text="Density",
                font=dict(color="black", size=14, weight="bold")
            ),
            tickfont=dict(color="black", size=12, weight="bold")
        ),
        annotations=[
            dict(
                x=1.1,
                y=1.05,
                text="Select",
                showarrow=False,
                xref="paper",
                yref="paper",
                font=dict(size=16, color="black")
            )
        ]
    )
    st.subheader("Age Distribution w.r.t. Sports (medalists only)")
    st.plotly_chart(fig)

    st.subheader("Most successful players")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox("Select a sport", sport_list)
    x = helper.most_successful(df, selected_sport)
    st.table(x)

if user_menu == "Country-wise Analysis":
    st.sidebar.title("Country-wise analysis")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    country_list.insert(0, 'Select')
    selected_country = st.sidebar.selectbox("Select a country", country_list)

    if selected_country == 'Select':
        st.subheader("Citius, Altius, Fortius – Communiter")
        image_path = "https://raw.githubusercontent.com/rajnish-dubey/olympics-analysis/main/pictures/d6xr603fq0g71.webp"
        st.image(image_path, use_column_width=True)

    else:
        country_df = helper.year_wise_medal_tally(df, selected_country)
        if not country_df.empty:
            medals = helper.total_medals_by_country(df, selected_country)
            st.markdown(f"<h2 style='font-size: 24px;'>Total {medals} medals won by {selected_country}.</h2>",
                        unsafe_allow_html=True)
            fig = px.line(country_df, x="Year", y="Medals", color_discrete_sequence=["royalblue"])
            fig.update_layout(
                plot_bgcolor="#f0f0f0",
                paper_bgcolor="#ffffff",
                font=dict(color="#000000"),
                xaxis=dict(
                    title=dict(
                        font=dict(
                            color="black",
                            size=14,
                            family="Arial",
                            weight="bold"
                        )
                    ),
                    tickfont=dict(
                        color="black",
                        size=12,
                        weight="bold"
                    )
                ),
                yaxis=dict(
                    title=dict(
                        font=dict(
                            color="black",
                            size=14,
                            family="Arial",
                            weight="bold"
                        )
                    ),
                    tickfont=dict(
                        color="black",
                        size=12,
                        weight="bold"
                    )
                )
            )
            st.subheader(selected_country + " Medal tally over the years")
            st.plotly_chart(fig)

            st.subheader(selected_country + " Excels in the following Sports")
            pt = helper.country_event_heatmap(df, selected_country)
            fig, y = plt.subplots(figsize=(20, 20))
            ax = sns.heatmap(pt, annot=True)
            st.pyplot(fig)

            st.subheader("Top 10 player of " + selected_country)
            top_df = helper.most_successful_country_wise(df, selected_country)
            st.table(top_df)
        else:
            st.markdown(f"<h2 style='font-size: 24px;'>No medals won by {selected_country}.</h2>",
                        unsafe_allow_html=True)

if user_menu == "Player-wise Analysis":
    medalist_df = df[df['Medal'].notna()]
    athlete_df = medalist_df[['Name', 'region']].drop_duplicates()
    medalist_names = athlete_df['Name'].sort_values(ascending=True).tolist()
    medalist_names.insert(0, 'Select')
    selected_player = st.sidebar.selectbox("Search for a medalist", medalist_names)

    if selected_player == 'Select':
        st.subheader("Men vs Women participation over years")
        final = helper.men_vs_women(df)
        fig = px.line(final, x='Year', y=['Male', 'Female'])
        fig.update_layout(
            autosize=False,
            width=1000,
            height=600,
            plot_bgcolor='rgba(240, 240, 240, 0.8)',
            paper_bgcolor='rgba(255, 255, 255, 1)',
            font=dict(color="black"),
            xaxis=dict(
                title=dict(font=dict(color="black", size=14, weight="bold")),
                tickfont=dict(color="black", size=12, weight="bold")
            ),
            yaxis=dict(
                title=dict(font=dict(color="black", size=14, weight="bold")),
                tickfont=dict(color="black", size=12, weight="bold")
            )
        )
        st.plotly_chart(fig)

        st.subheader("Height vs Weight analysis of players")
        sport_list = df['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0, 'Overall')
        selected_sport = st.selectbox("Select a sport", sport_list)
        temp_df = helper.weight_v_height(df, selected_sport)
        palette = {
            "Gold": "#FFDF00",
            "Silver": "#00C000",
            "Bronze": "#FF0000",
            "No Medals": "#87CEEB"
        }
        temp_df['Color'] = temp_df.apply(lambda x: 'No Medals' if pd.isna(x['Medal']) else x['Medal'], axis=1)
        temp_df['Color'] = temp_df['Color'].replace({"No Medal": "No Medals"})
        unique_colors = temp_df['Color'].unique()
        for color in unique_colors:
            if color not in palette:
                palette[color] = color
        g = sns.FacetGrid(temp_df, col="Sex", height=12, aspect=1)
        g.map_dataframe(sns.scatterplot, x="Weight", y="Height", hue="Color", s=210, alpha=1, palette=palette)
        for ax in g.axes.flatten():
            ax.tick_params(labelsize=20)
        g.set_axis_labels("Weight (kg)", "Height (cm)", fontdict={'size': 24})
        g.add_legend(title="Medal", bbox_to_anchor=(1.05, 0.5), loc="center left")
        st.pyplot(g)

        new_df = df[df['Medal'].notna()]
        modify_df = new_df[['Name', 'Age', 'Medal']].drop_duplicates()
        x1 = modify_df['Age'].dropna()
        x2 = modify_df[modify_df['Medal'] == 'Gold']['Age'].dropna()
        x3 = modify_df[modify_df['Medal'] == 'Silver']['Age'].dropna()
        x4 = modify_df[modify_df['Medal'] == 'Bronze']['Age'].dropna()
        fig = ff.create_distplot(
            [x1, x2, x3, x4],
            ["Overall Age", "Gold Medalist", "Silver Medalist", "Bronze Medalist"],
            show_hist=False,
            show_rug=False
        )
        fig.update_layout(
            autosize=False,
            width=1000,
            height=600,
            plot_bgcolor='rgba(240, 240, 240, 0.8)',
            paper_bgcolor='rgba(255, 255, 255, 1)',
            font=dict(color="black"),
            xaxis=dict(
                title=dict(
                    text="Age",
                    font=dict(
                        color="black",
                        size=14,
                        weight="bold"
                    )
                ),
                tickfont=dict(
                    color="black",
                    size=12,
                    weight="bold"
                )
            ),
            yaxis=dict(
                title=dict(
                    text="Density",
                    font=dict(
                        color="black",
                        size=14,
                        weight="bold"
                    )
                ),
                tickfont=dict(
                    color="black",
                    size=12,
                    weight="bold"
                )
            ),
            annotations=[
                dict(
                    x=1.1,
                    y=1.05,
                    text="Select",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    font=dict(size=16, color="black")
                )
            ]
        )
        fig.update_traces(marker=dict(line=dict(color='black', width=1)))
        fig.update_traces(visible='legendonly')
        fig.data[0].visible = True
        st.subheader("Age Distribution")
        st.plotly_chart(fig)

    else:
        image_path = "https://raw.githubusercontent.com/rajnish-dubey/olympics-analysis/main/pictures/wu_1626844917.jpg"
        st.image(image_path, use_column_width=True)

        athlete_data = df[df['Name'] == selected_player]
        st.subheader(f"Details for {selected_player}")
        st.write(f"Region: {athlete_data.iloc[0]['region']}")
        st.write(f"Sport: {athlete_data.iloc[0]['Sport']}")
        if pd.notna(athlete_data.iloc[0]['Height']):
            st.write(f"Height: {athlete_data.iloc[0]['Height']} cm")
        gold_medals = athlete_data['Gold'].sum()
        silver_medals = athlete_data['Silver'].sum()
        bronze_medals = athlete_data['Bronze'].sum()
        st.write(
            f"Medals: {gold_medals + silver_medals + bronze_medals} ({gold_medals} Gold + {silver_medals} Silver + {bronze_medals} Bronze)")

        st.subheader(f"Participation history of {selected_player}")
        medal_counts = athlete_data.groupby(['Year', 'Event']).agg(
            {'Gold': 'sum', 'Silver': 'sum', 'Bronze': 'sum'}).reset_index()
        medal_counts['Total Medals'] = medal_counts['Gold'] + medal_counts['Silver'] + medal_counts['Bronze']
        fig = px.bar(medal_counts, x='Year', y='Total Medals', color='Event', hover_data={'Total Medals': False})
        fig.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=medal_counts['Year'].unique(),
                ticktext=medal_counts['Year'].unique(),
                title=dict(font=dict(size=14, weight='bold'))
            ),
            yaxis=dict(
                dtick=1,
                title=dict(font=dict(size=14, weight='bold'))
            ),
            font=dict(size=14)
        )
        st.plotly_chart(fig)
