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
git clone https://github.com/mrnetmakers/ansible-workshop.git ~/ansible-workshop
cd ~/ansible-workshop
```

Inspect the repository:

```bash
find . -maxdepth 3 -type f | sort
```

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

Verify these tools are present:

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

# 2. Learn YAML Syntax – Build Your First Playbook

Ansible playbooks are written in **YAML**. Before we start configuring remote systems, we need to understand a few basic YAML concepts.

Instead of learning YAML separately from Ansible, you will create a small playbook that defines different types of data and prints their values.

By the end of this exercise, you will know how to work with:

- strings
- numbers
- booleans
- lists
- dictionaries
- lists containing dictionaries

You will also create and execute your **first Ansible playbook**.

---

## 2.1 Create a directory for your workshop

Enter the workshop directory:

```bash
cd ~/ansible-workshop
```

Verify your current location:

```bash
pwd
```

You should see something similar to:

```text
/home/stud01/ansible-workshop
```

---

## 2.2 Understanding YAML indentation

YAML uses **indentation to describe structure**.

Unlike some programming languages, YAML does not use `{ }` or other characters to group blocks of information.

For example:

```yaml
server:
  hostname: server01
  port: 8080
```

`hostname` and `port` belong to `server` because they are indented underneath it.

### Important YAML rules

Keep these rules in mind throughout the workshop:

1. Use **spaces**, not tabs.
2. Indentation must be consistent.
3. A key and value are separated by a colon:

```yaml
course: Ansible Deep Dive
```

4. Lists use a dash:

```yaml
packages:
  - httpd
  - curl
  - vim-enhanced
```

5. Ansible playbooks usually start with:

```yaml
---
```

The `---` indicates the beginning of a YAML document.

---

# 2.3 Create your first playbook

Create a new file:

```bash
vi playbooks/01_yaml_basics.yml
```

Start with the following:

```yaml
---
- name: Learn YAML data types
  hosts: localhost
  gather_facts: false

  vars:

  tasks:
```

Do not execute it yet. We are going to add different variables first.

---

# 2.4 Strings

A **string** represents text.

Examples include:

```text
Ansible Deep Dive
development
server01
/etc/httpd/conf/httpd.conf
```

Strings are commonly used for things such as:

- usernames
- hostnames
- package names
- service names
- file paths
- environment names
- configuration values

Add the following underneath `vars:`:

```yaml
    course_name: "Ansible Deep Dive"
    student_name: "stud01"
    environment: "training"
```

Replace `stud01` with your own student account.

Your playbook should now look like:

```yaml
---
- name: Learn YAML data types
  hosts: localhost
  gather_facts: false

  vars:
    course_name: "Ansible Deep Dive"
    student_name: "stud01"
    environment: "training"

  tasks:
```

Quotes are optional for many strings, so this would also be valid:

```yaml
course_name: Ansible Deep Dive
```

Using quotes can make the intended data type clearer and avoids ambiguity for certain values.

---

# 2.5 Numbers

Numbers can be stored directly without quotes.

Add the following variables:

```yaml
    course_duration: 8
    number_of_servers: 3
    webserver_port: 8080
```

Numbers are useful for values such as:

- TCP/UDP ports
- timeouts
- retry counts
- memory limits
- number of processes
- thresholds

For example:

```yaml
webserver_port: 8080
```

is a number.

Compare this with:

```yaml
webserver_port: "8080"
```

The second value is a **string** because it is quoted.

---

# 2.6 Booleans

A boolean represents a value that is either **true** or **false**.

Add:

```yaml
    install_webserver: true
    enable_firewall: true
    enable_debugging: false
```

Booleans are particularly useful for enabling or disabling functionality.

For example, later we could write:

```yaml
install_webserver: true
```

and use that variable to decide whether Ansible should install a web server.

Typical use cases include:

```yaml
enable_firewall: true
create_users: true
enable_debugging: false
start_service: true
```

We will use booleans later when working with **conditionals**.

---

# 2.7 Lists

Sometimes one variable needs to contain **multiple values**.

For example, we may want Ansible to install several packages.

Add:

```yaml
    packages:
      - httpd
      - curl
      - vim-enhanced
      - tar
```

This is called a **list**.

Lists are frequently used in Ansible for things such as:

- packages
- users
- services
- directories
- firewall ports
- files
- hostnames

Each list item begins with `-`.

Another example would be:

```yaml
    administrators:
      - alice
      - bob
      - charlie
```

Later in the workshop, you will use **loops** to process every item in a list.

---

# 2.8 Dictionaries

A dictionary groups related information together using **key/value pairs**.

Add:

```yaml
    webserver:
      package: httpd
      service: httpd
      port: 80
      document_root: /var/www/html
```

Here, `webserver` contains four related values.

This is useful because these variables logically belong together.

Instead of creating:

```yaml
webserver_package: httpd
webserver_service: httpd
webserver_port: 80
webserver_document_root: /var/www/html
```

we can group them:

```yaml
webserver:
  package: httpd
  service: httpd
  port: 80
  document_root: /var/www/html
```

Dictionaries are useful for representing structured configuration such as:

- application settings
- server configuration
- user properties
- network configuration
- database configuration

---

# 2.9 Lists of dictionaries

Lists and dictionaries can also be combined.

Imagine that we want to create several users. Each user has multiple properties.

Add:

```yaml
    training_users:
      - name: alice
        department: development
        shell: /bin/bash

      - name: bob
        department: operations
        shell: /bin/bash

      - name: charlie
        department: security
        shell: /sbin/nologin
```

`training_users` is a **list**.

Each item in that list is a **dictionary**.

Conceptually, the structure looks like:

```text
training_users
    |
    +-- user 1
    |     name
    |     department
    |     shell
    |
    +-- user 2
    |     name
    |     department
    |     shell
    |
    +-- user 3
          name
          department
          shell
```

This is one of the most useful data structures in Ansible.

Later, you will use exactly this type of structure together with loops to create multiple users.

---

# 2.10 Your variables so far

Before continuing, compare the `vars:` section of your playbook.

It should look similar to:

```yaml
  vars:
    course_name: "Ansible Deep Dive"
    student_name: "stud01"
    environment: "training"

    course_duration: 8
    number_of_servers: 3
    webserver_port: 8080

    install_webserver: true
    enable_firewall: true
    enable_debugging: false

    packages:
      - httpd
      - curl
      - vim-enhanced
      - tar

    webserver:
      package: httpd
      service: httpd
      port: 80
      document_root: /var/www/html

    training_users:
      - name: alice
        department: development
        shell: /bin/bash

      - name: bob
        department: operations
        shell: /bin/bash

      - name: charlie
        department: security
        shell: /sbin/nologin
```

---

# 2.11 Print a string variable

Now we need some tasks.

Under `tasks:`, add:

```yaml
    - name: Display course information
      ansible.builtin.debug:
        msg: "Welcome {{ student_name }} to {{ course_name }}!"
```

The expression:

```text
{{ student_name }}
```

tells Ansible to replace it with the value stored in the variable.

The same applies to:

```text
{{ course_name }}
```

---

# 2.12 Print number and boolean variables

Add another task:

```yaml
    - name: Display basic variables
      ansible.builtin.debug:
        msg:
          - "Course duration: {{ course_duration }} hours"
          - "Number of managed servers: {{ number_of_servers }}"
          - "Web server port: {{ webserver_port }}"
          - "Install web server: {{ install_webserver }}"
          - "Enable firewall: {{ enable_firewall }}"
          - "Enable debugging: {{ enable_debugging }}"
```

Notice that `msg` can itself contain a list.

---

# 2.13 Print a complete list

Add:

```yaml
    - name: Display package list
      ansible.builtin.debug:
        var: packages
```

`debug` can display a complete variable using:

```yaml
var: variable_name
```

---

# 2.14 Access individual list elements

We can also access individual elements.

Add:

```yaml
    - name: Display individual packages
      ansible.builtin.debug:
        msg:
          - "First package: {{ packages[0] }}"
          - "Second package: {{ packages[1] }}"
          - "Third package: {{ packages[2] }}"
```

List positions start with **0**, not 1.

Therefore:

```text
packages[0]  → httpd
packages[1]  → curl
packages[2]  → vim-enhanced
packages[3]  → tar
```

---

# 2.15 Access dictionary values

Now access information from the `webserver` dictionary.

Add:

```yaml
    - name: Display web server configuration
      ansible.builtin.debug:
        msg:
          - "Package: {{ webserver.package }}"
          - "Service: {{ webserver.service }}"
          - "Port: {{ webserver.port }}"
          - "Document root: {{ webserver.document_root }}"
```

The expression:

```text
{{ webserver.port }}
```

means:

> Read the value `port` from the dictionary `webserver`.

---

# 2.16 Access a list containing dictionaries

Finally, add:

```yaml
    - name: Display information about one user
      ansible.builtin.debug:
        msg:
          - "Username: {{ training_users[0].name }}"
          - "Department: {{ training_users[0].department }}"
          - "Shell: {{ training_users[0].shell }}"
```

Look closely at:

```text
training_users[0].department
```

It means:

1. Open the `training_users` list.
2. Select item `0`, the first user.
3. Read its `department` property.

---

# 2.17 Check your playbook

Before executing a playbook, it is a good habit to check its syntax.

Run:

```bash
ansible-playbook playbooks/01_yaml_basics.yml --syntax-check
```

You should receive output similar to:

```text
playbook: playbooks/01_yaml_basics.yml
```

If you receive an error, carefully check:

- indentation;
- missing `:`;
- incorrect `-`;
- tabs instead of spaces.

Fix all errors before continuing.

---

# 2.18 Execute your first playbook

Now execute it:

```bash
ansible-playbook playbooks/01_yaml_basics.yml
```

Study the output.

You should see your variables being resolved by Ansible.

For example:

```text
TASK [Display course information]
ok: [localhost] => {
    "msg": "Welcome stud01 to Ansible Deep Dive!"
}
```

You should also see the package list and the web server configuration.

Congratulations — you have written and executed your first Ansible playbook.

---

# 2.19 Challenge – Extend the data model

Do not copy an example for this exercise. Modify your playbook yourself.

### Task 1 – Add another string

Create a variable containing the name of your favorite Linux command.

Print it using `debug`.

### Task 2 – Add another boolean

Create:

```yaml
reboot_allowed:
```

Decide whether its value should be `true` or `false`.

Print the value.

### Task 3 – Extend the package list

Add two additional packages to:

```yaml
packages:
```

Print the complete list again.

# 2.20 Bonus Challenge – Intentionally break YAML

Understanding errors is an important part of learning Ansible.

Make a copy of your working playbook:

```bash
cp playbooks/01_yaml_basics.yml playbooks/01_yaml_broken.yml
```

Open it:

```bash
vi playbooks/01_yaml_broken.yml
```

Find:

```yaml
    packages:
      - httpd
      - curl
```

Change it to:

```yaml
    packages:
      - httpd
        - curl
```

Now run:

```bash
ansible-playbook playbooks/01_yaml_broken.yml --syntax-check
```

Read the error message carefully.

Try to identify:

1. approximately where the problem occurred;
2. what is wrong with the YAML structure;
3. how Ansible reports YAML syntax errors.

Fix the file and run the syntax check again.

---

# 2.21 What did we learn?

You have already used the most important YAML data structures that you will encounter during the rest of this workshop:

| Data type | Example | Typical Ansible use |
|---|---|---|
| String | `"httpd"` | Package names, usernames, paths, environments |
| Number | `8080` | Ports, limits, timeouts, thresholds |
| Boolean | `true` | Enable/disable functionality |
| List | `[httpd, curl, tar]` | Packages, users, services, files |
| Dictionary | `webserver: ...` | Structured configuration |
| List of dictionaries | `training_users: ...` | Multiple structured objects |

You do not need to memorize every YAML feature.

For Ansible, the most important question is usually:

> **What kind of data do I need to represent?**

If it is one value, use a simple variable:

```yaml
environment: production
```

If it is multiple similar values, consider a list:

```yaml
packages:
  - httpd
  - curl
  - tar
```

If several values belong together, consider a dictionary:

```yaml
webserver:
  package: httpd
  service: httpd
  port: 80
```

If you have multiple objects and every object has several properties, a list of dictionaries is often the right choice:

```yaml
users:
  - name: alice
    shell: /bin/bash

  - name: bob
    shell: /bin/bash
```

You will encounter all of these structures again throughout the workshop.


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

# 4. Prepare SSH Key Authentication

Ansible normally connects to Linux managed hosts using SSH.

In our lab environment, you have three RHEL systems:

```text
rhelmain    Ansible control node
rhel1       Managed host
rhel2       Managed host
rhel3       Managed host
```

You initially access these systems using the `ec_user` account and the SSH key provided for the lab.

However, **Ansible should not run as `ec_user`**.

Each student has a dedicated account named:

```text
studXX
```

For example:

```text
stud01
stud02
stud03
...
```

Your goal in this exercise is to configure SSH public-key authentication so that your `studXX` account on `rhelmain` can connect directly to the same `studXX` account on all three managed hosts.

At the end of the exercise, the following should work **without entering a password**:

```bash
ssh studXX@rhel1
ssh studXX@rhel2
ssh studXX@rhel3
```

---

# 4.1 Understand the authentication setup

There are two different SSH authentication scenarios in this lab.

## Initial lab access

You connect to the RHEL instances as:

```text
ec_user
```

using the SSH private key provided for the lab.

For example, from your workstation you might connect with a command similar to:

```bash
ssh -i <provided-key> ec_user@<server>
```

The exact connection information will be provided by your instructor.

## Ansible communication

Ansible will later connect from:

```text
rhelmain
```

to:

```text
rhel1
rhel2
rhel3
```

using your personal:

```text
studXX
```

account.

For example:

```text
                    SSH
                    │
                    │  stud01
                    ▼
              +-----------+
              |   rhel1   |
              +-----------+
                    ▲
                    │
+-----------+       │
| rhelmain  |-------+
|           |-------+-----> rhel2
|  stud01   |-------+-----> rhel3
+-----------+

Private key:
~/.ssh/id_ed25519

Public key installed on remote hosts:
~/.ssh/authorized_keys
```

We therefore need to create an SSH key pair for `studXX` on `rhelmain` and install its **public key** on each managed host.

---

# 4.2 Switch to your student account on rhelmain

First connect to `rhelmain` using the `ec_user` account as described by your instructor.

Check your current user:

```bash
whoami
```

You should see:

```text
ec_user
```

Now switch to your assigned student account.

For example, if you are `stud01`:

```bash
sudo su - stud01
```

Replace `stud01` with your assigned username.

Check again:

```bash
whoami
```

You should now see:

```text
stud01
```

Also check your home directory:

```bash
pwd
```

You should see something similar to:

```text
/home/stud01
```

The `-` in:

```bash
sudo su - stud01
```

is important. It starts a login shell and switches to the target user's environment and home directory.

---

# 4.3 Examine your SSH directory

Check whether an SSH directory already exists:

```bash
ls -la ~/.ssh
```

If it does not exist, you may see:

```text
ls: cannot access '/home/stud01/.ssh': No such file or directory
```

That is fine.

If the directory already exists, inspect its contents carefully.

You may see files such as:

```text
known_hosts
authorized_keys
```

Do not delete existing SSH configuration unless instructed to do so.

---

# 4.4 Generate your SSH key pair

We will create an Ed25519 SSH key pair.

Run:

```bash
ssh-keygen -t ed25519
```

You will be asked:

```text
Enter file in which to save the key (/home/stud01/.ssh/id_ed25519):
```

Press **Enter** to accept the default.

For this isolated training environment, follow your instructor's direction regarding the passphrase. If instructed to create the key without a passphrase, press **Enter** twice when prompted.

Afterwards, you should see output similar to:

```text
Your identification has been saved in /home/stud01/.ssh/id_ed25519
Your public key has been saved in /home/stud01/.ssh/id_ed25519.pub
```

---

# 4.5 Examine the generated keys

List your SSH directory:

```bash
ls -la ~/.ssh
```

You should now have at least:

```text
id_ed25519
id_ed25519.pub
```

These two files have very different purposes.

## Private key

```text
~/.ssh/id_ed25519
```

This is your **private key**.

It must remain private.

Never:

- copy it to the managed hosts;
- put it into a Git repository;
- send it to another student;
- paste it into documentation;
- publish it anywhere.

Check its permissions:

```bash
ls -l ~/.ssh/id_ed25519
```

It should normally only be readable by you.

---

## Public key

```text
~/.ssh/id_ed25519.pub
```

This is your **public key**.

The public key is intended to be copied to systems that should allow you to log in.

Display it:

```bash
cat ~/.ssh/id_ed25519.pub
```

The output will look similar to:

```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... stud01@rhelmain
```

The exact value will be different for every student.

The entire output is **one public key**.

---

# 4.6 Understand authorized_keys

On a remote Linux system, SSH normally checks:

```text
~/.ssh/authorized_keys
```

to determine which public keys are allowed to authenticate as that user.

For example, when connecting as:

```text
stud01
```

to `rhel1`, SSH will check:

```text
/home/stud01/.ssh/authorized_keys
```

on `rhel1`.

Conceptually:

```text
rhelmain
========

/home/stud01/.ssh/id_ed25519
             |
             | proves possession
             |
             +----------------------------+
                                          |
                                          v

rhel1
=====

/home/stud01/.ssh/authorized_keys

contains:

ssh-ed25519 AAAA... stud01@rhelmain
```

The **private key remains on `rhelmain`**.

Only the **public key** is added to `authorized_keys` on the managed hosts.

---

# 4.7 Copy your public key

On `rhelmain`, make sure you are still your student user:

```bash
whoami
```

Now display your public key:

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the **complete line** to your clipboard.

It starts with:

```text
ssh-ed25519
```

Make sure you copy the entire line.

You will add this key manually to:

```text
rhel1
rhel2
rhel3
```

---

# 4.8 Install your public key on rhel1

Open a separate terminal and connect to `rhel1` using the lab's `ec_user` credentials and SSH key.

Once connected, verify:

```bash
whoami
```

Expected:

```text
ec_user
```

Now switch to your student account.

For example:

```bash
sudo su - stud01
```

Verify:

```bash
whoami
```

Expected:

```text
stud01
```

Check your home directory:

```bash
pwd
```

Expected:

```text
/home/stud01
```

---

## Create the .ssh directory

Create:

```bash
mkdir -p ~/.ssh
```

Set the correct permissions:

```bash
chmod 700 ~/.ssh
```

Verify:

```bash
ls -ld ~/.ssh
```

The permissions should look similar to:

```text
drwx------.
```

---

## Create authorized_keys

Open:

```bash
vi ~/.ssh/authorized_keys
```

Paste the public key that you copied from `rhelmain`.

It should be one complete line similar to:

```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... stud01@rhelmain
```

Save and exit.

Set the correct permissions:

```bash
chmod 600 ~/.ssh/authorized_keys
```

Verify:

```bash
ls -l ~/.ssh/authorized_keys
```

The permissions should look similar to:

```text
-rw-------
```

---

# 4.9 Verify ownership and permissions

Still on `rhel1`, run:

```bash
ls -ld ~/.ssh
ls -l ~/.ssh/authorized_keys
```

You can also run:

```bash
stat ~/.ssh
stat ~/.ssh/authorized_keys
```

Both files should belong to your `studXX` account.

For example:

```text
stud01 stud01
```

The important permissions are:

```text
~/.ssh                   700
~/.ssh/authorized_keys   600
```

SSH deliberately checks permissions carefully.

If private SSH files are writable by other users, SSH may refuse to use them.

---

# 4.10 Test SSH authentication to rhel1

Return to your `studXX` shell on **rhelmain**.

Verify:

```bash
hostname
whoami
```

You should be on:

```text
rhelmain
```

as:

```text
studXX
```

Now try:

```bash
ssh studXX@rhel1
```

Replace `studXX` with your username.

On the first connection, SSH may display:

```text
The authenticity of host 'rhel1 (...)' can't be established.
...
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

Enter:

```text
yes
```

The host key will be added to:

```text
~/.ssh/known_hosts
```

If everything is configured correctly, you should log in **without being asked for your account password**.

Check:

```bash
hostname
whoami
```

You should see:

```text
rhel1
studXX
```

Exit:

```bash
exit
```

You should return to `rhelmain`.

---

# 4.11 Test a command without opening an interactive shell

Instead of opening an SSH session, you can execute a single command remotely.

From `rhelmain`, run:

```bash
ssh studXX@rhel1 hostname
```

Expected output:

```text
rhel1
```

Try:

```bash
ssh studXX@rhel1 whoami
```

Expected:

```text
studXX
```

And:

```bash
ssh studXX@rhel1 id
```

This way of using SSH is particularly relevant for Ansible.

Ansible does not normally require you to interactively log in and type commands. It establishes SSH connections and executes automation remotely.

---

# 4.12 Repeat the procedure for rhel2

Now install the same public key on `rhel2`.

Connect to `rhel2` as `ec_user`.

Switch to your account:

```bash
sudo su - studXX
```

Create the SSH directory:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
```

Create:

```bash
vi ~/.ssh/authorized_keys
```

Paste your public key.

Then:

```bash
chmod 600 ~/.ssh/authorized_keys
```

Return to `rhelmain` and test:

```bash
ssh studXX@rhel2 hostname
```

Expected:

```text
rhel2
```

---

# 4.13 Repeat for rhel3

Perform the same procedure on `rhel3`.

On `rhel3`:

```bash
sudo su - studXX
```

Then:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
vi ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

Return to `rhelmain` and test:

```bash
ssh studXX@rhel3 hostname
```

Expected:

```text
rhel3
```

---

# 4.14 Final SSH test

You should now be back on `rhelmain` as your student account.

Verify:

```bash
hostname
whoami
```

Now test all three managed hosts:

```bash
ssh studXX@rhel1 hostname
ssh studXX@rhel2 hostname
ssh studXX@rhel3 hostname
```

You should receive:

```text
rhel1
rhel2
rhel3
```

None of these commands should ask for the `studXX` account password.

Also test the remote user:

```bash
ssh studXX@rhel1 whoami
ssh studXX@rhel2 whoami
ssh studXX@rhel3 whoami
```

All three commands should return your student username.

---

# 4.15 Optional: Verify which SSH key is being used

SSH can display detailed information about a connection using `-v`.

Try:

```bash
ssh -v studXX@rhel1 hostname
```

The output is quite verbose.

Look for messages mentioning:

```text
id_ed25519
```

and:

```text
publickey
```

This output can be extremely useful when troubleshooting SSH authentication problems.

For even more detail, SSH supports:

```bash
ssh -vv studXX@rhel1
```

or:

```bash
ssh -vvv studXX@rhel1
```

Do not worry about understanding every line. The important lesson is:

> If SSH authentication does not work, `ssh -v` is one of your first troubleshooting tools.

---

# 4.16 Troubleshooting

If SSH still asks for a password, check the following.

## Are you using the correct user?

From `rhelmain`:

```bash
whoami
```

Then make sure you connect using the same student account:

```bash
ssh studXX@rhel1
```

---

## Does the private key exist on rhelmain?

Check:

```bash
ls -l ~/.ssh/id_ed25519
```

---

## Is the correct public key installed remotely?

On the managed host:

```bash
cat ~/.ssh/authorized_keys
```

Compare it with the public key on `rhelmain`:

```bash
cat ~/.ssh/id_ed25519.pub
```

They should match.

---

## Are the permissions correct?

On the managed host:

```bash
ls -ld ~/.ssh
ls -l ~/.ssh/authorized_keys
```

They should be:

```text
700  ~/.ssh
600  ~/.ssh/authorized_keys
```

You can correct them with:

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

---

## Does everything belong to your user?

Run:

```bash
ls -ld ~/.ssh
ls -l ~/.ssh/authorized_keys
```

The owner should be your `studXX` account.

---

## Ask SSH for details

From `rhelmain`:

```bash
ssh -v studXX@rhel1
```

Look for information about which identities SSH is trying and whether public-key authentication succeeds.

---

# 4.17 Security checkpoint

Before continuing, make sure you understand the difference between the two key files.

On `rhelmain`:

```text
~/.ssh/id_ed25519
```

is your:

**PRIVATE KEY**

It stays on `rhelmain`.

Do not copy it to `rhel1`–`rhel3`.

Do not commit it to Git.

Do not share it.

---

The file:

```text
~/.ssh/id_ed25519.pub
```

is your:

**PUBLIC KEY**

A copy of this key is stored on each managed host in:

```text
~/.ssh/authorized_keys
```

The resulting setup is:

```text
                       Public key
                 +--------------------+
                 |                    |
                 v                    |
           authorized_keys            |
              on rhel1                |
                                      |
           authorized_keys            |
              on rhel2                |
                                      |
           authorized_keys            |
              on rhel3                |
                                      |
                                      |
+-------------------------------------+
|
| rhelmain
|
| studXX
|
| ~/.ssh/id_ed25519
|       PRIVATE KEY
|
+-------------------------------------
```

The private key proves your identity.

The public key tells the remote systems that this identity is allowed to log in.

---

# 4.18 Why are we doing this before using Ansible?

Ansible will soon need to connect from:

```text
rhelmain
```

to:

```text
rhel1
rhel2
rhel3
```

Before troubleshooting Ansible, we first make sure that the underlying SSH connection works.

This gives us a useful troubleshooting principle:

> **If SSH does not work, Ansible over SSH will not work either.**

Always test the underlying SSH connection first:

```bash
ssh studXX@rhel1 hostname
```

Once that works without a password, we can configure Ansible to use exactly the same connection.

---

# 4.19 Exercise complete

Before continuing, verify all three hosts one final time:

```bash
ssh studXX@rhel1 "hostname; whoami"
ssh studXX@rhel2 "hostname; whoami"
ssh studXX@rhel3 "hostname; whoami"
```

You should get results similar to:

```text
rhel1
stud01
rhel2
stud01
rhel3
stud01
```

If all three connections work without entering a password, your SSH environment is ready for Ansible.


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

```bash
vi playbooks/03_remote_hostname.yml
```

Add:

```yaml
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

```bash
ansible-playbook playbooks/03_remote_hostname.yml
```

Notice:

```yaml
changed_when: false
```

The `hostname` command only reads information. It does not modify the managed host.

Without this setting, the `command` module normally reports the task as:

```text
changed
```

By adding:

```yaml
changed_when: false
```

we tell Ansible:

> This command does not modify the target system.

The result should therefore be reported as:

```text
ok
```

instead of:

```text
changed
```

---

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
/tmp/ansible-workshop
```

on all managed systems.

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

# 6. Execute simple playbooks

The repository contains three introductory playbooks.

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

Add a task that prints the third item using its numeric list index.

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

# 8. Work with Ansible Modules

In this unit, you will work with several commonly used Ansible modules.

These exercises modify the managed systems, for example by installing packages, starting services, creating directories, creating users, and modifying files below `/etc`.

Before using a new module, get into the habit of checking its documentation.

Examples:

```bash
ansible-doc ansible.builtin.package
ansible-doc ansible.builtin.service
ansible-doc ansible.builtin.file
ansible-doc ansible.builtin.copy
ansible-doc ansible.builtin.user
ansible-doc ansible.builtin.lineinfile
```

You do not need to memorize every module option. Being able to find and understand the documentation is more important.

---

## 8.1 Inspect the package playbook

Start by looking at the first playbook:

```bash
cat playbooks/20_packages.yml
```

You should see that it contains:

```yaml
become: true
```

This tells Ansible that the tasks require elevated privileges.

For example, installing software packages requires root access.

Do **not** modify the `become` setting in the playbook.

Try running it:

```bash
ansible-playbook playbooks/20_packages.yml
```

At this point, you will probably receive an error similar to:

```text
fatal: [rhel1]: FAILED! => {"msg": "Missing sudo password"}
fatal: [rhel2]: FAILED! => {"msg": "Missing sudo password"}
fatal: [rhel3]: FAILED! => {"msg": "Missing sudo password"}
```

This happens because your `studXX` account can connect through SSH, but it is not yet allowed to use `sudo` without a password.

We will fix that now.

---

## 8.2 Enable sudo access for your student account

Your `studXX` account cannot grant itself sudo privileges.

For each managed host, connect using the privileged lab account:

```text
ec2-user
```

Then become root:

```bash
sudo -i
```

Create a sudo configuration file for your student account.

For example, for `stud01`:

```bash
visudo -f /etc/sudoers.d/stud01
```

Add:

```text
stud01 ALL=(ALL) NOPASSWD: ALL
```

Replace `stud01` with your own student account.

Save the file and set the correct permissions:

```bash
chmod 440 /etc/sudoers.d/stud01
```

Validate the configuration:

```bash
visudo -cf /etc/sudoers.d/stud01
```

You should see:

```text
/etc/sudoers.d/stud01: parsed OK
```

Repeat this on:

```text
rhel1
rhel2
rhel3
```

For this isolated training environment, `NOPASSWD: ALL` is used to allow Ansible to perform administrative tasks without prompting for a sudo password.

---

## 8.3 Verify privilege escalation

Return to `rhelmain` as your `studXX` account.

Test one host manually:

```bash
ssh studXX@rhel1 "sudo whoami"
```

Expected:

```text
root
```

Now test all managed hosts with Ansible:

```bash
ansible managed \
  -b \
  -m ansible.builtin.command \
  -a "whoami"
```

All three hosts should return:

```text
root
```

The option:

```text
-b
```

is the short form of:

```text
--become
```

The playbooks in this unit already contain the required:

```yaml
become: true
```

so you do not need to add `-b` when running them.

---

## 8.4 Package module

Now run the package playbook again:

```bash
cat playbooks/20_packages.yml
ansible-playbook playbooks/20_packages.yml
```

This playbook uses:

```text
ansible.builtin.package
```

to install packages on all managed hosts.

Verify one of the installed packages:

```bash
ansible managed -m ansible.builtin.command -a "rpm -q httpd"
```

### Customize the playbook

Open:

```bash
vi playbooks/20_packages.yml
```

Add the following packages:

```text
tar
tree
```

Run the playbook again:

```bash
ansible-playbook playbooks/20_packages.yml
```

Verify:

```bash
ansible managed -m ansible.builtin.command -a "rpm -q tree"
```

Now run the playbook one more time.

Compare the recap from the first and second execution.

Question:

> Why should already installed packages no longer report `changed`?

---

## 8.5 Service module

Inspect the playbook:

```bash
cat playbooks/21_service.yml
```

It uses: `ansible.builtin.service`

to manage the Apache service.

Run:

```bash
ansible-playbook playbooks/21_service.yml
```

Verify that the service is running:

```bash
ansible managed -b -m ansible.builtin.command -a "systemctl is-active httpd"
```

Expected:

```text
active
```

Also verify that it is enabled at boot:

```bash
ansible managed -b -m ansible.builtin.command -a "systemctl is-enabled httpd"
```

Expected:

```text
enabled
```

### Think about the module choice

You could technically run:

```bash
systemctl start httpd
```

through the command module.

However, the service module is preferable because it describes the desired state:

```yaml
state: started
enabled: true
```

This allows Ansible to check the current state and only make changes when necessary.

---

## 8.6 File and copy modules

Inspect:

```bash
cat playbooks/22_files.yml
```

This playbook uses:

```text
ansible.builtin.file
ansible.builtin.copy
```

The playbook should create a student-specific directory below `/opt/training`.

For example, for `stud10`:

```text
/opt/training/stud10
```

Run:

```bash
ansible-playbook playbooks/22_files.yml
```

Verify the created directory:

```bash
ansible managed -b -m ansible.builtin.command -a "ls -ld /opt/training/$USER"
```

Also inspect the created file:

```bash
ansible managed -b -m ansible.builtin.command -a "cat /opt/training/$USER/info.txt"
```

Your playbook should use the Ansible remote-user variable instead of hard-coding a student name.

For example:

```yaml
path: "/opt/training/{{ ansible_user }}"
```

and:

```yaml
dest: "/opt/training/{{ ansible_user }}/info.txt"
```

This ensures that every student works in a separate directory even though all students share the same managed hosts.

For example:

```text
/opt/training/stud01
/opt/training/stud02
/opt/training/stud03
...
/opt/training/stud10
```

### Customize the playbook

Modify the playbook so it also creates a configuration directory for your student account:

```text
/opt/training/studXX/config
```

Do not hard-code `studXX`.

Use:

```yaml
{{ ansible_user }}
```

so that the resulting path is created automatically for the currently configured student account.

The new directory should have:

```text
owner: root
group: root
mode: 0750
```

Use:

```text
ansible.builtin.file
```

Do not use `mkdir` through the command or shell module.

Run the playbook again:

```bash
ansible-playbook playbooks/22_files.yml
```

Verify:

```bash
ansible managed -b -m ansible.builtin.command -a "ls -ld /opt/training/$USER/config"
```

You should see your own student-specific path on all three managed hosts, for example:

```text
/opt/training/stud10/config
```

This is an important pattern for shared lab environments:

> Use variables to create student-specific resources instead of hard-coding common paths that would cause students to overwrite each other's work.

## 8.7 User module

In this exercise, you will use Ansible to create a Linux user on all three managed hosts.

Because the managed systems are shared by multiple students, **each student must create their own unique user**.

The naming convention is:

```text id="06fc7j"
Student account     User to create
---------------     --------------
stud01              ansible01
stud02              ansible02
stud03              ansible03
...
stud10              ansible10
```

Instead of hard-coding the username, we will derive it from your existing `ansible_user` variable.

Remember that `ansible_user` is already defined in:

```text id="qqsh70"
inventory/group_vars/managed.yml
```

For example:

```yaml id="3uj1yw"
ansible_user: stud10
```

---

### Inspect the playbook

Open:

```bash id="1l0tqy"
cat playbooks/23_users.yml
```

This playbook uses:

```text id="rm5t18"
ansible.builtin.user
```

to manage Linux user accounts.

Modify the playbook so that the username is derived from your student account.

Use:

```yaml id="4c4w3c"
name: "{{ ansible_user | replace('stud', 'ansible') }}"
```

For example, if:

```yaml id="ghqgvf"
ansible_user: stud10
```

the expression:

```text id="os0fvg"
{{ ansible_user | replace('stud', 'ansible') }}
```

produces:

```text id="2mrksr"
ansible10
```

The `replace` part is a **Jinja filter**. It replaces `stud` with `ansible` in the value of the variable.

Your user task should look similar to:

```yaml id="bn2aqa"
- name: Create student-specific Ansible user
  ansible.builtin.user:
    name: "{{ ansible_user | replace('stud', 'ansible') }}"
    comment: "Created by {{ ansible_user }} using Ansible"
    shell: /bin/bash
    state: present
```

---

### Run the playbook

Execute:

```bash id="e5nv15"
ansible-playbook playbooks/23_users.yml
```

The user should now be created on:

```text id="bswrxe"
rhel1
rhel2
rhel3
```

---

### Verify the result

First determine which username your expression produces.

For example:

```text id="im8n3a"
stud01 → ansible01
stud07 → ansible07
stud10 → ansible10
```

You can verify the user without hard-coding the student number by using the shell variable `$USER`:

```bash id="u2w48y"
ANSIBLE_USER="${USER/stud/ansible}"
```

Check:

```bash id="fwc5w2"
echo "$ANSIBLE_USER"
```

For `stud10`, this should display:

```text id="fzbt4c"
ansible10
```

Now query all managed hosts:

```bash id="r6hzdk"
ansible managed -m ansible.builtin.command -a "getent passwd $ANSIBLE_USER"
```

You should receive an entry from all three hosts similar to:

```text id="0hr2ym"
ansible10:x:1015:1015:Created by stud10 using Ansible:/home/ansible10:/bin/bash
```

---

### Customize the user

Now change the `comment` field in your playbook.

For example, change:

```yaml id="8ijou4"
comment: "Created by {{ ansible_user }} using Ansible"
```

to:

```yaml id="st7lru"
comment: "Managed by {{ ansible_user }} - Ansible Workshop"
```

Run the playbook again:

```bash id="w81bln"
ansible-playbook playbooks/23_users.yml
```

Ansible should report a change because the existing user account does not yet have the requested comment.

Verify:

```bash id="evqgf9"
ANSIBLE_USER="${USER/stud/ansible}"

ansible managed -m ansible.builtin.command -a "getent passwd $ANSIBLE_USER"
```

Compare the result with the previous output.

Which field changed?

---

### Test idempotency

Run the playbook once more **without changing anything**:

```bash id="2mtrhg"
ansible-playbook playbooks/23_users.yml
```

This time, the user task should report:

```text id="qgrx2o"
ok
```

instead of:

```text id="m3fx8c"
changed
```

Question:

> Why does Ansible no longer modify the user?

The user already exists and all properties managed by the playbook match the desired state.

This demonstrates idempotency again: Ansible changes a resource only when its current state differs from the state described in the playbook.

---

### Verify that students do not interfere with each other

Because every student creates a different account, multiple students can safely execute this exercise against the same managed hosts.

For example, after several students have completed the exercise, a managed host might contain:

```text id="mx24ma"
ansible01
ansible02
ansible03
ansible04
...
ansible10
```

Each account belongs to the student who created it:

```text id="1m5lq8"
stud01 → ansible01
stud02 → ansible02
...
stud10 → ansible10
```

This is another example of why using variables instead of hard-coded resource names is important when writing reusable Ansible automation.

## 8.8 lineinfile module

Inspect:

```bash
cat playbooks/24_lineinfile.yml
```

This playbook uses:

```text
ansible.builtin.lineinfile
```

to ensure that a specific line exists in:

```text
/etc/motd
```

Run:

```bash
ansible-playbook playbooks/24_lineinfile.yml
```

Verify:

```bash
ansible managed \
  -m ansible.builtin.command \
  -a "cat /etc/motd"
```

Run the playbook a second time:

```bash
ansible-playbook playbooks/24_lineinfile.yml
```

Verify again:

```bash
ansible managed \
  -m ansible.builtin.command \
  -a "cat /etc/motd"
```

Question:

> Why does the configured line not appear multiple times?

The `lineinfile` module checks whether the desired line already exists and only changes the file when necessary.

---

## 8.9 Why use modules instead of shell commands?

Many of the tasks in this unit could technically be implemented using shell commands.

For example:

```bash
dnf install httpd
systemctl start httpd
mkdir /opt/training
useradd ansibledemo
echo "message" >> /etc/motd
```

However, Ansible provides purpose-built modules:

```text
ansible.builtin.package
ansible.builtin.service
ansible.builtin.file
ansible.builtin.copy
ansible.builtin.user
ansible.builtin.lineinfile
```

These modules understand the desired state of the resource.

For example:

```yaml
ansible.builtin.package:
  name: httpd
  state: present
```

means:

> Ensure that `httpd` is installed.

It does not mean:

> Run an installation command every time.

This state-based approach is one of the reasons Ansible automation can be **idempotent**.

---

## 8.10 Student challenge – Find the correct module

Use:

```bash
ansible-doc -l
```

and:

```bash
ansible-doc <module-name>
```

to find an appropriate Ansible module for each requirement:

1. Create a directory.
2. Install a package.
3. Start and enable a service.
4. Create a Linux user.
5. Copy a static file.
6. Ensure that one particular line exists in a file.
7. Change ownership and permissions of an existing file.

Write down the fully qualified module name for each task.

For example:

```text
ansible.builtin.file
```

---

## 8.11 What did we learn?

In this unit, you used several important Ansible modules:

| Module | Purpose |
|---|---|
| `ansible.builtin.package` | Install or remove packages |
| `ansible.builtin.service` | Start, stop and enable services |
| `ansible.builtin.file` | Manage files, directories and permissions |
| `ansible.builtin.copy` | Copy or create static files |
| `ansible.builtin.user` | Manage Linux users |
| `ansible.builtin.lineinfile` | Ensure individual lines exist in files |

You also configured privilege escalation for your student account.

The connection path now looks like this:

```text
rhelmain
   |
   | SSH as studXX
   |
   +------> rhel1
   +------> rhel2
   +------> rhel3
               |
               | sudo / become
               v
              root
```

Remember:

```text
SSH        = how Ansible connects
become     = how Ansible gains elevated privileges
```

And the most important rule from this unit is:

> Prefer a dedicated Ansible module whenever one exists instead of solving every task with `command` or `shell`.

## Next

In the next unit, you will extend Ansible with **collections from Ansible Galaxy**.


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
