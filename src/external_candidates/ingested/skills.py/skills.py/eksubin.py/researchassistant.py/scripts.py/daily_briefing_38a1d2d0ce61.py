# Extracted from: C:\DEV\PyAgent\.external\skills\skills\eksubin\researchassistant\scripts\daily_briefing.py
import argparse
import json
import os
from datetime import datetime

CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "research_config.json"
)


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {"topics": [], "last_checked": "1970-01-01"}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)


def add_topic(topic):
    config = load_config()
    if topic not in config["topics"]:
        config["topics"].append(topic)
        save_config(config)
        print(f"Topic '{topic}' added.")
    else:
        print(f"Topic '{topic}' already exists.")


def list_topics():
    config = load_config()
    print("Current Research Topics:")
    for t in config["topics"]:
        print(f"- {t}")


def update_last_checked():
    config = load_config()
    config["last_checked"] = datetime.now().strftime("%Y-%m-%d")
    save_config(config)
    print(f"Last checked date updated to {config['last_checked']}.")


def main():
    parser = argparse.ArgumentParser(
        description="Manage Research Monitor configuration."
    )
    parser.add_argument("--add-topic", type=str, help="Add a new research topic.")
    parser.add_argument(
        "--list-topics", action="store_true", help="List all research topics."
    )
    parser.add_argument(
        "--update-date", action="store_true", help="Update last checked date to today."
    )

    args = parser.parse_args()

    if args.add_topic:
        add_topic(args.add_topic)
    elif args.list_topics:
        list_topics()
    elif args.update_date:
        update_last_checked()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
