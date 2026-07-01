import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration

RTC_CONFIGURATION = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

class DummyVideoProcessor(VideoProcessorBase):
    def recv(self, frame): return frame

def render_camera():
    st.write("### 🎥 Live Video Feed")
    webrtc_streamer(
        key="live-interview-stream",
        video_processor_factory=DummyVideoProcessor,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": True, "audio": False}
    )