#!/bin/bash
psql -U postgres -c "create extension postgis" 
psql -c 'DROP DATABASE IF EXISTS odm2test;' -U postgres;
psql -c 'create database odm2test;' -U postgres;
#psql -U postgres -d odm2test -a -f ./tests/schemas/postgresql/ODM2_for_PostgreSQL.sql
psql -c 'DROP DATABASE IF EXISTS odm2;' -U postgres;
psql -c 'create database odm2;' -U postgres;
  ## install
  # add -a to psql to see full log, -q is quiet
psql -U postgres -q  -f ./tests/usecasesql/marchantariats/marchantariats.sql