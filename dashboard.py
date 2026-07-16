import streamlit as st
import pandas as pd
import plotly.express as px


def dashboard_page(df, model, features):

    st.title("📊 Executive Dashboard")

    # ----------------------------
    # Data Cleaning
    # ----------------------------

    data = df.copy()

    data["TotalCharges"] = pd.to_numeric(
        data["TotalCharges"],
        errors="coerce"
    )

    data["TotalCharges"] = data["TotalCharges"].fillna(
        data["TotalCharges"].median()
    )

    # ----------------------------
    # KPIs
    # ----------------------------

    total_customers = len(data)

    churn_customers = len(
        data[data["Churn"] == "Yes"]
    )

    churn_rate = (
        churn_customers / total_customers
    ) * 100

    retention_rate = 100 - churn_rate

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👥 Total Customers",
        total_customers
    )

    col2.metric(
        "📉 Churn Rate",
        f"{churn_rate:.2f}%"
    )

    col3.metric(
        "💚 Retention Rate",
        f"{retention_rate:.2f}%"
    )

    revenue_at_risk = data[
        data["Churn"] == "Yes"
    ]["MonthlyCharges"].sum()

    col4.metric(
        "💰 Revenue At Risk",
        f"${revenue_at_risk:,.0f}"
    )

    st.divider()

    # ----------------------------
    # Charts
    # ----------------------------

    col1, col2 = st.columns(2)

    with col1:

        contract_chart = px.histogram(
            data,
            x="Contract",
            color="Churn",
            barmode="group",
            title="Churn by Contract"
        )

        st.plotly_chart(
            contract_chart,
            use_container_width=True
        )

    with col2:

        internet_chart = px.histogram(
            data,
            x="InternetService",
            color="Churn",
            barmode="group",
            title="Churn by Internet Service"
        )

        st.plotly_chart(
            internet_chart,
            use_container_width=True
        )

    col1, col2 = st.columns(2)

    with col1:

        payment_chart = px.pie(
            data,
            names="PaymentMethod",
            title="Payment Method Distribution"
        )

        st.plotly_chart(
            payment_chart,
            use_container_width=True
        )

    with col2:

        monthly_chart = px.histogram(
            data,
            x="MonthlyCharges",
            color="Churn",
            title="Monthly Charges Distribution"
        )

        st.plotly_chart(
            monthly_chart,
            use_container_width=True
        )

    st.divider()

    # ----------------------------
    # Customer Risk Segmentation
    # ----------------------------

    st.subheader("🚦 Customer Risk Segmentation")

    encoded = pd.get_dummies(
        data.drop(
            ["customerID", "Churn"],
            axis=1
        ),
        drop_first=True
    )

    encoded = encoded.reindex(
        columns=features,
        fill_value=0
    )

    probabilities = model.predict_proba(
        encoded
    )[:, 1]

    data["Probability"] = probabilities

    def risk(prob):

        if prob >= 0.75:
            return "High"

        elif prob >= 0.45:
            return "Medium"

        return "Low"

    data["Risk"] = data["Probability"].apply(risk)

    risk_counts = data["Risk"].value_counts()

    fig = px.pie(
        values=risk_counts.values,
        names=risk_counts.index,
        title="Customer Risk Segmentation"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ----------------------------
    # Top Customers
    # ----------------------------

    st.subheader("🚨 Top Customers About To Leave")

    columns_to_show = [
        "customerID",
        "MonthlyCharges",
        "Probability",
        "Risk"
    ]

    top = data.sort_values(
        "Probability",
        ascending=False
    )[columns_to_show].head(10)

    top["Probability"] = (
        top["Probability"] * 100
    ).round(2)

    st.dataframe(
        top,
        use_container_width=True
    )