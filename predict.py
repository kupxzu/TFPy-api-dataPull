import tensorflow as tf
import numpy as np

def detect_trend(weekly_counts):
    if len(weekly_counts) < 2:
        return 0.0, weekly_counts[0] if weekly_counts else 0, 0.0

    x = tf.constant(list(range(len(weekly_counts))), dtype=tf.float32)
    y = tf.constant(weekly_counts, dtype=tf.float32)

    x_mean = tf.reduce_mean(x)
    y_mean = tf.reduce_mean(y)

    slope = tf.reduce_sum((x - x_mean) * (y - y_mean)) / tf.reduce_sum((x - x_mean) ** 2)
    intercept = y_mean - slope * x_mean

    next_week_index = len(weekly_counts)
    forecast = max(0, round(float(slope * next_week_index + intercept)))

    # Calculate volatility (standard deviation of historical weekly counts)
    volatility = float(tf.math.reduce_std(y))

    return float(slope), forecast, volatility


def classify_risk(slope, weekly_counts):
    latest = weekly_counts[-1] if weekly_counts else 0
    avg = (sum(weekly_counts) / len(weekly_counts)) if weekly_counts else 0
    growth_rate = ((latest - avg) / avg * 100) if avg > 0 else 0

    if slope > 1.0 and growth_rate > 30:
        return 'HIGH - Outbreak Warning', 'high'
    elif slope > 0.5:
        return 'MODERATE - Monitor Closely', 'moderate'
    elif slope > 0:
        return 'LOW - Slight Increase', 'low'
    else:
        return 'STABLE / DECLINING', 'stable'


def get_nursing_advisory(disease_name, risk_code, forecast, slope, volatility=0.0):
    """
    DYNAMIC CLINICAL KEYWORD ENGINE & RESPONSIVE PROTOCOL ADVISORY
    Broadened keyword coverage across multiple medical domains + volatility responsiveness.
    """
    disease_clean = disease_name.lower()

    # Broadened Clinical Keyword Categories
    categories = {
        'respiratory': ['asthma', 'bronchitis', 'flu', 'influenza', 'covid', 'pneumonia', 'cough', 'copd', 'sars', 'rsv', 'tuberculosis', 'pharyngitis'],
        'gastrointestinal': ['gastroenteritis', 'diarrhea', 'cholera', 'typhoid', 'amoebiasis', 'food poisoning', 'rotavirus', 'norovirus', 'dysentery'],
        'vector_borne': ['dengue', 'malaria', 'chikungunya', 'zika', 'leptospirosis', 'rabies', 'typhus'],
        'cardiovascular': ['hypertension', 'cardiac', 'heart failure', 'arrhythmia', 'angina', 'ischemic', 'stroke', 'hypertensive'],
        'metabolic_endocrine': ['diabetes', 'ketoacidosis', 'thyroid', 'hyperglycemia', 'metabolic', 'obesity', 'ckd', 'kidney'],
        'neurological': ['migraine', 'epilepsy', 'seizure', 'meningitis', 'encephalitis', 'neuropathy', 'stroke'],
        'dermatological_skin': ['chickenpox', 'measles', 'rubella', 'scabies', 'cellulitis', 'mpox', 'monkeypox', 'shingles'],
        'pediatric_geriatric': ['pediatric', 'neonatal', 'geriatric', 'dementia', 'alzheimer']
    }

    # Match active categories
    matched_cats = [cat for cat, keywords in categories.items() if any(k in disease_clean for k in keywords)]

    # 1. Volatility Response Warning
    volatility_alert = ""
    if volatility > 2.0 and risk_code in ['high', 'moderate']:
        volatility_alert = "⚠️ <strong>HIGH VOLATILITY DETECTED:</strong> Sudden case spikes observed. Prepare rapid-response triage staff."

    # 2. Risk-Based Directive Base
    directives = []

    if risk_code == 'high':
        directives.append(f"🚨 <strong>OUTBREAK PROTOCOL ACTIVATED:</strong> Projected +{forecast} new cases next week (Slope: +{slope:.2f}).")
    elif risk_code == 'moderate':
        directives.append(f"⚠️ <strong>ELEVATED WATCH:</strong> Upward trend detected (+{forecast} forecasted cases).")
    else:
        directives.append(f"✅ <strong>ROUTINE SURVEILLANCE:</strong> Stable trajectory.")

    # 3. Dynamic Category Action Mappings
    if 'respiratory' in matched_cats:
        if risk_code == 'high':
            directives.append("Enforce strict isolation bays, restock O2 cylinders & nebulizers, and mandate N95 mask compliance in triage.")
        elif risk_code == 'moderate':
            directives.append("Audit respiratory supplies, verify swab kit availability, and monitor pediatric bed capacity.")
        else:
            directives.append("Maintain routine aerosol infection control and monitor outpatient cough logs.")

    if 'gastrointestinal' in matched_cats:
        if risk_code == 'high':
            directives.append("Isolate active cases, verify water/food sanitation sources, and stock IV fluids & ORS lines.")
        elif risk_code == 'moderate':
            directives.append("Increase communal ward sanitation frequency and audit oral rehydration salts stock.")
        else:
            directives.append("Enforce standard hand hygiene protocols and food handler health screening.")

    if 'vector_borne' in matched_cats:
        if risk_code == 'high':
            directives.append("Alert local health unit for fogging/vector control. Prepare blood product/platelet monitoring kits.")
        elif risk_code == 'moderate':
            directives.append("Ensure adequate mosquito netting in wards and stock rapid diagnostic tests (RDTs).")
        else:
            directives.append("Continue routine fever surveillance and standing water vector checks.")

    if 'cardiovascular' in matched_cats:
        if risk_code == 'high':
            directives.append("Reserve telemetry/ICU beds, restock emergency cardiac meds, and prioritize BP triage screening.")
        elif risk_code == 'moderate':
            directives.append("Audit antihypertensive stocks and increase cardiac triage vigilance for acute chest pain.")
        else:
            directives.append("Maintain standard outpatient blood pressure screening protocols.")

    if 'metabolic_endocrine' in matched_cats:
        if risk_code == 'high':
            directives.append("Alert Endocrinology unit, verify point-of-care glucometer strips, and prepare IV insulin lines.")
        elif risk_code == 'moderate':
            directives.append("Audit chronic care bed allocations and review diabetic diet compliance records.")
        else:
            directives.append("Continue routine glycemic management and outpatient lifestyle counseling.")

    if 'neurological' in matched_cats:
        if risk_code == 'high':
            directives.append("Prepare quiet/low-light stabilization rooms and verify anticonvulsant & acute pain medication stocks.")
        elif risk_code == 'moderate':
            directives.append("Monitor outpatient neurology appointment backlogs and track acute headache admissions.")
        else:
            directives.append("Standard triage assessment for neurological symptom progression.")

    if 'dermatological_skin' in matched_cats:
        if risk_code == 'high':
            directives.append("Set up contact-isolation wards, restock topical/antiviral meds, and mandate PPE glove/gown protocols.")
        else:
            directives.append("Standard contact precaution protocols in triage.")

    # Generic Fallback if no keywords matched
    if not matched_cats:
        if risk_code == 'high':
            directives.append("Escalate case load to Infection Control & Chief of Clinics. Prepare overflow ward capacity.")
        elif risk_code == 'moderate':
            directives.append("Increase triage vigilance and audit general nursing supply buffer stocks.")
        else:
            directives.append("Maintain standard nursing care protocols and regular case logging.")

    if volatility_alert:
        directives.insert(1, volatility_alert)

    return " ".join(directives)