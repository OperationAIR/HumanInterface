#/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

CFG_DIR=$DIR/../config

echo 'replace config.yml with config.yml.dev'
cp $CFG_DIR/config.yml.dev $CFG_DIR/config.yml
