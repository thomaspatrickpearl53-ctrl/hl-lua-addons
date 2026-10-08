# Half-Life: Lua Addons

A reviewed community addon library for Half-Life: Lua. This is a catalog and download host for addons, not the game itself. Garry's Mod addons are not automatically compatible.

## Submit an addon

Open [Submit an addon](https://github.com/thomaspatrickpearl53-ctrl/hl-lua-addons/issues/new?template=submit-addon.yml), sign in to GitHub, complete the form and attach a ZIP. Submissions and attachments are public. New submissions do not appear in the approved catalog until the owner reviews and publishes them.

The first version uses a browser-based GitHub form. It does not yet upload directly from inside the game. An in-game Submit button can open this link later.

## Download and install

Approved versions are listed in `catalog.json` and distributed as GitHub Release ZIP assets. Extract a ZIP into `Half-Life/hl_lua/`. Restart/reload the game as the addon requires. The planned Installed/Available Mods menu is not implemented yet.

ZIP layout:

```
addons/my_weapon/addon.json
addons/my_weapon/LICENSE.txt
addons/my_weapon/lua/weapons/weapon_my_weapon.lua
models/my_weapon/...       (optional)
sound/my_weapon/...        (optional)
```

Use a stable lowercase folder ID and a version such as 1.0.0. Keep custom asset paths namespaced under the addon ID so addons do not overwrite one another. Do not include base-game files, other authors' unlicensed assets, config.cfg, executables, DLLs, saves or credentials. Declare dependencies in addon.json and the submission form.

## Review and publication

The owner downloads a submission, inspects its files and tests it in a separate game folder. After approving it, the owner places the ZIP in the local `.owner/approved/` folder. The publisher validates the package as data; it never executes submitted Lua or extracts files. Explicit publish mode uploads a release asset and updates the catalog. It then moves the processed local ZIP to `.owner/published/`.

The publisher is not a malware detector or compatibility guarantee; manual review is required. Do not run submitted scripts on the publishing machine just to inspect them.

Maintainer setup, email configuration and publishing commands: [SETUP.md](SETUP.md).

## Catalog contract

`schema_version: 1`, with an `addons` array. Each approved entry has id, name, author, description, version, dependencies, download_url, sha256 and size_bytes. The library is initially empty. Checksums allow a future game downloader to verify that its download matches the reviewed archive; catalog signature verification and the in-game downloader are separate future work.

Addon licenses are included by their creators. There is no blanket license overriding an author's addon license.
