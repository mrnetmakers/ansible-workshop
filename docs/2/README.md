[← Chapter 1](../1/) | [↑ Workshop index](../../) | [Chapter 3 →](../3/)

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
- name: Learn YAML data types
  hosts: localhost
  gather_facts: false

```

Change it to:

```yaml
- name: Learn YAML data types
  hosts: localhost
   gather_facts: false
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

---

[← Chapter 1](../1/) | [↑ Workshop index](../../) | [Chapter 3 →](../3/)
