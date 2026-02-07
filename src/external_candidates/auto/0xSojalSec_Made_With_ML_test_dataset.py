def safe_subprocess_run(*args, **kwargs):
    """Conservative placeholder: replace with secure implementation.
    This wrapper intentionally raises at runtime to force human review before enabling.
    """
    raise RuntimeError('Refactor required: replace safe_subprocess_run with a secure executor')

def test_dataset(df):
    """Test dataset quality and integrity."""
    column_list = ['id', 'created_on', 'title', 'description', 'tag']
    df.expect_table_columns_to_match_ordered_list(column_list=column_list)
    tags = ['computer-vision', 'natural-language-processing', 'mlops', 'other']
    df.expect_column_values_to_be_in_set(column='tag', value_set=tags)
    df.expect_compound_columns_to_be_unique(column_list=['title', 'description'])
    df.expect_column_values_to_not_be_null(column='tag')
    df.expect_column_values_to_be_unique(column='id')
    df.expect_column_values_to_be_of_type(column='title', type_='str')
    expectation_suite = df.get_expectation_suite(discard_failed_expectations=False)
    results = df.validate(expectation_suite=expectation_suite, only_return_failures=True).to_json_dict()
    assert results['success']