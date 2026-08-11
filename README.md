# Ansible Deep-Dive Hands-On Workshop

A full-day, hands-on Ansible workshop for RHEL 9. This repository is designed to be cloned by students onto an Ansible control VM. Each student has an account such as `stud01`, `stud02`, etc. The same account exists on three RHEL 9 managed nodes.

## Lab environment

You need:

- one RHEL 9 control VM with `ansible-core` already installed;
- three RHEL 9 managed VMs;
- the same student account (`studXX`) on the control VM and all three managed VMs;
- SSH connectivity from the control VM to the managed VMs;
- `sudo` access for `studXX` on the managed VMs for privileged exercises;
- internet access from the control VM for the collection exercise, or collections pre-staged by the instructor.

Throughout the workshop the managed nodes are called `rhel1`, `rhel2`, and `rhel3`. Replace the example IP addresses in `inventory/hosts.yml` with the addresses supplied by your instructor.

> **Important:** This repository contains working examples so you can recover if you get stuck. Do not simply run every file. Follow the exercises in order, read each playbook, make the requested changes, and inspect the results.

## Schedule

| Block | Topic | Approx. time |
|---|---|---:|
| 1 | Ansible basics, localhost, ping, YAML | 60 min |
| 2 | Project configuration, SSH, inventory | 60 min |
| 3 | First playbooks, variables and data structures | 75 min |
| 4 | Modules and collections | 75 min |
| 5 | Conditionals, register and facts | 75 min |
| 6 | Loops | 45 min |
| 7 | Roles and Git project structure | 45 min |
| 8 | Templates, shell and final challenge | 45 min |

The timings are approximate and allow the instructor to insert breaks and discussion.

---

# 0. Get the workshop repository

Clone the repository URL provided by your instructor:

```bash
git clone <REPOSITORY_URL> ~/ansible-workshop
cd ~/ansible-workshop
```

Inspect the repository:

```bash
find . -maxdepth 3 -type f | sort
```

Do not run `site.yml` yet. The role-based part of the repository is used later in the day.

---

# 1. Ansible basics: localhost and ping

## 1.1 Verify your account

```bash
whoami
id
```

Your username should be similar to `stud01`.

## 1.2 Verify Ansible

```bash
ansible --version
which ansible
ls -1 /usr/bin/ansible*
```

Locate these tools if present:

- `ansible`
- `ansible-config`
- `ansible-doc`
- `ansible-galaxy`
- `ansible-inventory`
- `ansible-playbook`

## 1.3 Use Ansible locally

Run the Ansible ping module against the local machine:

```bash
ansible localhost -m ansible.builtin.ping
```

Expected result contains:

```text
"ping": "pong"
```

The Ansible `ping` module is not an ICMP ping. It verifies that Ansible can execute a module successfully on the target.

Run a command locally:

```bash
ansible localhost -m ansible.builtin.command -a "hostname"
ansible localhost -m ansible.builtin.command -a "id"
ansible localhost -m ansible.builtin.command -a "uptime"
```

## 1.4 Discover module documentation

```bash
ansible-doc ansible.builtin.command
```

Inside the pager, search for `EXAMPLES` by typing:

```text
/EXAMPLES
```

Exit with `q`.

### Checkpoint

You should now be able to explain the difference between:

- `ansible`
- `ansible-playbook`
- an Ansible module
- the control node
- a managed node

---

# 2. Learn YAML syntax

Create a scratch file outside the supplied examples:

```bash
cat > ~/yaml-test.yml <<'EOFYAML'
---
student: stud01
course: Ansible Deep Dive
enabled: true
max_connections: 10

packages:
  - httpd
  - curl
  - vim

server:
  hostname: rhel1
  port: 80
  environment: training

users:
  - name: alice
    department: development
  - name: bob
    department: operations
EOFYAML
```

Replace `stud01` with your actual username.

Identify these YAML data structures:

```yaml
student: stud01
```

A scalar/key-value pair.

```yaml
packages:
  - httpd
  - curl
```

A list.

```yaml
server:
  hostname: rhel1
  port: 80
```

A dictionary.

```yaml
users:
  - name: alice
    department: development
```

A list of dictionaries.

## 2.1 Break YAML deliberately

Change:

```yaml
packages:
  - httpd
  - curl
```

to:

```yaml
packages:
  - httpd
    - curl
```

Observe that indentation changes the structure and will make this invalid for the intended data model. Restore the original content.

### YAML rules to remember

- indentation matters;
- use spaces, not tabs;
- lists use `-`;
- dictionaries use `key: value`;
- quote values when YAML might otherwise interpret them unexpectedly;
- Ansible files commonly begin with `---`.

---

# 3. Understand and customize `ansible.cfg`

Open the repository configuration:

```bash
cat ansible.cfg
```

It contains project-local settings such as:

```ini
[defaults]
inventory = ./inventory/hosts.yml
host_key_checking = False
retry_files_enabled = False
forks = 10
timeout = 15
roles_path = ./roles
collections_path = ./collections
```

Check which configuration Ansible is using:

```bash
ansible --version
```

Look for the `config file` line.

Inspect only settings that differ from defaults:

```bash
ansible-config dump --only-changed
```

## 3.1 Explore configuration documentation

Run:

```bash
ansible-config list | less
```

Find settings for:

- inventory;
- forks;
- timeout;
- host key checking.

### Discussion

Why is a project-local `ansible.cfg` useful when automation is stored in Git?

---

# 4. Prepare SSH key authentication

## 4.1 Inspect your SSH directory

```bash
ls -la ~/.ssh
```

If you already have a training key approved by the instructor, use it. Otherwise create a new Ed25519 key:

```bash
ssh-keygen -t ed25519
```

Use the default path:

```text
~/.ssh/id_ed25519
```

Follow the instructor's policy for passphrases.

Verify the files:

```bash
ls -l ~/.ssh/id_ed25519 ~/.ssh/id_ed25519.pub
```

`id_ed25519` is the private key. Never copy or share it.

`id_ed25519.pub` is the public key and may be installed on remote systems.

## 4.2 Install your public key on all three managed nodes

Replace the addresses below with the real addresses supplied by the instructor and replace `studXX` with your username:

```bash
ssh-copy-id studXX@<RHEL1_IP>
ssh-copy-id studXX@<RHEL2_IP>
ssh-copy-id studXX@<RHEL3_IP>
```

Test all three hosts:

```bash
ssh studXX@<RHEL1_IP> hostname
ssh studXX@<RHEL2_IP> hostname
ssh studXX@<RHEL3_IP> hostname
```

The commands should run without requesting the remote account password for SSH authentication.

---

# 5. Inventory and first remote execution

## 5.1 Edit the inventory

Open:

```bash
vi inventory/hosts.yml
```

Replace the example documentation addresses:

```yaml
rhel1:
  ansible_host: 192.0.2.101
rhel2:
  ansible_host: 192.0.2.102
rhel3:
  ansible_host: 192.0.2.103
```

with the actual addresses supplied by the instructor.

Now edit:

```bash
vi inventory/group_vars/managed.yml
```

Replace:

```yaml
ansible_user: studXX
```

with your username.

## 5.2 Inspect the parsed inventory

```bash
ansible-inventory --graph
```

Then:

```bash
ansible-inventory --host rhel1
```

List the hosts in the group:

```bash
ansible managed --list-hosts
```

## 5.3 Ping all managed systems

```bash
ansible managed -m ansible.builtin.ping
```

Try one host:

```bash
ansible rhel1 -m ansible.builtin.ping
```

If a host fails, diagnose SSH before continuing:

```bash
ssh studXX@<RHEL_IP> hostname
```

## 5.4 Ad-hoc remote execution

Run:

```bash
ansible managed -m ansible.builtin.command -a "hostname"
ansible managed -m ansible.builtin.command -a "uname -r"
ansible managed -m ansible.builtin.command -a "uptime"
ansible managed -m ansible.builtin.command -a "free -m"
```

Use verbose mode once:

```bash
ansible rhel1 -m ansible.builtin.ping -vv
```

Identify the SSH user and connection steps in the output.

---

# 6. First playbooks

The repository contains four introductory playbooks.

## 6.1 Connectivity playbook

Read it first:

```bash
cat playbooks/01_ping.yml
```

Run it:

```bash
ansible-playbook playbooks/01_ping.yml
```

## 6.2 Hostname playbook

```bash
cat playbooks/02_hostname.yml
ansible-playbook playbooks/02_hostname.yml
```

Notice:

```yaml
changed_when: false
```

The `hostname` command only reads data. We tell Ansible that executing it should not count as a configuration change.

## 6.3 Create a directory

Read:

```bash
cat playbooks/03_directory.yml
```

Run:

```bash
ansible-playbook playbooks/03_directory.yml
```

Verify:

```bash
ansible managed -m ansible.builtin.command -a "ls -ld /tmp/ansible-$USER"
```

Run the playbook a second time:

```bash
ansible-playbook playbooks/03_directory.yml
```

The second run should normally report no change for the directory task. This is your first example of **idempotency**.

## 6.4 Create a managed file

```bash
cat playbooks/04_file.yml
ansible-playbook playbooks/04_file.yml
```

Verify:

```bash
ansible managed -m ansible.builtin.command -a "cat /tmp/ansible-$USER/README.txt"
```

### Customization task

Modify `playbooks/04_file.yml` so the generated file contains a third line:

```text
Workshop user: studXX
```

Do not hard-code your username. Use an Ansible variable.

---

# 7. Variables, lists, dictionaries and variable files

## 7.1 Simple variables

Read and execute:

```bash
cat playbooks/10_variables.yml
ansible-playbook playbooks/10_variables.yml
```

Modify these values:

```yaml
course_room: Linux Lab
course_day: Tuesday
```

Run again.

## 7.2 Lists

```bash
cat playbooks/11_lists.yml
ansible-playbook playbooks/11_lists.yml
```

Add `tree` to the `packages` list.

Add a task that prints the fourth item using its numeric list index.

## 7.3 Dictionaries

```bash
cat playbooks/12_dictionary.yml
ansible-playbook playbooks/12_dictionary.yml
```

Add these dictionary keys:

```yaml
tls_enabled: false
admin_email: admin@example.invalid
```

Add a `debug` task that prints both values.

## 7.4 External variable files

Inspect:

```bash
cat vars/webserver.yml
cat playbooks/13_varfile.yml
```

Run:

```bash
ansible-playbook playbooks/13_varfile.yml
```

Add a variable to `vars/webserver.yml`:

```yaml
webserver_description: Training HTTP server
```

Then display it from the playbook.

### Checkpoint

Be able to explain these structures:

- scalar variable;
- list;
- dictionary;
- list of dictionaries;
- variable file;
- inventory variable.

---

# 8. Work with Ansible modules

These exercises change the managed systems and require `sudo` access.

Before using a new module, inspect its documentation. Examples:

```bash
ansible-doc ansible.builtin.package
ansible-doc ansible.builtin.service
ansible-doc ansible.builtin.file
ansible-doc ansible.builtin.user
ansible-doc ansible.builtin.lineinfile
```

## 8.1 Package module

```bash
cat playbooks/20_packages.yml
ansible-playbook playbooks/20_packages.yml
```

Customize the package list to also install:

```text
tar
tree
```

Run the playbook twice and compare the recap.

## 8.2 Service module

```bash
cat playbooks/21_service.yml
ansible-playbook playbooks/21_service.yml
```

Verify:

```bash
ansible managed -b -m ansible.builtin.command -a "systemctl is-active httpd"
ansible managed -b -m ansible.builtin.command -a "systemctl is-enabled httpd"
```

## 8.3 File and copy modules

```bash
cat playbooks/22_files.yml
ansible-playbook playbooks/22_files.yml
```

Customize the playbook so it also creates:

```text
/opt/training/config
```

with mode `0750`.

## 8.4 User module

```bash
cat playbooks/23_users.yml
ansible-playbook playbooks/23_users.yml
```

Verify:

```bash
ansible managed -m ansible.builtin.command -a "getent passwd ansibledemo"
```

Change the comment field and execute again. Identify exactly what changed.

## 8.5 lineinfile module

```bash
cat playbooks/24_lineinfile.yml
ansible-playbook playbooks/24_lineinfile.yml
```

Run it twice.

Verify:

```bash
ansible managed -m ansible.builtin.command -a "cat /etc/motd"
```

Question: Why does the configured line not appear multiple times?

---

# 9. Collections and Ansible Galaxy

## 9.1 Inspect installed collections

```bash
ansible-galaxy collection list
```

The repository declares two public collections in `requirements.yml`:

```bash
cat requirements.yml
```

Install them into the project-local `collections/` directory:

```bash
ansible-galaxy collection install -r requirements.yml -p ./collections
```

List them:

```bash
ansible-galaxy collection list -p ./collections
```

> If your training environment has no internet access, use the collection content provided by your instructor instead.

## 9.2 `ansible.posix.firewalld`

Inspect:

```bash
ansible-doc ansible.posix.firewalld
```

Read and execute:

```bash
cat playbooks/25_firewall.yml
ansible-playbook playbooks/25_firewall.yml
```

Verify on a managed host:

```bash
ansible managed -b -m ansible.builtin.command -a "firewall-cmd --list-services"
```

## 9.3 `community.general.ini_file`

```bash
ansible-doc community.general.ini_file
cat playbooks/26_ini.yml
ansible-playbook playbooks/26_ini.yml
```

Verify:

```bash
ansible managed -b -m ansible.builtin.command -a "cat /etc/training-app.conf"
```

Customize the playbook with a new section:

```ini
[logging]
level=info
```

## 9.4 Collection discovery exercise

Inspect another module:

```bash
ansible-doc ansible.posix.selinux
```

Do not change SELinux mode. Instead answer:

1. Which states does the module accept?
2. Which parameter controls the policy?
3. Can the module make persistent changes?

---

# 10. Conditionals

## 10.1 Basic boolean

```bash
cat playbooks/30_condition_basic.yml
ansible-playbook playbooks/30_condition_basic.yml
```

Change:

```yaml
install_webserver: true
```

to:

```yaml
install_webserver: false
```

Run again and observe `skipping`.

## 10.2 String comparison

```bash
cat playbooks/31_condition_string.yml
ansible-playbook playbooks/31_condition_string.yml
```

Change the environment from `development` to `production`. Run again.

Add a third environment named `testing` and an appropriate task.

## 10.3 Multiple conditions

```bash
cat playbooks/32_condition_multiple.yml
ansible-playbook playbooks/32_condition_multiple.yml
```

The task executes only when both conditions are true.

Change:

```yaml
configure_web: false
```

and rerun.

## 10.4 Advanced condition with facts and list membership

```bash
cat playbooks/32b_condition_advanced.yml
ansible-playbook playbooks/32b_condition_advanced.yml
```

Increase:

```yaml
minimum_memory_mb: 1024
```

to a value larger than your lab VMs contain, for example `16384`. Observe the result.

---

# 11. Register task results

## 11.1 Capture command output

```bash
cat playbooks/33_register.yml
ansible-playbook playbooks/33_register.yml
```

Study the registered object. Find:

- `stdout`;
- `stderr`;
- `rc`;
- `changed`.

Add a task that displays only the return code.

## 11.2 Combine `register` and `when`

```bash
cat playbooks/33b_register_condition.yml
ansible-playbook playbooks/33b_register_condition.yml
```

Stop Apache temporarily on one host if your instructor permits it, then rerun the playbook limited to that host. Restore the service afterwards.

The important pattern is:

```text
execute -> register -> evaluate -> take action
```

---

# 12. Discover and use host facts

Gather all facts:

```bash
ansible managed -m ansible.builtin.setup
```

Filter the output:

```bash
ansible managed -m ansible.builtin.setup -a "filter=ansible_distribution*"
ansible managed -m ansible.builtin.setup -a "filter=ansible_memtotal_mb"
ansible managed -m ansible.builtin.setup -a "filter=ansible_default_ipv4"
```

Run the facts playbook:

```bash
cat playbooks/34_facts.yml
ansible-playbook playbooks/34_facts.yml
```

## Fact discovery challenge

Modify `playbooks/34_facts.yml` so it also displays:

- hostname;
- kernel version;
- processor count;
- default IPv4 address.

Use facts rather than shell commands.

---

# 13. Loops

## 13.1 Basic loop

```bash
cat playbooks/40_loop_basic.yml
ansible-playbook playbooks/40_loop_basic.yml
```

Add two more items.

## 13.2 Loop over package names

```bash
cat playbooks/41_loop_packages.yml
ansible-playbook playbooks/41_loop_packages.yml
```

Now consider this alternative:

```yaml
- name: Install all packages in one operation
  ansible.builtin.package:
    name: "{{ training_packages }}"
    state: present
```

Replace the loop with the list-based version and compare the output.

**Lesson:** not every task that can use a loop should use a loop.

## 13.3 Loop over dictionaries

```bash
cat playbooks/42_loop_dictionary.yml
ansible-playbook playbooks/42_loop_dictionary.yml
```

Add a fourth user to the list.

Then add a dictionary key called `comment` to every user and use it in the `user` module task.

---

# 14. Transition to roles and Git

> **From this point onward, all new configuration tasks must be implemented in roles.** Top-level playbooks should stay small and select hosts/roles rather than containing large task lists.

## 14.1 Examine the role layout

```bash
find roles/webserver -maxdepth 2 -type f | sort
```

Key directories:

```text
tasks/       tasks executed by the role
handlers/    event-driven tasks
templates/   Jinja2 templates
files/       static files
defaults/    customizable default variables
vars/        higher-precedence role variables
meta/        role metadata
```

The supplied repository already contains reference roles. To learn how Ansible generates one, create a disposable role:

```bash
ansible-galaxy role init /tmp/example_role
find /tmp/example_role -maxdepth 2 -type f | sort
rm -rf /tmp/example_role
```

## 14.2 Initialize your own Git history

Because you cloned the instructor repository, it may already have Git history. For the workshop, create your own branch:

```bash
git switch -c studXX-workshop
```

Replace `studXX` with your username.

Check status:

```bash
git status
```

Make a small documentation change, then:

```bash
git add .
git commit -m "Configure student workshop environment"
```

View history:

```bash
git log --oneline --decorate -5
```

## 14.3 Understand the top-level playbook

```bash
cat site.yml
```

Notice that it contains only host selection, privilege escalation and role assignment.

---

# 15. Role exercise: `webserver`

Inspect the default variables:

```bash
cat roles/webserver/defaults/main.yml
```

Inspect the tasks:

```bash
cat roles/webserver/tasks/main.yml
```

Inspect the handler:

```bash
cat roles/webserver/handlers/main.yml
```

Run the role against one host first using the supplied small role-runner playbook:

```bash
ansible-playbook playbooks/50_webserver_role.yml --limit rhel1
```

Then run it against all managed hosts:

```bash
ansible-playbook playbooks/50_webserver_role.yml
```

### Handler experiment

Run `playbooks/50_webserver_role.yml` a second time. The webserver restart handler should not be triggered merely because the playbook was executed.

Then modify a visible line in:

```text
roles/webserver/templates/index.html.j2
```

Run `playbooks/50_webserver_role.yml` again. Observe when the handler executes.

---

# 16. Templates

## 16.1 Template example 1: customized HTML page

Open:

```bash
vi roles/webserver/templates/index.html.j2
```

The same template is rendered separately for every managed node using facts and variables.

Customize it to display all of the following:

- student username (`ansible_user`);
- kernel version;
- default IPv4 address;
- processor count;
- deployment environment.

Run:

```bash
ansible-playbook site.yml
```

Test each web server using its actual IP address:

```bash
curl http://<RHEL1_IP>/
curl http://<RHEL2_IP>/
curl http://<RHEL3_IP>/
```

## 16.2 Template example 2: application configuration

Inspect:

```bash
cat roles/training_app/defaults/main.yml
cat roles/training_app/templates/training-app.conf.j2
cat roles/training_app/tasks/main.yml
```

The three hosts already have different `training_app` dictionaries in:

```text
inventory/host_vars/rhel1.yml
inventory/host_vars/rhel2.yml
inventory/host_vars/rhel3.yml
```

Run:

```bash
ansible-playbook site.yml
```

Compare the generated files:

```bash
ansible managed -b -m ansible.builtin.command -a "cat /etc/training-app.conf"
```

### Customization

Add:

```yaml
training_app_log_level: info
```

to the role defaults and render it into the template under a `[logging]` section.

Override `training_app_log_level` for `rhel3` to `warning`.

Run again and compare the hosts.

---

# 17. Running command and shell tasks inside a role

Inspect:

```bash
cat roles/system_report/tasks/main.yml
```

This role demonstrates both `ansible.builtin.command` and `ansible.builtin.shell`.

Use `command` when you simply need to execute a program. Use `shell` only when you need shell features such as pipes, redirects, compound expressions or shell expansion.

Run:

```bash
ansible-playbook site.yml
```

The role:

1. runs `uptime` with `command`;
2. stores the output with `register`;
3. displays it with `debug`;
4. uses a shell pipeline to find large entries under `/etc`;
5. uses another shell pipeline to determine root filesystem utilization;
6. compares the result to `system_report_disk_warning` with a conditional.

## 17.1 Customize the threshold

Edit:

```bash
vi roles/system_report/defaults/main.yml
```

Set:

```yaml
system_report_disk_warning: 1
```

Run the role and observe the warning. Restore the value afterwards.

## 17.2 Shell safety exercise

Find the `set -o pipefail` lines in the role.

Discuss why checking pipeline failures is useful in automation.

---

# 18. Check mode, diff mode and limiting execution

Before a potentially disruptive change, try check mode:

```bash
ansible-playbook site.yml --check
```

Add differences where supported:

```bash
ansible-playbook site.yml --check --diff
```

Modify a template and run `--check --diff` again without applying the change.

Limit a play to one host:

```bash
ansible-playbook site.yml --limit rhel1
```

Limit it to two:

```bash
ansible-playbook site.yml --limit 'rhel1,rhel2'
```

This is an important operational practice: validate on a smaller target set before broad rollout.

---

# 19. Final challenge: professional `server_baseline` role

The role skeleton already exists at:

```text
roles/server_baseline/
```

Do **not** put the implementation into `site.yml`. All configuration belongs inside the role.

## Requirements

### Packages

Install:

```text
curl
vim-enhanced
tar
tree
```

The list should be defined as a variable.

### Directories

Create:

```text
/opt/company
/opt/company/scripts
/opt/company/config
```

Use a loop.

### Accounts

Create three application users using a list of dictionaries and a loop. Include at least:

- username;
- shell;
- comment;
- whether a home directory should be created.

### MOTD template

Replace `roles/server_baseline/templates/motd.j2` with a real template and deploy it to `/etc/motd`.

The rendered file must contain:

- hostname;
- operating system;
- OS version;
- default IP address;
- environment;
- the text `Managed by Ansible - manual changes may be overwritten`.

### Conditional environment banner

If the host's environment is `production`, add:

```text
*** PRODUCTION SYSTEM ***
```

Otherwise add:

```text
Non-production environment
```

Implement the condition in the template or role tasks and be prepared to explain your choice.

### Register

Run a command that determines system uptime and store the result using `register`.

Display the result with `debug`.

### Shell

Add one useful read-only system-reporting task that genuinely requires shell functionality. It must:

- use `ansible.builtin.shell`;
- not change the host;
- use `changed_when: false`;
- store its output using `register`.

### Add the role to the site playbook

Uncomment:

```yaml
- server_baseline
```

in `site.yml`.

## Validate your work

Check syntax:

```bash
ansible-playbook site.yml --syntax-check
```

Review possible changes:

```bash
ansible-playbook site.yml --check --diff
```

Run against one host:

```bash
ansible-playbook site.yml --limit rhel1
```

Then all hosts:

```bash
ansible-playbook site.yml
```

Run it immediately a second time:

```bash
ansible-playbook site.yml
```

Investigate every task that still reports `changed` on the second run. Decide whether the change is legitimate or whether the task can be made more idempotent.

---

# 20. Final Git delivery

Review your work:

```bash
git status
git diff
```

Commit the role:

```bash
git add .
git commit -m "Implement server baseline role"
```

Review your commit history:

```bash
git log --oneline --decorate
```

A professional project should contain logical commits rather than one giant end-of-day commit.

Suggested milestones:

```text
Configure student inventory
Customize variable and module exercises
Implement webserver and templates
Implement system reporting
Implement server baseline role
```

---

# 21. End-of-day self-check

You should now be able to answer all of these questions without looking at the solutions:

1. What is the difference between an ad-hoc command and a playbook?
2. What does `ansible.builtin.ping` actually test?
3. Where does this project get its inventory path from?
4. What is the purpose of SSH public-key authentication?
5. What is the difference between a YAML list and dictionary?
6. How do you reference an item in a list?
7. How do you reference a key in a dictionary?
8. Why prefer a module such as `package` or `file` over a shell command?
9. What is an Ansible collection?
10. What does `when` do?
11. What does `register` do?
12. What are Ansible facts?
13. When are loops useful?
14. Why can passing an entire package list be better than looping over it?
15. What belongs in a role's `defaults/`, `tasks/`, `handlers/`, and `templates/` directories?
16. Why should top-level playbooks remain small once roles are used?
17. What is a Jinja2 template used for?
18. When should you use `shell` instead of `command`?
19. What is idempotency?
20. Why are `--check`, `--diff`, and `--limit` useful before production rollout?

---

# Command cheat sheet

```bash
# Version and configuration
ansible --version
ansible-config dump --only-changed

# Module help
ansible-doc ansible.builtin.copy
ansible-doc ansible.builtin.file
ansible-doc ansible.builtin.package

# Inventory
ansible-inventory --graph
ansible-inventory --list
ansible managed --list-hosts

# Connectivity
ansible managed -m ansible.builtin.ping

# Ad-hoc command
ansible managed -m ansible.builtin.command -a "hostname"

# Privileged command
ansible managed -b -m ansible.builtin.command -a "id"

# Playbook
ansible-playbook site.yml

# Syntax validation
ansible-playbook site.yml --syntax-check

# Limit execution
ansible-playbook site.yml --limit rhel1

# Check/diff
ansible-playbook site.yml --check
ansible-playbook site.yml --check --diff

# Verbosity
ansible-playbook site.yml -v
ansible-playbook site.yml -vv

# Facts
ansible managed -m ansible.builtin.setup

# Collections
ansible-galaxy collection list
ansible-galaxy collection install -r requirements.yml -p ./collections

# Create a role
ansible-galaxy role init roles/example

# Git
git status
git diff
git add .
git commit -m "Description"
git log --oneline
```

---

# Repository structure

```text
ansible-deep-dive-workshop/
├── ansible.cfg
├── .gitignore
├── README.md
├── INSTRUCTOR.md
├── requirements.yml
├── site.yml
├── inventory/
│   ├── hosts.yml
│   ├── group_vars/
│   │   └── managed.yml
│   └── host_vars/
│       ├── rhel1.yml
│       ├── rhel2.yml
│       └── rhel3.yml
├── vars/
│   └── webserver.yml
├── playbooks/
│   ├── 01_ping.yml
│   ├── 02_hostname.yml
│   ├── 03_directory.yml
│   ├── 04_file.yml
│   ├── 10_variables.yml
│   ├── 11_lists.yml
│   ├── 12_dictionary.yml
│   ├── 13_varfile.yml
│   ├── 20_packages.yml
│   ├── 21_service.yml
│   ├── 22_files.yml
│   ├── 23_users.yml
│   ├── 24_lineinfile.yml
│   ├── 25_firewall.yml
│   ├── 26_ini.yml
│   ├── 30_condition_basic.yml
│   ├── 31_condition_string.yml
│   ├── 32_condition_multiple.yml
│   ├── 32b_condition_advanced.yml
│   ├── 33_register.yml
│   ├── 33b_register_condition.yml
│   ├── 34_facts.yml
│   ├── 40_loop_basic.yml
│   ├── 41_loop_packages.yml
│   └── 42_loop_dictionary.yml
└── roles/
    ├── webserver/
    ├── training_app/
    ├── system_report/
    └── server_baseline/
```

Have fun automating, and remember: if you perform the same manual change more than once, ask whether Ansible should be doing it for you.
