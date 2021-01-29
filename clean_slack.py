import argparse
from datetime import datetime, timedelta
import time
from typing import Tuple

from slack_cleaner2 import SlackCleaner, match


API_THROTTLE = 30


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser("Clean Travis-CI slack messages")
    parser.add_argument('slack_token', type=str)
    parser.add_argument('channel', type=str, default='travis-ci')
    return parser.parse_args()


def delete_messages(
    slack: SlackCleaner,
    channel: str,
    count: int
) -> Tuple[bool, int]:
    before = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')
    msgs = slack.msgs(
        filter(match('travis-ci'), slack.conversations),
        before=before
    )
    completed = True
    try:
        for msg in msgs:
            if msg.bot is True:
                msg.delete()
                count += 1
                if count % API_THROTTLE == 0:
                    print(f"  {str(count).rjust(5, ' ')}")
                    time.sleep(60)
    except:
        completed = False

    return (completed, count)


def clean_slack(token: str, channel: str) -> None:
    slack = SlackCleaner(token)
    count = 0

    while True:
        (completed, count) = delete_messages(slack, channel, count)
        if completed:
            break

    print(str(count).rjust(2 + 5 + (API_THROTTLE - count), ' '))
    print('')
    print(f'Messages Deleted: {count}')


def main() -> None:
    args = parse_args()
    channel = args.channel.lstrip('#')
    print(f"Deleting Travis-CI messages from #{channel}")
    clean_slack(args.slack_token, channel)


if __name__ == "__main__":
    main()
