import os
from dotenv import load_dotenv

load_dotenv()

class Settings():
    # SSL 인증서
    SSL_CERT_PATH = r"C:\cert\cacert.pem"

    # LLM
    LLM_MODEL: str = "gpt-4.1"
    TEMPERATURE: float = 0.1

    # DB
    DB_PATH: str = "agent_memory.db"

    @classmethod
    def setup_ssl(cls):
        if os.path.exists(cls.SSL_CERT_PATH):
            os.environ["SSL_CERT_FILE"] = cls.SSL_CERT_PATH
            os.environ["CURL_CA_BUNDLE"] = cls.SSL_CERT_PATH
        else:
            print(f"⚠️ 경고: 인증서 파일을 찾을 수 없습니다: {cls.SSL_CERT_PATH}")

settings = Settings()