# ospsd-team-2
Welcome to the official repository of Team 2 for the class CS-GY 9223/CS-UY 3943 - Special Topics in Computer Science : Open Source and Professional Software Development! 

# Installation
You can install with pip (WIP): 
```shell
$ pip install [our-project]
```

## Contributing 
To start developing locally, create a fork of this repository and clone your fork with the following command replacing YOUR-USERNAME with your GitHub username:
```shell
$ git clone git@github.com:YOUR-USERNAME/ospsd-team-2
```
[Install uv](https://docs.astral.sh/uv/getting-started/installation/) if you haven't already done it before:

```shell
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex
```

You can now install the project's dependencies using:
```shell
$ cd ospsd-team-2
$ uv sync
```
To test if everything works, run the tests:
```shell
$ uv run pytest tests/
```

Create a feature branch to start developing, and open a pull-request once it's ready to be merged. One of the core team members will take a look and approve accordingly.

## Dependencies
These project relies on these excellent tools:

* `ruff` - An extremely fast Python linter and code formatter, written in Rust. 
* `ty` - An extremely fast Python type checker and language server, written in Rust.
* `mypy` - An optional, open-source static type checker for Python that boosts code quality, safety, and readability by analyzing type hints (PEP 484) without running code.
* `pytest` - An testing framework that makes it easy to write small, readable tests, and can scale to support complex functional testing for applications and libraries.

# Team 
## Core Members:
1. [Ajay Temal](mailto:at5722@nyu.edu)
2. [Aarav Agrawal](mailto:aa10698@nyu.edu)
3. [Daniel J. Barros](mailto:djb10118@nyu.edu)
4. [Hari Varsha V](mailto:hv2241@nyu.edu)
5. [Nicholas Maspons](mailto:nem8891@nyu.edu)

## TA's:
1. [Iván Aristy Eusebio](mailto:iae225@stern.nyu.edu)
2. [Adithya Balachandra](mailto:ab12095@nyu.edu)
3. [Aranya Aryaman](mailto:aa12939@nyu.edu) 

# License
This project is licensed under the **MIT License**. See the `LICENSE` file for details.
