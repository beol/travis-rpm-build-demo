#!/bin/bash

curl -L https://www.kernel.org/pub/software/scm/git/git-2.11.0.tar.gz | tar xzf -

cd git-2.11.0

make configure && ./configure && make all
