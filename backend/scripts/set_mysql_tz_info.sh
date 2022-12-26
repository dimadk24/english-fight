#!/usr/bin/env bash
# Usage: cd to project root and run ./scripts/set_mysql_tzinfo.sh <mysql user name>
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u "$1" -p mysql
