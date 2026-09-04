# predict.py
import tensorflow as tf
import numpy as np

def detect_trend(weekly_counts):
    if len(weekly_counts) < 2:
        return 0.0, weekly_counts[0] if weekly_counts else 0

    x = tf.constant(list(range(len(weekly_counts))), dtype=tf.float32)
    y = tf.constant(weekly_counts, dtype=tf.float32)

    x_mean = tf.reduce_mean(x)
    y_mean = tf.reduce_mean(y)

    slope = tf.reduce_sum((x - x_mean) * (y - y_mean)) / tf.reduce_sum((x - x_mean) ** 2)
    intercept = y_mean - slope * x_mean

    next_week_index = len(weekly_counts)
    forecast = max(0, round(float(slope * next_week_index + intercept)))

    return float(slope), forecast

def classify_risk(slope, weekly_counts):
    latest = weekly_counts[-1]
    avg = sum(weekly_counts) / len(weekly_counts)
    growth_rate = ((latest - avg) / avg * 100) if avg > 0 else 0

    if slope > 1.0 and growth_rate > 30:
        return 'HIGH - Possible Outbreak Warning'
    elif slope > 0.5:
        return 'MODERATE - Monitor Closely'
    elif slope > 0:
        return 'LOW - Slight Increase'
    else:
        return 'STABLE / DECLINING'