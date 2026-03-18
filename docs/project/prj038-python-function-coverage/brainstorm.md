# Python Function Coverage Test Brainstorm

## Motivation

- Current test coverage reports show large amounts of untested code in `src/`.
- Motivation is not to prove correctness, but to catch runtime issues such as missing imports, invalid defaults, or other immediate exceptions.
- Similar approach already exists for `rust_core` with `tests/test_rust_core.py`.

## Approach

- Create a test that walks `src/` and dynamically imports modules.
- For each function definition (excluding test helpers and private helpers), attempt to call it with default/dummy args.
- Record failures; if *all* calls fail, the test should fail (simple safety net).

## Considerations

- Limit the number of attempted calls to avoid long CI times.
- Exclude known problematic modules (e.g., ones that rely on external services or heavy setup).
- Ensure the test is safe and does not modify state.

## Next steps

- Tune heuristics for argument generation.
- Add a `--quick` mode or marker to skip this in quick runs.
