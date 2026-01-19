=========================================
Parnoud Centreon Collection Release Notes
=========================================

.. contents:: Topics

v1.5.0
======

Major Changes
-------------

- Module creation host category
- Update Documentation

New Modules
-----------

- parnoud.centreon.create_host_category - Create a host category
- parnoud.centreon.delete_host_category - Delete a host severity configuration
- parnoud.centreon.get_host_category - Get a host category configuration
- parnoud.centreon.list_all_host_categories - List of host category configurations
- parnoud.centreon.update_host_category - Update a host category

v1.4.0
======

Major Changes
-------------

- Module creation host severity
- Update Documentation

New Modules
-----------

- parnoud.centreon.create_host_severity - Create a host severity
- parnoud.centreon.delete_host_severity - Delete a host severity configuration
- parnoud.centreon.get_host_severity - Get a host severity configuration
- parnoud.centreon.list_all_host_severities - List of all host severity configurations
- parnoud.centreon.update_host_severity - Update a host severity

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
