# Owner setup

Intended public repository: thomaspatrickpearl53-ctrl/hl-lua-addons.

## GitHub access

The Codex GitHub app connection and the local GitHub CLI are separate. The publisher uses the CLI. Authenticate locally with `gh auth login --hostname github.com --git-protocol https --web`, then `gh auth setup-git`. Do not put tokens in game files, ZIPs or this repository.

Once these local files have been reviewed, create the public repository with Issues enabled and push the main branch. No automatic issue-triggered workflow executes submitted code. All uploads are manual-owner-approved through the local folder.

## Email notifications

In GitHub Settings > Emails, add and verify the intended Gmail address if it is not already verified. In Settings > Notifications, enable email delivery for watched repositories and select that verified address as the default notification email (or configure routing where GitHub supports it). On this repository select Watch > Custom > Issues, or All Activity.

Local `.owner/owner.json` records the owner's requested email but cannot configure GitHub notification delivery. It is ignored by Git and must remain private. No SMTP password, Gmail app password, mail service, or email account connection is needed for GitHub's own notifications.

After publication, have another GitHub account submit a clearly marked test addon issue through the form, check that the attachment downloads, and verify receipt in the intended inbox. GitHub generally does not email you for your own activity. Close the test issue. Email delivery is not verified until the owner confirms receiving that message.

GitHub documentation:
- https://docs.github.com/en/subscriptions-and-notifications/get-started/configuring-notifications
- https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/attaching-files

## Approved folder

Inspect and test submitted ZIPs before placing them in `.owner/approved/`.

```
python tools/publish_approved.py
```

Default mode validates and previews only. To publish one batch:

```
python tools/publish_approved.py --publish
```

To monitor the Approved folder and publish stable ZIPs automatically:

```
python tools/publish_approved.py --publish --watch
```

Only ZIPs that have not changed for at least 20 seconds are considered. Keep the publisher running on your computer; it is not installed as a background service. Exit with Ctrl+C. Use a clean, up-to-date repository checkout on main. Each release is tagged `<id>-v<version>` and published before its catalog entry is pushed. On a catalog push failure, publication stops with the ZIP retained for retry. The script never replaces an existing release asset with different bytes.

GitHub release notifications are separate from submission emails. A future in-game browser will read the public catalog, and its download/enable/disable/remove code will be added to the game later.
