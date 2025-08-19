import streamlit as st
import time

# --- Initialize Session State with default settings ---
if 'timer' not in st.session_state:
    st.session_state.timer = {
        'running': False,
        'remaining_seconds': 25 * 60,
        'total_time': 25 * 60,
        'is_work_session': True, # True for work, False for break
        'work_cycles_completed': 0,
        'settings': {
            "work_minutes": 25,
            "work_seconds": 0,
            "short_break_minutes": 5,
            "short_break_seconds": 0,
            "long_break_minutes": 15,
            "long_break_seconds": 0,
            "long_break_after": 4,
            "enable_long_break": True,
        }
    }

# --- Functions to manage timer state and settings ---
def get_total_time():
    """Calculates the total time in seconds for the current session type."""
    settings = st.session_state.timer['settings']
    if st.session_state.timer['is_work_session']:
        return settings["work_minutes"] * 60 + settings["work_seconds"]
    else:
        # Check if it's time for a long break
        if (settings["enable_long_break"] and
            st.session_state.timer['work_cycles_completed'] % settings["long_break_after"] == 0 and
            st.session_state.timer['work_cycles_completed'] > 0):
            return settings["long_break_minutes"] * 60 + settings["long_break_seconds"]
        else:
            return settings["short_break_minutes"] * 60 + settings["short_break_seconds"]

def start_timer():
    """Starts the timer countdown."""
    st.session_state.timer['running'] = True

def pause_timer():
    """Pauses the timer countdown."""
    st.session_state.timer['running'] = False

def reset_timer():
    """Resets the timer to the beginning of the current session type."""
    st.session_state.timer['running'] = False
    st.session_state.timer['is_work_session'] = True
    st.session_state.timer['work_cycles_completed'] = 0
    st.session_state.timer['total_time'] = get_total_time()
    st.session_state.timer['remaining_seconds'] = st.session_state.timer['total_time']

def handle_end_of_session():
    """Manages the logic when a session finishes."""
    if st.session_state.timer['is_work_session']:
        st.session_state.timer['work_cycles_completed'] += 1
        st.session_state.timer['is_work_session'] = False
        st.info("Work session complete! Time for a break. ☕️")
    else:
        st.session_state.timer['is_work_session'] = True
        st.success("Break is over! Get back to it. 🚀")
        
    st.session_state.timer['running'] = False
    st.session_state.timer['total_time'] = get_total_time()
    st.session_state.timer['remaining_seconds'] = st.session_state.timer['total_time']
    st.rerun()

# --- Main App Interface ---
st.title("Motivation Timer 🍅")

# Display session type and timer
session_type = "Work Session" if st.session_state.timer['is_work_session'] else "Break Time"
st.subheader(f"Current Session: {session_type}")

minutes, seconds = divmod(int(st.session_state.timer['remaining_seconds']), 60)
timer_display = f"{minutes:02d}:{seconds:02d}"
st.markdown(f"<h1 style='text-align: center;'>{timer_display}</h1>", unsafe_allow_html=True)
st.progress(st.session_state.timer['remaining_seconds'] / st.session_state.timer['total_time'])
st.caption(f"Work cycles completed: {st.session_state.timer['work_cycles_completed']}")

# Control buttons
col1, col2 = st.columns(2)
with col1:
    if st.session_state.timer['running']:
        if st.button("Pause", use_container_width=True):
            pause_timer()
    else:
        if st.button("Start", use_container_width=True):
            start_timer()
with col2:
    if st.button("Reset", use_container_width=True):
        reset_timer()

# Timer logic loop
if st.session_state.timer['running']:
    st.session_state.timer['remaining_seconds'] -= 1
    if st.session_state.timer['remaining_seconds'] <= 0:
        st.session_state.timer['remaining_seconds'] = 0
        handle_end_of_session()
    time.sleep(1)
    st.rerun()

# --- Sidebar for Settings ---
with st.sidebar:
    st.header("Settings")
    
    # Work Time Inputs
    st.subheader("Work Time")
    col1_work, col2_work = st.columns(2)
    with col1_work:
        st.session_state.timer['settings']['work_minutes'] = st.number_input("Minutes", min_value=0, value=st.session_state.timer['settings']['work_minutes'], key="work_minutes")
    with col2_work:
        st.session_state.timer['settings']['work_seconds'] = st.number_input("Seconds", min_value=0, max_value=59, value=st.session_state.timer['settings']['work_seconds'], key="work_seconds")
    
    # Short Break Inputs
    st.subheader("Short Break")
    col1_short, col2_short = st.columns(2)
    with col1_short:
        st.session_state.timer['settings']['short_break_minutes'] = st.number_input("Minutes", min_value=0, value=st.session_state.timer['settings']['short_break_minutes'], key="short_break_minutes")
    with col2_short:
        st.session_state.timer['settings']['short_break_seconds'] = st.number_input("Seconds", min_value=0, max_value=59, value=st.session_state.timer['settings']['short_break_seconds'], key="short_break_seconds")

    # Long Break Inputs
    st.subheader("Long Break")
    st.session_state.timer['settings']['enable_long_break'] = st.checkbox("Enable Long Break", value=st.session_state.timer['settings']['enable_long_break'])
    if st.session_state.timer['settings']['enable_long_break']:
        col1_long, col2_long = st.columns(2)
        with col1_long:
            st.session_state.timer['settings']['long_break_minutes'] = st.number_input("Minutes", min_value=0, value=st.session_state.timer['settings']['long_break_minutes'], key="long_break_minutes")
        with col2_long:
            st.session_state.timer['settings']['long_break_seconds'] = st.number_input("Seconds", min_value=0, max_value=59, value=st.session_state.timer['settings']['long_break_seconds'], key="long_break_seconds")
        st.session_state.timer['settings']['long_break_after'] = st.number_input("After (work cycles)", min_value=1, value=st.session_state.timer['settings']['long_break_after'], key="long_break_after")
    
    # Update button
    if st.button("Apply Settings"):
        st.session_state.timer['total_time'] = get_total_time()
        st.session_state.timer['remaining_seconds'] = st.session_state.timer['total_time']
        st.success("Settings applied! The timer is ready.")
        st.rerun()