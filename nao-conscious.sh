#! /bin/sh
export LD_LIBRARY_PATH="/fluentnao/src/main/python/pynaoqi-python2.7-2.1.4.13-linux64:$LD_LIBRARY_PATH"
export PYTHONPATH=src/main/python:/fluentnao/src/main/python/naoutil:/fluentnao/src/main/python/fluentnao:/fluentnao/src/main/python/pynaoqi-python2.7-2.1.4.13-linux64:${PYTHONPATH}
python -i src/main/python/nao-conscious/nao-conscious.py
