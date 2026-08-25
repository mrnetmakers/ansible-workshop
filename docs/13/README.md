[← Chapter 12](../12/) | [↑ Workshop index](../../) | [Chapter 14 →](../14/)

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

Lists can also contain dictionaries. This is very useful when every item has several properties.

In this exercise, you will create multiple users. Because the managed hosts are shared by all students, every username must contain your individual **student ID**.

For example:

```text id="f3n4ly"
Student     Users
-------     -------------------------------
stud01      developer01, operator01, auditor01
stud02      developer02, operator02, auditor02
stud10      developer10, operator10, auditor10
```

This prevents students from modifying each other's accounts.

---

### Inspect the playbook

Open:

```bash id="x6ezxl"
cat playbooks/42_loop_dictionary.yml
```

The playbook contains a list of dictionaries describing several users.

Modify it so it looks similar to:

```yaml id="9iz7du"
---
- name: Create multiple student-specific users
  hosts: managed
  become: true

  vars:
    student_id: "{{ ansible_user | regex_replace('^stud', '') }}"

    training_users:
      - name: developer
        shell: /bin/bash
        comment: "Development user"

      - name: operator
        shell: /bin/bash
        comment: "Operations user"

      - name: auditor
        shell: /sbin/nologin
        comment: "Audit user"

  tasks:
    - name: Create training users
      ansible.builtin.user:
        name: "{{ item.name }}{{ student_id }}"
        shell: "{{ item.shell }}"
        comment: "{{ item.comment }}"
        state: present
      loop: "{{ training_users }}"
```

---

### Understand the student ID

Your Ansible remote user is already stored in:

```text id="52jbql"
{{ ansible_user }}
```

For example:

```text id="j99hxq"
stud01
```

This expression:

```text id="g16gcg"
{{ ansible_user | regex_replace('^stud', '') }}
```

removes `stud` from the beginning of the string.

The result is:

```text id="vb0zvw"
10
```

We store that result in:

```yaml id="i8jpw3"
student_id: "{{ ansible_user | regex_replace('^stud', '') }}"
```

The task can then combine:

```text id="fdftle"
item.name + student_id
```

For example:

```text id="tm0o5g"
developer + 10 → developer10
operator  + 10 → operator10
auditor   + 10 → auditor10
```

---

### Run the playbook

Execute:

```bash id="8m80x6"
ansible-playbook playbooks/42_loop_dictionary.yml
```

Ansible should loop over all three dictionaries and create three student-specific users on:

```text id="a6njyw"
rhel1
rhel2
rhel3
```

---

### Verify the users

You can derive your student ID in the shell as well:

```bash id="jow19p"
STUDENT_ID="${USER#stud}"
```

Check:

```bash id="zm7p3e"
echo "$STUDENT_ID"
```

For `stud01`, this returns:

```text id="cnq79u"
10
```

Now verify your users:

```bash id="q3ofus"
ansible managed -m ansible.builtin.command -a "getent passwd developer${STUDENT_ID}"
```

Try the other users:

```bash id="q3ofus"
ansible managed -m ansible.builtin.command -a "getent passwd operator${STUDENT_ID}"
```

```bash id="q3ofus"
ansible managed -m ansible.builtin.command -a "getent passwd auditor${STUDENT_ID}"
```

---

### Challenge 1 – Add another user

Add a **fourth dictionary** to:

```yaml id="h2y4im"
training_users:
```

Create a user with the base name:

```text id="1yjf4k"
support
```

Use:

```text id="fbpkzs"
/bin/bash
```

as its shell and choose a suitable comment.

Do **not** include your student ID directly in the dictionary.

In other words, do not write:

```yaml id="m4psq8"
name: support10
```

Instead, use:

```yaml id="1ty2x5"
name: support
```

The task should automatically append your student ID.

For `stud01`, the resulting user should therefore be:

```text id="8w0k96"
support10
```

For `stud03`:

```text id="ocgjj5"
support03
```

Run the playbook again:

```bash id="93o4y5"
ansible-playbook playbooks/42_loop_dictionary.yml
```

Verify your new account:

```bash id="8efqzb"
STUDENT_ID="${USER#stud}"

ansible managed -m ansible.builtin.command -a "getent passwd support${STUDENT_ID}"
```

---

### Challenge 2 – Customize the comments

Change the `comment` value for every user so that it also contains your Ansible username.

For example, the resulting comments for `stud01` could be:

```text id="sy2dce"
Development user managed by stud01
Operations user managed by stud01
Audit user managed by stud01
Support user managed by stud01
```

Do not hard-code `stud01`.

Use:

```text id="67f2xk"
{{ ansible_user }}
```

in the appropriate place.

Run the playbook again and verify one account:

```bash id="6e1hcm"
ansible managed -m ansible.builtin.command -a "getent passwd developer${STUDENT_ID}"
```

Question:

> What did Ansible report as `changed`, and why?

Run the playbook once more without changing anything.

Question:

> Why should all four user items now report `ok`?

---

---

[← Chapter 12](../12/) | [↑ Workshop index](../../) | [Chapter 14 →](../14/)
