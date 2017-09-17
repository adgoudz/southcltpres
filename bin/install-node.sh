#!/bin/bash

source $NVM_DIR/nvm.sh

nvm install $NODE_VERSION
nvm alias default $NODE_VERSION
nvm use default
