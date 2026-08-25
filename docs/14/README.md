[← Chapter 13](../13/) | [↑ Workshop index](../../) | [Chapter 15 →](../15/)

---

# 14. Transition to roles and Git

> **From this point onward, all new configuration tasks must be implemented in roles.** Top-level playbooks should stay small and select hosts/roles rather than containing large task lists.

## 14.1 Examine the role layout

```bash
find roles/webserver -maxdepth 2 -type f | sort
```

Key directories:

```text
tasks/       tasks executed by the role
handlers/    event-driven tasks
templates/   Jinja2 templates
files/       static files
defaults/    customizable default variables
vars/        higher-precedence role variables
meta/        role metadata
```

The supplied repository already contains reference roles. To learn how Ansible generates one, create a disposable role:

```bash
ansible-galaxy role init ~/example_role
find ~/example_role -maxdepth 2 -type f | sort
rm -rf ~/example_role
```

## 14.2 Create your own Git branch and first commit

Because you cloned the instructor repository, it already contains Git history.

For the workshop, create your own branch:

```bash id="8y8v03"
git switch -c studXX-workshop
```

Replace `studXX` with your username.

For example:

```bash id="a83q5m"
git switch -c stud01-workshop
```

Verify your current branch:

```bash id="mqkjma"
git branch --show-current
```

You should see your student-specific branch, for example:

```text id="3bnf5s"
stud01-workshop
```

---

### Configure your Git identity

Before Git can create commits, it needs to know who created them.

Check the currently configured identity:

```bash id="fb7zxl"
git config user.name
git config user.email
```

If these commands return no values, configure an identity for this repository.

Use your student account as the name:

```bash id="gvvdrp"
git config user.name "$USER"
```

For the workshop, use a local example email address:

```bash id="sq1ip4"
git config user.email "$USER@ansible-workshop.local"
```

For `stud01`, this results in:

```text id="q4qf8x"
user.name  = stud01
user.email = stud01@ansible-workshop.local
```

Verify:

```bash id="tbttno"
git config user.name
git config user.email
```

You can also display both settings together:

```bash id="mh5fs3"
git config --local --list
```

> We intentionally do not use `--global`. The configuration should apply only to your workshop repository and should not modify your general Git configuration.

---

### Check your repository status

Run:

```bash id="pvsl99"
git status
```

Git shows which files have been modified since the repository was cloned.

By this point in the workshop, you may already have changed files such as:

```text id="muj8yq"
inventory/group_vars/managed.yml
requirements.yml
playbooks/...
```

---

### Stage your changes

Add your changes to the Git staging area:

```bash id="aykqla"
git add .
```

Check again:

```bash id="dl0tnp"
git status
```

Notice how the files are now listed under:

```text id="3qgj2v"
Changes to be committed:
```

This means the changes are staged and will be included in the next commit.

---

### Create your first commit

Now create a commit:

```bash id="ptu2pi"
git commit -m "Configure student workshop environment"
```

You should now see output indicating that a new commit was created.

---

### View the Git history

Run:

```bash id="12tf0p"
git log --oneline --decorate -5
```

Your new commit should appear at the top.

You should also see your current branch pointing to this commit, for example:

```text id="2g8w5q"
a1b2c3d (HEAD -> stud01-workshop) Configure student workshop environment
```

The exact commit ID will be different.

---

### Understand what you just did

You have now completed the basic Git workflow:

```text id="ytghxb"
Modify files
     ↓
git status
     ↓
git add .
     ↓
Staging area
     ↓
git commit
     ↓
Git history
```

Your changes are now stored as a commit in your own student branch.

From this point onward, commit meaningful changes as you develop and customize your Ansible roles.

For example:

```bash id="7yd3fd"
git add .
git commit -m "Customize webserver role"
```

This gives you a history of how your Ansible project evolves during the remaining exercises.

---

---

[← Chapter 13](../13/) | [↑ Workshop index](../../) | [Chapter 15 →](../15/)
