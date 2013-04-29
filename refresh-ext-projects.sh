#! /bin/sh
# Copies files from external projects into FluentNao. This is to allow
# ease of use for others whilst still allowing other projects to be managed
# separately.

PYTHON_SRC="src/main/python"

EXT_PROJECTS="../naoutil/naoutil/src/main/python/naoutil"

for ppath in $EXT_PROJECTS
do
    pname=`basename $ppath`
    dest="${PYTHON_SRC}/${pname}"

    # delete old python files
    rm -f ${dest}/*.py*

    # replace with new ones
    cp ${ppath}/*.py $dest

    # make read-only to prevent accidental modification
    chmod 444 ${dest}/*.py
done
