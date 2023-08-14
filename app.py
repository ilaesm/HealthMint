import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import requests


def calculate_bmi(weight, height):
    return weight / (height ** 2)
# the following function calculates BMR, the formula is taken from a source (i did not create the formula, just put it into python)
def calculate_calories(age, gender, weight, height, exercise_time):
    if gender == "Male":
        BMR = 88.36 + (13.4 * weight) + (4.8 * height * 100) - (5.7 * age)
    else:
        BMR = 447.6 + (9.2 * weight) + (3.1 * height * 100) - (4.3 * age)

    if exercise_time <= 1:
        return BMR * 1.2
    elif exercise_time <= 3:
        return BMR * 1.375
    elif exercise_time <= 5:
        return BMR * 1.55
    else:
        return BMR * 1.725

def main():
    st.set_page_config(layout='wide', page_title="HealthMint Wellness App", page_icon=":sleep:")
    with open("logo.svg", "r") as file:
        svg_logo = file.read()
    st.markdown(svg_logo, unsafe_allow_html=True)
    st.subheader("HealthMint is a health and wellness app, designed to enhance your well-being through personalized insights and tools")
    st.sidebar.caption('Please fill out the following information:')
    # session state
    if 'age' not in st.session_state:
        st.session_state['age'] = 1
        st.session_state['gender'] = "Male"
        st.session_state['weight'] = 1
        st.session_state['height'] = 0.1
        st.session_state['calorie'] = 1
        st.session_state['exercise_time'] = 1
        st.session_state['consumption_options'] = "None"
        st.session_state['sleep_time'] = 1

    # user inputs (using stored values as initial values)
    st.session_state['age'] = st.sidebar.number_input('Age', min_value=1, value=st.session_state['age'])
    st.session_state["gender"] = st.sidebar.selectbox("Biological Gender", ("Male", "Female"), index=0)
    st.session_state['weight'] = st.sidebar.number_input('Weight (kg)', min_value=1, value=st.session_state['weight'])
    st.session_state['height'] = st.sidebar.number_input('Height (m)', min_value=0.1, value=st.session_state['height'])
    st.session_state['calorie'] = st.sidebar.number_input('What is your average daily caloric intake?', min_value=1, value=st.session_state['calorie'])
    st.session_state['exercise_time'] = st.sidebar.number_input('How many hours do you exercise per day?', min_value=1, value=st.session_state['exercise_time'])
    st.session_state['consumption_options'] = st.sidebar.multiselect(
        'Which of the following do you regularly consume?',
        ['Caffeine', 'Alcohol', 'Nicotine', 'Other drugs', "None"],
        default=st.session_state['consumption_options'])
    st.session_state['sleep_time'] = st.sidebar.number_input('How many hours do you sleep on average?', min_value=1, value=st.session_state['sleep_time'])

 


    # Runs function with inputs as params
    bmi = calculate_bmi(st.session_state['weight'], st.session_state['height'])
    maintenance_calories = calculate_calories(st.session_state['age'], st.session_state['gender'], st.session_state['weight'], st.session_state['height'], st.session_state['exercise_time'])
    rounded_calories = round(maintenance_calories, 2)

    # BMI caption logic
    bmi_caption = ""
    if bmi < 18.5:
        bmi_caption = "Underweight"
    elif bmi < 24.9:
        bmi_caption = "Normal Weight"
    elif bmi < 29.9:
        bmi_caption = "Overweight"
    else:
        bmi_caption = "Obese"
    rounded_bmi = round(bmi, 2)

    data = {
        'Age': [st.session_state['age']],
        'Gender': [st.session_state['gender']],
        'Weight (kg)': [st.session_state['weight']],
        'Height (m)': [st.session_state['height']],
        'Caloric Intake': [st.session_state['calorie']],
        'Exercise Time (hours)': [st.session_state['exercise_time']],
        'Substance Consumption': [', '.join(st.session_state['consumption_options'])],
        'Sleep Time': [st.session_state['sleep_time']]
    }
  
    df = pd.DataFrame(data).T
    # overview dataframe as a table
    st.table(df)
    # turns dataframe into csv
    @st.cache_resource
    def convert_df(df):
        return df.to_csv().encode('utf-8')
    csv = convert_df(df)
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="BMI Score", value=round(bmi, 2))
        st.write("Your BMI score is classified as " + bmi_caption)
    with col2:
        st.metric(label="Amount of calories needed to maintain weight", value=rounded_calories)
    
    # sets calorie info as a dataframe
    data = {
        'Value': ['Recommended Calories', 'Your Average Calories'],
        'Calorie Consumption': [rounded_calories, st.session_state['calorie']]
    }
    df_chart = pd.DataFrame(data)
    fig = px.bar(df_chart, x='Value', y='Calorie Consumption', width=600, height=500)
    fig.update_traces(width=[0.3, 0.3])
    # plotly figure with streamlit
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig)
 


    # the following code is for the verbwire api

    url = "https://api.verbwire.com/v1/nft/store/file"

    files = {"filePath": ("health_info%20(2).csv", csv, "text/csv")}
    headers = {
        "accept": "application/json",
        "X-API-Key": "sk_live_8e60c27a-b8a9-4f7c-b8aa-3d931e558b99"
    }

    response = requests.post(url, files=files, headers=headers)
    response_json = response.json()
    # extracting the IPFS url from the api call response
    ipfs_url = response_json["ipfs_storage"]["ipfs_url"]

    with col2:
        st.subheader(f"Blockchain Storage URL (IPFS): {ipfs_url}")

if __name__ == "__main__":
    main()