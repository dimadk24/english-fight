import re
from typing import Tuple

import pytest
from django.conf import settings
from rest_framework.test import APIClient

from data.pictures import PicturesTopic, PICTURES
from game.models import AppUser, Question


def authenticate(api_client):
    user = AppUser.objects.create(vk_id=1, username="1")
    api_client.force_authenticate(user)


def get_correct_answer_data_for_picture_question(
    question: Question,
) -> Tuple[PicturesTopic, Tuple[str, str]]:
    answer_path = question.question
    regex = (
        settings.STATIC_URL + r"picture-questions/(\d+)-([a-z\-]+)/(\d+)\..*"
    )
    match = re.match(regex, answer_path)
    assert match
    topic_number = int(match.group(1))
    topic_name = match.group(2).replace("-", " ")
    picture_number = int(match.group(3))
    found_topic: PicturesTopic = PICTURES[topic_number - 1]
    assert found_topic.name == topic_name
    found_item = found_topic.items[picture_number - 1]
    return found_topic, found_item


@pytest.fixture
def api_client():
    client = APIClient()
    authenticate(client)
    yield client


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
