import os
from openai import OpenAI
from dotenv import load_dotenv

# 파이썬의 표준 라이브러리(예: urllib, ssl)가 참조할 인증서 파일 경로를 설정합니다.
# 'r'은 Raw String으로, 역슬래시(\)를 경로 기호로 그대로 인식하게 합니다.
os.environ["SSL_CERT_FILE"] = r"C:\cert\cacert.pem"

# curl 기반의 라이브러리나 일부 하위 시스템이 참조할 인증서 묶음(Bundle) 경로를 설정합니다.
# 보안 네트워크(방화벽) 환경에서 인증서 오류를 해결하기 위해 자주 사용됩니다.
os.environ["CURL_CA_BUNDLE"] = r"C:\cert\cacert.pem"

load_dotenv()
client = OpenAI() # 환경변수 OPENAI_API_KEY를 읽음

try:
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[{"role": "user", "content": "안녕!"}]
    )
    print("연결 성공! 응답:", response.choices[0].message.content)
except Exception as e:
    print("연결 실패 사유:", e)