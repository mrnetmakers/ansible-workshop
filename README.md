# Ansible Deep-Dive Hands-On Workshop

A full-day, hands-on Ansible workshop for RHEL 9.

The workshop is organized into separate chapters under [`docs/`](docs/). Work through the chapters in order. The repository also contains the inventories, playbooks, roles, templates, and other files used by the exercises.

## Workshop environment

- one RHEL 9 Ansible control node (`rhelmain`);
- three RHEL 9 managed nodes (`rhel1`, `rhel2`, `rhel3`);
- one individual `studXX` account per student on all systems;
- `ansible-core` installed on the control node.

> **Important:** Several students use the same managed systems. Follow the exercises in order and use the student-specific resource names described in the workshop.

## Contents

- [0. Get the workshop repository](docs/0/)
- [1. Ansible basics: localhost and ping](docs/1/)
- [2. Learn YAML Syntax – Build Your First Playbook](docs/2/)
- [3. Understand and customize `ansible.cfg`](docs/3/)
- [4. Prepare SSH Key Authentication](docs/4/)
- [5. Inventory and First Remote Execution](docs/5/)
- [6. Execute simple playbooks](docs/6/)
- [7. Variables, lists, dictionaries and variable files](docs/7/)
- [8. Work with Ansible Modules](docs/8/)
- [9. Collections and Ansible Galaxy](docs/9/)
- [10. Conditionals](docs/10/)
- [11. Register task results](docs/11/)
- [12. Discover and use host facts](docs/12/)
- [13. Loops](docs/13/)
- [14. Transition to roles and Git](docs/14/)
- [15. Role exercise: `webserver`](docs/15/)

## Start here

Begin with [Chapter 0 – Get the workshop repository](docs/0/).

## Repository structure

```text
.
├── README.md
├── ansible.cfg
├── requirements.yml
├── inventory/
├── playbooks/
├── roles/
└── docs/
    ├── 0/
    ├── 1/
    ├── 2/
    └── ...
```

Each chapter directory contains its own `README.md`, so GitHub automatically renders the chapter when you open the directory.
