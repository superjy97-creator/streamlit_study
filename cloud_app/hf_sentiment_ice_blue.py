import html
import textwrap
import truststore

# Windows 기관 네트워크에서의 HTTPS 인증서 문제 대응
truststore.inject_into_ssl()

import streamlit as st
import torch
from transformers.pipelines import pipeline

st.set_page_config(page_title="Sentiment Aurora | Ice Blue", page_icon="❄️", layout="centered")


def render_html(markup):
    cleaned = textwrap.dedent(markup).strip()
    cleaned = "\n".join(line.lstrip() for line in cleaned.splitlines())
    st.markdown(cleaned, unsafe_allow_html=True)


st.markdown("""
<style>
.stApp {
  background: linear-gradient(145deg,#eaf9ff 0%,#d7efff 24%,#c7e2f7 48%,#e3e9ff 73%,#f7fcff 100%);
  color: #27445e;
}
.stApp::before {
  content:""; position:fixed; inset:-15%; z-index:0; pointer-events:none;
  background: radial-gradient(ellipse 42% 35% at 16% 20%,rgba(129,205,255,.48),transparent 75%),
              radial-gradient(ellipse 40% 35% at 85% 34%,rgba(180,207,255,.55),transparent 78%),
              radial-gradient(ellipse 50% 38% at 55% 85%,rgba(255,255,255,.75),transparent 80%);
  filter:blur(35px); animation:iceGlow 20s ease-in-out infinite alternate;
}
.stApp::after {
  content:""; position:fixed; inset:0; z-index:0; pointer-events:none;
  background:radial-gradient(ellipse 65% 25% at 78% 86%,rgba(255,255,255,.40),transparent 75%),
             radial-gradient(ellipse 75% 20% at 12% 65%,rgba(117,193,246,.18),transparent 75%);
}
@keyframes iceGlow {
  0% { transform:translate(-2%,-1%) scale(1); }
  50% { transform:translate(3%,2%) scale(1.06); }
  100% { transform:translate(-1%,3%) scale(1.03); }
}
@media (prefers-reduced-motion: reduce) { .stApp::before {animation:none;} }
[data-testid="stHeader"] {background:transparent;}
.block-container {position:relative;z-index:1;max-width:850px;padding-top:2.6rem;padding-bottom:4rem;}
.hero {
  position:relative;overflow:hidden;
  background:linear-gradient(125deg,rgba(255,255,255,.88),rgba(229,247,255,.82),rgba(218,231,255,.78));
  border:1px solid rgba(255,255,255,.95);border-radius:28px;padding:42px 36px;margin-bottom:28px;
  box-shadow:0 18px 55px rgba(71,126,174,.14);backdrop-filter:blur(20px);
}
.hero::after {content:"";position:absolute;width:230px;height:230px;right:-75px;top:-95px;border-radius:50%;
  background:radial-gradient(circle,rgba(130,203,255,.42),transparent 73%);pointer-events:none;}
.eyebrow {color:#4588b8;font-weight:800;font-size:.8rem;letter-spacing:.16em;}
.hero h1 {color:#244c70!important;font-size:clamp(2rem,5vw,2.8rem);font-weight:800;margin:15px 0;line-height:1.25;}
.hero p {color:#57758d;font-size:1rem;line-height:1.9;}
.chips {display:flex;gap:9px;flex-wrap:wrap;margin-top:23px;}
.chips span {background:rgba(255,255,255,.72);color:#4584ac;border:1px solid rgba(116,185,227,.35);
  border-radius:99px;padding:7px 13px;font-size:.79rem;font-weight:600;}
.section-label {color:#285777;font-size:1.22rem;font-weight:800;margin:26px 0 10px;}
.note {color:#56788e;font-size:.94rem;margin-bottom:12px;}
.stApp label,.stApp [data-testid="stCaptionContainer"] {color:#42647b!important;}
div[data-baseweb="select"] > div {background:rgba(255,255,255,.92)!important;border:1px solid rgba(126,188,230,.45)!important;
  border-radius:14px!important;color:#315a79!important;}
[data-testid="stTextArea"] textarea {background:rgba(255,255,255,.94)!important;color:#294a65!important;
  border:1px solid rgba(124,185,226,.50)!important;border-radius:16px!important;box-shadow:0 8px 26px rgba(81,142,188,.09);}
[data-testid="stTextArea"] textarea:focus {border-color:#63b5ea!important;box-shadow:0 0 0 3px rgba(116,198,246,.22)!important;}
[data-testid="stTextArea"] textarea::placeholder {color:#8da9ba!important;}
.stButton > button[kind="primary"] {background:linear-gradient(105deg,#3d91d2,#65b9ed 52%,#8bcff2)!important;
  color:white!important;border:1px solid rgba(255,255,255,.7)!important;border-radius:15px!important;
  min-height:54px;font-size:1rem;font-weight:800;box-shadow:0 9px 24px rgba(60,143,207,.24);}
.stButton > button[kind="primary"]:hover {filter:brightness(1.07);}
.result-card {background:linear-gradient(130deg,rgba(255,255,255,.97),var(--result-background));
  border:1px solid var(--result-border);border-radius:23px;padding:30px;box-shadow:0 15px 45px rgba(80,132,176,.13);}
.result-kicker {color:#6b879c;font-size:.88rem;}
.result-name {color:var(--result-color);font-size:1.65rem;font-weight:800;margin:12px 0 8px;}
.result-number {color:#294a66;font-size:3rem;font-weight:800;line-height:1.3;}
.result-desc {color:#55758c;font-size:.93rem;margin-top:16px;}
.meter {height:13px;background:rgba(132,181,219,.20);border-radius:99px;overflow:hidden;margin-top:22px;}
.meter > div {width:var(--score);height:100%;border-radius:99px;background:linear-gradient(90deg,#8fc8eb,var(--result-color));}
.custom-footer {text-align:center;color:#64859b;font-size:.83rem;margin-top:30px;}
[data-testid="stExpander"],[data-testid="stAlert"] {border-radius:14px;}
#MainMenu {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

render_html("""
<div class="hero">
  <div class="eyebrow">✦ SENTIMENT AURORA · ICE BLUE</div>
  <h1>❄️ 한국어 감정 분석 AI</h1>
  <p>문장에 담긴 감정을 맑고 섬세하게 읽어보세요.<br>
  Hugging Face BERT 기반의 한국어 긍정·부정 감정 분석 서비스입니다.</p>
  <div class="chips"><span>Hugging Face</span><span>Korean BERT</span><span>Streamlit</span></div>
</div>
""")


@st.cache_resource(show_spinner=False)
def load_model():
    device = 0 if torch.cuda.is_available() else -1
    return pipeline("text-classification", model="WhitePeak/bert-base-cased-Korean-sentiment", device=device)


examples = {
    "직접 입력": "",
    "☀️ 긍정 예시": "오늘 날씨, 쌀쌀하긴 하지만 맑아서 정말 좋다!!",
    "🌧️ 부정 예시": "기대했는데 결과가 너무 실망스러워요.",
    "🌤️ 복합 표현 예시": "조금 피곤하지만 오늘 하루는 꽤 만족스러웠어요.",
}

if "sentiment_text" not in st.session_state:
    st.session_state.sentiment_text = ""
if "sentiment_result" not in st.session_state:
    st.session_state.sentiment_result = None


def fill_example():
    selected = st.session_state.example_choice
    if selected != "직접 입력":
        st.session_state.sentiment_text = examples[selected]
        st.session_state.sentiment_result = None


render_html("""
<div class="section-label">✍️ 문장 분석하기</div>
<div class="note">한국어 문장을 입력하거나 예시 문장을 선택해 감정을 분석해 보세요.</div>
""")

st.selectbox("예시 문장 선택", options=list(examples), key="example_choice", on_change=fill_example)
user_text = st.text_area(
    "분석할 한국어 문장", key="sentiment_text", height=145, max_chars=500,
    placeholder="오늘 하루의 기분을 한 문장으로 적어보세요..."
)
st.caption(f"입력 글자 수: {len(user_text)} / 500")

if st.button("❄️ 감정 분석 시작", type="primary", use_container_width=True):
    if not user_text.strip():
        st.warning("분석할 문장을 먼저 입력해 주세요.")
    else:
        try:
            with st.spinner("AI가 문장에 담긴 감정을 분석하고 있습니다..."):
                classifier = load_model()
                result = classifier(user_text, truncation=True, max_length=512)
            st.session_state.sentiment_result = {"text": user_text, "output": result}
        except Exception as error:
            st.session_state.sentiment_result = None
            st.error("모델 실행에 실패했습니다. 터미널 로그를 확인해 주세요.")
            with st.expander("오류 상세 정보"):
                st.code(str(error))

saved = st.session_state.sentiment_result
if saved is not None:
    output = saved["output"]
    label = output[0]["label"]
    score = float(output[0]["score"])

    if label == "LABEL_1":
        emotion, emoji = "긍정적인 문장", "😊"
        accent, border, background = "#299F91", "rgba(41,159,145,.32)", "rgba(218,249,239,.85)"
        description = "문장에서 긍정적인 감정이 감지되었습니다."
    elif label == "LABEL_0":
        emotion, emoji = "부정적인 문장", "😔"
        accent, border, background = "#7D79B8", "rgba(125,121,184,.35)", "rgba(235,233,255,.85)"
        description = "문장에서 부정적인 감정이 감지되었습니다."
    else:
        emotion, emoji = "기타 분류", "🔎"
        accent, border, background = "#438CB5", "rgba(67,140,181,.35)", "rgba(226,242,255,.85)"
        description = f"모델 분류: {label}"

    render_html('<div class="section-label">📊 감정 분석 결과</div>')
    render_html(f"""
    <div class="result-card" style="--result-color:{accent};--result-border:{border};
    --result-background:{background};--score:{score * 100:.2f}%;">
      <div class="result-kicker">AI가 분석한 감정</div>
      <div class="result-name">{emoji} {html.escape(emotion)}</div>
      <div class="result-number">{score:.2%}</div>
      <div class="result-kicker">선택된 분류의 모델 점수</div>
      <div class="meter"><div></div></div>
      <div class="result-desc">{html.escape(description)}</div>
    </div>
    """)
    st.caption("※ 이 점수는 해당 문장에 대한 모델의 분류 점수이며, 모델 전체 정확도를 의미하지 않습니다.")
    st.markdown("**분석한 문장**")
    st.info(saved["text"])
    with st.expander("🔍 상세 분석 데이터 확인"):
        st.json(output)

render_html("""
<div class="custom-footer">
  SENTIMENT AURORA · ICE BLUE EDITION<br>
  Powered by Hugging Face × Streamlit
</div>
""")
