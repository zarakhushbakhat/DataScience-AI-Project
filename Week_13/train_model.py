# ============================================================
# FIXED TRAIN MODEL SCRIPT - Streamlit Compatible
# ============================================================

import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import os

print("🔄 Loading dataset...")
df = pd.read_csv("Customer_support_data.csv")
print(f"✅ Dataset loaded: {df.shape}")

# -----------------------------
# 1️⃣ Remove ID/UUID Columns
# -----------------------------
print("\n🧹 Cleaning data...")
for col in df.columns:
    if df[col].dtype == 'object':
        sample_val = str(df[col].dropna().iloc[0]) if len(df[col].dropna()) > 0 else ""
        if '-' in sample_val and len(sample_val) > 15:
            df.drop(columns=[col], inplace=True)
            print(f"  Removed UUID column: {col}")

# -----------------------------
# 2️⃣ Identify Numeric Columns (excluding CSAT Score)
# -----------------------------
# These are the features users can actually input via sliders
numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

# Remove CSAT Score from features (it's our target)
if 'CSAT Score' in numeric_cols:
    numeric_cols.remove('CSAT Score')

print(f"\n📊 Numeric features to use: {len(numeric_cols)}")
for col in numeric_cols:
    print(f"  • {col}")

# -----------------------------
# 3️⃣ Handle Missing Values
# -----------------------------
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

# -----------------------------
# 4️⃣ Create Target Variable
# -----------------------------
df['CSAT_Category'] = (df['CSAT Score'] >= 4).astype(int)

# Select ONLY numeric features
X = df[numeric_cols].copy()
y = df['CSAT_Category']

print(f"\n✅ Final feature set: {X.shape[1]} features")
print(f"✅ Target distribution:")
print(y.value_counts())

# -----------------------------
# 5️⃣ Save Feature Names
# -----------------------------
feature_names = X.columns.tolist()

# -----------------------------
# 6️⃣ Train-Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -----------------------------
# 7️⃣ Feature Scaling
# -----------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# -----------------------------
# 8️⃣ Train Model
# -----------------------------
print("\n🤖 Training Random Forest model...")
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=15,
    min_samples_split=5,
    min_samples_leaf=2,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

model.fit(X_train_scaled, y_train)

# -----------------------------
# 9️⃣ Evaluate Model
# -----------------------------
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

print("\n" + "="*60)
print("📊 MODEL EVALUATION")
print("="*60)
print(f"Accuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# -----------------------------
# 🔟 Feature Importance
# -----------------------------
feature_importance = pd.DataFrame({
    'feature': feature_names,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n📈 Top 10 Most Important Features:")
print(feature_importance.head(10).to_string(index=False))

# -----------------------------
# 1️⃣1️⃣ Save Model Artifacts
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

joblib.dump(model, os.path.join(BASE_DIR, "model.pkl"))
joblib.dump(scaler, os.path.join(BASE_DIR, "scaler.pkl"))
joblib.dump(feature_names, os.path.join(BASE_DIR, "features.pkl"))

print("\n" + "="*60)
print("✅ MODEL ARTIFACTS SAVED")
print("="*60)
print(f"📁 Location: {BASE_DIR}")
print(f"📝 Features saved: {len(feature_names)}")
print("\nFiles created:")
print("  • model.pkl")
print("  • scaler.pkl")
print("  • features.pkl")
print("\n✅ Ready for deployment!")