import pandas as pd


def preprocessor(df, region_df):
    # filtering of summer olympics
    df = df[df['Season'] == 'Summer']

    # merge to region_df for country
    df = df.merge(region_df, on='NOC', how='left')

    # drop duplicates
    df.drop_duplicates(inplace=True)

    df['Sex'] = df['Sex'].replace({'M': 'Male', 'F': 'Female'})

    # one hot encoding medals
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)

    return df
