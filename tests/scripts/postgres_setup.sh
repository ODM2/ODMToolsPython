#!/bin/bash
psql -U postgres -c "create extension postgis" 
psql -c 'DROP DATABASE IF EXISTS odmtest;' -U postgres;
psql -c 'create database odmtest;' -U postgres;
#psql -U postgres -d odmtest -a -f .tests/scripts/sampledb/odm_postgres.sql
psql -c 'DROP DATABASE IF EXISTS odm;' -U postgres;
psql -c 'create database odm;' -U postgres;
  ## install
  # add -a to psql to see full log, -q is quiet
psql -U postgres -q  -f .tests/scripts/sampledb/odm_postgres.sql