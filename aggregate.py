import pandas as pd

def group_by_disease_and_week(records):
    df = pd.DataFrame(records)
    df['date'] = pd.to_datetime(df['date'])

    # reference point: pinakaunang date
    start_date = df['date'].min()

    # kunin yung week index relative sa start_date
    df['week_index'] = ((df['date'] - start_date).dt.days // 7) + 1

    # i-group by disease + week, bilangin ang cases
    grouped = df.groupby(['disease', 'week_index']).size().reset_index(name='count')

    return grouped

def to_weekly_series(grouped, disease_name):
    subset = grouped[grouped['disease'] == disease_name]
    if subset.empty:
        return []

    max_week = subset['week_index'].max()
    weekly_counts = [0] * max_week

    for _, row in subset.iterrows():
        weekly_counts[row['week_index'] - 1] = row['count']

    return weekly_counts