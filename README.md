# kazoo-ansible
Ansible Playbooks to orchestrate the various components of [2600hz Kazoo](https://github.com/2600hz/kazoo).

## Features
- Automatically clusters CouchDB, Freeswitch, Kamailio, and Kazoo
- Let's Encrypt TLS certificate generation for Monster UI, including 
support for multiple Monster UI hosts
- Uses CouchDB instead of BigCouch
- Uses specific versions of Freeswitch, Kamailio, Kazoo, and Monster UI 
by default
- Splits up roles for CouchDB, Freeswitch, Kamailio, Kazoo, Monster UI, 
and RabbitMQ to allow lots of cluster custimization
- Publishes roles to Ansible Galaxy to allow easy integration into 
custom playbooks
- Manages Kazoo, Monster UI, Kamailio, and Freeswitch component versions 
by default to prevent untested versions from making it into production

## Desired Future Improvements
- Support for multiple zones
- CouchDB backup roles

## License
MIT License

## Contributions
There are many ways to contribute:
- Suggestions
- Bug Reports
- Pull Requests

## Versioning Strategy
This project uses [Semantic Versioning](http://semver.org). In 
practical terms, this means:
- Version numbers include MAJOR.MINOR.PATC
- Major versions include backward-incompatible changes. This includes 
updating to major Kazoo versions, CentOS upgrades, or any other 
breaking changes.
- Minor versions include backward-compatible changes, such as new 
features. This includes updating to minor Kazoo versions, or any 
other backward-compatible changes.
- Patch versions include backward-compatible bug fixes. This includes 
updating to patch Kazoo versions, or any other backward-compatible 
bug fixes.

