#!/usr/bin/env bash

make install && pg_dump --dbname=$DATABASE_URL && psql -a -d $DATABASE_URL -f database.sql