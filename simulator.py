import streamlit as st
import pandas as pd


# -----------------------------
# Prediction Function
# -----------------------------

def predict_churn(customer, model, features):

    df = pd.DataFrame([customer])


    encoded = pd.get_dummies(
        df,
        drop_first=True
    )


    encoded = encoded.reindex(
        columns=features,
        fill_value=0
    )


    probability = model.predict_proba(
        encoded
    )[0][1]


    return probability



# -----------------------------
# Risk Level
# -----------------------------

def risk_level(prob):

    if prob >= 0.75:
        return "🔴 High Risk"

    elif prob >= 0.45:
        return "🟠 Medium Risk"

    else:
        return "🟢 Low Risk"



# -----------------------------
# Simulator Page
# -----------------------------

def simulator_page(model, features):


    st.title(
        "🎯 Customer Retention What-If Simulator"
    )


    st.write(
        """
        Test different retention strategies and see
        how they affect customer churn probability.
        """
    )


    st.divider()


    # -------------------------
    # Customer Current Situation
    # -------------------------

    st.subheader(
        "👤 Current Customer Information"
    )


    col1, col2 = st.columns(2)


    with col1:


        tenure = st.slider(
            "Tenure (Months)",
            0,
            72,
            12
        )


        monthly = st.number_input(
            "Monthly Charges",
            0.0,
            200.0,
            70.0
        )


        total = st.number_input(
            "Total Charges",
            0.0,
            10000.0,
            1000.0
        )


        contract = st.selectbox(
            "Current Contract",
            [
                "Month-to-month",
                "One year",
                "Two year"
            ]
        )


        internet = st.selectbox(
            "Internet Service",
            [
                "DSL",
                "Fiber optic",
                "No"
            ]
        )


    with col2:


        tech = st.selectbox(
            "Tech Support",
            [
                "No",
                "Yes",
                "No internet service"
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


    # -------------------------
    # Retention Actions
    # -------------------------

    st.divider()


    st.subheader(
        "💡 Try Retention Actions"
    )


    new_contract = st.selectbox(
        "Offer New Contract",
        [
            "Keep Current",
            "One year",
            "Two year"
        ]
    )


    add_support = st.selectbox(
        "Add Technical Support?",
        [
            "No Change",
            "Yes"
        ]
    )



    simulate = st.button(
        "🚀 Run Simulation"
    )



    if simulate:


        # Current Customer

        current_customer = {

            "SeniorCitizen": senior,

            "tenure": tenure,

            "MonthlyCharges": monthly,

            "TotalCharges": total,

            "gender": "Male",

            "Partner": partner,

            "Dependents": dependents,

            "PhoneService": "Yes",

            "MultipleLines": "No",

            "InternetService": internet,

            "OnlineSecurity": "No",

            "OnlineBackup": "No",

            "DeviceProtection": "No",

            "TechSupport": tech,

            "StreamingTV": "No",

            "StreamingMovies": "No",

            "Contract": contract,

            "PaperlessBilling": "Yes",

            "PaymentMethod": payment

        }



        # After Retention Action

        improved_customer = current_customer.copy()



        if new_contract != "Keep Current":

            improved_customer["Contract"] = new_contract



        if add_support == "Yes":

            improved_customer["TechSupport"] = "Yes"



        before = predict_churn(
            current_customer,
            model,
            features
        )


        after = predict_churn(
            improved_customer,
            model,
            features
        )



        st.divider()


        col1, col2 = st.columns(2)



        with col1:

            st.subheader(
                "Before Action"
            )

            st.metric(
                "Churn Probability",
                f"{before*100:.2f}%"
            )

            st.write(
                risk_level(before)
            )



        with col2:

            st.subheader(
                "After Action"
            )

            st.metric(
                "Churn Probability",
                f"{after*100:.2f}%"
            )

            st.write(
                risk_level(after)
            )



        improvement = (before-after)*100



        st.divider()


        if improvement > 0:

            st.success(
                f"""
                🎉 Retention strategy reduced churn risk by
                {improvement:.2f}%
                """
            )

        else:

            st.warning(
                """
                This strategy did not reduce churn risk.
                Try another action.
                """
            )