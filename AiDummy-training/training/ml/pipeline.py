from sklearn.feature_extraction.text import TfidfVectorizer  # 문장을 숫자로 바꾸는 도구
from sklearn.linear_model import LogisticRegression   # 분류 모델
from sklearn.pipeline import Pipeline  # 여러 단계를 한줄 흐름에 묶는 도구

# 텍스트 분류용 파이프라인을 만들어서 반환하는 함수
def build_text_classification_pipeline() -> Pipeline:  # TfidfVectorizer() 랑 LogisticRegression()를 하나의 객체처럼 쓸수 있게 만듬
    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(     # 문장을 숫자 벡터로 바꿈 (보정 옵션)
                    ngram_range=(1, 2),   # 단어 1개짜리도 보고 2개짜리 묶음도 보겠다 ex) 배송 완료
                    min_df=1,      # 한번만 나온 단어라도 버리지 않고 쓰겠다
                    sublinear_tf=True,    # 단어가 너무 많이 반복된다고 해서 그 횟수를 그대로 세게 반영하지 않도록 완화하는 옵션
                ),
            ),
            (
                "classifier",
                LogisticRegression(   # 실제 분류 모델
                    max_iter=1000,   # 학습을 반복하는 최대 횟수
                    random_state=42,   # 랜덤 요소를 고정해서 매번 결과가 들쭉날쭉하지 않게 함
                ),
            ),
        ]
    )

