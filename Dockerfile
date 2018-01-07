# <WARNING>
# Everything within sections like <TAG> is generated and can
# be automatically replaced on deployment. You can disable
# this functionality by simply removing the wrapping tags.
# </WARNING>

# <DOCKER_FROM>
FROM aldryn/base-project:py3-3.23
# </DOCKER_FROM>

# <PYTHON>
ENV PIP_INDEX_URL=${PIP_INDEX_URL:-https://wheels.aldryn.net/v1/aldryn-extras+pypi/${WHEELS_PLATFORM:-aldryn-baseproject-py3}/+simple/} \
    WHEELSPROXY_URL=${WHEELSPROXY_URL:-https://wheels.aldryn.net/v1/aldryn-extras+pypi/${WHEELS_PLATFORM:-aldryn-baseproject-py3}/}
COPY requirements.* /app/
COPY addons-dev /app/addons-dev/
RUN pip-reqs compile && \
    pip-reqs resolve && \
    pip install \
        --no-index --no-deps \
        --requirement requirements.urls
# </PYTHON>

COPY bin /app/bin/

# Install build tools
ENV NODE_VERSION=8.5.0 \
    NODE_ENV=production
ENV NODE_PATH=$NVM_DIR/versions/node/v$NODE_VERSION/lib/node_modules \
    PATH=$NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH
RUN bin/install-node.sh
RUN bin/install-yarn.sh

# Environment Variables
ENV GOOGLE_API_KEY=
ENV GA_TRACKING_ID=

COPY . /app

# Install and run webpack
RUN NODE_ENV=development yarn install --pure-lockfile
RUN yarn build

# Consolidate all static files
RUN DJANGO_MODE=build python manage.py collectstatic --noinput

CMD start web

