# 데이터 파일이 안망가졌는지 확인하는 파일

from training.data.dummy_inquiries import DUMMY_INQUIRIES, LABEL_DESCRIPTIONS


def test_dummy_dataset_has_examples() -> None:
    assert len(DUMMY_INQUIRIES) >= 50


def test_all_labels_have_descriptions() -> None:
    labels = {item["label"] for item in DUMMY_INQUIRIES}
    assert labels == set(LABEL_DESCRIPTIONS.keys())

