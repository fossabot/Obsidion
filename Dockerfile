FROM python:3.8

# Create the working directory
WORKDIR /obsidion

# Only copying these files here in order to take advantage of Docker cache. We only want the
# next stage (poetry install) to run if these files change, but not the rest of the app.
COPY pyproject.toml poetry.lock ./

# install poetry
RUN pip install "poetry==1.1.4"

# Currently poetry install is significantly slower than pip install, so we're creating a
# requirements.txt output and running pip install with it.
# Follow this issue: https://github.com/python-poetry/poetry/issues/338
# Setting --without-hashes because of this issue: https://github.com/pypa/pip/issues/4995
RUN poetry config virtualenvs.create false \
    && poetry export --without-hashes -f requirements.txt \
    |  poetry run pip install -r /dev/stdin \
    && poetry debug

COPY  . ./

# Because initially we only copy the lock and pyproject file, we can only install the dependencies
# in the RUN above, as the `packages` portion of the pyproject.toml file is not
# available at this point. Now, after the whole package has been copied in, we run `poetry install`
# again to only install packages, scripts, etc. (and thus it should be very quick).
# See this issue for more context: https://github.com/python-poetry/poetry/issues/1899
RUN poetry install --no-interaction --no-dev

# We're setting the entrypoint to `poetry run` because poetry installed entry points aren't
# available in the PATH by default, but it is available for `poetry run`
ENTRYPOINT ["python"]

CMD ["-m", "obsidion"]
