# Capstone Project – Deploy a Two-Tier Gitea Platform with Ansible and Podman

**Estimated time:** 4–8 hours  
**Team size:** 2 students  
**Difficulty:** Advanced

This is an independent project.

Unlike the previous exercises, you will **not receive step-by-step implementation instructions**.

You will receive:

- an architecture;
- required container images;
- technical constraints;
- acceptance criteria;
- team responsibilities.

Your team must design and implement the Ansible solution.

You are expected to use the concepts covered throughout the workshop.

---

# 1. Scenario

Your team has been asked to deploy an internal Git service.

The application must consist of two separate tiers:

```text
                    Users
                      |
                      | HTTP
                      v
              +---------------+
              |    rhel1      |
              |               |
              | Gitea         |
              | Container     |
              +-------+-------+
                      |
                      | PostgreSQL
                      | TCP
                      v
              +---------------+
              |    rhel2      |
              |               |
              | PostgreSQL    |
              | Container     |
              +---------------+
```

The solution must be deployed entirely through **Ansible**.

Do not manually create the final containers with `podman run`.

Manual commands may be used while researching and troubleshooting, but the final deployment must be reproducible from the Git repository using Ansible.

---

# 2. Required container images

Use the following images.

## Application tier

```text
docker.gitea.com/gitea:1.27.2-rootless
```

Gitea provides the web interface and Git repository service.

The container must use an external PostgreSQL database.

---

## Database tier

```text
docker.io/library/postgres:17
```

PostgreSQL stores the Gitea application data.

Do not replace PostgreSQL with SQLite.

---

# 3. Host assignment

Use:

```text
rhel1    Application tier – Gitea
rhel2    Database tier – PostgreSQL
rhel3    Reserved for testing / optional extensions
```

`rhelmain` remains the Ansible control node.

---

# 4. Team responsibilities

Each team consists of two students.

## Team Member A – Database Engineer

Responsible for:

```text
PostgreSQL service
rhel2
```

Responsibilities include:

- PostgreSQL container deployment;
- persistent database storage;
- database credentials;
- container configuration;
- published database port;
- container health validation;
- Ansible role for PostgreSQL;
- documentation for the database tier.

---

## Team Member B – Application Engineer

Responsible for:

```text
Gitea service
rhel1
```

Responsibilities include:

- Gitea container deployment;
- persistent application storage;
- connection to PostgreSQL;
- application configuration;
- published HTTP port;
- container health validation;
- Ansible role for Gitea;
- documentation for the application tier.

---

## Shared responsibility

Both team members are responsible for:

- architecture decisions;
- variable naming;
- Git structure;
- integration;
- end-to-end testing;
- security of credentials;
- final documentation.

The project is only complete when **both services work together**.

---

# 5. Shared lab environment

Several teams are using the same RHEL systems.

Your deployment must therefore not interfere with another team.

Every resource that can conflict must contain a team identifier.

Examples include:

```text
container names
host ports
volumes
directories
configuration files
```

---

# 6. Team identifier

Your instructor will assign each team a numeric identifier.

Examples:

```text
Team 01
Team 02
Team 03
...
```

Store the identifier in an Ansible variable.

For example:

```yaml
team_id: "01"
```

Do not hard-code the team number throughout your roles.

Use variables.

---

# 7. Port allocation

Every team must use its own host ports.

Use the following convention.

For Team `01`:

```text
Gitea HTTP      3001
PostgreSQL      5401
```

For Team `02`:

```text
Gitea HTTP      3002
PostgreSQL      5402
```

For Team `10`:

```text
Gitea HTTP      3010
PostgreSQL      5410
```

The internal container ports remain unchanged.

Gitea:

```text
3000/tcp
```

PostgreSQL:

```text
5432/tcp
```

For example, Team 01 would conceptually publish:

```text
rhel1:3001 → Gitea:3000
rhel2:5401 → PostgreSQL:5432
```

The actual Ansible implementation is up to your team.

---

# 8. Container naming

Containers must also use team-specific names.

For example:

```text
gitea-team01
postgres-team01
```

Another team might have:

```text
gitea-team02
postgres-team02
```

Do not simply use:

```text
gitea
postgres
```

as globally assumed names in your automation.

---

# 9. Container management

Use the Ansible collection:

```text
containers.podman
```

Your project must declare the collection dependency in:

```text
requirements.yml
```

The collection provides modules for managing Podman containers, images, volumes and container information.

Your implementation should investigate modules such as:

```text
containers.podman.podman_container
containers.podman.podman_image
containers.podman.podman_volume
containers.podman.podman_container_info
```

Do not simply call:

```text
podman run
```

using `ansible.builtin.shell`.

---

# 10. Rootless containers

The actual application containers should run as **rootless Podman containers**.

This means the container belonging to a student should run inside that student's Podman environment.

Do not solve the project by running all containers as root unless your instructor explicitly permits this.

Before implementing the roles, research:

```bash
podman info
```

and:

```bash
podman ps
```

as your student account.

---

# 11. Required Git repository structure

Your team must create a structured Ansible repository.

A possible starting structure is:

```text
two-tier-project/
├── README.md
├── ansible.cfg
├── requirements.yml
├── site.yml
│
├── inventory/
│   ├── hosts.yml
│   └── group_vars/
│
└── roles/
    ├── postgresql/
    │   ├── defaults/
    │   ├── tasks/
    │   ├── templates/
    │   └── handlers/
    │
    └── gitea/
        ├── defaults/
        ├── tasks/
        ├── templates/
        └── handlers/
```

You may extend this structure if appropriate.

---

# 12. Inventory design

Your inventory must contain meaningful groups.

At minimum, create groups representing:

```text
application
database
```

For example, conceptually:

```text
application
    └── rhel1

database
    └── rhel2
```

Do not repeat host-specific values unnecessarily inside playbooks.

Use:

```text
inventory
group_vars
host_vars
role defaults
```

where appropriate.

---

# 13. Required roles

Your project must contain at least two roles:

```text
roles/gitea
roles/postgresql
```

One role belongs primarily to each team member.

The top-level playbook must remain small.

For example, the final architecture should follow the principle:

```text
site.yml
   |
   +-- database hosts
   |      └── postgresql role
   |
   +-- application hosts
          └── gitea role
```

Do not put the complete implementation directly into `site.yml`.

---

# 14. PostgreSQL requirements

The PostgreSQL role must deploy:

```text
docker.io/library/postgres:17
```

The database must be configured for Gitea.

Research the official image documentation and determine how to configure:

```text
database name
database user
database password
```

The PostgreSQL image supports the environment variables:

```text
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
```

The database must survive container recreation.

Deleting and recreating the PostgreSQL container must **not destroy the Gitea database**.

Use persistent storage.

---

# 15. Gitea requirements

The Gitea role must deploy:

```text
docker.gitea.com/gitea:1.27.2-rootless
```

Gitea must use PostgreSQL rather than its built-in SQLite database.

Research the Gitea container configuration.

Relevant configuration values include settings for:

```text
database type
database host
database name
database user
database password
```

Gitea supports container environment variables in the form:

```text
GITEA__section__KEY=value
```

for configuration.

The final application must connect automatically to the PostgreSQL service deployed by the other team member.

---

# 16. Inter-service configuration

The most important integration problem in this project is:

> How does the Gitea container on `rhel1` connect to PostgreSQL on `rhel2`?

Your team must solve this using variables.

Do not hard-code an IP address directly inside the Gitea role.

The information should be derived from your inventory or variables.

The application role must know:

```text
database host
database port
database name
database username
database password
```

Think carefully about which role owns each variable.

---

# 17. Persistent storage

Both services require persistent storage.

You must provide persistence for:

```text
PostgreSQL database data
Gitea application data
Gitea configuration
```

You may use Podman named volumes or carefully designed bind mounts.

Document your choice.

Your team should be able to explain:

> Why is persistent storage required for a container?

And:

> What happens to the data if the container is deleted and recreated?

---

# 18. Secrets

The database password must **not** be duplicated throughout multiple task files.

Store it in one appropriate variable.

Minimum requirement:

- keep credentials outside task files;
- do not hard-code passwords inside container tasks.

Better solution:

- use a dedicated variable file.

Advanced solution:

- use Ansible Vault.

For example:

```bash
ansible-vault create ...
```

Using Ansible Vault is optional but earns bonus credit.

Do not commit plaintext production-style secrets to a public repository.

---

# 19. Variables

Your implementation must use variables for at least:

```text
team ID
container images
container names
ports
database name
database username
database password
volume names
```

Changing the team identifier should require changing **one variable**, not editing several task files.

---

# 20. Lists and dictionaries

Use at least one meaningful:

```text
list
```

and one meaningful:

```text
dictionary
```

in the project.

Examples where these may make sense include:

- container environment variables;
- volume definitions;
- required directories;
- port definitions;
- application settings.

Do not introduce a list purely to satisfy the requirement.

It should simplify the implementation.

---

# 21. Templates

Use at least one Jinja2 template somewhere in the project.

Possible uses include:

```text
application configuration
environment file
deployment information
health report
service documentation
```

The rendered file must contain values coming from Ansible variables.

---

# 22. Conditionals

Use at least two meaningful conditionals.

Examples could include:

- perform initialization only when required;
- create something only for the database tier;
- output diagnostics only when a health check fails;
- configure optional functionality;
- execute a task depending on a registered container state.

The conditionals must serve a real purpose.

---

# 23. Register

Use `register` at least twice.

At least one registered result must influence another task.

For example:

```text
query container status
        ↓
register result
        ↓
evaluate condition
        ↓
display or perform action
```

Do not use `register` only to satisfy the requirement.

---

# 24. Facts

Use at least two Ansible facts in a meaningful way.

Examples:

```text
host IP address
hostname
operating system
architecture
```

One possible use is deriving the address that the application should use to connect to the database host.

---

# 25. Loops

Use at least one meaningful loop.

Possible uses:

```text
directories
volumes
validation checks
configuration files
```

The loop should reduce duplicated tasks.

---

# 26. Modules

Prefer dedicated Ansible modules.

Use built-in modules where appropriate, for example:

```text
ansible.builtin.file
ansible.builtin.template
ansible.builtin.debug
ansible.builtin.assert
ansible.builtin.uri
```

For containers, use:

```text
containers.podman.*
```

Avoid using `shell` simply because you already know the corresponding Linux command.

---

# 27. Shell commands

At least one shell or command task may be included where it provides useful operational information.

For example:

```text
podman version
database query
network connectivity diagnostic
```

If you use `shell`, be prepared to explain:

> Why was a dedicated Ansible module not a better choice?

Read-only commands should normally use:

```yaml
changed_when: false
```

---

# 28. Service validation

Simply having two running containers is **not enough**.

Your automation must validate the deployment.

At minimum, verify:

### PostgreSQL container

- container exists;
- container is running;
- database accepts connections.

### Gitea container

- container exists;
- container is running;
- HTTP endpoint responds.

### Integration

- Gitea successfully uses PostgreSQL;
- the application is usable after both containers have started.

Consider modules such as:

```text
containers.podman.podman_container_info
ansible.builtin.uri
ansible.builtin.assert
```

`containers.podman` includes modules for inspecting running containers as well as managing them.

---

# 29. Startup ordering

Gitea depends on PostgreSQL.

Your automation must account for this dependency.

Starting the PostgreSQL container does not necessarily mean that PostgreSQL is immediately ready to accept connections.

Your solution should deal with this appropriately.

Think about:

```text
start PostgreSQL
       ↓
wait until PostgreSQL is ready
       ↓
start/configure Gitea
```

Do not rely only on an arbitrary:

```text
sleep 30
```

Find a more reliable test.

---

# 30. Idempotency

The complete deployment must be safe to execute repeatedly.

Run:

```bash
ansible-playbook site.yml
```

twice.

The second execution should make no unnecessary changes.

Your team must be able to explain any task that still reports:

```text
changed
```

on the second run.

---

# 31. Container recreation test

Your solution must demonstrate that persistent storage works.

After a successful deployment:

1. create a test user or repository in Gitea;
2. remove the Gitea container;
3. run the Ansible deployment again;
4. confirm that the application data still exists.

Perform a similar test for PostgreSQL if appropriate.

The Ansible roles must be able to recreate the containers without destroying application data.

---

# 32. Team Git workflow

Both students must actively contribute to the repository.

Use separate branches.

For example:

```text
main

feature/postgresql
feature/gitea
```

Team Member A primarily works on:

```text
feature/postgresql
```

Team Member B primarily works on:

```text
feature/gitea
```

Each member should make several meaningful commits.

Examples:

```text
Add PostgreSQL role structure
Add persistent PostgreSQL volume
Add database readiness check
```

and:

```text
Add Gitea container role
Configure PostgreSQL connection
Add HTTP validation
```

Do not make one single commit containing the complete project.

---

# 33. Integration

At some point the two branches must be combined.

Before merging, each team member should review the other member's implementation.

Look for:

- hard-coded values;
- duplicated variables;
- missing idempotency;
- credentials in task files;
- repeated tasks that should use loops;
- unnecessary shell commands;
- missing validation.

Then integrate both roles.

---

# 34. Documentation

Your repository must contain a `README.md`.

It must document:

- architecture;
- team members and responsibilities;
- container images;
- inventory design;
- variables that need customization;
- deployment command;
- service URLs;
- validation steps;
- known limitations.

Include a small architecture diagram.

For example:

```text
Browser
   |
   | HTTP :30XX
   v
rhel1
+-------------------+
| Gitea container   |
+---------+---------+
          |
          | PostgreSQL :54XX
          v
rhel2
+-------------------+
| PostgreSQL        |
| container         |
+-------------------+
```

---

# 35. Required final deployment command

A new administrator should be able to clone the repository, configure the required variables, install collections and deploy the complete environment using something close to:

```bash
ansible-galaxy collection install \
  -r requirements.yml \
  --collections-path ./collections

ansible-playbook site.yml
```

No manual `podman run` commands should be required for the final deployment.

---

# 36. Acceptance criteria

Your project is complete when all of the following are true:

- `rhel1` runs the team's Gitea container;
- `rhel2` runs the team's PostgreSQL container;
- both use the required container images;
- containers run rootless;
- every team uses unique names and ports;
- Gitea connects to PostgreSQL;
- PostgreSQL data is persistent;
- Gitea data is persistent;
- Gitea is accessible through the team's assigned HTTP port;
- Ansible validates the application endpoint;
- the project uses roles;
- the project uses variables;
- the project contains a list and dictionary;
- the project uses a template;
- the project uses loops;
- the project uses facts;
- the project uses conditionals;
- the project uses `register`;
- Podman is managed using the `containers.podman` collection;
- repeated deployment is idempotent;
- both team members contributed through Git;
- the repository contains useful documentation.

---

# 37. Final demonstration

Each team must demonstrate the following to the instructor.

### 1. Clean Ansible execution

```bash
ansible-playbook site.yml
```

### 2. Second execution

Run it again and explain the recap.

### 3. Containers

Show the two running containers.

### 4. Application

Open your team-specific Gitea URL.

For example, Team 01:

```text
http://rhel1:3001
```

### 5. Database integration

Demonstrate that the application is using PostgreSQL.

### 6. Persistence

Demonstrate that deleting and recreating a container does not delete the application data.

### 7. Git history

Show:

```bash
git log --oneline --graph --decorate --all
```

Both team members should have meaningful contributions.

---

# 38. Optional advanced challenges

If your team finishes early, choose one or more extensions.

### Challenge A – Ansible Vault

Move database credentials into an encrypted Ansible Vault file.

---

### Challenge B – Firewall

Use:

```text
ansible.posix.firewalld
```

to expose only the required team-specific ports.

Make sure you do not interfere with other teams.

---

### Challenge C – Health reporting

Create a final validation role that prints a report such as:

```text
Team:             01
Gitea host:       rhel1
Gitea port:       3001
Gitea status:     RUNNING
PostgreSQL host:  rhel2
PostgreSQL port:  5401
Database status:  READY
HTTP status:      200
```

Use:

```text
register
facts
conditionals
debug
```

to generate the report.

---

### Challenge D – Backup

Create an Ansible task or role that backs up the PostgreSQL database.

The backup filename should include:

```text
team ID
date
database name
```

Do not overwrite another team's backups.

---

### Challenge E – Restore test

Create data in Gitea, back up the database, remove the deployment and demonstrate that the data can be restored.

---

### Challenge F – Systemd / Quadlet

Investigate how Podman containers can be managed through systemd/Quadlet.

Adapt your deployment so the services can survive host reboots.

Document your design choice.

---

# 39. Evaluation

The project will primarily be evaluated on:

| Area | Weight |
|---|---:|
| Functional two-tier deployment | 25% |
| Ansible design and role structure | 20% |
| Idempotency and validation | 15% |
| Variables and reusable design | 10% |
| Persistence and integration | 10% |
| Git teamwork | 10% |
| Documentation | 10% |

A working application implemented through a large collection of shell commands is **not** considered a high-quality Ansible solution.

The goal is to demonstrate that you can translate a technical requirement into structured, reusable and maintainable automation.