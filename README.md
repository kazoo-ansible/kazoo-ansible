# kazoo-ansible
Ansible Playbooks to orchestrate the various components of [2600hz Kazoo](https://github.com/2600hz/kazoo).

## Pre-release Notice
kazoo-ansible is currently in a pre-release state and may introduce backward 
incompatible changes until 1.0.0 is released and this notice is removed. 
This is to provide an opportunity to greatly improve kazoo-ansible without 
needing to wait for a major release. Once we are happy with kazoo-ansible, 
it will be released as 1.0.0 and subject to backward compatibility 
guarantees.

## Features
- Automatically clusters CouchDB, Freeswitch, Kamailio, and Kazoo
- Optional Let's Encrypt TLS certificate generation for Monster UI, including 
  support for multiple Monster UI hosts
- Uses CouchDB instead of BigCouch
- Splits up roles for CouchDB, Freeswitch, Kamailio, Kazoo, Monster UI, 
  and RabbitMQ to allow lots of cluster custimization
- Publishes roles to Ansible Galaxy to allow easy integration into 
  custom playbooks
- Easy to install using included bootstrap scripts

## Desired Future Improvements
- Support for multiple zones
- CouchDB backup roles

## License
MIT License

## Installation Instructions
Check out the [Installation Instructions](INSTALL.md) to install 
kazoo-ansible.

## Using kazoo-ansible with Existing Playbooks
If you want to use kazoo-ansible with existing playbooks, simply 
include the roles in your playbook rather than using the playbook 
in this repository.

## Contributions
There are many ways to contribute:
- Suggestions
- Bug Reports
- Pull Requests
- Donations

## Versioning Strategy
This project uses [Semantic Versioning](http://semver.org). In 
practical terms, this means:
- Version numbers include MAJOR.MINOR.PATCH
- Major versions include backward-incompatible changes. This includes 
updating to major Kazoo versions, CentOS upgrades, or any other 
breaking changes.
- Minor versions include backward-compatible changes, such as new 
features. This includes updating to minor Kazoo versions, or any 
other backward-compatible changes.
- Patch versions include backward-compatible bug fixes. This includes 
updating to patch Kazoo versions, or any other backward-compatible 
bug fixes.

