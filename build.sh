#!/usr/bin/env bash

make install && pg_dump -Fc padb > padb.dump && psql -a -d $DATABASE_URL -f database.sql