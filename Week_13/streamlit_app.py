import streamlit as st
import pandas as pd
import joblib
import os
import numpy as np

# =====================================
# Page Config
# =====================================
st.set_page_config(
    page_title="Customer Satisfaction Predictor",
    page_icon="📊",
    layout="wide"
)

# =====================================
# Load Model, Scaler, and Features
# =====================================
BASE_DIR = os.path.dirname(__file__)
model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
scaler = joblib.load(os.path.join(BASE_DIR, "scaler.pkl"))
feature_names = joblib.load(os.path.join(BASE_DIR, "features.pkl"))

# =====================================
# Header
# =====================================
st.title("📊 Customer Satisfaction Prediction System")
st.markdown(
    "Predict whether a customer is **Satisfied** or **Not Satisfied** "
    "based on multiple service-related factors."
)
st.markdown("---")

# =====================================
# Define Input Ranges for Common Features
# =====================================
# Map features to appropriate ranges based on common patterns
def get_feature_range(feature_name):
    """Return (min, max, step, default) for a feature"""
    name_lower = feature_name.lower()
    
    # Time-based features (in minutes or hours)
    if any(x in name_lower for x in ['time', 'duration', 'wait']):
        if 'response' in name_lower:
            return (0.0, 120.0, 1.0, 30.0)  # Response time in minutes
        elif 'resolution' in name_lower:
            return (0.0, 480.0, 5.0, 120.0)  # Resolution time in minutes
        elif 'wait' in name_lower:
            return (0.0, 60.0, 1.0, 15.0)  # Waiting time
        else:
            return (0.0, 100.0, 1.0, 20.0)  # Generic time
    
    # Score/Rating features (0-10 scale)
    if any(x in name_lower for x in ['score', 'rating', 'quality', 'satisfaction']):
        return (0.0, 10.0, 0.1, 5.0)
    
    # Count features (tickets, issues, interactions)
    if any(x in name_lower for x in ['ticket', 'count', 'number', 'issue', 'resolved', 'interaction']):
        return (0, 100, 1, 10)
    
    # Percentage features
    if any(x in name_lower for x in ['percent', 'rate', '%']):
        return (0.0, 100.0, 1.0, 50.0)
    
    # Price/Cost features
    if any(x in name_lower for x in ['price', 'cost', 'amount', 'value']):
        return (0.0, 1000.0, 10.0, 100.0)
    
    # Boolean/Binary features (0 or 1)
    if any(x in name_lower for x in ['is_', 'has_', 'flag']):
        return (0, 1, 1, 0)
    
    # Default range for unknown features
    return (0.0, 10.0, 0.1, 5.0)

# =====================================
# Sidebar – User Inputs
# =====================================
st.sidebar.header("📝 Customer Input Parameters")
st.sidebar.markdown("Adjust the sliders below to input customer data:")

user_input = {}

# Group features for better organization
st.sidebar.markdown("### 📊 Service Metrics")
for feature in feature_names:
    min_val, max_val, step, default_val = get_feature_range(feature)
    
    # Determine input type based on step
    if step == 1 and max_val <= 1:
        # Binary feature - use selectbox
        user_input[feature] = st.sidebar.selectbox(
            label=feature.replace("_", " "),
            options=[0, 1],
            index=int(default_val),
            help=f"Select value for {feature.replace('_', ' ')}"
        )
    else:
        # Numeric feature - use slider
        user_input[feature] = st.sidebar.slider(
            label=feature.replace("_", " "),
            min_value=float(min_val) if isinstance(min_val, (int, float)) else min_val,
            max_value=float(max_val) if isinstance(max_val, (int, float)) else max_val,
            value=float(default_val) if isinstance(default_val, (int, float)) else default_val,
            step=float(step) if isinstance(step, (int, float)) else step,
            help=f"Range: {min_val} to {max_val}"
        )

# Convert input to DataFrame in the EXACT order of features
input_df = pd.DataFrame([user_input])[feature_names]

# =====================================
# Main Panel – Display Info
# =====================================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔍 Current Input Values")
    
    # Display input in a nice formatted way
    display_df = input_df.T.reset_index()
    display_df.columns = ['Feature', 'Value']
    st.dataframe(display_df, use_container_width=True, height=400)

with col2:
    st.subheader("📋 Model Info")
    st.info(f"""
    **Features**: {len(feature_names)}
    
    **Model**: Random Forest
    
    **Target**: Customer Satisfaction
    - ✅ Satisfied (CSAT ≥ 4)
    - ❌ Not Satisfied (CSAT < 4)
    """)

# =====================================
# Prediction Section
# =====================================
st.markdown("---")

if st.button("🔮 Predict Customer Satisfaction", use_container_width=True, type="primary"):
    try:
        # Verify input shape
        if input_df.shape[1] != len(feature_names):
            st.error(f"❌ Feature mismatch! Expected {len(feature_names)}, got {input_df.shape[1]}")
        else:
            # Scale inputs
            scaled_input = scaler.transform(input_df)
            
            # Predict
            prediction = model.predict(scaled_input)[0]
            probs = model.predict_proba(scaled_input)[0]
            
            # Display results
            st.markdown("### 📈 Prediction Result")
            
            # Create columns for result display
            res_col1, res_col2 = st.columns(2)
            
            with res_col1:
                if prediction == 1:
                    st.success(f"""
                    ### 😊 Customer is SATISFIED
                    
                    **Confidence**: {round(probs[1]*100, 2)}%
                    
                    The model predicts this customer will be satisfied with the service.
                    """)
                else:
                    st.error(f"""
                    ### 😞 Customer is NOT SATISFIED
                    
                    **Confidence**: {round(probs[0]*100, 2)}%
                    
                    The model predicts this customer will be dissatisfied. Consider improving service quality.
                    """)
            
            with res_col2:
                st.markdown("#### 📊 Probability Distribution")
                prob_df = pd.DataFrame({
                    'Outcome': ['Not Satisfied', 'Satisfied'],
                    'Probability': [probs[0], probs[1]]
                })
                st.bar_chart(prob_df.set_index('Outcome'))
            
            # Confidence indicator
            st.markdown("#### 🎯 Confidence Meter")
            confidence = max(probs[0], probs[1])
            st.progress(int(confidence * 100))
            
            if confidence < 0.6:
                st.warning("⚠️ Low confidence prediction. Results may be uncertain.")
            elif confidence < 0.8:
                st.info("ℹ️ Moderate confidence prediction.")
            else:
                st.success("✅ High confidence prediction.")
                
    except Exception as e:
        st.error(f"❌ Prediction error: {str(e)}")
        st.exception(e)

# =====================================
# Additional Information
# =====================================
with st.expander("ℹ️ How to Use This App"):
    st.markdown("""
    1. **Adjust Input Values**: Use the sliders in the sidebar to input customer data
    2. **Review Inputs**: Check the input values displayed in the main panel
    3. **Predict**: Click the "Predict Customer Satisfaction" button
    4. **Interpret Results**: 
       - Green = Customer likely satisfied
       - Red = Customer likely not satisfied
       - Check confidence percentage for prediction reliability
    
    **Note**: This model uses {num_features} features to make predictions.
    """.format(num_features=len(feature_names)))

# =====================================
# Footer
# =====================================
st.markdown("---")
st.caption("🤖 Machine Learning Model | 🎨 Streamlit | ☁️ Hugging Face Spaces")