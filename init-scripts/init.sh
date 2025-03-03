#!/bin/bash

set -e
set -u

function create_database() {
    local database=$1
    echo "  Creating database '$database' with utf8mb4 character set and collation"
    mysql -u root -p$MYSQL_ROOT_PASSWORD -e "CREATE DATABASE IF NOT EXISTS $database CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"
}

function create_grant() {
    local user=$1
    local password=$2
    local database=$3
    echo "  Granting privileges to '$user' on database '$database'"
    mysql -u root -p$MYSQL_ROOT_PASSWORD -e "GRANT ALL PRIVILEGES ON $database.* TO '$user'@'%';"
    mysql -u root -p$MYSQL_ROOT_PASSWORD -e 'FLUSH PRIVILEGES;'
}

function alter_user() {
    local user=$1
    local password=$2
    echo "  Altering user '$user' with caching_sha2_password"
    mysql -u root -p$MYSQL_ROOT_PASSWORD -e "ALTER USER '$user'@'%' IDENTIFIED WITH caching_sha2_password BY '$password';"
    mysql -u root -p$MYSQL_ROOT_PASSWORD -e 'FLUSH PRIVILEGES;'
}

function show_created_databases() {
    echo "  Show databases"
    mysql -u root -p$MYSQL_ROOT_PASSWORD -e 'SHOW DATABASES;'
}

if [ -n "$MYSQL_MULTIPLE_DATABASES" ]; then
    echo "Multiple database creation requested: $MYSQL_MULTIPLE_DATABASES"
    for db in $(echo $MYSQL_MULTIPLE_DATABASES | tr ',' ' '); do
        create_database $db
        # Создаем пользователя и даем привилегии
        create_grant $MYSQL_USER $MYSQL_PASSWORD $db
    done


    # Изменяем пользователя для использования caching_sha2_password
    alter_user $MYSQL_USER $MYSQL_PASSWORD
    echo "Multiple databases and grants created"
    show_created_databases
    echo "  Finish work ------------------------------------------------------------------"
fi
