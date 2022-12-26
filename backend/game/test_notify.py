from unittest import mock

import pytest
from click.testing import CliRunner

from game.management.commands.notify import handler
from game.models import AppUser
from game.notifications_utils import NotificationsUtils


def run(message="", fragment=""):
    runner = CliRunner()
    if fragment:
        result = runner.invoke(handler, ["--fragment", fragment, message])
    else:
        result = runner.invoke(handler, [message])
    if result.exit_code:
        print(result.output)
        print(result.exception)
        assert False
    return result.output


@pytest.fixture(autouse=True)
def mock_vk_send_notifications():
    mock_send_notification = mock.patch(
        "game.notifications_utils.NotificationsUtils.send_notification"
    )
    mock_send_notification.start()
    mock_send_notification.return_value = []
    yield mock_send_notification
    mock_send_notification.stop()


def test_when_no_users():
    AppUser.objects.all().delete()
    output = run()
    assert "No users with enabled notifications" in output


def test_when_no_users_with_notifications():
    AppUser.objects.create(
        vk_id=2, username="2", notifications_status=AppUser.BLOCK
    )
    AppUser.objects.create(
        vk_id=3, username="3", notifications_status=AppUser.TO_BE_REQUESTED
    )
    output = run()
    assert "No users with enabled notifications" in output


def test_send_successful_notifications(mock_vk_send_notifications):
    AppUser.objects.create(
        vk_id=2, username="2", notifications_status=AppUser.ALLOW
    )
    AppUser.objects.create(
        vk_id=3, username="3", notifications_status=AppUser.ALLOW
    )
    NotificationsUtils.send_notification.return_value = [
        {
            "user_id": 2,
            "status": True,
        },
        {
            "user_id": 3,
            "status": True,
        },
    ]
    output = run("test")
    assert NotificationsUtils.send_notification.called_once_with(
        [2, 3], "test", ""
    )
    assert "Found 2 users with enabled notifications" in output
    assert "Successfully sent 2 notifications" in output


def test_send_failed_notification():
    AppUser.objects.create(
        vk_id=2, username="2", notifications_status=AppUser.ALLOW
    )
    AppUser.objects.create(
        vk_id=3, username="3", notifications_status=AppUser.ALLOW
    )
    NotificationsUtils.send_notification.return_value = [
        {
            "user_id": 2,
            "status": False,
            "error": {
                "code": 1,
            },
        },
        {
            "user_id": 3,
            "status": False,
        },
    ]
    output = run("test", "fragment")
    assert NotificationsUtils.send_notification.called_once_with(
        [2, 3], "test", "fragment"
    )
    assert "Found 2 users with enabled notifications" in output
    assert "Failed to send 2 notifications" in output
    assert "Changed notification status of 1 users to block" in output
    assert AppUser.users.filter(
        vk_id=2, notifications_status=AppUser.BLOCK
    ).exists()


def test_send_both_failed_and_successful_notifications():
    AppUser.objects.create(
        vk_id=2, username="2", notifications_status=AppUser.ALLOW
    )
    AppUser.objects.create(
        vk_id=3, username="3", notifications_status=AppUser.ALLOW
    )
    NotificationsUtils.send_notification.return_value = [
        {
            "user_id": 2,
            "status": False,
            "error": {
                "code": 1,
            },
        },
        {
            "user_id": 3,
            "status": True,
        },
    ]
    output = run()
    assert "Found 2 users with enabled notifications" in output
    assert "Successfully sent 1 notifications" in output
    assert "Failed to send 1 notifications" in output
    assert "Changed notification status of 1 users to block" in output
    assert AppUser.users.filter(
        vk_id=2, notifications_status=AppUser.BLOCK
    ).exists()


# Happens when send invalid value in user_ids to vk api
def test_raises_when_number_of_results_does_not_match_number_of_input_ids():
    AppUser.objects.create(
        vk_id=2, username="2", notifications_status=AppUser.ALLOW
    )
    AppUser.objects.create(
        vk_id=3, username="3", notifications_status=AppUser.ALLOW
    )
    NotificationsUtils.send_notification.return_value = [
        {
            "user_id": 2,
            "status": False,
            "error": {
                "code": 1,
            },
        },
    ]
    runner = CliRunner()
    result = runner.invoke(handler, ["test message"])
    assert (
        "number of results (1) does not match number of input ids (2)"
        in str(result.exception)
    )
    assert "Successfully sent" not in result.output
    assert "Failed to send" not in result.output
    assert result.exit_code == 1
