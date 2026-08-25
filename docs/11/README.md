[← Chapter 10](../10/) | [↑ Workshop index](../../) | [Chapter 12 →](../12/)

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

---

[← Chapter 10](../10/) | [↑ Workshop index](../../) | [Chapter 12 →](../12/)
