#!/bin/sh
gtts-cli "$@" | mpg123 - > /dev/null 2>&1
