import djclick as click

from game.models import AppUser
from game.notifications_utils import NotificationsUtils


@click.command(
    help="Send notification to all users with allowed notifications"
)
@click.argument("message")
@click.option(
    "--fragment", help="relative hash url to be opened by click", default=""
)
def handler(message, fragment):
    click.secho(f"Message: {message}")
    if fragment:
        click.secho(f"Fragment: {fragment}")
    user_ids = AppUser.users.filter(
        notifications_status=AppUser.ALLOW
    ).values_list("vk_id", flat=True)
    if not len(user_ids):
        click.secho("No users with enabled notifications")
        return
    total_users = len(user_ids)
    click.secho(f"Found {total_users} users with enabled notifications")
    response = NotificationsUtils.send_notification(
        user_ids, message, fragment
    )
    if not len(response) == total_users:
        raise Exception(
            f"number of results ({len(response)}) "
            f"does not match number of input ids ({total_users})"
        )
    successful_number = sum(1 for item in response if item["status"])
    failed_number = total_users - successful_number
    if successful_number:
        click.secho(f"Successfully sent {successful_number} notifications")
    if failed_number:
        click.secho(f"Failed to send {failed_number} notifications:", fg="red")
        updated_users = 0
        for item in response:
            if not item["status"]:
                click.secho(str(item))
                if item.get("error") and item["error"]["code"] in [1, 4]:
                    AppUser.users.filter(vk_id=item["user_id"],).update(
                        notifications_status=AppUser.BLOCK,
                    )
                    updated_users += 1
        click.secho(
            f"Changed notification status of {updated_users} users to block"
        )
    click.secho("OK")
