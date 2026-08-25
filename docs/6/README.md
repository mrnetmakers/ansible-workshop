[← Chapter 5](../5/) | [↑ Workshop index](../../) | [Chapter 7 →](../7/)

---

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

---

[← Chapter 5](../5/) | [↑ Workshop index](../../) | [Chapter 7 →](../7/)
