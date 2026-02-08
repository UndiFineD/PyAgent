# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\scripts\migrate_descriptor_key.py
import argparse

from ovo import db
from sqlalchemy import text

# Usage:
#   python scripts/migrate_descriptor_key.py "old_key" "new_key"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Rename descriptor from one key to another",
    )
    parser.add_argument("old_key", help="old key")
    parser.add_argument("new_key", help="new key")
    args = parser.parse_args()
    old_key = args.old_key
    new_key = args.new_key

    session = db._create_session()
    result = session.execute(
        text("UPDATE descriptor_value SET descriptor_key = :new_key WHERE descriptor_key = :old_key"),
        dict(old_key=old_key, new_key=new_key),
    )
    session.commit()
    # num updated
    print(f"Updated {result.rowcount} rows in descriptor_value table")

    num_jobs = 0
    for job in db.DesignJob.select():
        if job.workflow and job.workflow.acceptance_thresholds and old_key in job.workflow.acceptance_thresholds:
            threshold = job.workflow.acceptance_thresholds.pop(old_key)
            job.workflow.acceptance_thresholds[new_key] = threshold
            db.DesignJob.save_value("workflow", job.workflow, id=job.id)
            num_jobs += 1

    print(f"Updated {num_jobs} workflow acceptance thresholds in design_job table")
