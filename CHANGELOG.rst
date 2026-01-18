=========================================
Parnoud Centreon Collection Release Notes
=========================================

.. contents:: Topics

v1.3.0
======

Release Summary
---------------

Adding support for Host_group

Major Changes
-------------

- Module creation Host_group

Bugfixes
--------

- manage_host update issue with list
- manage_host_group update issue with list

New Modules
-----------

- parnoud.centreon.add_host_group - Add a new host group configuration
- parnoud.centreon.delete_host_group - Delete host group
- parnoud.centreon.find_all_host_configurations - Return all host configurations
- parnoud.centreon.get_host_group - Get an existing host group
- parnoud.centreon.list_all_host_groups - Return all host group configurations
- parnoud.centreon.update_host_group - Update host group

v1.2.0
======

Release Summary
---------------

Adding support for monitoring server

Major Changes
-------------

- Documentation creation
- Renaming some interne naming

Deprecated Features
-------------------

- find_all_host_configuration

New Modules
-----------

- generate_configuration_all_monitoring_server - Generate and move the configuration files for all monitoring servers.
- generate_configuration_all_monitoring_server - Generate and move the configuration files of the monitoring server
- generate_reload_configuration_all_monitoring_server - Generate, move and reload the configuration files for all monitoring servers
- generate_reload_configuration_monitoring_server - Generate, move and reload the configuration files of the monitoring server
- list_all_monitoring_servers_configurations - List all monitoring servers configurations
- reload_configuration_all_monitoring_server - Reload the configuration files for all monitoring servers
- reload_configuration_monitoring_server - Reload the configuration files of the monitoring server
