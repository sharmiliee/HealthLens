# 🌷 HealthLens

### Personal Health Pattern & Appointment Preparation Assistant

HealthLens is a simple web application designed to help users record daily health observations, identify recurring patterns, and prepare organized information for healthcare appointments.

## ✨ Features

- 📝 **Daily Check-ins**
  - Record energy, sleep, stress, mood, and symptoms.
  - Add personal notes for each day.
  - Store check-ins using Supabase.

- 📊 **My Patterns**
  - View health observations across multiple days.
  - Track energy, sleep, and stress trends.
  - Identify recurring symptoms.
  - View simple observations based on recorded data.

- 🩺 **Appointment Preparation**
  - View a recent health overview.
  - Identify frequently recorded symptoms.
  - Generate an appointment-ready summary.
  - Download the summary as a text file.
  - Write questions to discuss with a doctor.

## 🛠️ Technologies Used

- Python
- Streamlit
- Supabase
- Pandas
- Python-dotenv

## 🎯 Purpose

HealthLens is designed to help users organize and communicate their personal health observations more clearly.

The application focuses on recording observations and identifying patterns across multiple check-ins. HealthLens does not diagnose medical conditions or replace professional medical advice.

## 🚀 Running the Project

### 1. Install dependencies

~~~bash
pip install streamlit supabase python-dotenv pandas
~~~

### 2. Configure Supabase

Create a `.env` file in the project folder:

~~~text
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_publishable_key
~~~

Do not upload the `.env` file to GitHub.

### 3. Run the application

~~~bash
python -m streamlit run app.py
~~~

The application will open in your browser.

## 🔐 Security

The `.env` file contains private configuration and must not be uploaded to GitHub.

The repository includes a `.gitignore` file to prevent `.env` from being committed.

## 🌷 Project

Built as a hackathon project focused on making personal health observations easier to organize and discuss.
