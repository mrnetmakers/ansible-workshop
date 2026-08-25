[← Chapter 4](../4/) | [↑ Workshop index](../../) | [Chapter 6 →](../6/)

---

# 5. Inventory and First Remote Execution

In this exercise, you will create your first Ansible inventory and use it to run commands against the managed RHEL systems.

Before you start, make sure you are working as your assigned `studXX` user on `rhelmain`.

Check:

```bash
whoami
hostname
pwd
```

You should be:

```text
studXX
rhelmain
/home/studXX/ansible-workshop
```

If necessary, return to your workshop directory:

```bash
cd ~/ansible-workshop
```

---

## 5.1 What is an Ansible inventory?

Ansible needs to know which systems it should manage.

This information is stored in an **inventory**.

An inventory can contain:

- hostnames
- IP addresses
- groups of hosts
- connection information
- host-specific variables
- group-specific variables

For this workshop, the managed systems are:

```text
rhel1
rhel2
rhel3
```

We will create one group named:

```text
managed
```

and place all three hosts into that group.

---

## 5.2 Determine the IP addresses

Before adding hosts to the inventory, verify that `rhelmain` can resolve the names of the managed systems.

A simple test is:

```bash
getent hosts rhel1
```

You should see output similar to:

```text
192.168.10.101   rhel1
```

Repeat this for all managed hosts:

```bash
getent hosts rhel1
getent hosts rhel2
getent hosts rhel3
```

`getent hosts` is generally more useful than `ping` for this check because it directly shows which IP address the operating system resolves for a hostname.

You can also use:

```bash
ping -c 1 rhel1
```

The first line usually shows the resolved address:

```text
PING rhel1 (192.168.10.101) 56(84) bytes of data.
```

Repeat if needed:

```bash
ping -c 1 rhel2
ping -c 1 rhel3
```

Do not worry if ICMP echo requests are blocked. In that case, the hostname may still resolve correctly even though `ping` does not receive a reply.

For checking name resolution, prefer:

```bash
getent hosts rhel1
```

---

## 5.3 Verify the remote system identity

It is also useful to verify that each hostname actually connects to the system you expect.

From `rhelmain`, run:

```bash
ssh studXX@rhel1 hostname
```

Replace `studXX` with your username.

Expected output:

```text
rhel1
```

Repeat:

```bash
ssh studXX@rhel2 hostname
ssh studXX@rhel3 hostname
```

You should receive:

```text
rhel2
rhel3
```

This checks more than DNS resolution. It verifies:

1. the hostname resolves;
2. SSH connectivity works;
3. your SSH key works;
4. you are reaching the expected system.

If this does not work, fix the SSH problem before continuing with Ansible.

---

## 5.4 Create the inventory directory

Check whether the inventory directory already exists:

```bash
ls
```

If necessary, create it:

```bash
mkdir -p inventory
```

Now create the inventory file:

```bash
vi inventory/hosts.yml
```

Add:

```yaml
---
all:
  children:
    managed:
      hosts:
        rhel1:
          ansible_host: 192.168.10.101

        rhel2:
          ansible_host: 192.168.10.102

        rhel3:
          ansible_host: 192.168.10.103
```

Replace the example IP addresses with the addresses from your environment.

---

## 5.5 Understand the inventory structure

The inventory contains several levels.

At the top:

```yaml
all:
```

`all` represents all hosts known to this inventory.

Underneath that:

```yaml
children:
```

we define groups.

Our group is:

```yaml
managed:
```

Inside that group are the hosts:

```yaml
hosts:
  rhel1:
  rhel2:
  rhel3:
```

For each host, we define:

```yaml
ansible_host:
```

For example:

```yaml
rhel1:
  ansible_host: 192.168.10.101
```

This means:

> In Ansible, call this host `rhel1`, but connect to `192.168.10.101`.

The name:

```text
rhel1
```

is the **inventory hostname**.

The value:

```text
192.168.10.101
```

is the actual SSH connection target.

This separation is useful because playbooks can use stable, readable names even if IP addresses change.

---

## 5.6 Why not just use IP addresses as hostnames?

Technically, you could create an inventory like:

```yaml
hosts:
  192.168.10.101:
  192.168.10.102:
```

But this is harder to read.

Compare:

```bash
ansible 192.168.10.101 -m ansible.builtin.ping
```

with:

```bash
ansible rhel1 -m ansible.builtin.ping
```

The second version is much easier to understand.

Meaningful inventory names are therefore preferable.

---

## 5.7 Check your Ansible configuration

Your project-specific `ansible.cfg` should point Ansible to the inventory file used for this workshop.

Check:

```bash
cat ansible.cfg
```

You should see a setting similar to:

```ini
[defaults]
inventory = ./inventory/hosts.yml
```

This tells Ansible to use:

```text
inventory/hosts.yml
```

as the default inventory for this project.

You can verify which configuration file Ansible is currently using with:

```bash
ansible --version
```

Look for:

```text
config file =
```

It should point to the `ansible.cfg` inside your workshop directory.

---

### Configure your remote user

The SSH user for the managed hosts is **not configured in `ansible.cfg`**.

For this workshop, the remote user is defined as a group variable for all hosts in the `managed` group.

Open:

```bash
vi inventory/group_vars/managed.yml
```

You should find:

```yaml
---
ansible_user: studXX
```

Replace:

```text
studXX
```

with your assigned student account.

For example:

```yaml
---
ansible_user: stud01
```

Save the file.


## 5.8 Validate the inventory

Before running anything remotely, ask Ansible to read the inventory.

Run:

```bash
ansible-inventory --graph
```

You should see something similar to:

```text
@all:
  |--@ungrouped:
  |--@managed:
  |  |--rhel1
  |  |--rhel2
  |  |--rhel3
```

This confirms that Ansible recognizes:

- the `managed` group;
- all three hosts.

If a host is missing, check your YAML indentation carefully.

---

## 5.10 Display the complete inventory

You can also ask Ansible to display the parsed inventory:

```bash
ansible-inventory --list
```

This produces much more output.

For a smaller view, try:

```bash
ansible-inventory --host rhel1
```

You should see information similar to:

```json
{
    "ansible_host": "192.168.10.101"
}
```

Try:

```bash
ansible-inventory --host rhel2
```

This is useful for checking which variables Ansible associates with a particular host.

---

## 5.11 List hosts without connecting to them

Before executing a command, you can ask Ansible which systems would be targeted.

Run:

```bash
ansible managed --list-hosts
```

Expected output:

```text
  hosts (4):
    rhel1
    rhel2
    rhel3
```

Try a single host:

```bash
ansible rhel1 --list-hosts
```

Expected:

```text
  hosts (1):
    rhel1
```

This is a very useful habit when working with larger inventories.

Before making a change, always make sure your host pattern selects the systems you actually intend to manage.

---

## 5.12 Your first remote Ansible connection

Now use Ansible's `ping` module.

Run:

```bash
ansible rhel1 -m ansible.builtin.ping
```

If everything is configured correctly, you should see output similar to:

```text
rhel1 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

This is an important milestone.

Ansible has now:

1. read your inventory;
2. selected `rhel1`;
3. connected through SSH;
4. authenticated using your SSH key;
5. executed an Ansible module remotely;
6. returned the result.

---

## 5.13 Ansible ping is not network ping

The command:

```bash
ping rhel1
```

uses the ICMP network protocol.

The command:

```bash
ansible rhel1 -m ansible.builtin.ping
```

does something different.

The Ansible `ping` module verifies that Ansible can successfully communicate with and execute code on the managed host.

A successful:

```text
pong
```

therefore tells you much more than a normal network ping.

It confirms that the basic Ansible communication path works.

---

## 5.14 Ping all managed hosts

Now run:

```bash
ansible managed -m ansible.builtin.ping
```

You should receive a successful result from all three hosts.

For example:

```text
rhel1 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}

rhel2 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}

rhel3 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}

```

If one host fails while the others succeed, troubleshoot that host separately.

For example:

```bash
ssh studXX@rhel3 hostname
```

Then:

```bash
ansible rhel3 -m ansible.builtin.ping -vv
```

The additional `-vv` option provides more information about what Ansible is doing.

---

## 5.15 Execute your first remote command

Now run a real command on all managed hosts:

```bash
ansible managed \
  -m ansible.builtin.command \
  -a "hostname"
```

You should receive each remote hostname.

Example:

```text
rhel1 | CHANGED | rc=0 >>
rhel1

rhel2 | CHANGED | rc=0 >>
rhel2
```

The module used here is:

```text
ansible.builtin.command
```

The argument:

```text
hostname
```

is the command that should be executed remotely.

---

## 5.16 Find out which user Ansible uses

Run:

```bash
ansible managed \
  -m ansible.builtin.command \
  -a "whoami"
```

Every host should return your student account:

```text
studXX
```

For example:

```text
rhel1 | CHANGED | rc=0 >>
stud01
```

This confirms that Ansible is connecting with the account configured in:

```text
ansible.cfg
```

---

## 5.17 Run several useful commands

Try:

```bash
ansible managed \
  -m ansible.builtin.command \
  -a "uname -r"
```

This displays the kernel version.

Try:

```bash
ansible managed \
  -m ansible.builtin.command \
  -a "uptime"
```

Try:

```bash
ansible managed \
  -m ansible.builtin.command \
  -a "id"
```

Try:

```bash
ansible managed \
  -m ansible.builtin.command \
  -a "cat /etc/redhat-release"
```

Compare the output from all three hosts.

---

## 5.18 Target individual hosts

Ansible does not always have to target an entire group.

Run:

```bash
ansible rhel1 \
  -m ansible.builtin.command \
  -a "hostname"
```

Then:

```bash
ansible rhel3 \
  -m ansible.builtin.command \
  -a "hostname"
```

The first argument after `ansible` is called a **host pattern**.

Examples:

```text
managed
rhel1
rhel2
all
```

---

## 5.19 Target multiple specific hosts

You can also target multiple hosts with a pattern.

For example:

```bash
ansible 'rhel1:rhel2' \
  -m ansible.builtin.command \
  -a "hostname"
```

This targets:

```text
rhel1
rhel2
```

Try:

```bash
ansible 'rhel2:rhel3' \
  -m ansible.builtin.command \
  -a "uptime"
```

The quotes are a good habit because some shell characters used in Ansible host patterns can otherwise be interpreted by the shell.

---

## 5.20 Use all hosts

The special group:

```text
all
```

contains every host in the inventory.

Try:

```bash
ansible all -m ansible.builtin.ping
```

In our current inventory, this produces effectively the same result as:

```bash
ansible managed -m ansible.builtin.ping
```

because all three systems currently belong to the `managed` group.

Later, when the inventory contains multiple groups, `all` and `managed` may no longer mean the same thing.

---

## 5.21 Create your first remote playbook

So far, you have used **ad-hoc commands**.

Ad-hoc commands are useful for quick, one-time operations.

For repeatable automation, we normally use **playbooks**.

Create:

```bash
vi playbooks/02_remote_ping.yml
```

Add:

```yaml
---
- name: Verify connectivity to managed hosts
  hosts: managed
  gather_facts: false

  tasks:
    - name: Ping managed hosts
      ansible.builtin.ping:
```

Check the syntax:

```bash
ansible-playbook playbooks/02_remote_ping.yml --syntax-check
```

Then execute it:

```bash
ansible-playbook playbooks/02_remote_ping.yml
```

You should receive successful results from all three managed hosts.

---

## 5.22 Create a hostname playbook

Create:

```bash id="ng9yex"
vi playbooks/03_remote_hostname.yml
```

Add:

```yaml id="dl4mta"
---
- name: Display remote hostnames
  hosts: managed
  gather_facts: false

  tasks:
    - name: Get hostname
      ansible.builtin.command:
        cmd: hostname
      changed_when: false
```

Run:

```bash id="1jewg0"
ansible-playbook playbooks/03_remote_hostname.yml
```

Notice:

```yaml id="hcc9r9"
changed_when: false
```

The `hostname` command only reads information. It does not modify the managed host.

Without this setting, the `command` module normally reports the task as:

```text id="k5anli"
changed
```

By adding:

```yaml id="hvtc2m"
changed_when: false
```

we tell Ansible:

> This command does not modify the target system.

The result should therefore be reported as:

```text id="v8pjrj"
ok
```

instead of:

```text id="v9alws"
changed
```

---

### Store and display the command result

So far, Ansible executed the `hostname` command, but we did not use its result in another task.

Ansible can store the result of a task in a variable using:

```text id="81yfxr"
register
```

Modify your playbook:

```yaml id="o4z8cf"
---
- name: Display remote hostnames
  hosts: managed
  gather_facts: false

  tasks:
    - name: Get hostname
      ansible.builtin.command:
        cmd: hostname
      register: hostname_result
      changed_when: false

    - name: Display hostname
      ansible.builtin.debug:
        msg: "The hostname of {{ inventory_hostname }} is {{ hostname_result.stdout }}"
```

Run the playbook again:

```bash id="2b6ehy"
ansible-playbook playbooks/03_remote_hostname.yml
```

You should now see output similar to:

```text id="ff39zk"
TASK [Display hostname]
ok: [rhel1] => {
    "msg": "The hostname of rhel1 is rhel1"
}
```

The line:

```yaml id="g45t5u"
register: hostname_result
```

stores the result of the command in a variable named:

```text id="7me03y"
hostname_result
```

Command results contain several values. One of the most commonly used is:

```text id="ehddg4"
stdout
```

which contains the standard output of the command.

Therefore:

```text id="kjcdaz"
{{ hostname_result.stdout }}
```

contains the output produced by:

```bash id="uw1f3i"
hostname
```

You can inspect the **complete registered result** by temporarily adding:

```yaml id="x3o0vu"
    - name: Display complete command result
      ansible.builtin.debug:
        var: hostname_result
```

Run the playbook again and look for values such as:

```text id="vtidty"
stdout
stderr
rc
changed
```

You will work with `register` in more detail later in the workshop. For now, remember the basic pattern:

```text id="k87k32"
Task executes
     ↓
register
     ↓
Variable stores result
     ↓
debug / msg uses result
```

## 5.23 Create a file remotely

Now create a playbook that actually changes the remote systems.

Create:

```bash
vi playbooks/05_create_training_file.yml
```

Add:

```yaml
---
- name: Create a training file
  hosts: managed
  gather_facts: false

  tasks:
    - name: Create workshop information file
      ansible.builtin.copy:
        dest: "/tmp/ansible-training-{{ ansible_user }}.txt"
        content: |
          This file was created by Ansible.
          Inventory host: {{ inventory_hostname }}
          Remote user: {{ ansible_user }}
        mode: "0644"
```

Run:

```bash
ansible-playbook playbooks/05_create_training_file.yml
```

This time, Ansible should report:

```text
changed
```

because a file was created.

---

## 5.24 Verify the file

Use an ad-hoc command:

```bash
ansible managed \
  -m ansible.builtin.command \
  -a "cat /tmp/ansible-training-$USER.txt"
```

You should see different inventory hostnames on the different systems.

For example:

```text
This file was created by Ansible.
Inventory host: rhel1
Remote user: stud01
```

and on another system:

```text
This file was created by Ansible.
Inventory host: rhel3
Remote user: stud01
```

The same playbook therefore generated host-specific content.

---

## 5.25 Run the playbook a second time

Run again:

```bash
ansible-playbook playbooks/05_create_training_file.yml
```

This time, the task should normally report:

```text
ok
```

instead of:

```text
changed
```

Why?

Because the file already exists with exactly the content Ansible expects.

Ansible checks the desired state and sees that no modification is required.

This introduces one of the most important Ansible concepts:

> **Idempotency**

A well-written Ansible playbook can normally be executed repeatedly without making unnecessary changes.

---

## 5.26 Challenge

Complete the following tasks yourself.

## Task 1

Create a playbook named:

```text
playbooks/06_student_info.yml
```

It should run against:

```text
managed
```

and display:

```text
hostname
whoami
uname -r
uptime
```

All information-gathering tasks should report:

```text
ok
```

instead of:

```text
changed
```

---

## Task 2

Create another playbook:

```text
playbooks/07_student_directory.yml
```

It should create:

```text
/tmp/ansible-workshop-studXX
```

on all managed systems. Replace studXX with your student id.

Use:

```text
ansible.builtin.file
```

instead of the `command` module.

Use:

```bash
ansible-doc ansible.builtin.file
```

if you need help.

The directory should have mode:

```text
0755
```

---

## Task 3

Run your directory playbook twice.

Compare the output from the first and second execution.

Be prepared to explain why the results are different.

---

## 5.27 Useful troubleshooting commands

If something does not work, troubleshoot from the bottom up.

First verify hostname resolution:

```bash
getent hosts rhel1
```

Then verify SSH:

```bash
ssh studXX@rhel1 hostname
```

Then verify Ansible inventory:

```bash
ansible-inventory --graph
```

Then verify the specific host:

```bash
ansible rhel1 -m ansible.builtin.ping
```

For more verbose output:

```bash
ansible rhel1 -m ansible.builtin.ping -vv
```

This gives you a useful troubleshooting sequence:

```text
Name resolution
      ↓
SSH
      ↓
Inventory
      ↓
Ansible connectivity
      ↓
Playbook
```

Try to identify which layer is failing before changing configuration.

---

## 5.28 What did we learn?

In this exercise, you learned how to:

- verify the IP address associated with a hostname;
- test SSH connectivity before using Ansible;
- create a YAML inventory;
- define inventory groups;
- use readable inventory hostnames with `ansible_host`;
- inspect an inventory with `ansible-inventory`;
- select hosts using Ansible host patterns;
- run ad-hoc commands;
- use `ansible.builtin.ping`;
- execute remote commands;
- create your first remote playbooks;
- distinguish between `ok` and `changed`;
- understand the basic idea of idempotency.

You now have the basic communication path required for the rest of the workshop:

```text
rhelmain
   |
   | Ansible
   | SSH as studXX
   |
   +------> rhel1
   +------> rhel2
   +------> rhel3
```

## Next

In the next exercise, you will work more deeply with **Ansible variables, lists, dictionaries, and external variable files**.

---

[← Chapter 4](../4/) | [↑ Workshop index](../../) | [Chapter 6 →](../6/)
