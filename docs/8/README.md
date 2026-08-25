[← Chapter 7](../7/) | [↑ Workshop index](../../) | [Chapter 9 →](../9/)

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

For example, for `stud01`:

```text
/opt/training/stud01
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

```bash
vi playbooks/22_files.yml
```

Do not hard-code `studXX`.

Use:

```yaml
{{ ansible_user }}
```

so that the resulting path is created automatically for the currently configured student account.

When done, run the playbook again:

```bash
ansible-playbook playbooks/22_files.yml
```

Verify:

```bash
ansible managed -b -m ansible.builtin.command -a "ls -al /opt/training/$USER"
```

You should see your own student-specific path on all three managed hosts, for example:

```text
/opt/training/stud01
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
ansible_user: stud01
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
ansible_user: stud01
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

For `stud01`, this should display:

```text id="fzbt4c"
ansible10
```

Now query all managed hosts:

```bash id="r6hzdk"
ansible managed -m ansible.builtin.command -a "getent passwd $ANSIBLE_USER"
```

You should receive an entry from all three hosts similar to:

```text id="0hr2ym"
ansible10:x:1015:1015:Created by stud01 using Ansible:/home/ansible01:/bin/bash
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

In this exercise, you will use:

>ansible.builtin.lineinfile

to ensure that a specific line exists in a file.

On a normal Linux system, `/etc/motd` contains the system-wide **Message of the Day**.

However, our managed hosts are shared by multiple students. If everyone modified `/etc/motd`, all students would be changing the same file.

Instead, every student will manage their own MOTD-style file inside their training directory:

```text id="hz1i4r"
/opt/training/studXX/motd
```

For example:

```text id="gtlf6s"
/opt/training/stud01/motd
/opt/training/stud02/motd
/opt/training/stud10/motd
```

---

### Inspect the playbook

Run:

```bash id="i6haxd"
cat playbooks/24_lineinfile.yml
```

The playbook uses:

```text id="8b1hde"
ansible.builtin.lineinfile
```

to manage a line inside your student-specific file.

The important part should look similar to:

```yaml id="6lrzmg"
- name: Add workshop marker to student MOTD
  ansible.builtin.lineinfile:
    path: "/opt/training/{{ ansible_user }}/motd"
    line: "This server is managed by {{ ansible_user }} using Ansible."
    create: true
    mode: "0644"
```

Notice that the student name is **not hard-coded**.

Instead, the playbook uses:

```text id="vv2p91"
{{ ansible_user }}
```

For `stud01`, Ansible therefore manages:

```text id="xdseou"
/opt/training/stud01/motd
```

while `stud03` manages:

```text id="95zwwl"
/opt/training/stud03/motd
```

This allows multiple students to run the same playbook against the same managed hosts without overwriting each other's files.

---

### Run the playbook

Execute:

```bash id="b3b4sc"
ansible-playbook playbooks/24_lineinfile.yml
```

The file should now be created on:

```text id="83o22p"
rhel1
rhel2
rhel3
```

---

### Verify the result

You can use your local `$USER` variable to construct the correct path:

```bash id="1i5kpm"
ansible managed -b -m ansible.builtin.command -a "cat /opt/training/$USER/motd"
```

For example, `stud01` should see:

```text id="o99j6q"
This server is managed by stud01 using Ansible.
```

---

### Add another line

Now customize the playbook.

Add a second `lineinfile` task that ensures the following line exists:

```text id="v3lml3"
Welcome to the Ansible Deep Dive Workshop!
```

Do not use `shell`, `command`, or `echo`.

Use another:

```text id="nxzndg"
ansible.builtin.lineinfile
```

task.

Run the playbook:

```bash id="z0qdta"
ansible-playbook playbooks/24_lineinfile.yml
```

Verify:

```bash id="dnixby"
ansible managed -b -m ansible.builtin.command -a "cat /opt/training/$USER/motd"
```

Your file should now contain:

```text id="3x3ypo"
This server is managed by stud01 using Ansible.
Welcome to the Ansible Deep Dive Workshop!
```

The exact student username will depend on your account.

---

### Test idempotency

Run the playbook again:

```bash id="iwj7vi"
ansible-playbook playbooks/24_lineinfile.yml
```

Then inspect the file again:

```bash id="9myy9c"
ansible managed -b -m ansible.builtin.command -a "cat /opt/training/$USER/motd"
```

Question:

> Why do the configured lines not appear multiple times?

The `lineinfile` module does not simply append text to a file.

Instead, it checks whether the requested line already exists. If the line is already present, no modification is necessary and the task reports:

```text id="pdty5g"
ok
```

instead of:

```text id="q0zj2c"
changed
```

This is another example of **idempotency**.

---

### Compare it with a shell command

Imagine that instead of `lineinfile`, we had executed:

```bash id="3i18lr"
echo "Welcome to the Ansible Deep Dive Workshop!" >> /opt/training/stud01/motd
```

Running that command three times would result in:

```text id="ej1gl4"
Welcome to the Ansible Deep Dive Workshop!
Welcome to the Ansible Deep Dive Workshop!
Welcome to the Ansible Deep Dive Workshop!
```

With:

```text id="1w5nm6"
ansible.builtin.lineinfile
```

we describe the desired state:

> This line must exist in the file.

Ansible checks the current state and only modifies the file when necessary.

That difference between **executing commands** and **describing desired state** is an important concept when writing reliable Ansible automation.

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

Find an appropriate Ansible module for each requirement:

1. Create a directory.
2. Install a package.
3. Start and enable a service.
4. Create a Linux user.
5. Copy a static file.
6. Ensure that one particular line exists in a file.
7. Change ownership and permissions of an existing file.

Use:

```bash
ansible-doc -l
```

and:

```bash
ansible-doc <module-name>
```

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

---

[← Chapter 7](../7/) | [↑ Workshop index](../../) | [Chapter 9 →](../9/)
