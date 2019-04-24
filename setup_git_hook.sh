#!/usr/bin/env bash

REPLACE_CRLF_TO_LF=$(cat $1 | sed 's/[\r\n]/#/g' | tr '\n' '#')
LEN=$(echo ${REPLACE_CRLF_TO_LF} | wc -m)

test "${LEN}" = "$(cat $1 | sed 's/[\r\n]/#/g' | tr '\n' '#' |
    grep -oP '^(feat|fix|docs|style|refactor|perf|test|chore|revert)(\([^\)]+\))?:[^\n]+(#{4}[^#{4}]+){0,2}' |
    wc -m)" || {
    echo >&2 bad commit style "(feat|fix|docs|style|refactor|perf|test|chore|revert)(scope):..."
    exit 1
}

