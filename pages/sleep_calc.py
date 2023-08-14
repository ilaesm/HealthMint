import streamlit as st
from datetime import datetime, timedelta

# function to calculate sleep times based on sleep cycles
def calculate_sleep_times(wake_up_time):
    sleep_times = []
    # feature considers 6 sleep cycles
    for i in range(1, 7):
        # 90-minute cycles + 15 minutes grace period to fall asleep
        sleep_time = wake_up_time - timedelta(minutes=i * 90 + 15)
        sleep_times.append(sleep_time.strftime("%I:%M %p")) # 12-hour clock format
    return sleep_times

def main():
    with open("logo.svg", "r") as file:
            svg_logo = file.read()
    st.markdown(svg_logo, unsafe_allow_html=True)
    st.header('Sleep Cycle Calculator')
    st.divider()

    wake_up_input = st.time_input(
        'Select the time you have to sleep up at:', value=datetime.now().time()
    )


    if wake_up_input:
        wake_up_time = datetime.combine(datetime.today(), wake_up_input)
        sleep_times = calculate_sleep_times(wake_up_time)
        
        st.subheader('The most optimal wake up time is:')
        cols = st.columns(len(sleep_times))
        for i, time in enumerate(sleep_times):
            cols[i].subheader(time)

if __name__ == '__main__':
    main()