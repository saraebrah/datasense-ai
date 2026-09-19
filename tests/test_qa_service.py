import pytest

from app.qa_service import (
    build_qa_prompt,
    validate_question,
)

def test_valid_question():
    result = validate_question(
        "Which event type is most common?"
    )

    assert result == (
        "Which event type is most common?"
    )


def test_question_whitespace_is_removed():
    result = validate_question(
        "   How many users are there?   "
    )

    assert result == (
        "How many users are there?"
    )


def test_empty_question_raises_error():

    with pytest.raises(
        ValueError,
        match="cannot be empty",
    ):

        validate_question("   ")



def test_long_question_raises_error():

    question = "a" * 301

    with pytest.raises(
        ValueError,
        match="too long",
    ):

        validate_question(question)


def test_qa_prompt_contains_context_and_question():

    context = {
        "total_events": 10,
        "unique_users": 3,
    }

    question = (
        "How many users are there?"
    )

    prompt = build_qa_prompt(
        context,
        question,
    )

    assert "10" in prompt
    assert "3" in prompt
    assert question in prompt

    assert (
        "Do not invent numbers or facts"
        in prompt
    )

    