# main.py
from api import get_diseases
from aggregate import group_by_disease_and_week, to_weekly_series
from predict import detect_trend, classify_risk

def main():
    records = get_diseases()
    print(f"Total records fetched: {len(records)}")

    grouped = group_by_disease_and_week(records)
    diseases = grouped['disease'].unique()

    warning_list = []

    for disease in diseases:
        weekly_counts = to_weekly_series(grouped, disease)
        slope, forecast = detect_trend(weekly_counts)
        risk = classify_risk(slope, weekly_counts)

        warning_list.append({
            'disease': disease,
            'weekly_counts': weekly_counts,
            'trend_slope': round(slope, 2),
            'next_week_forecast': forecast,
            'risk_level': risk,
        })

    # i-sort, pinaka-mataas na slope muna
    warning_list.sort(key=lambda w: w['trend_slope'], reverse=True)

    print("\n=== EARLY WARNING LIST ===\n")
    for w in warning_list:
        print(f"{w['disease']}")
        print(f"  Weekly counts: {w['weekly_counts']}")
        print(f"  Trend slope: {w['trend_slope']}")
        print(f"  Forecast next week: {w['next_week_forecast']}")
        print(f"  Risk level: {w['risk_level']}\n")

if __name__ == '__main__':
    main()