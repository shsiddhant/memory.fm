# Contributing to memory.fm

Thanks for your interest in contributing to **memory.fm**.

This project is still evolving, so contributions are especially valuable, be it fixing bugs, improving UI, or suggesting new analytics ideas. 

**Front-end contributions are especially sought.**


## Ways to Contribute


- Reporting Bugs
- Feature requests
- Ideas on Improving UI / UX
- Documentation
- Contributing Code - Back-end, Front-end or Data Service Layer

For bug reports or feature requests, please open an [issue](https://github.com/shsiddhant/memory.fm/issues/new/choose) using an appropriate template.

Before opening a new issue, please check existing ones to avoid duplicates.


## Contributing code

This guide explains how to setup the project locally, make changes, and submit them. Even if you make a small fix like a typo, please follow the [code guidelines](#code-guidelines).

### Requirements

- Python 3.10+
- Node.js 18+

### 1. Fork and Clone

1. Fork the project from the GitHub.
2. Clone the fork to your machine.

```shell
git clone https://github.com/your-username/memory.fm.git
cd memory.fm
git remote add upstream https://github.com/shsiddhant/memory.fm.git
git fetch upstream
```


### 2. Setup the Back-end environment

#### A. Using uv

The project uses [uv](https://docs.astral.sh/uv/) to manage dependencies. Follow the instructions on their website to install it to your system.

```shell
uv sync --all-groups --all-extras
```

#### B. Using pip

```shell
python -m venv .venv
source .venv/bin/activate
pip install -e ".[all]"
```


### 3. Run the Back-end

```
cd apps
uvicorn api.main:app --reload
```

The API will be available at http://localhost:8000
API Docs available at http://localhost:8000/docs

### 4. Run the Front-end

```
cd apps/web
npm install
npm run dev
```

App will be available at: http://localhost:5173

### Run Tests

Make sure to add / update `pytest` tests in the `tests` directory, and run the tests either using `uv` or directly.

```shell
uv run pytest
# Or
pytest
```


### Opening a Pull Request

1. Ensure that your changes have followed the [code guidelines](#code-guidelines).
2. Make sure that the tests pass and CI is green.
3. Open a PR from your branch -> main
3. Please write a descriptive title with appropriate prefixes like: 'bug', 'doc', 'api'. You can check out the existing closed PRs for more details.
4. Describe your changes and make sure to link any open issues related to your changes.

### Review Process

- PRs are reviewed on a best-effort basis.
- Feedback may take a few days depending on availability.
- You may be asked to make changes before merging.
- Some PRs may not be merged if they don’t align with the project direction.


### Project Structure

```
apps/
    api/        # FastAPI Back-end
    web/        # React Front-end
src/memoryfm/   # Database and Analytics Services
tests/          # Tests
```


### Code guidelines

This project emphasizes type safety and consistency across both back-end and front-end.

#### Back-end API and Services(Python)

- Ruff is used for linting and formatting.
- Type hints are expected for all new code.
- mypy is used for static type checking.
- Follow NumPy style for docstrings.

It is recommended that you also install the pre-commit hooks for linting and formatting.

```shell
pre-commit install
```

#### Front-end (TypeScript)

- Always define an interface for component props.
- Avoid using `any` and be explicit about what your components expect.
- Add any shared interfaces or global types to `apps/web/src/typing.ts`.
- Avoid defining types inside component files unless they are strictly local.
- Use PascalCase for components and types.
- Use camelCase for variables and functions.


### Need Help?

If you're unsure about something, feel free to open an issue or start a discussion. Even small questions are welcome.

