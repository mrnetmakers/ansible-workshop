[← Chapter 8](../8/) | [↑ Workshop index](../../) | [Chapter 10 →](../10/)

---

# 9. Collections and Ansible Galaxy

So far, most modules we have used came from:

```text id="5tv9hr"
ansible.builtin
```

Examples include:

```text id="ofxjqp"
ansible.builtin.package
ansible.builtin.file
ansible.builtin.copy
ansible.builtin.user
```

Ansible can be extended with additional content through **collections**.

A collection can contain:

- modules
- plugins
- roles
- playbooks
- documentation

Collections are distributed through **Ansible Galaxy** and other sources.

The general naming format for content inside a collection is:

```text id="bfv0z4"
namespace.collection.module
```

For example:

```text id="40q0g5"
community.general.ini_file
```

Here:

```text id="umtz28"
community
```

is the namespace,

```text id="c2fw4e"
general
```

is the collection,

and:

```text id="i8t0ke"
ini_file
```

is the module.

This complete name is called the **Fully Qualified Collection Name**, or **FQCN**.

---

## 9.1 Inspect Ansible collections

Before installing additional collections, let's first understand where Ansible looks for collection content.

Make sure you are in your workshop directory:

```bash id="yd7ncd"
cd ~/ansible-workshop
```

Check:

```bash id="hufp13"
pwd
```

You should see something similar to:

```text id="4v42bs"
/home/stud01/ansible-workshop
```

---

### Check the project collection directory

This workshop uses a **project-local collection directory**:

```text id="7pt6g3"
collections/
```

Check whether it already exists:

```bash id="1drc5p"
ls -ld collections
```

If the directory does not exist yet, create it:

```bash id="16v2fn"
mkdir -p collections
```

At this point it may still be empty.

Check:

```bash id="0jll2j"
ls -la collections
```

---

### List collections from a specific path

`ansible-galaxy` can explicitly be told where to look for collections.

Run:

```bash id="tx6f1w"
ansible-galaxy collection list --collections-path ./collections
```

Since we have not installed the workshop collections yet, the directory may currently contain no collections.

That is expected.

Depending on your Ansible version and configuration, running:

```bash id="z13epp"
ansible-galaxy collection list
```

without specifying a collection path may also produce an error such as:

```text id="gdswdr"
ERROR! - None of the provided paths were usable.
Please specify a valid path with --collections-path
```

For this workshop, we will therefore explicitly use the project-local directory:

```text id="puxq3i"
./collections
```

---

### Check Ansible's configured collection paths

You can also ask Ansible which collection paths are currently configured:

```bash id="ak8e1j"
ansible-config dump | grep COLLECTIONS_PATHS
```

Depending on your Ansible Core version, the setting may be displayed slightly differently.

You can also check:

```bash id="spgb9i"
ansible --version
```

Look for the line showing the collection locations, if present.

The important point is that collections must exist in a location where Ansible knows how to find them.

---

### Try to inspect a collection module

Now try:

```bash id="6lgtyo"
ansible-doc community.general.ini_file
```

If `community.general` is not installed yet, Ansible will not be able to display the module documentation.

That is fine.

In the next exercise, we will install the required collections into:

```text id="6cd7v2"
./collections
```

and then repeat the check.

---

### Why use project-local collections?

Instead of relying on collections installed globally on `rhelmain`, this workshop keeps its additional collections inside the project:

```text id="4spfnv"
ansible-workshop/
├── ansible.cfg
├── requirements.yml
├── inventory/
├── playbooks/
└── collections/
```

This has several advantages.

Each student gets their own collection installation:

```text id="m7jey4"
/home/stud01/ansible-workshop/collections/
/home/stud02/ansible-workshop/collections/
/home/stud03/ansible-workshop/collections/
...
```

Students therefore do not modify a shared system-wide Ansible installation.

It also makes the project more reproducible: `requirements.yml` defines **what the project needs**, while `collections/` is the location where those dependencies are installed.

In the next step, you will use `requirements.yml` to install those dependencies.

## 9.2 Install compatible collection versions

Our RHEL 9 training environment uses a specific ansible version. For example:

```text
ansible-core 2.14.18
```

Collections evolve independently from Ansible Core. New collection releases may therefore require a newer Ansible version than the one installed on our training system.

For this workshop, we will use **fixed collection versions** that are compatible with the Ansible Core version used in the lab.

This also ensures that every student works with exactly the same collection versions.

### Check your Ansible version

Run:

```bash
ansible --version
```

You should see:

```text
core 2.14.18
```

The exact formatting may differ slightly.

---

### Update `requirements.yml`

Open:

```bash
vi requirements.yml
```

Replace the collection definitions with:

```yaml
---
collections:
  - name: ansible.posix
    version: "1.4.0"

  - name: community.general
    version: "6.0.1"

  - name: community.crypto
    version: "2.8.1"

  - name: community.dns
    version: "2.4.1"

  - name: community.postgresql
    version: "2.3.0"
```

The `version` field pins each dependency to a specific version.

This is important for reproducible automation.

Without version pinning:

```yaml
- name: community.general
```

Ansible Galaxy normally installs a current version, which may require a newer Ansible Core release.

With version pinning:

```yaml
- name: community.general
  version: "6.0.1"
```

every student receives the same tested version.

---

### Remove previously installed incompatible collections

If you already installed newer collection versions during an earlier attempt, remove the project-local collection directory:

```bash
rm -rf collections
```

Recreate it:

```bash
mkdir -p collections
```

This only removes collections installed inside your own workshop directory.

It does not modify the system-wide Ansible installation.

---

### Install the workshop collections

Run:

```bash
ansible-galaxy collection install -r requirements.yml --collections-path ./collections
```

Ansible Galaxy will download and install the versions specified in `requirements.yml`.

---

### Verify the installation

Run:

```bash
ansible-galaxy collection list --collections-path ./collections
```

You should see output similar to:

```text
Collection            Version
--------------------- -------
ansible.posix         1.4.0
community.crypto      2.8.1
community.dns         2.4.1
community.general     6.0.1
community.postgresql  2.3.0
```

Your project now has a predictable dependency set that matches the Ansible Core generation used in this workshop.

> In real projects, version pinning also protects automation from unexpected behavior changes caused by automatically installing newer collection releases.

# 9.4 Collection 1 – `ansible.posix`

The `ansible.posix` collection contains modules and plugins related to POSIX/Linux system administration.

Examples include modules for:

```text id="l31qxi"
SELinux
firewalld
mounts
sysctl
authorized_keys
```

Explore the collection:

```bash id="st6b5e"
ansible-doc -l | grep '^ansible.posix'
```

---

## Example 1 – Inspect SELinux configuration

First inspect:

```bash id="8ecoxc"
ansible-doc ansible.posix.selinux
```

Find the parameters:

```text id="0zqxb3"
policy
state
```

Do **not** change the SELinux configuration.

Instead, check the current state on all managed systems:

```bash id="idjhc3"
ansible managed -m ansible.builtin.command -a "getenforce"
```

Then answer:

1. Which values does `state` accept?
2. Which parameter controls the SELinux policy?
3. Can the module make the configuration persistent?
4. Would changing SELinux mode be safe in a shared training environment?

The last question is important.

Not every module that you discover should automatically be executed.

---

## Example 2 – Manage a student-specific firewall port

Now inspect:

```bash id="tzm3kt"
ansible-doc ansible.posix.firewalld
```

In this lab, multiple students share:

```text id="w0b82a"
rhel1
rhel2
rhel3
```

Therefore, students should not all manage the same firewall rule.

Instead, each student will use their student number as part of the port.

For example:

```text id="9dkd5h"
stud01 → 8001/tcp
stud02 → 8002/tcp
stud10 → 8010/tcp
stud15 → 8015/tcp
```

Inspect:

```bash id="owmqf4"
cat playbooks/25_firewall.yml
```

The playbook should derive the port from `ansible_user`, for example:

```yaml id="45ok0y"
student_number: "{{ ansible_user | regex_replace('^stud', '') }}"
student_port: "80{{ student_number }}"
```

The firewall task can then use:

```yaml id="j3bf6b"
- name: Open student-specific firewall port
  ansible.posix.firewalld:
    port: "{{ student_port }}/tcp"
    permanent: true
    immediate: true
    state: enabled
```

Run:

```bash id="3f4dml"
ansible-playbook playbooks/25_firewall.yml
```

Verify:

```bash id="yyoh9d"
ansible managed -b -m ansible.builtin.command -a "firewall-cmd --list-ports"
```

Find your own port in the output.

---

# 9.5 Collection 2 – `community.general`

`community.general` is a large community-maintained collection containing modules for many different technologies and configuration formats.

Explore:

```bash id="m51gjd"
ansible-doc -l | grep '^community.general' | head -30
```

---

## Example 1 – Manage an INI file

Inspect:

```bash id="kgssq9"
ansible-doc community.general.ini_file
```

Then inspect the provided playbook:

```bash id="n0pn07"
cat playbooks/26_ini.yml
```

Because the managed hosts are shared, the configuration file must be student-specific.

The playbook should manage:

```text id="qurxrh"
/opt/training/studXX/training-app.conf
```

For example:

```yaml id="6gv8h4"
path: "/opt/training/{{ ansible_user }}/training-app.conf"
```

Run:

```bash id="p1vdtw"
ansible-playbook playbooks/26_ini.yml
```

Verify:

```bash id="v3nm4r"
ansible managed -b -m ansible.builtin.command -a "cat /opt/training/$USER/training-app.conf"
```

---

### Customize the INI file

Add another task that creates:

```ini id="ox7h68"
[logging]
level=info
```

Run:

```bash id="ixsaxm"
ansible-playbook playbooks/26_ini.yml
```

Verify the result.

Then run the playbook a second time.

Question:

> Does `level=info` appear more than once?

---

## Example 2 – Manage a student-specific archive

Find the archive module:

```bash id="dnvpjo"
ansible-doc community.general.archive
```

Your existing directory:

```text id="kmx4cn"
/opt/training/studXX
```

contains files created during previous exercises.

Create:

```text id="frvf0d"
playbooks/27_archive.yml
```

Use `community.general.archive` to create:

```text id="0fqdwa"
/tmp/studXX-training.tar.gz
```

from:

```text id="v4mrcu"
/opt/training/studXX
```

Do not hard-code your username.

Use:

```text id="3fjx21"
{{ ansible_user }}
```

Run your playbook and verify the archive:

```bash id="i2t5ar"
ansible managed -b -m ansible.builtin.command -a "ls -lh /tmp/$USER-training.tar.gz"
```

---

# 9.6 Collection 3 – `community.crypto`

The `community.crypto` collection contains modules for working with:

- private keys
- public keys
- certificates
- certificate signing requests
- OpenSSL-related objects

Explore:

```bash id="0o4c2c"
ansible-doc -l | grep '^community.crypto' | head -30
```

This collection is particularly useful when automating TLS infrastructure.

---

## Example 1 – Create a private key

Inspect:

```bash id="h9uy41"
ansible-doc community.crypto.openssl_privatekey
```

Create:

```text id="okrvqf"
playbooks/28_private_key.yml
```

The playbook should create a private key for each student under:

```text id="1l3n45"
/opt/training/studXX/tls/
```

First ensure that the directory exists:

```yaml id="rklj22"
- name: Create TLS directory
  ansible.builtin.file:
    path: "/opt/training/{{ ansible_user }}/tls"
    state: directory
    owner: root
    group: root
    mode: "0700"
```

Then use:

```text id="90k9a9"
community.crypto.openssl_privatekey
```

to create:

```text id="l99r3c"
/opt/training/studXX/tls/server.key
```

Run your playbook:

```bash id="z0icwp"
ansible-playbook playbooks/28_private_key.yml
```

Verify:

```bash id="4m5v5c"
ansible managed -b -m ansible.builtin.command -a "ls -l /opt/training/$USER/tls/server.key"
```

Run the playbook a second time and observe whether the key is recreated.

---

## Example 2 – Create a certificate signing request

Inspect:

```bash id="g86nnv"
ansible-doc community.crypto.openssl_csr
```

Extend your playbook with a task that creates:

```text id="ojp1dt"
/opt/training/studXX/tls/server.csr
```

Use the private key you created in the previous task.

Set the common name to something student-specific, for example:

```yaml id="1g89mx"
common_name: "{{ ansible_user }}.training.example"
```

For `stud01`, this would become:

```text id="lmlzq7"
stud01.training.example
```

Run the playbook and verify:

```bash id="vmm9vi"
ansible managed -b -m ansible.builtin.command -a "ls -l /opt/training/$USER/tls/"
```

You should now have both:

```text id="m9w2hq"
server.key
server.csr
```

# 9.7 What did we learn?

In this unit, you worked with several different collections:

| Collection | Example use |
|---|---|
| `ansible.posix` | Linux/POSIX administration |
| `community.general` | General-purpose community modules |
| `community.crypto` | Keys, CSRs and certificates |

You learned that collections extend Ansible beyond:

```text id="vfwcyx"
ansible.builtin
```

and that modules are normally referenced using their FQCN:

```text id="onph9f"
namespace.collection.module
```

For example:

```text id="8f2tgz"
ansible.posix.firewalld
community.general.ini_file
community.crypto.openssl_privatekey
```

You also learned an important distinction:

> **Installing a collection makes its Ansible content available. It does not automatically provide the external infrastructure, credentials, services, or Python dependencies required by every module in that collection.**

Finally, when working on shared systems, always ask:

> **Will this task create or modify a resource that another student is also using?**

Whenever possible, derive unique resource names from:

```text id="p5e3ya"
{{ ansible_user }}
```

For example:

```text id="eaj97q"
/opt/training/{{ ansible_user }}
training_{{ ansible_user }}
app_{{ ansible_user }}
```

This makes your automation safer and more reusable in shared environments.

---

[← Chapter 8](../8/) | [↑ Workshop index](../../) | [Chapter 10 →](../10/)
