import json
import webbrowser
from api import get_diseases
from aggregate import group_by_disease_and_week, to_weekly_series
from predict import detect_trend, classify_risk, get_nursing_advisory

def export_to_json(warning_list, filename="data.json"):
    """
    Serializes TensorFlow prediction outputs, risk metrics, and dynamic advisories 
    into a structured JSON file for consumption by external features/APIs.
    """
    payload = {
        "meta": {
            "total_conditions": len(warning_list),
            "generated_at": "2026-09-14 05:04:00",
            "source_api": "http://127.0.0.1:8000/api/diseases"
        },
        "diseases": warning_list
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4)

    print(f"Data successfully exported to {filename} for external features!")


def generate_chief_nurse_dashboard(warning_list):
    high_risk_count = sum(1 for w in warning_list if w['risk_code'] == 'high')
    mod_risk_count = sum(1 for w in warning_list if w['risk_code'] == 'moderate')

    table_rows = ""
    for w in warning_list:
        badge_styles = {
            'high': 'bg-red-100 text-red-800 border-red-300',
            'moderate': 'bg-amber-100 text-amber-800 border-amber-300',
            'low': 'bg-blue-100 text-blue-800 border-blue-300',
            'stable': 'bg-emerald-100 text-emerald-800 border-emerald-300'
        }
        badge_cls = badge_styles.get(w['risk_code'], 'bg-gray-100 text-gray-800')

        table_rows += f"""
        <tr class="hover:bg-slate-50 transition border-b border-gray-100">
            <td class="py-4 px-4 font-semibold text-slate-900">{w['disease']}</td>
            <td class="py-4 px-4">
                <span class="px-2.5 py-1 text-xs font-bold rounded-full border {badge_cls}">
                    {w['risk_level']}
                </span>
            </td>
            <td class="py-4 px-4 font-mono font-bold text-slate-700">{w['trend_slope']:.2f}</td>
            <td class="py-4 px-4 font-bold text-indigo-600 text-base">{w['next_week_forecast']} cases</td>
            <td class="py-4 px-4 text-xs text-slate-600 max-w-md">
                <div class="bg-slate-50 p-3 rounded-lg border border-slate-200 leading-relaxed">
                    {w['advisory']}
                </div>
            </td>
        </tr>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chief Nurse Early Warning Dashboard</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-100 font-sans text-slate-800">
        <header class="bg-slate-900 text-white py-5 px-8 shadow-md">
            <div class="max-w-7xl mx-auto flex justify-between items-center">
                <div>
                    <h1 class="text-2xl font-bold tracking-tight">Chief Nurse Clinical Surveillance Dashboard</h1>
                    <p class="text-xs text-slate-400 mt-1">AI-Powered Disease Trend Forecasting & Resource Planning</p>
                </div>
                <div>
                    <span class="bg-indigo-900 text-indigo-200 text-xs px-3 py-1 rounded-full border border-indigo-700 font-medium">TensorFlow Engine Active</span>
                </div>
            </div>
        </header>

        <main class="max-w-7xl mx-auto p-6 space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
                    <p class="text-xs font-bold text-slate-500 uppercase tracking-wider">High Risk / Outbreak Alerts</p>
                    <h3 class="text-3xl font-extrabold text-red-600 mt-2">{high_risk_count}</h3>
                    <p class="text-xs text-slate-500 mt-1">Immediate ward & supply action required</p>
                </div>
                <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
                    <p class="text-xs font-bold text-slate-500 uppercase tracking-wider">Moderate Watch List</p>
                    <h3 class="text-3xl font-extrabold text-amber-500 mt-2">{mod_risk_count}</h3>
                    <p class="text-xs text-slate-500 mt-1">Elevated trends needing close monitoring</p>
                </div>
                <div class="bg-white p-5 rounded-xl shadow-sm border border-slate-200">
                    <p class="text-xs font-bold text-slate-500 uppercase tracking-wider">Total Tracked Conditions</p>
                    <h3 class="text-3xl font-extrabold text-slate-800 mt-2">{len(warning_list)}</h3>
                    <p class="text-xs text-slate-500 mt-1">Live data fetched from Laravel API</p>
                </div>
            </div>

            <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
                <div class="px-6 py-4 border-b border-slate-200 flex justify-between items-center bg-slate-50">
                    <h2 class="font-bold text-slate-800">Prioritized Early Warning & Dynamic Protocol Advisory</h2>
                    <span class="text-xs text-slate-500">Sorted by highest trend slope</span>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse text-sm">
                        <thead class="bg-slate-100 text-slate-600 uppercase text-xs font-semibold">
                            <tr>
                                <th class="py-3 px-4">Condition</th>
                                <th class="py-3 px-4">Risk Level</th>
                                <th class="py-3 px-4">Trend Slope</th>
                                <th class="py-3 px-4">Next Week Forecast</th>
                                <th class="py-3 px-4">Automated Prevention & Nursing Protocol</th>
                            </tr>
                        </thead>
                        <tbody>
                            {table_rows}
                        </tbody>
                    </table>
                </div>
            </div>
        </main>
    </body>
    </html>
    """

    filename = "chief_nurse_dashboard.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Dashboard generated successfully! Opening {filename}...")
    webbrowser.open(filename)


def main():
    records = get_diseases()
    print(f"Total records fetched from API: {len(records)}")

    grouped = group_by_disease_and_week(records)
    diseases = grouped['disease'].unique()

    warning_list = []

    for disease in diseases:
        weekly_counts = to_weekly_series(grouped, disease)
        counts_list = [int(c) for c in weekly_counts]
        
        # UNPACK 3 VALUES HERE (added volatility)
        slope, forecast, volatility = detect_trend(weekly_counts)
        
        risk_level, risk_code = classify_risk(slope, weekly_counts)
        
        # PASS VOLATILITY TO THE ADVISORY ENGINE
        advisory = get_nursing_advisory(disease, risk_code, forecast, slope, volatility)

        warning_list.append({
            'disease': str(disease),
            'weekly_counts': counts_list,
            'trend_slope': round(float(slope), 2),
            'next_week_forecast': int(forecast),
            'volatility': round(float(volatility), 2),
            'risk_level': str(risk_level),
            'risk_code': str(risk_code),
            'advisory': str(advisory),
        })

    # Sort: highest trend slope first
    warning_list.sort(key=lambda w: w['trend_slope'], reverse=True)

    # 1. Export JSON data for external tools/microservices
    export_to_json(warning_list)

    # 2. Render and open Chief Nurse Dashboard
    generate_chief_nurse_dashboard(warning_list)

if __name__ == '__main__':
    main()