[← Chapter 9](../9/) | [↑ Workshop index](../../) | [Chapter 11 →](../11/)

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

---

[← Chapter 9](../9/) | [↑ Workshop index](../../) | [Chapter 11 →](../11/)
