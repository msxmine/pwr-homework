#!/bin/bash

mariadb -e "DROP DATABASE Webstore"
mariadb -e "CREATE DATABASE Webstore"
mariadb Webstore < ./dbback.sql

