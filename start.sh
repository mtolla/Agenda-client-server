#!/bin/sh
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python2 $DIR"/startServer.py" &&
python2 $DIR"/startClient.py" &
