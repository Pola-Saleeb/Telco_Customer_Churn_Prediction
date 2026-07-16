import streamlit as st
import pandas as pd


# -------------------------------------------------
# Risk Level
# -------------------------------------------------

def get_risk_level(probability):

    if probability >= 0.75:
        return "🔴 High Risk"

    elif probability >= 0.45:
        return "🟠 Medium Risk"

    else:
        return "🟢 Low Risk"


# -------------------------------------------------
# Explain Prediction
# -------------------------------------------------

def explain_prediction(encoded_df, model, features):

    coefficients = model.coef_[0]

    impacts = []

    for feature, value, coef in zip(
        features,
        encoded_df.iloc[0],
        coefficients
    ):

        contribution = value * coef

        impacts.append(
            {
                "Feature": feature,
                "Contribution": contribution
            }
        )

    impacts = sorted(
        impacts,
        key=lambda x: abs(x["Contribution"]),
        reverse=True
    )

    return impacts[:5]


# -------------------------------------------------
# Recommendation Engine
# -------------------------------------------------

def generate_recommendations(impacts):

    recommendations = []

    for item in impacts:

        feature = item["Feature"]

        if "Contract" in feature:

            recommendations.append(
                "Offer a longer contract discount (1 or 2 years)."
            )

        elif "MonthlyCharges" in feature:

            recommendations.append(
                "Provide a loyalty discount to reduce monthly charges."
            )

        elif "tenure" in feature:

            recommendations.append(
                "Create a loyalty reward program for this customer."
            )

        elif "TechSupport" in feature:

            recommendations.append(
                "Offer free technical support."
            )

        elif "InternetService_Fiber optic" in feature:

            recommendations.append(
                "Check customer satisfaction with internet quality."
            )

        elif "PaymentMethod_Electronic check" in feature:

            recommendations.append(
                "Encourage automatic payment methods."
            )


    if len(recommendations) == 0:

        recommendations.append(
            "Maintain regular communication with the customer."
        )


    return list(dict.fromkeys(recommendations))



# -------------------------------------------------
# Main Agent Page
# -------------------------------------------------

def customer_agent_page(model, features):

    st.title("🤖 AI Customer Risk Agent")

    st.write(
        "Enter customer information to predict churn risk."
    )


    with st.form("prediction_form"):


        col1, col2, col3 = st.columns(3)


        # -------------------------
        # Customer Information
        # -------------------------

        with col1:

            gender = st.selectbox(
                "Gender",
                [
                    "Female",
                    "Male"
                ]
            )


            senior = st.selectbox(
                "Senior Citizen",
                [
                    0,
                    1
                ]
            )


            partner = st.selectbox(
                "Partner",
                [
                    "No",
                    "Yes"
                ]
            )


            dependents = st.selectbox(
                "Dependents",
                [
                    "No",
                    "Yes"
                ]
            )


            phone = st.selectbox(
                "Phone Service",
                [
                    "No",
                    "Yes"
                ]
            )


            multiple = st.selectbox(
                "Multiple Lines",
                [
                    "No phone service",
                    "No",
                    "Yes"
                ]
            )


        # -------------------------
        # Service Information
        # -------------------------

        with col2:


            internet = st.selectbox(
                "Internet Service",
                [
                    "DSL",
                    "Fiber optic",
                    "No"
                ]
            )


            security = st.selectbox(
                "Online Security",
                [
                    "No",
                    "Yes",
                    "No internet service"
                ]
            )


            backup = st.selectbox(
                "Online Backup",
                [
                    "No",
                    "Yes",
                    "No internet service"
                ]
            )


            protection = st.selectbox(
                "Device Protection",
                [
                    "No",
                    "Yes",
                    "No internet service"
                ]
            )


            tech = st.selectbox(
                "Tech Support",
                [
                    "No",
                    "Yes",
                    "No internet service"
                ]
            )


            streaming_tv = st.selectbox(
                "Streaming TV",
                [
                    "No",
                    "Yes",
                    "No internet service"
                ]
            )


            streaming_movies = st.selectbox(
                "Streaming Movies",
                [
                    "No",
                    "Yes",
                    "No internet service"
                ]
            )



        # -------------------------
        # Billing Information
        # -------------------------

        with col3:


            tenure = st.slider(
                "Tenure (Months)",
                0,
                72,
                12
            )


            monthly = st.number_input(
                "Monthly Charges",
                min_value=0.0,
                max_value=200.0,
                value=70.0
            )


            total = st.number_input(
                "Total Charges",
                min_value=0.0,
                max_value=10000.0,
                value=1000.0
            )


            contract = st.selectbox(
                "Contract",
                [
                    "Month-to-month",
                    "One year",
                    "Two year"
                ]
            )


            paperless = st.selectbox(
                "Paperless Billing",
                [
                    "No",
                    "Yes"
                ]
            )


            payment = st.selectbox(
                "Payment Method",
                [
                    "Bank transfer (automatic)",
                    "Credit card (automatic)",
                    "Electronic check",
                    "Mailed check"
                ]
            )



        submitted = st.form_submit_button(
            "🔍 Predict Customer Risk"
        )



    # -------------------------------------------------
    # Prediction
    # -------------------------------------------------

    if submitted:


        customer = {


            "SeniorCitizen": senior,

            "tenure": tenure,

            "MonthlyCharges": monthly,

            "TotalCharges": total,


            "gender": gender,

            "Partner": partner,

            "Dependents": dependents,


            "PhoneService": phone,

            "MultipleLines": multiple,


            "InternetService": internet,

            "OnlineSecurity": security,

            "OnlineBackup": backup,

            "DeviceProtection": protection,

            "TechSupport": tech,

            "StreamingTV": streaming_tv,

            "StreamingMovies": streaming_movies,


            "Contract": contract,

            "PaperlessBilling": paperless,

            "PaymentMethod": payment

        }



        input_df = pd.DataFrame(
            [customer]
        )


        encoded = pd.get_dummies(
            input_df,
            drop_first=True
        )


        encoded = encoded.reindex(
            columns=features,
            fill_value=0
        )



        prediction = model.predict(
            encoded
        )[0]


        probability = model.predict_proba(
            encoded
        )[0][1]



        risk = get_risk_level(
            probability
        )


        impacts = explain_prediction(
            encoded,
            model,
            features
        )


        recommendations = generate_recommendations(
            impacts
        )



        st.divider()


        st.subheader(
            "Prediction Result"
        )


        if prediction == 1:

            st.error(
                "⚠ Customer is likely to leave."
            )

        else:

            st.success(
                "✅ Customer is likely to stay."
            )



        col1, col2 = st.columns(2)


        col1.metric(
            "Churn Probability",
            f"{probability*100:.2f}%"
        )


        col2.metric(
            "Risk Level",
            risk
        )



        st.subheader(
            "🔎 Why this prediction?"
        )


        explanation_df = pd.DataFrame(
            impacts
        )


        st.dataframe(
            explanation_df,
            use_container_width=True
        )



        st.subheader(
            "💡 Retention Recommendations"
        )


        for rec in recommendations:

            st.success(rec)