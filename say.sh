#!/bin/sh

cachedir=say_cache

h=$(echo "$@" | md5sum | awk '{ print $1 }')
file="${cachedir}/${h}.mp3"

if [ ! -d $cachedir ]
then
	mkdir $cachedir
fi

if [ ! -f ${file} ]
then
	gtts-cli "$@" > ${file}
fi

if [ -z "$SILENT_SAY" ]
then
  mpg123 ${file} >/dev/null 2>&1
fi
