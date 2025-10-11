# Contributing to memory.fm

Thanks for taking an interest in improving **memory.fm**.

This guide explains how to setup the project locally, make changes, and submit them. Even if you make a small fix like a typo, please follow the [code guidelines](#code-guidelines).



## Fork the repository

1. The project is hosted on [GitLab](https://gitlab.com/sharmasiddhant/memory.fm.git). Fork the project from there.
2. Clone the fork to your machine.
```shell
git clone https://gitlab.com/your-username/memory.fm.git
cd memory.fm
git remote add upstream https://gitlab.com/sharmasiddhant/memory.fm.git
git fetch upstream
```


## Setup the environment

### A. Using uv

1. The project uses [uv](https://docs.astral.sh/uv/) to manage dependencies. Follow the instructions on their website to install it to your system.
2.  Create a virtual environment and sync dependencies.
```shell
uv sync --all-groups --extra "dev" --extra "doc"
```

### B. Using pip

Create a virtual environment and install the project with dev and doc dependencies.
```shell
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev, doc]"
```

## Create a new branch

Always make sure to keep your local `main` branch up-to-date with the upstream.

```shell
git checkout main
git pull upstream main --ff-only
git checkout -b your-new-branch
```

## Make changes, commit and push to remote

After making changes, you can check via `git status`. Please make sure you follow the [code guidelines](#code-guidelines).

```shell
git status
```

Add or remove the files you want, depending on what you want to include in the commit.

```shell
git add <path to files you want included>
```

Verify again, and once satisfied, commit the changes with a simple descriptive commit message.

```shell
git commit -m "commit message"
```

Push your changes to remote.

```shell
git push origin your-new-branch
```

## Run Tests

Add new `pytest` tests in the `tests` directory, based on your changes and run the tests either using `uv` or directly.

```shell
uv run pytest
# Or
pytest
```

## Open a merge request

1. Make sure that your changes have followed the [code guidelines](#code-guidelines). Also ensure that the CI pipeline jobs run successfully. Once everything looks good, go over to your fork on GitLab. 
2. Create a new merge request, with `your-new-branch` as the source branch, and the upstream/original `main` as the target branch.
3. Please write a descriptive title with prefixes such as:
	- `fix` : If you fix something. Please include the issue # if you fix a bug that's open in the issues tracker.
	- `feat`: If you add some new feature or enhancement.
	- `docs`: If you update the docs.
4. Write a description of your changes in the description box and make sure to reference any open issues related to your changes.
5. Finally, create the merge request.

## Code guidelines

1. Use Ruff for linting and formatting.
2. Follow PEP 8 and make sure line lengths don't go above 88 characters
3. It is advised that you type-hint everything. See [PEP 484](https://peps.python.org/pep-0484/) for a general guideline.
4. Follow NumPy style for docstrings.
5. The documentation is to be written in **reStructuredText** in English, and built using [Sphinx](https://www.sphinx-doc.org/en/master/). The Sphinx documentation includes a [good introduction on writing **reStructuredText**.](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html). 


## Contact

If you want to report a bug, make a feature request or any suggestions, please open a [new issue](https://gitlab.com/sharmasiddhant/memory.fm/-/issues/new?type=ISSUE) using an appropriate template.

---