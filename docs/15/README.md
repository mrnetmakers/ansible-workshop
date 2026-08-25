[← Chapter 14](../14/) | [↑ Workshop index](../../)

---

# 15. Role exercise: `webserver`

In this exercise, you will work with your first complete Ansible role.

The managed hosts are shared by multiple students. Therefore, some resources will be shared while others must be student-specific.

The Apache package and service are shared:

```text
httpd package
httpd service
```

It does not matter which student installs or starts Apache first. Once the desired state has been reached, later executions by other students should simply report:

```text
ok
```

However, every student must deploy their **own website**.

For example:

```text
Student     Document root               URL
-------     --------------------------  ------------------------
stud01      /var/www/html/stud01        http://rhel1/stud01/
stud02      /var/www/html/stud02        http://rhel1/stud02/
stud03      /var/www/html/stud03        http://rhel1/stud03/
```

The role therefore uses the existing:

```text
{{ ansible_user }}
```

variable to create student-specific resources.

---

## 15.1 Inspect the role structure

Start by examining the role:

```bash
find roles/webserver -maxdepth 2 -type f | sort
```

Then inspect the default variables:

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

Also inspect the templates:

```bash
ls -l roles/webserver/templates/
```

The role should contain at least:

```text
roles/webserver/
├── defaults/
│   └── main.yml
├── handlers/
│   └── main.yml
├── tasks/
│   └── main.yml
└── templates/
    ├── index.html.j2
    └── student-site.conf.j2
```

---

## 15.2 Understand the default variables

Open:

```bash
cat roles/webserver/defaults/main.yml
```

The role should contain:

```yaml
---
webserver_package: httpd
webserver_service: httpd

webserver_document_root: "/var/www/html/{{ ansible_user }}"
webserver_title: "Ansible Workshop - {{ ansible_user }}"

webserver_config_file: "/etc/httpd/conf.d/{{ ansible_user }}.conf"
```

For `stud01`, these variables become:

```text
webserver_document_root
→ /var/www/html/stud01

webserver_title
→ Ansible Workshop - stud01

webserver_config_file
→ /etc/httpd/conf.d/stud01.conf
```

Another student running exactly the same role automatically gets different paths.

No student number needs to be hard-coded in the role.

---

## 15.3 Inspect the role tasks

Open:

```bash
cat roles/webserver/tasks/main.yml
```

The role should contain tasks similar to:

```yaml
---
- name: Install Apache
  ansible.builtin.package:
    name: "{{ webserver_package }}"
    state: present

- name: Ensure Apache is enabled and running
  ansible.builtin.service:
    name: "{{ webserver_service }}"
    enabled: true
    state: started

- name: Create student-specific document root
  ansible.builtin.file:
    path: "{{ webserver_document_root }}"
    state: directory
    owner: root
    group: root
    mode: "0755"

- name: Deploy student-specific website
  ansible.builtin.template:
    src: index.html.j2
    dest: "{{ webserver_document_root }}/index.html"
    owner: root
    group: root
    mode: "0644"

- name: Deploy student-specific Apache configuration
  ansible.builtin.template:
    src: student-site.conf.j2
    dest: "{{ webserver_config_file }}"
    owner: root
    group: root
    mode: "0644"
  notify: Restart Apache
```

Notice the difference between shared and student-specific resources.

These tasks are shared:

```yaml
- name: Install Apache
- name: Ensure Apache is enabled and running
```

But these resources include:

```text
{{ ansible_user }}
```

and are therefore unique for every student:

```text
/var/www/html/stud01
/etc/httpd/conf.d/stud01.conf
```

---

## 15.4 Inspect the website template

Open:

```bash
cat roles/webserver/templates/index.html.j2
```

A possible initial version is:

```html
<!DOCTYPE html>
<html>
<head>
  <title>{{ webserver_title }}</title>
</head>
<body>

<h1>{{ webserver_title }}</h1>

<p>This website is managed by Ansible.</p>

<ul>
  <li>Student: {{ ansible_user }}</li>
  <li>Inventory host: {{ inventory_hostname }}</li>
  <li>Operating system: {{ ansible_facts['distribution'] }}</li>
  <li>OS version: {{ ansible_facts['distribution_version'] }}</li>
  <li>Architecture: {{ ansible_facts['architecture'] }}</li>
</ul>

</body>
</html>
```

Because facts are used in the template, the role-runner playbook must gather facts.

---

## 15.5 Inspect the Apache configuration template

Open:

```bash
cat roles/webserver/templates/student-site.conf.j2
```

It should contain:

```apache
# Managed by Ansible for {{ ansible_user }}

<Directory "{{ webserver_document_root }}">
    Options -Indexes
    AllowOverride None
    Require all granted
</Directory>
```

Every student creates their own configuration file.

For example:

```text
/etc/httpd/conf.d/stud01.conf
/etc/httpd/conf.d/stud02.conf
/etc/httpd/conf.d/stud03.conf
```

This avoids students overwriting each other's Apache configuration.

---

## 15.6 Inspect the handler

Open:

```bash
cat roles/webserver/handlers/main.yml
```

The handler should contain:

```yaml
---
- name: Restart Apache
  ansible.builtin.service:
    name: "{{ webserver_service }}"
    state: restarted
```

Notice that the handler is only notified when the Apache configuration file changes.

Changing a static HTML page does **not** require Apache to restart.

This is important:

> Handlers should be triggered only when the changed resource actually requires the associated action.

---

## 15.7 Inspect the role-runner playbook

Open:

```bash
cat playbooks/50_webserver_role.yml
```

It should remain small:

```yaml
---
- name: Configure student webserver
  hosts: managed
  become: true
  gather_facts: true

  roles:
    - webserver
```

The top-level playbook decides:

- which hosts to target;
- whether privilege escalation is required;
- which roles should execute.

The implementation belongs inside the role.

---

# 15.8 Run the role against one host

Always test a new configuration against a limited target first.

Run:

```bash
ansible-playbook playbooks/50_webserver_role.yml --limit rhel1
```

The first student to execute the role may see Apache installation and service tasks report:

```text
changed
```

Students running afterwards may see:

```text
ok
```

because Apache is already installed and running.

However, your student-specific directory and configuration should still be created.

---

## 15.9 Verify your website files

For `stud01`, verify the document root:

```bash
ansible rhel1 -b -m ansible.builtin.command -a "ls -ld /var/www/html/$USER"
```

Then inspect your website:

```bash
ansible rhel1 -b -m ansible.builtin.command -a "cat /var/www/html/$USER/index.html"
```

Check your Apache configuration:

```bash
ansible rhel1 -b -m ansible.builtin.command -a "cat /etc/httpd/conf.d/$USER.conf"
```

For `stud01`, these commands inspect:

```text
/var/www/html/stud01/index.html
/etc/httpd/conf.d/stud01.conf
```

---

# 15.10 Access your website

From `rhelmain`, use:

```bash
curl http://rhel1/$USER/
```

For `stud01`, this is equivalent to:

```bash
curl http://rhel1/stud01/
```

You should see your generated HTML.

You can also explicitly test the HTTP status:

```bash
curl -I http://rhel1/$USER/
```

Look for:

```text
HTTP/1.1 200 OK
```

---

# 15.11 Run the role against all managed hosts

Once the test on `rhel1` works, run:

```bash
ansible-playbook playbooks/50_webserver_role.yml
```

The role now configures your website on:

```text
rhel1
rhel2
rhel3
```

Verify:

```bash
curl http://rhel1/$USER/
curl http://rhel2/$USER/
curl http://rhel3/$USER/
```

All three systems should return your student-specific website.

---

# 15.12 Customize your website

Now modify:

```bash
vi roles/webserver/templates/index.html.j2
```

Customize your website.

Add at least two of the following:

- your student username;
- total system memory;
- kernel version;
- processor architecture;
- a custom heading;
- a short workshop message.

For example, you could add:

```html
<p>
  This page was deployed by {{ ansible_user }}
  using an Ansible role.
</p>
```

Do not hard-code:

```text
stud01
```

Use:

```text
{{ ansible_user }}
```

instead.

Run:

```bash
ansible-playbook playbooks/50_webserver_role.yml
```

Verify:

```bash
curl http://rhel1/$USER/
```

Your changes should appear immediately.

---

## Question

Did Apache restart because you changed `index.html`?

It should **not**.

A static HTML file does not require an Apache restart.

This demonstrates why handlers should only be attached to tasks where a service reload or restart is actually required.

---

# 15.13 Handler experiment

Now we will intentionally change an Apache configuration file.

Open:

```bash
vi roles/webserver/templates/student-site.conf.j2
```

Add a comment, for example:

```apache
# Student website configuration for {{ ansible_user }}
```

The complete file might now look like:

```apache
# Managed by Ansible for {{ ansible_user }}
# Student website configuration for {{ ansible_user }}

<Directory "{{ webserver_document_root }}">
    Options -Indexes
    AllowOverride None
    Require all granted
</Directory>
```

Run:

```bash
ansible-playbook playbooks/50_webserver_role.yml
```

The task:

```text
Deploy student-specific Apache configuration
```

should report:

```text
changed
```

and notify:

```text
Restart Apache
```

At the end of the play, the handler should execute.

---

## 15.14 Run it again

Without modifying anything, run:

```bash
ansible-playbook playbooks/50_webserver_role.yml
```

The Apache configuration is already correct.

Therefore:

```text
Deploy student-specific Apache configuration
```

should report:

```text
ok
```

and the handler should **not** execute.

This demonstrates the relationship:

```text
configuration changes
        ↓
task reports changed
        ↓
notify
        ↓
handler executes
```

If nothing changes:

```text
configuration already correct
        ↓
task reports ok
        ↓
no notification
        ↓
handler does not execute
```

---

# 15.15 Observe the shared environment

You are working on shared systems.

For example, after several students have run the role, `rhel1` may contain:

```text
/var/www/html/stud01/
/var/www/html/stud02/
/var/www/html/stud03/
/var/www/html/stud04/
...
```

and:

```text
/etc/httpd/conf.d/stud01.conf
/etc/httpd/conf.d/stud02.conf
/etc/httpd/conf.d/stud03.conf
/etc/httpd/conf.d/stud04.conf
...
```

Each student owns a separate automation namespace.

The shared resources remain:

```text
httpd package
httpd service
```

This is a common automation design principle:

> Shared infrastructure can be managed centrally, while user-specific resources should use unique names derived from variables.

---

# 15.16 Commit your role changes

Review your changes:

```bash
git status
```

Inspect the differences:

```bash
git diff
```

Stage them:

```bash
git add roles/webserver
```

Commit:

```bash
git commit -m "Customize student webserver role"
```

View the recent history:

```bash
git log --oneline --decorate -5
```

You now have a Git checkpoint containing your first customized Ansible role.

---

[← Chapter 14](../14/) | [↑ Workshop index](../../)
