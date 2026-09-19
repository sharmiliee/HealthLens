import os
import textwrap
from datetime import date

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="HealthLens",
    page_icon="🌷",
    layout="wide"
)


# =========================================================
# SUPABASE CONNECTION
# =========================================================

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Supabase details were not found. Please check your .env file.")
    st.stop()


@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)


supabase = get_supabase()


# =========================================================
# HELPER FOR HTML
# =========================================================

def show_html(content):
    st.html(textwrap.dedent(content).strip())


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
<style>

.stApp {
    background-color: #F8F3EA;
    color: #3E3630;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background-color: #933B5B;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

section[data-testid="stSidebar"] .stRadio label {
    font-size: 16px;
}


/* Main headings */

h1 {
    color: #933B5B;
    font-weight: 700;
}

h2 {
    color: #933B5B;
}

h3 {
    color: #933B5B;
}


/* Buttons */

.stButton > button {
    background-color: #933B5B;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.55rem 1.2rem;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #B5728A;
    color: white;
}


/* Welcome */

.welcome-box {
    background-color: #E3D6BF;
    padding: 30px;
    border-radius: 18px;
    margin-bottom: 25px;
}

.welcome-title {
    font-size: 30px;
    font-weight: 700;
    color: #933B5B;
    margin-bottom: 8px;
}

.welcome-text {
    font-size: 16px;
    color: #4D453E;
    line-height: 1.5;
}


/* Health cards */

.health-card {
    background-color: white;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #E3D6BF;
    min-height: 125px;
}

.card-title {
    color: #9F9679;
    font-size: 15px;
    font-weight: 600;
}

.card-value {
    color: #933B5B;
    font-size: 29px;
    font-weight: 700;
    margin-top: 8px;
}


/* Green insight */

.insight-card {
    background-color: #AABAAE;
    padding: 22px;
    border-radius: 16px;
    margin-bottom: 16px;
}

.insight-title {
    color: #3E5147;
    font-size: 18px;
    font-weight: 700;
}

.insight-text {
    color: #34433B;
    font-size: 15px;
    margin-top: 8px;
    line-height: 1.5;
}


/* Pink insight */

.pink-insight {
    background-color: #F1DCE4;
    padding: 22px;
    border-radius: 16px;
    margin-bottom: 16px;
}

.pink-title {
    color: #933B5B;
    font-size: 18px;
    font-weight: 700;
}

.pink-text {
    color: #4D3941;
    font-size: 15px;
    margin-top: 8px;
    line-height: 1.5;
}


/* White sections */

.section-card {
    background-color: white;
    padding: 24px;
    border-radius: 16px;
    border: 1px solid #E3D6BF;
    margin-bottom: 20px;
}


/* Small text */

.small-text {
    color: #756D64;
    font-size: 14px;
    line-height: 1.5;
}


/* Symptom pills */

.symptom-pill {
    display: inline-block;
    background-color: #F1DCE4;
    color: #933B5B;
    padding: 7px 12px;
    border-radius: 20px;
    margin: 4px;
    font-size: 14px;
    font-weight: 600;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    show_html(
        """
        <div style="text-align:center; padding:20px 0;">
            <div style="font-size:42px;">🌷</div>
            <h1 style="color:white; margin-bottom:0;">
                HealthLens
            </h1>
            <p style="color:#F8E8EE !important;">
                Understand your health patterns
            </p>
        </div>
        """
    )

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📝 Daily Check-in",
            "📊 My Patterns",
            "🩺 Appointment Prep"
        ]
    )


# =========================================================
# GET DATA
# =========================================================

def get_checkins():

    try:

        response = (
            supabase
            .table("health_checkins")
            .select("*")
            .order("checkin_date", desc=True)
            .execute()
        )

        return response.data

    except Exception as e:

        st.error(f"Could not load your check-ins: {e}")

        return []


# =========================================================
# SYMPTOMS
# =========================================================

symptom_columns = {
    "fatigue": "Fatigue",
    "headache": "Headache",
    "cramps": "Cramps",
    "bloating": "Bloating",
    "skin": "Skin changes",
    "hair": "Hair changes",
    "sleep_difficulty": "Difficulty sleeping",
    "other_symptom": "Other symptom"
}


def get_symptom_counts(df):

    counts = {}

    for column, label in symptom_columns.items():

        if column in df.columns:

            counts[label] = int(
                df[column]
                .fillna(False)
                .astype(bool)
                .sum()
            )

    return counts


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    show_html(
        """
        <div class="welcome-box">
            <div class="welcome-title">
                Welcome to HealthLens 🌷
            </div>

            <div class="welcome-text">
                A simple space to track how you feel,
                understand your health patterns, and
                prepare for healthcare appointments.
            </div>
        </div>
        """
    )

    checkins = get_checkins()

    if checkins:

        latest = checkins[0]

        energy = latest.get("energy", 0)
        sleep = latest.get("sleep", 0)
        stress = latest.get("stress", 0)
        mood = latest.get("mood", "Not recorded")

    else:

        energy = 0
        sleep = 0
        stress = 0
        mood = "No check-in yet"


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        show_html(
            f"""
            <div class="health-card">
                <div class="card-title">
                    ⚡ Energy
                </div>

                <div class="card-value">
                    {energy}/10
                </div>
            </div>
            """
        )


    with col2:

        show_html(
            f"""
            <div class="health-card">
                <div class="card-title">
                    🌙 Sleep
                </div>

                <div class="card-value">
                    {sleep} hrs
                </div>
            </div>
            """
        )


    with col3:

        show_html(
            f"""
            <div class="health-card">
                <div class="card-title">
                    🌿 Stress
                </div>

                <div class="card-value">
                    {stress}/10
                </div>
            </div>
            """
        )


    with col4:

        show_html(
            f"""
            <div class="health-card">
                <div class="card-title">
                    ♡ Mood
                </div>

                <div class="card-value" style="font-size:22px;">
                    {mood}
                </div>
            </div>
            """
        )


    if checkins:

        show_html(
            """
            <div class="insight-card">
                <div class="insight-title">
                    🌿 Keep building your health timeline
                </div>

                <div class="insight-text">
                    Your check-ins become more useful over time.
                    HealthLens looks at your observations across
                    multiple days to help you notice patterns
                    worth discussing with your healthcare professional.
                </div>
            </div>
            """
        )

    else:

        show_html(
            """
            <div class="insight-card">
                <div class="insight-title">
                    🌷 Start your health timeline
                </div>

                <div class="insight-text">
                    Complete your first Daily Check-in to begin
                    tracking your observations.
                </div>
            </div>
            """
        )


    st.markdown("### 🩺 Appointment Preparation")


    show_html(
        """
        <div class="section-card">
            <b>Preparing for a doctor appointment?</b>

            <br><br>

            HealthLens organizes your recent observations
            so you can communicate them more clearly during
            your appointment.
        </div>
        """
    )


# =========================================================
# DAILY CHECK-IN
# =========================================================

elif page == "📝 Daily Check-in":

    st.title("📝 Daily Check-in")

    st.write(
        "Take a minute to record how you are feeling today."
    )


    st.markdown("### 📅 Basic Information")


    checkin_date = st.date_input(
        "Date",
        value=date.today()
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        energy = st.slider(
            "⚡ Energy",
            1,
            10,
            5
        )


    with col2:

        sleep = st.number_input(
            "🌙 Sleep (hours)",
            0.0,
            24.0,
            7.0,
            0.5
        )


    with col3:

        stress = st.slider(
            "🌿 Stress",
            1,
            10,
            5
        )


    mood = st.selectbox(
        "♡ Mood",
        [
            "Very Good",
            "Good",
            "Okay",
            "Low",
            "Very Low"
        ]
    )


    st.markdown("### 🌷 Symptoms")


    col1, col2 = st.columns(2)


    with col1:

        fatigue = st.checkbox("Fatigue")

        headache = st.checkbox("Headache")

        cramps = st.checkbox("Cramps")

        bloating = st.checkbox("Bloating")


    with col2:

        skin = st.checkbox("Skin changes")

        hair = st.checkbox("Hair changes")

        sleep_difficulty = st.checkbox(
            "Difficulty sleeping"
        )

        other_symptom = st.checkbox(
            "Other symptom"
        )


    notes = st.text_area(
        "📝 Notes",
        placeholder="Anything else you noticed today..."
    )


    if st.button("💾 Save Check-in"):

        data = {
            "checkin_date": str(checkin_date),
            "energy": energy,
            "sleep": sleep,
            "stress": stress,
            "mood": mood,
            "fatigue": fatigue,
            "headache": headache,
            "cramps": cramps,
            "bloating": bloating,
            "skin": skin,
            "hair": hair,
            "sleep_difficulty": sleep_difficulty,
            "other_symptom": other_symptom,
            "notes": notes
        }


        try:

            supabase \
                .table("health_checkins") \
                .insert(data) \
                .execute()


            st.success(
                "🌷 Your check-in has been saved successfully!"
            )


        except Exception as e:

            st.error(
                "We couldn't save your check-in."
            )

            st.code(str(e))


# =========================================================
# MY PATTERNS
# =========================================================

elif page == "📊 My Patterns":

    st.title("📊 My Patterns")

    st.write(
        "See what your recent check-ins reveal over time."
    )


    checkins = get_checkins()


    if not checkins:

        st.info(
            "🌷 Complete a few Daily Check-ins to start "
            "seeing your patterns."
        )


    else:

        df = pd.DataFrame(checkins)

        df["checkin_date"] = pd.to_datetime(
            df["checkin_date"]
        )

        df = df.sort_values("checkin_date")


        # =================================================
        # OVERVIEW
        # =================================================

        st.markdown("### 📌 Your Recent Overview")


        avg_energy = round(
            df["energy"].mean(),
            1
        )

        avg_sleep = round(
            df["sleep"].mean(),
            1
        )

        avg_stress = round(
            df["stress"].mean(),
            1
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            show_html(
                f"""
                <div class="health-card">
                    <div class="card-title">
                        ⚡ Average Energy
                    </div>

                    <div class="card-value">
                        {avg_energy}/10
                    </div>
                </div>
                """
            )


        with col2:

            show_html(
                f"""
                <div class="health-card">
                    <div class="card-title">
                        🌙 Average Sleep
                    </div>

                    <div class="card-value">
                        {avg_sleep} hrs
                    </div>
                </div>
                """
            )


        with col3:

            show_html(
                f"""
                <div class="health-card">
                    <div class="card-title">
                        🌿 Average Stress
                    </div>

                    <div class="card-value">
                        {avg_stress}/10
                    </div>
                </div>
                """
            )


        # =================================================
        # INSIGHTS
        # =================================================

        st.markdown("### 🌿 Insights from your check-ins")


        if len(df) >= 3:

            low_sleep = df[df["sleep"] < 7]

            normal_sleep = df[df["sleep"] >= 7]


            if len(low_sleep) > 0 and len(normal_sleep) > 0:

                low_sleep_energy = round(
                    low_sleep["energy"].mean(),
                    1
                )

                normal_sleep_energy = round(
                    normal_sleep["energy"].mean(),
                    1
                )


                if normal_sleep_energy > low_sleep_energy:

                    show_html(
                        f"""
                        <div class="insight-card">

                            <div class="insight-title">
                                🌙 Sleep & Energy
                            </div>

                            <div class="insight-text">
                                Your lower-sleep days had an average
                                energy score of {low_sleep_energy}/10,
                                compared with {normal_sleep_energy}/10
                                on days with 7 or more hours of sleep.
                                These observations coincided in your
                                recent check-ins.
                            </div>

                        </div>
                        """
                    )

                else:

                    show_html(
                        """
                        <div class="insight-card">

                            <div class="insight-title">
                                🌙 Sleep & Energy
                            </div>

                            <div class="insight-text">
                                Your recent check-ins do not show a
                                clear difference in energy between
                                lower-sleep and higher-sleep days.
                            </div>

                        </div>
                        """
                    )


        # =================================================
        # STRESS INSIGHT
        # =================================================

        high_stress = df[df["stress"] >= 6]

        lower_stress = df[df["stress"] < 6]


        if len(high_stress) > 0 and len(lower_stress) > 0:

            high_stress_energy = round(
                high_stress["energy"].mean(),
                1
            )

            lower_stress_energy = round(
                lower_stress["energy"].mean(),
                1
            )


            if lower_stress_energy > high_stress_energy:

                show_html(
                    f"""
                    <div class="pink-insight">

                        <div class="pink-title">
                            🌿 Stress & Energy
                        </div>

                        <div class="pink-text">
                            Your higher-stress check-ins had an
                            average energy score of
                            {high_stress_energy}/10, compared with
                            {lower_stress_energy}/10 during lower-stress
                            check-ins.
                        </div>

                    </div>
                    """
                )


        # =================================================
        # SYMPTOM SUMMARY
        # =================================================

        symptom_counts = get_symptom_counts(df)


        recurring_symptoms = [
            (name, count)
            for name, count in symptom_counts.items()
            if count >= 2
        ]


        if recurring_symptoms:

            symptom_html = ""

            for name, count in recurring_symptoms:

                symptom_html += (
                    f'<span class="symptom-pill">'
                    f'{name} · {count} days'
                    f'</span>'
                )


            show_html(
                f"""
                <div class="insight-card">

                    <div class="insight-title">
                        🌷 Recurring Symptoms
                    </div>

                    <div class="insight-text">
                        These symptoms appeared repeatedly
                        in your recent check-ins:
                    </div>

                    <div style="margin-top:10px;">
                        {symptom_html}
                    </div>

                    <div class="small-text" style="margin-top:12px;">
                        This is a record of your observations,
                        not a medical diagnosis.
                    </div>

                </div>
                """
            )

        else:

            show_html(
                """
                <div class="insight-card">

                    <div class="insight-title">
                        🌷 Symptom Overview
                    </div>

                    <div class="insight-text">
                        No symptom has appeared repeatedly
                        in your current check-in history yet.
                    </div>

                </div>
                """
            )


        # =================================================
        # GRAPHS
        # =================================================

        st.markdown("### 📈 Trends over time")


        st.markdown("#### ⚡ Energy")


        energy_chart = (
            df[
                ["checkin_date", "energy"]
            ]
            .set_index("checkin_date")
        )


        st.line_chart(
            energy_chart,
            height=300
        )


        st.markdown("#### 🌙 Sleep")


        sleep_chart = (
            df[
                ["checkin_date", "sleep"]
            ]
            .set_index("checkin_date")
        )


        st.line_chart(
            sleep_chart,
            height=300
        )


        st.markdown("#### 🌿 Stress")


        stress_chart = (
            df[
                ["checkin_date", "stress"]
            ]
            .set_index("checkin_date")
        )


        st.line_chart(
            stress_chart,
            height=300
        )


        # =================================================
        # RECENT CHECK-INS
        # =================================================

        st.markdown("### 📋 Recent Check-ins")


        display_df = df[
            [
                "checkin_date",
                "energy",
                "sleep",
                "stress",
                "mood"
            ]
        ].copy()


        display_df["checkin_date"] = (
            display_df["checkin_date"]
            .dt.strftime("%d %b %Y")
        )


        display_df = display_df.sort_values(
            "checkin_date",
            ascending=False
        )


        display_df.columns = [
            "Date",
            "Energy",
            "Sleep",
            "Stress",
            "Mood"
        ]


        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# APPOINTMENT PREP
# =========================================================

elif page == "🩺 Appointment Prep":

    st.title("🩺 Appointment Prep")

    st.write(
        "Turn your recent observations into a simple "
        "appointment-ready summary."
    )


    checkins = get_checkins()


    if not checkins:

        st.info(
            "🌷 Complete some Daily Check-ins first."
        )


    else:

        df = pd.DataFrame(checkins)


        df["checkin_date"] = pd.to_datetime(
            df["checkin_date"]
        )


        df = df.sort_values("checkin_date")


        avg_energy = round(
            df["energy"].mean(),
            1
        )

        avg_sleep = round(
            df["sleep"].mean(),
            1
        )

        avg_stress = round(
            df["stress"].mean(),
            1
        )


        st.markdown("### 📌 Recent Overview")


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Average Energy",
                f"{avg_energy}/10"
            )


        with col2:

            st.metric(
                "Average Sleep",
                f"{avg_sleep} hrs"
            )


        with col3:

            st.metric(
                "Average Stress",
                f"{avg_stress}/10"
            )


        # =================================================
        # APPOINTMENT SUMMARY
        # =================================================

        st.markdown("### 📄 Appointment Summary")

        st.write(
            "Generate a simple summary of your recent observations "
            "that you can use when preparing for a doctor appointment."
        )

        if st.button("📄 Generate Appointment Summary"):

            summary_lines = [
                "HEALTHLENS — APPOINTMENT SUMMARY",
                "",
                f"Check-in period: "
                f"{df['checkin_date'].min().strftime('%d %b %Y')} "
                f"to {df['checkin_date'].max().strftime('%d %b %Y')}",
                f"Number of check-in days: {len(df)}",
                "",
                "RECENT AVERAGES",
                f"- Average energy: {avg_energy}/10",
                f"- Average sleep: {avg_sleep} hours",
                f"- Average stress: {avg_stress}/10",
                "",
                "RECORDED SYMPTOMS",
            ]

            symptom_found = False

            for column, label in symptom_columns.items():

                if column in df.columns:

                    count = int(
                        df[column]
                        .fillna(False)
                        .astype(bool)
                        .sum()
                    )

                    if count > 0:

                        symptom_found = True

                        summary_lines.append(
                            f"- {label}: reported on "
                            f"{count} of {len(df)} check-in days"
                        )

            if not symptom_found:
                summary_lines.append(
                    "- No symptoms were recorded."
                )

            lowest_energy_day = df.loc[
                df["energy"].idxmin()
            ]

            highest_stress_day = df.loc[
                df["stress"].idxmax()
            ]

            summary_lines.extend([
                "",
                "NOTABLE OBSERVATIONS",
                f"- Lowest recorded energy: "
                f"{lowest_energy_day['energy']}/10 on "
                f"{lowest_energy_day['checkin_date'].strftime('%d %b %Y')}",
                f"- Highest recorded stress: "
                f"{highest_stress_day['stress']}/10 on "
                f"{highest_stress_day['checkin_date'].strftime('%d %b %Y')}",
                "",
                "Note: This summary records personal observations "
                "and is not a medical diagnosis.",
            ])

            appointment_summary = "\n".join(summary_lines)

            st.text_area(
                "Your appointment summary",
                appointment_summary,
                height=350
            )

            st.download_button(
                "⬇️ Download Summary",
                appointment_summary,
                file_name="healthlens_appointment_summary.txt",
                mime="text/plain"
            )


        # =================================================
        # RECURRING SYMPTOMS
        # =================================================

        symptom_counts = get_symptom_counts(df)


        recurring_symptoms = [
            (name, count)
            for name, count in symptom_counts.items()
            if count >= 2
        ]


        st.markdown("### 🌷 Observations to Discuss")


        if recurring_symptoms:

            symptom_lines = ""

            for name, count in recurring_symptoms:

                symptom_lines += (
                    f"• {name} — reported on "
                    f"{count} of {len(df)} check-in days"
                    f"<br><br>"
                )


            show_html(
                f"""
                <div class="section-card">

                    <b>Frequently recorded symptoms</b>

                    <br><br>

                    {symptom_lines}

                </div>
                """
            )

        else:

            show_html(
                """
                <div class="section-card">

                    No recurring symptoms have been
                    identified from the current check-ins.

                </div>
                """
            )


        # =================================================
        # HEALTH SNAPSHOT
        # =================================================

        st.markdown("### 🌿 Recent Health Snapshot")


        if len(df) >= 3:

            lowest_energy_day = df.loc[
                df["energy"].idxmin()
            ]

            highest_stress_day = df.loc[
                df["stress"].idxmax()
            ]


            show_html(
                f"""
                <div class="insight-card">

                    <div class="insight-title">
                        📌 What stood out
                    </div>

                    <div class="insight-text">

                        Lowest recorded energy:
                        <b>{lowest_energy_day["energy"]}/10</b>
                        on
                        <b>
                        {lowest_energy_day["checkin_date"].strftime("%d %b")}
                        </b>.

                        <br><br>

                        Highest recorded stress:
                        <b>{highest_stress_day["stress"]}/10</b>
                        on
                        <b>
                        {highest_stress_day["checkin_date"].strftime("%d %b")}
                        </b>.

                    </div>

                </div>
                """
            )


        # =================================================
        # QUESTIONS
        # =================================================

        st.markdown("### 💬 Questions for my doctor")

        if "doctor_questions" not in st.session_state:
            st.session_state.doctor_questions = []

        question = st.text_area(
            "Write down anything you want to remember.",
            placeholder=(
                "Example: What could be contributing to "
                "my recurring fatigue?"
            ),
            height=140,
            key="doctor_question_input"
        )

        if st.button("➕ Add Question"):

            if question.strip():
                st.session_state.doctor_questions.append(
                    question.strip()
                )
                st.rerun()
            else:
                st.warning("Please write a question first.")

        if st.session_state.doctor_questions:

            st.markdown("#### 📋 My questions")

            for q in st.session_state.doctor_questions:
                st.markdown(f"• {q}")

        show_html(
            """
            <div class="small-text">

                HealthLens is designed to help you organize
                and communicate your observations. It does
                not diagnose medical conditions or replace
                professional medical advice.

            </div>
            """
        )

