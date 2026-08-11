# Instructor Notes

This repository accompanies the student-facing `README.md`.

## Before class

1. Ensure `ansible-core` is installed on the RHEL 9 control VM.
2. Ensure every student has an account `studXX` on the control VM and all three managed RHEL 9 VMs.
3. Ensure students can SSH from the control VM to the managed nodes.
4. Ensure the `studXX` accounts can use `sudo` for privileged labs. If sudo requires a password, students can run playbooks with `--ask-become-pass`; if passwordless sudo is configured, no extra option is needed.
5. Provide the IP addresses/DNS names for the three managed VMs.
6. Provide internet access to Ansible Galaxy, or pre-stage `ansible.posix` and `community.general`.
7. Put this repository in GitHub/GitLab or another reachable Git service.

## Important repository choices

The committed inventory uses RFC 5737 documentation addresses (`192.0.2.0/24`) so students cannot accidentally target real infrastructure. Students must edit `inventory/hosts.yml` before remote exercises.

The remote username is stored in `inventory/group_vars/managed.yml` and initially set to `studXX`. This avoids forcing every student to modify `ansible.cfg` just for their username while still giving them a project-local configuration exercise.

The repository intentionally contains complete examples for the standalone-playbook part of the course. The final `server_baseline` role is only a skeleton, so the final exercise requires students to synthesize what they learned.

## Suggested classroom checkpoints

After SSH/inventory setup:

```bash
ansible-inventory --graph
ansible managed -m ansible.builtin.ping
```

Before privileged labs:

```bash
ansible managed -b -m ansible.builtin.command -a "id"
```

Expected effective UID is root.

Before the role section:

```bash
ansible-playbook playbooks/34_facts.yml
ansible-playbook playbooks/42_loop_dictionary.yml
```

Final validation:

```bash
ansible-playbook site.yml --syntax-check
ansible-playbook site.yml --check --diff
ansible-playbook site.yml --limit rhel1
ansible-playbook site.yml
ansible-playbook site.yml
```

Ask students to explain any task that reports `changed` on the second full run.

## Optional adjustments

### Sudo password required

Have students use:

```bash
ansible-playbook playbooks/20_packages.yml --ask-become-pass
```

and similarly for other privileged playbooks.

### No internet access

From a connected preparation system, download/install the required collections and distribute them separately, or configure an internal Automation Hub/Galaxy mirror. Do not commit a large `collections/` tree to every student repository unless that is intentional.

### Shared managed VMs

If all students target the same three managed machines simultaneously, account-specific `/tmp/ansible-{{ ansible_user }}` exercises are safe, but privileged exercises affect shared system state. For a large class, use per-student managed VMs or stagger/adjust the exercises.

### GitHub classroom

A convenient workflow is to use this repository as a template. Each student can create/receive a copy, clone it to the RHEL control instance, edit inventory and variables, and commit their work throughout the workshop.

## Files students are expected to customize

At minimum:

- `inventory/hosts.yml`
- `inventory/group_vars/managed.yml`
- selected example playbooks during exercises
- `roles/webserver/templates/index.html.j2`
- `roles/training_app/defaults/main.yml`
- `roles/training_app/templates/training-app.conf.j2`
- `roles/system_report/defaults/main.yml`
- all implementation files under `roles/server_baseline/`
- `site.yml` to enable the final role

## Suggested grading rubric for the final role

- 10% repository and YAML structure
- 15% variables and sensible defaults
- 15% module use and idempotency
- 15% loop over directories/users
- 15% template using facts and variables
- 10% conditional behavior
- 10% register and reporting
- 5% appropriate shell usage
- 5% Git history and commit quality
