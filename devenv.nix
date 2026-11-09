{ pkgs, ... }:
{
  languages.python = {
    enable = true;
    package = pkgs.python312.withPackages (ps: [
      ps.pytest
      ps.hypothesis
    ]);
  };

  packages = [
    pkgs.ruff
    pkgs.pyright
  ];

  scripts = {
    fmt.exec = ''
      set -e
      ruff check --select I --fix .
      ruff format .
    '';
    lint.exec = "ruff check .";
    typecheck.exec = "pyright";
    check.exec = ''
      set -e
      ruff format --check .
      ruff check .
      pyright
      python -m pytest
    '';
  };

  enterTest = "check";
}
