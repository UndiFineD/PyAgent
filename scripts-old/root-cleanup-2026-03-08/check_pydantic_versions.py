"""test Pydantic versions to ensure we are running with the expected versions in our tests."""
import pydantic
import pydantic_core

print('pydantic', pydantic.__version__)
print('pydantic_core', pydantic_core.__version__)
