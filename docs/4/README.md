[← Chapter 3](../3/) | [↑ Workshop index](../../) | [Chapter 5 →](../5/)

---

# 4. Prepare SSH Key Authentication

Ansible normally connects to Linux managed hosts using SSH.

In our lab environment, you have three RHEL systems:

```text
rhelmain    Ansible control node
rhel1       Managed host
rhel2       Managed host
rhel3       Managed host
```

You initially access these systems using the `ec2_user` account and the SSH key provided for the lab.

However, **Ansible should not run as `ec2_user`**.

Each student has a dedicated account named:

```text
studXX
```

For example:

```text
stud01
stud02
stud03
...
```

Your goal in this exercise is to configure SSH public-key authentication so that your `studXX` account on `rhelmain` can connect directly to the same `studXX` account on all three managed hosts.

At the end of the exercise, the following should work **without entering a password**:

```bash
ssh studXX@rhel1
ssh studXX@rhel2
ssh studXX@rhel3
```

---

# 4.1 Understand the authentication setup

There are two different SSH authentication scenarios in this lab.

## Initial lab access

You connect to the RHEL instances as:

```text
ec2_user
```

using the SSH private key provided for the lab.

For example, from your workstation you might connect with a command similar to:

```bash
ssh -i <provided-key> ec2_user@<server>
```

The exact connection information will be provided by your instructor.

## Ansible communication

Ansible will later connect from:

```text
rhelmain
```

to:

```text
rhel1
rhel2
rhel3
```

using your personal:

```text
studXX
```

account.

For example:

```text
                    SSH
                    │
                    │  stud01
                    ▼
              +-----------+
              |   rhel1   |
              +-----------+
                    ▲
                    │
+-----------+       │
| rhelmain  |-------+
|           |-------+-----> rhel2
|  stud01   |-------+-----> rhel3
+-----------+

Private key:
~/.ssh/id_ed25519

Public key installed on remote hosts:
~/.ssh/authorized_keys
```

We therefore need to create an SSH key pair for `studXX` on `rhelmain` and install its **public key** on each managed host.

---

# 4.2 Switch to your student account on rhelmain

First connect to `rhelmain` using the `ec2_user` account as described by your instructor.

Check your current user:

```bash
whoami
```

You should see:

```text
ec2_user
```

Now switch to your assigned student account.

For example, if you are `stud01`:

```bash
sudo su - stud01
```

Replace `stud01` with your assigned username.

Check again:

```bash
whoami
```

You should now see:

```text
stud01
```

Also check your home directory:

```bash
pwd
```

You should see something similar to:

```text
/home/stud01
```

The `-` in:

```bash
sudo su - stud01
```

is important. It starts a login shell and switches to the target user's environment and home directory.

---

# 4.3 Examine your SSH directory

Check whether an SSH directory already exists:

```bash
ls -la ~/.ssh
```

If it does not exist, you may see:

```text
ls: cannot access '/home/stud01/.ssh': No such file or directory
```

That is fine.

If the directory already exists, inspect its contents carefully.

You may see files such as:

```text
known_hosts
authorized_keys
```

Do not delete existing SSH configuration unless instructed to do so.

---

# 4.4 Generate your SSH key pair

We will create an Ed25519 SSH key pair.

Run:

```bash
ssh-keygen -t ed25519
```

You will be asked:

```text
Enter file in which to save the key (/home/stud01/.ssh/id_ed25519):
```

Press **Enter** to accept the default.

For this isolated training environment, follow your instructor's direction regarding the passphrase. If instructed to create the key without a passphrase, press **Enter** twice when prompted.

Afterwards, you should see output similar to:

```text
Your identification has been saved in /home/stud01/.ssh/id_ed25519
Your public key has been saved in /home/stud01/.ssh/id_ed25519.pub
```

---

# 4.5 Examine the generated keys

List your SSH directory:

```bash
ls -la ~/.ssh
```

You should now have at least:

```text
id_ed25519
id_ed25519.pub
```

These two files have very different purposes.

## Private key

```text
~/.ssh/id_ed25519
```

This is your **private key**.

It must remain private.

Never:

- copy it to the managed hosts;
- put it into a Git repository;
- send it to another student;
- paste it into documentation;
- publish it anywhere.

Check its permissions:

```bash
ls -l ~/.ssh/id_ed25519
```

It should normally only be readable by you.

---

## Public key

```text
~/.ssh/id_ed25519.pub
```

This is your **public key**.

The public key is intended to be copied to systems that should allow you to log in.

Display it:

```bash
cat ~/.ssh/id_ed25519.pub
```

The output will look similar to:

```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... stud01@rhelmain
```

The exact value will be different for every student.

The entire output is **one public key**.

---

# 4.6 Understand authorized_keys

On a remote Linux system, SSH normally checks:

```text
~/.ssh/authorized_keys
```

to determine which public keys are allowed to authenticate as that user.

For example, when connecting as:

```text
stud01
```

to `rhel1`, SSH will check:

```text
/home/stud01/.ssh/authorized_keys
```

on `rhel1`.

Conceptually:

```text
rhelmain
========

/home/stud01/.ssh/id_ed25519
             |
             | proves possession
             |
             +----------------------------+
                                          |
                                          v

rhel1
=====

/home/stud01/.ssh/authorized_keys

contains:

ssh-ed25519 AAAA... stud01@rhelmain
```

The **private key remains on `rhelmain`**.

Only the **public key** is added to `authorized_keys` on the managed hosts.

---

# 4.7 Copy your public key

On `rhelmain`, make sure you are still your student user:

```bash
whoami
```

Now display your public key:

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the **complete line** to your clipboard.

It starts with:

```text
ssh-ed25519
```

Make sure you copy the entire line.

You will add this key manually to:

```text
rhel1
rhel2
rhel3
```

---

# 4.8 Install your public key on rhel1

Open a separate terminal and connect to `rhel1` using the lab's `ec2_user` credentials and SSH key.

Once connected, verify:

```bash
whoami
```

Expected:

```text
ec2_user
```

Now switch to your student account.

For example:

```bash
sudo su - stud01
```

Verify:

```bash
whoami
```

Expected:

```text
stud01
```

Check your home directory:

```bash
pwd
```

Expected:

```text
/home/stud01
```

---

## Create the .ssh directory

Create:

```bash
mkdir -p ~/.ssh
```

Set the correct permissions:

```bash
chmod 700 ~/.ssh
```

Verify:

```bash
ls -ld ~/.ssh
```

The permissions should look similar to:

```text
drwx------.
```

---

## Create authorized_keys

Open:

```bash
vi ~/.ssh/authorized_keys
```

Paste the public key that you copied from `rhelmain`.

It should be one complete line similar to:

```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... stud01@rhelmain
```

Save and exit.

Set the correct permissions:

```bash
chmod 600 ~/.ssh/authorized_keys
```

Verify:

```bash
ls -l ~/.ssh/authorized_keys
```

The permissions should look similar to:

```text
-rw-------
```

---

# 4.9 Verify ownership and permissions

Still on `rhel1`, run:

```bash
ls -ld ~/.ssh
ls -l ~/.ssh/authorized_keys
```

You can also run:

```bash
stat ~/.ssh
stat ~/.ssh/authorized_keys
```

Both files should belong to your `studXX` account.

For example:

```text
stud01 stud01
```

The important permissions are:

```text
~/.ssh                   700
~/.ssh/authorized_keys   600
```

SSH deliberately checks permissions carefully.

If private SSH files are writable by other users, SSH may refuse to use them.

---

# 4.10 Test SSH authentication to rhel1

Return to your `studXX` shell on **rhelmain**.

Verify:

```bash
hostname
whoami
```

You should be on:

```text
rhelmain
```

as:

```text
studXX
```

Now try:

```bash
ssh studXX@rhel1
```

Replace `studXX` with your username.

On the first connection, SSH may display:

```text
The authenticity of host 'rhel1 (...)' can't be established.
...
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

Enter:

```text
yes
```

The host key will be added to:

```text
~/.ssh/known_hosts
```

If everything is configured correctly, you should log in **without being asked for your account password**.

Check:

```bash
hostname
whoami
```

You should see:

```text
rhel1
studXX
```

Exit:

```bash
exit
```

You should return to `rhelmain`.

---

# 4.11 Test a command without opening an interactive shell

Instead of opening an SSH session, you can execute a single command remotely.

From `rhelmain`, run:

```bash
ssh studXX@rhel1 hostname
```

Expected output:

```text
rhel1
```

Try:

```bash
ssh studXX@rhel1 whoami
```

Expected:

```text
studXX
```

And:

```bash
ssh studXX@rhel1 id
```

This way of using SSH is particularly relevant for Ansible.

Ansible does not normally require you to interactively log in and type commands. It establishes SSH connections and executes automation remotely.

---

# 4.12 Repeat the procedure for rhel2

Now install the same public key on `rhel2`.

Connect to `rhel2` as `ec2_user`.

Switch to your account:

```bash
sudo su - studXX
```

Create the SSH directory:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
```

Create:

```bash
vi ~/.ssh/authorized_keys
```

Paste your public key.

Then:

```bash
chmod 600 ~/.ssh/authorized_keys
```

Return to `rhelmain` and test:

```bash
ssh studXX@rhel2 hostname
```

Expected:

```text
rhel2
```

---

# 4.13 Repeat for rhel3

Perform the same procedure on `rhel3`.

On `rhel3`:

```bash
sudo su - studXX
```

Then:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
vi ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

Return to `rhelmain` and test:

```bash
ssh studXX@rhel3 hostname
```

Expected:

```text
rhel3
```

---

# 4.14 Final SSH test

You should now be back on `rhelmain` as your student account.

Verify:

```bash
hostname
whoami
```

Now test all three managed hosts:

```bash
ssh studXX@rhel1 hostname
ssh studXX@rhel2 hostname
ssh studXX@rhel3 hostname
```

You should receive:

```text
rhel1
rhel2
rhel3
```

None of these commands should ask for the `studXX` account password.

Also test the remote user:

```bash
ssh studXX@rhel1 whoami
ssh studXX@rhel2 whoami
ssh studXX@rhel3 whoami
```

All three commands should return your student username.

---

# 4.15 Optional: Verify which SSH key is being used

SSH can display detailed information about a connection using `-v`.

Try:

```bash
ssh -v studXX@rhel1 hostname
```

The output is quite verbose.

Look for messages mentioning:

```text
id_ed25519
```

and:

```text
publickey
```

This output can be extremely useful when troubleshooting SSH authentication problems.

For even more detail, SSH supports:

```bash
ssh -vv studXX@rhel1
```

or:

```bash
ssh -vvv studXX@rhel1
```

Do not worry about understanding every line. The important lesson is:

> If SSH authentication does not work, `ssh -v` is one of your first troubleshooting tools.

---

# 4.16 Troubleshooting

If SSH still asks for a password, check the following.

## Are you using the correct user?

From `rhelmain`:

```bash
whoami
```

Then make sure you connect using the same student account:

```bash
ssh studXX@rhel1
```

---

## Does the private key exist on rhelmain?

Check:

```bash
ls -l ~/.ssh/id_ed25519
```

---

## Is the correct public key installed remotely?

On the managed host:

```bash
cat ~/.ssh/authorized_keys
```

Compare it with the public key on `rhelmain`:

```bash
cat ~/.ssh/id_ed25519.pub
```

They should match.

---

## Are the permissions correct?

On the managed host:

```bash
ls -ld ~/.ssh
ls -l ~/.ssh/authorized_keys
```

They should be:

```text
700  ~/.ssh
600  ~/.ssh/authorized_keys
```

You can correct them with:

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

---

## Does everything belong to your user?

Run:

```bash
ls -ld ~/.ssh
ls -l ~/.ssh/authorized_keys
```

The owner should be your `studXX` account.

---

## Ask SSH for details

From `rhelmain`:

```bash
ssh -v studXX@rhel1
```

Look for information about which identities SSH is trying and whether public-key authentication succeeds.

---

# 4.17 Security checkpoint

Before continuing, make sure you understand the difference between the two key files.

On `rhelmain`:

```text
~/.ssh/id_ed25519
```

is your:

**PRIVATE KEY**

It stays on `rhelmain`.

Do not copy it to `rhel1`–`rhel3`.

Do not commit it to Git.

Do not share it.

---

The file:

```text
~/.ssh/id_ed25519.pub
```

is your:

**PUBLIC KEY**

A copy of this key is stored on each managed host in:

```text
~/.ssh/authorized_keys
```

The resulting setup is:

```text
                       Public key
                 +--------------------+
                 |                    |
                 v                    |
           authorized_keys            |
              on rhel1                |
                                      |
           authorized_keys            |
              on rhel2                |
                                      |
           authorized_keys            |
              on rhel3                |
                                      |
                                      |
+-------------------------------------+
|
| rhelmain
|
| studXX
|
| ~/.ssh/id_ed25519
|       PRIVATE KEY
|
+-------------------------------------
```

The private key proves your identity.

The public key tells the remote systems that this identity is allowed to log in.

---

# 4.18 Why are we doing this before using Ansible?

Ansible will soon need to connect from:

```text
rhelmain
```

to:

```text
rhel1
rhel2
rhel3
```

Before troubleshooting Ansible, we first make sure that the underlying SSH connection works.

This gives us a useful troubleshooting principle:

> **If SSH does not work, Ansible over SSH will not work either.**

Always test the underlying SSH connection first:

```bash
ssh studXX@rhel1 hostname
```

Once that works without a password, we can configure Ansible to use exactly the same connection.

---

# 4.19 Exercise complete

Before continuing, verify all three hosts one final time:

```bash
ssh studXX@rhel1 "hostname; whoami"
ssh studXX@rhel2 "hostname; whoami"
ssh studXX@rhel3 "hostname; whoami"
```

You should get results similar to:

```text
rhel1
stud01
rhel2
stud01
rhel3
stud01
```

If all three connections work without entering a password, your SSH environment is ready for Ansible.

---

[← Chapter 3](../3/) | [↑ Workshop index](../../) | [Chapter 5 →](../5/)
