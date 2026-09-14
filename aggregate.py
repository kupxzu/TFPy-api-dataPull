import pandas as pd

def filter_records_by_date(df, filter_type="all", date_ref=None):
    """
    Filters the DataFrame based on filter_type: 'today', 'month', 'year', or 'all'.
    """
    if date_ref is None:
        date_ref = pd.Timestamp.now()
    else:
        date_ref = pd.to_datetime(date_ref)

    if filter_type == "today":
        return df[df['date'].dt.date == date_ref.date()]
    elif filter_type == "month":
        return df[(df['date'].dt.year == date_ref.year) & (df['date'].dt.month == date_ref.month)]
    elif filter_type == "year":
        return df[df['date'].dt.year == date_ref.year]
    
    return df

def group_by_disease_and_week(records, filter_type="all", date_ref=None):
    if not records:
        return pd.DataFrame(columns=['disease', 'week_index', 'count'])

    df = pd.DataFrame(records)
    df['date'] = pd.to_datetime(df['date'])

    # Apply date filter
    df = filter_records_by_date(df, filter_type=filter_type, date_ref=date_ref)

    if df.empty:
        return pd.DataFrame(columns=['disease', 'week_index', 'count'])

    # Reference point: start date of filtered data
    start_date = df['date'].min()

    # Calculate week index relative to filtered start date
    df['week_index'] = ((df['date'] - start_date).dt.days // 7) + 1

    # Group by disease + week index
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