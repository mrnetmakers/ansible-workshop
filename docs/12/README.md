[← Chapter 11](../11/) | [↑ Workshop index](../../) | [Chapter 13 →](../13/)

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

---

[← Chapter 11](../11/) | [↑ Workshop index](../../) | [Chapter 13 →](../13/)
