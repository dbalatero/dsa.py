# dsa.py

Learning data structures in Python, one runnable file at a time.

Run `direnv allow` to load the tools, or use `devenv shell`.
The environment provides Python 3.12, Ruff, Pyright, pytest, and Hypothesis.

```sh
python src/01_dynamic_arrays.py  # Run the hello-world placeholder and its tests
python -m pytest                # Run tests in all src/*.py files
fmt                             # Sort imports and format
lint                            # Ruff lint checks
typecheck                       # Strict Pyright checks
check                           # Check formatting, lint, types, and tests
```
