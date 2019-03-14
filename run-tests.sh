#!/usr/bin/env bash

shopt -s nullglob

# This script is located on the root of the repository:
basedir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

ok="yes"
for testdir in tests/*; do
    if test -d "$testdir"; then
        cur_ok=yes
        if test -f "${testdir}/TRAVIS_SKIP" -a "x$TRAVIS" = xtrue; then
            echo "Skipping $testdir on Travis"
            continue
        fi
        echo "Running $testdir"
        cd "$testdir"
        ./run.sh > output.stdout.txt 2>output.stderr.txt
        run_exit=$?
        if test $run_exit -ne "0"; then
            echo "Error non-zero exit in test: $testdir"
            cur_ok=no
        fi
        for f in expected.*; do
            out=output${f#expected}
            diff -u "$f" "$out"
            if test $? -ne "0"; then
               echo "ERROR in test $testdir: $out did not match $f"
               cur_ok=no
            fi
        done
        if test -x ./check.sh; then
            ./check.sh
            if test $? -ne "0"; then
                echo "ERROR in test $testdir: ./check.sh failed"
                cur_ok=no
            fi
        fi

        if test $cur_ok = "no"; then
            echo "STDOUT was"
            cat output.stdout.txt
            echo "STDERR was"
            cat output.stderr.txt
            ok=no
        fi

        if test -x ./cleanup.sh; then
            ./cleanup.sh
        fi
        rm -rf temp
        rm -f output.*
        cd "$basedir"
    fi
done

if test $ok = "yes"; then
    echo "All done."
else
    echo "An error occurred."
    exit 1
fi
