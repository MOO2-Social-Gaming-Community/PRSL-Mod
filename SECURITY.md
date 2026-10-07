# Security policy (pre-alpha)

**This code is research-stage and is not safe to install as a live turn hook.** Do not enable it by toggling a launcher checkbox or editing a manifest. PRSL must fail closed when game identity, adapter compatibility, engine phase or coordinator state is uncertain.

Threat boundaries:

- Exact SHA-256 and bytes are necessary for hook selection but do not themselves prove gameplay compatibility.
- A hostile archive must not traverse paths, write symlinks, override original game files or supply unauthorized executables. Use the safe source importer, and inspect imported code before execution.
- PRSL coordinator commands must not expose emulator memory to the internet, and must authenticate sessions and bind commits to turn epochs. IPX tunnel and PRSL control transport are different trust domains.
- Disabled PRSL must not inject game code, emit PRSL packets, or modify game config. Updates may never occur mid-session.
- Logs should redact tokens, credentials and personal filesystem details. Do not publish original game binaries or private keys.

Security reports should be raised privately with the repository maintainer through GitHub's private vulnerability reporting mechanism if enabled; otherwise contact the project's published contact address. Avoid posting exploitation details on public issues before a fix exists.
