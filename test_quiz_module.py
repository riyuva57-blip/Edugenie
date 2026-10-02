from quiz_module import _normalize_question


def test_normalize_index_answer():
    item = {
        "question": "2 + 2 = ?",
        "options": ["3", "4", "5", "6"],
        "correct_answer": "B",
    }
    result = _normalize_question(item)
    assert result["correct_answer"] == "4"
