import streamlit as st
import base64
from core.ai_engine import get_next_question, get_final_analytics
from core.voice_engine import listen_to_user, generate_audio_base64
from ui.components import render_camera, DummyVideoProcessor # <- यहाँ इम्पोर्ट कर लिया
from ui.dashboard import render_scorecard
from streamlit_webrtc import webrtc_streamer, RTCConfiguration # <- इम्पोर्ट यहाँ शिफ्ट कर दिया

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
    
    # Layout configuration
    left_layout, right_layout = st.columns(2)
    
    with left_layout:
        st.write("### 🎥 Live Video Feed")
        
        RTC_CONFIGURATION = RTCConfiguration({
            "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
        })

        # WebRTC Streamer ko hum pehle render kar rahe hain
        ctx = webrtc_streamer(
            key="live-interview-stream",
            video_processor_factory=DummyVideoProcessor,
            rtc_configuration=RTC_CONFIGURATION,
            media_stream_constraints={"video": True, "audio": False}
        )
        
    # Check karo ki camera sach me chal raha hai ya nahi
    is_camera_active = ctx is not None and ctx.state.playing

    # 🚨 SAFE AUDIO LAYER: Audio tabhi chalega jab camera active ho aur trigger True ho
    if is_camera_active and st.session_state.play_trigger:
        audio_b64 = generate_audio_base64(st.session_state.curr_q)
        if audio_b64:
            audio_tag = f"""
            <audio autoplay id="interview-player" style="display:none;">
                <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
            </audio>
            """
            st.html(audio_tag)
        st.session_state.play_trigger = False # Play hone ke baad trigger off

    with right_layout:
        st.info(f"**🤖 AI Interviewer Prompt:** {st.session_state.curr_q}")
        
        col_repeat, _ = st.columns([1, 2])
        with col_repeat:
            if st.button("🔁 Repeat Question", use_container_width=True):
                st.session_state.play_trigger = True
                st.rerun()

    st.write("---")
    st.write("### 🎙️ Voice Capture Workspace")

    if not is_camera_active:
        st.error("⚠️ CAMERA BLOCKED: Click START on the camera first to load the question audio.")
    else:
        st.info("🎤 Record your answer below.")
        captured_string = listen_to_user()

        if captured_string:
            if captured_string.startswith("ERROR"):
                st.error(captured_string)
            else:
                st.success("✅ Voice Captured Successfully")
                st.session_state.temp_user_response = captured_string

    if st.session_state.temp_user_response:
        st.markdown("#### 📝 Automated Transcript Verification")

        edited_string = st.text_area(
            "Review or edit transcribed response manually:",
            value=st.session_state.temp_user_response,
            height=120
        )
        st.session_state.temp_user_response = edited_string

        if st.button("💾 Confirm & Submit Final Response", type="primary"):
            st.session_state.history.append({
                "role": "candidate",
                "content": st.session_state.temp_user_response
            })
            st.session_state.temp_user_response = ""

            if st.session_state.q_num >= MAX_QUESTIONS:
                st.session_state.stage = "ANALYTICS"
            else:
                st.session_state.q_num += 1
                with st.spinner("Generating next question..."):
                    st.session_state.curr_q = get_next_question(
                        st.session_state.role,
                        st.session_state.history
                    )
                    st.session_state.history.append({
                        "role": "interviewer",
                        "content": st.session_state.curr_q
                    })
                    st.session_state.play_trigger = True

            st.rerun()

# --- STEP 3: FINAL EVALUATION DASHBOARD WITH GRAPHS ---
elif st.session_state.stage == "ANALYTICS":
    st.title("📊 Interview Performance Analytics")
    st.subheader(f"Evaluation Summary for: {st.session_state.role}")
    st.write("---")

    with st.spinner("Generating automated technical evaluation report and charts..."):
        # Groq/AI se final report fetch karega
        report_text = get_final_analytics(st.session_state.role, st.session_state.history)

    # --- SCORE PARSING LOGIC FOR GRAPH ---
    tech_score = 0
    comm_score = 0
    conf_score = 0

    try:
        # Report text me se scores extract karne ke liye helper loop
        for line in report_text.split("\n"):
            if "Technical Score:" in line:
                tech_score = int(line.split(":")[1].split("/")[0].strip())
            elif "Communication Score:" in line:
                comm_score = int(line.split(":")[1].split("/")[0].strip())
            elif "Confidence Score:" in line:
                conf_score = int(line.split(":")[1].split("/")[0].strip())
    except Exception:
        # Fallback values agar parse na ho paye
        tech_score, comm_score, conf_score = 50, 50, 50

    # Layout for Metrics and Charts
    col_metrics, col_chart = st.columns([1, 2])

    with col_metrics:
        st.markdown("### 🎯 Performance Metrics")
        st.metric(label="💻 Technical Score", value=f"{tech_score} / 100")
        st.metric(label="🗣️ Communication Score", value=f"{comm_score} / 100")
        st.metric(label="⚡ Confidence Score", value=f"{conf_score} / 100")

    with col_chart:
        st.markdown("### 📈 Skill Performance Visualizer")
        
        # Streamlit Bar Chart data prepration
        chart_data = {
            "Metric": ["Technical", "Communication", "Confidence"],
            "Score": [tech_score, comm_score, conf_score]
        }
        
        # Render a beautiful native horizontal bar chart
        st.bar_chart(data=chart_data, x="Metric", y="Score", use_container_width=True)

    st.write("---")

    # Detailed text area for Strengths, Weaknesses and Suggestions
    st.markdown("### 📋 AI Interviewer Detailed Feedback")
    st.text_area("Detailed Matrix (Strengths & Weaknesses)", value=report_text, height=350, disabled=True)

    st.write("---")
    
    # Reset Button
    if st.button("🔄 Start New Interview Session", type="primary"):
        st.session_state.stage = "SETUP"
        st.session_state.history = []
        st.session_state.curr_q = ""
        st.session_state.q_num = 1
        st.session_state.play_trigger = False
        st.session_state.temp_user_response = ""
        st.rerun()