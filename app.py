import streamlit as st
import base64
from core.ai_engine import get_next_question, get_final_analytics
from core.voice_engine import listen_to_user, generate_audio_base64
from ui.components import render_camera
from ui.dashboard import render_scorecard

st.set_page_config(page_title="AI Pro Interviewer", page_icon="🤖", layout="wide")

# App State Configurations
if "stage" not in st.session_state: st.session_state.stage = "SETUP"
if "history" not in st.session_state: st.session_state.history = []
if "curr_q" not in st.session_state: st.session_state.curr_q = ""
if "q_num" not in st.session_state: st.session_state.q_num = 1
if "play_trigger" not in st.session_state: st.session_state.play_trigger = False
if "temp_user_response" not in st.session_state: st.session_state.temp_user_response = ""

MAX_QUESTIONS = 4

# --- STEP 1: INITIAL PROFILE SCREEN ---
if st.session_state.stage == "SETUP":
    st.title("🚀 Enterprise AI Technical Interviewer")
    st.markdown("Configure your target workspace settings below to deploy the adaptive grading agent.")
    
    role = st.text_input("Target Job Position / Profile Title:", placeholder="e.g., Cloud DevOps Engineer / Senior Backend Developer")
    
    if st.button("Initiate Interview Session", type="primary"):
        if role:
            st.session_state.role = role
            with st.spinner("Generating opening round constraints..."):
                st.session_state.curr_q = get_next_question(role, [])
            st.session_state.history.append({"role": "interviewer", "content": st.session_state.curr_q})
            st.session_state.play_trigger = True  
            st.session_state.stage = "LIVE"
            st.rerun()
        else:
            st.warning("Please provide a valid corporate profile context.")

# --- STEP 2: ACTIVE LIVE EVALUATION TRACK ---
elif st.session_state.stage == "LIVE":
    st.title(f"💼 Active Session Panel: {st.session_state.role}")
    st.progress(st.session_state.q_num / MAX_QUESTIONS, text=f"Progress Tracking: Metric Node {st.session_state.q_num} of {MAX_QUESTIONS}")
    
   # Audio Generation Loop Handler (Updated with native st.html)
    if st.session_state.play_trigger:
        audio_b64 = generate_audio_base64(st.session_state.curr_q)
        if audio_b64:
            # Clean HTML5 wrapper for autoplay audio
            audio_tag = f'<audio autoplay src="data:audio/mp3;base64,{audio_b64}">'
            
            # FIX: Using st.html to safely inject raw HTML without iframe keyword errors
            st.html(audio_tag)
            
        st.session_state.play_trigger = False  # Lock down loop to prevent unintended automatic replays

    left_layout, right_layout = st.columns(2)
    
    with left_layout:
        st.write("### 🎥 Live Video Feed")
        # CRITICAL CHANGE: Storing the webrtc context state to monitor camera hardware activity
        from streamlit_webrtc import webrtc_streamer, RTCConfiguration
        from ui.components import DummyVideoProcessor
        
        RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        
        # rendering the streamer object directly to capture context pipelines
        ctx = webrtc_streamer(
            key="live-interview-stream",
            video_processor_factory=DummyVideoProcessor,
            rtc_configuration=RTC_CONFIGURATION,
            media_stream_constraints={"video": True, "audio": False}
        )
        
    with right_layout:
        st.info(f"**🤖 AI Interviewer Prompt:** {st.session_state.curr_q}")
        
        # Audio Control Interface
        col_repeat, col_spacer = st.columns([1, 2])
        with col_repeat:
            if st.button("🔁 Repeat Question", use_container_width=True):
                st.session_state.play_trigger = True
                st.rerun()
                
        st.write("---")
        st.write("### 🎙️ Voice Capture Workspace")
        
        # Validation Logic: Checking if camera media track stream is functional
        is_camera_active = ctx is not None and ctx.state.playing
        
        if not is_camera_active:
            st.error("⚠️ CAMERA BLOCKED: You must click the 'START' button on the camera stream to activate your video feed before speaking.")
            
        col_action, _ = st.columns([1, 1])
        with col_action:
            # Button disabled state dynamically toggles based on WebRTC stream parameters
            if st.button("🎙️ Capture Voice Answer", type="secondary", use_container_width=True, disabled=not is_camera_active):
                with st.spinner("Mic open. Delivering voice data package..."):
                    captured_string = listen_to_user()
                    if "ERROR" in captured_string:
                        st.error(captured_string)
                    else:
                        st.session_state.temp_user_response = captured_string
                        
        # Review & Submission Panel
        if st.session_state.temp_user_response:
            st.markdown("#### 📝 Automated Transcript Verification")
            edited_string = st.text_area("Review or edit transcribed response content manually:", value=st.session_state.temp_user_response, height=120)
            st.session_state.temp_user_response = edited_string
            
            if st.button("💾 Confirm & Submit Final Response", type="primary"):
                st.session_state.history.append({"role": "candidate", "content": st.session_state.temp_user_response})
                st.session_state.temp_user_response = ""  
                
                if st.session_state.q_num >= MAX_QUESTIONS:
                    st.session_state.stage = "ANALYTICS"
                else:
                    st.session_state.q_num += 1
                    with st.spinner("Processing performance telemetry & generating follow-up..."):
                        st.session_state.curr_q = get_next_question(st.session_state.role, st.session_state.history)
                        st.session_state.history.append({"role": "interviewer", "content": st.session_state.curr_q})
                        st.session_state.play_trigger = True  
                st.rerun()

# --- STEP 3: ANALYTICS MATRIX REPORT ---
elif st.session_state.stage == "ANALYTICS":
    with st.spinner("Compiling cross-layer performance matrix charts..."):
        report = get_final_analytics(st.session_state.role, st.session_state.history)
    render_scorecard(report)
    
    if st.button("🔄 Initiate New Evaluation Lifecycle"):
        st.session_state.clear()
        st.rerun()