# ❄️ Sentiment Aurora – Ice Blue Edition

Hugging Face의 한국어 BERT 감정 분석 모델을 활용하여 개발한 **Streamlit 기반 한국어 감정 분석 웹 애플리케이션**입니다.

사용자가 한국어 문장을 입력하면 AI 모델이 문장의 감정을 긍정 또는 부정으로 분류하고, 예측 점수를 시각적으로 표시합니다.

## 🌐 배포 주소

**[한국어 감정 분석 AI 실행하기](https://korean-sentiment-aurora.streamlit.app)**

## 🛠️ 사용 기술

- **Python 3.11**
- **Streamlit 1.66.1** — 웹 인터페이스
- **Hugging Face Transformers 4.57.6** — AI 모델 실행
- **PyTorch 2.6.0** — 딥러닝 모델 추론
- **모델:** `WhitePeak/bert-base-cased-Korean-sentiment`
- **배포:** Streamlit Community Cloud
- **버전 관리:** Git 및 GitHub

## ✨ 주요 기능

- 한국어 문장 입력 및 감정 분석
- 긍정·부정 감정 분류
- 예측 신뢰 점수(%) 표시
- 긍정·부정·복합 표현 예시 문장 제공
- Ice Blue 테마 기반 사용자 인터페이스
- GPU 및 CPU 환경 자동 선택

## 📂 프로젝트 구조

```text
streamlit_study/
├── .gitignore
└── cloud_app/
    ├── hf_sentiment_ice_blue.py
    └── requirements.txt
```

## 🚀 로컬 실행 방법

Python 3.11 환경에서 다음 명령어를 실행합니다.

```bash
pip install -r cloud_app/requirements.txt
python -m streamlit run cloud_app/hf_sentiment_ice_blue.py
```

최초 실행 시 Hugging Face에서 모델 가중치를 다운로드하므로 인터넷 연결이 필요합니다.

## 🧪 테스트

긍정·부정·복합 감정 표현을 입력하여 분류 결과를 확인했습니다.

Streamlit Community Cloud에 공개 배포하고, 웹 애플리케이션의 감정 분석 기능이 정상 작동하는 것을 확인했습니다.

## 📌 참고 사항

- 본 프로젝트는 사전 학습된 Hugging Face 모델을 활용한 추론 애플리케이션입니다.
- 표시되는 예측 점수는 모델의 개별 입력에 대한 신뢰 점수이며, 모델의 전체 정확도를 의미하지 않습니다.
- 무료 클라우드 배포 환경에서는 CPU로 모델을 실행할 수 있습니다.