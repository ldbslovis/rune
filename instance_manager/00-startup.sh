#!/bin/bash
./01-install-packages.sh
./02-generate-admin-openrc.sh
./03-setup-server-environment.sh
./04-setup-openstack-environment.sh
./05-init-database.sh
./06-sync-database.sh
./07-bootstrap-openstack.sh
./08-restart-service.sh
