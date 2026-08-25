[← Chapter 6](../6/) | [↑ Workshop index](../../) | [Chapter 8 →](../8/)

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

---

[← Chapter 6](../6/) | [↑ Workshop index](../../) | [Chapter 8 →](../8/)
