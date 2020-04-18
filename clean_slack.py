import argparse
from datetime import datetime, timedelta

from slack_cleaner2 import SlackCleaner, match


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser("Clean Travis-CI slack messages")
    parser.add_argument('slack_token', type=str)
    return parser.parse_args()


def clean_slack(token: str, max_count: int = 30) -> None:
    slack = SlackCleaner(token)
    count = 0
    before = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')
    msgs = slack.msgs(
        filter(match('travis-ci'), slack.conversations),
        before=before
    )
    for msg in msgs:
        if msg.bot is True:
            msg.delete()
            count += 1
            if count == max_count:
                return


def main() -> None:
    args = parse_args()
    clean_slack(args.slack_token)


if __name__ == "__main__":
    main()
