import numpy as np
import pandas as pd
import plotly.figure_factory as ff


def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', "Year", 'City', 'Sport', 'Event', 'Medal'])

    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                                ascending=False).reset_index()

    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['Total'] = medal_tally['Total'].astype('int')
    return medal_tally


def country_year_list(df):
    year = df['Year'].unique().tolist()
    year.sort()
    year.insert(0, 'Overall')
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')
    return year, country


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', "Year", 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    temp_df = pd.DataFrame()

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year',
                                                                                    ascending=False).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total'] = x['Total'].astype('int')
    return x


def data_over_time(df, col):
    data_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    data_over_time.rename(columns={'Year': 'Edition', 'count': col}, inplace=True)
    return data_over_time


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    top_athletes = temp_df['Name'].value_counts().reset_index().head(20)
    top_athletes.columns = ['Name', 'Medals']
    result = top_athletes.merge(df[['Name', 'region', 'Sex', 'Sport']], on='Name', how='left')
    result = result.drop_duplicates(subset=['Name', 'Sport'])
    result.rename(columns={'region': 'Region'}, inplace=True)
    result['S No'] = range(1, len(result) + 1)
    if sport == 'Overall':
        result = result[['S No', 'Name', 'Region', 'Sex', 'Sport', 'Medals']]
    else:
        result = result[['S No', 'Name', 'Region', 'Sex', 'Medals']]
    return result


def total_medals_by_country(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    temp_df = temp_df.drop_duplicates(subset=['Year', 'Event', 'Medal', 'Sport'])
    total_medals = temp_df['Medal'].count()
    return total_medals


def year_wise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    new_df = temp_df[temp_df['region'] == country]
    if new_df.empty:
        return pd.DataFrame(columns=['Year', 'Medals'])
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    final_df.rename(columns={'Medal': 'Medals'}, inplace=True)
    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def most_successful_country_wise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    top_athletes = temp_df['Name'].value_counts().reset_index().head(10)
    top_athletes.columns = ['Name', 'Medals']
    result = top_athletes.merge(df[['Name', 'Sex', 'Sport']], on='Name', how='left')
    result = result.drop_duplicates('Name')
    result['S No'] = range(1, len(result) + 1)
    result = result[['S No', 'Name', 'Sex', 'Sport', 'Medals']]
    return result


def age_distribution(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x = []
    name = []
    famous_sport = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics', 'Swimming', 'Badminton', 'Sailing',
                    'Gymnastics', 'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey',
                    'Rowing', 'Fencing', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing', 'Tennis',
                    'Golf', 'Softball', 'Archery', 'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                    'Rhythmic Gymnastics', 'Rugby Sevens', 'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo',
                    'Ice Hockey']
    for sport in famous_sport:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df['Age'].dropna())
        name.append(sport)
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_traces(visible='legendonly')
    fig.data[-1].visible = True
    return fig


def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    temp_df = athlete_df[athlete_df['Sport'] == 'Gymnastics']
    return temp_df


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex'] == 'Male'].groupby('Year').count()['Name'].reset_index()
    men.rename(columns={'Name': 'Male'}, inplace=True)
    women = athlete_df[athlete_df['Sex'] == 'Female'].groupby('Year').count()['Name'].reset_index()
    women.rename(columns={'Name': 'Female'}, inplace=True)
    final = men.merge(women, on='Year', how='left')
    final.fillna(0, inplace=True)
    return final
