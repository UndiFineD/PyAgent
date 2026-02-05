def validate_dataset(df):
    required = ["id", "created_on", "title", "description", "tag"]
    cols = getattr(df, 'columns', None)
    if cols is not None:
        for c in required:
            if c not in cols:
                raise AssertionError(f"Missing column: {c}")
    return True
