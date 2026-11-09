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

Keep the implementation and `test_*` functions in the same file. The bottom
`if __name__ == "__main__"` block runs pytest when you execute the file directly.
Replace the hello-world function when you're ready to build the dynamic array.

Launch Neovim from this environment to use your existing Ruff and Pyright setup.
Tool settings live in `pyproject.toml`; versions are pinned in `devenv.lock`.
The `.envrc` uses the [devenv direnv integration](https://devenv.sh/integrations/direnv/).
