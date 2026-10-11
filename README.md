# Half-Life: Lua Addons

Addons for Half-Life: Lua. Download the ones you want and put them in your game's addons folder yourself. There is no in-game mod menu.

## Addons

| Addon | What it is | Needs | Download |
| --- | --- | --- | --- |
| GoldSrc Sandbox 1.6.0 | Garry's Mod style sandbox: 89 physical props, physgun and toolgun, welds, ropes, thrusters, motors, cars, NPC spawning, construction saves and dupes. Console: `sandbox_menu`, then click Enable sandbox. Already comes with the game; download this to update or reinstall it. | – | [sandbox-v1.6.0.zip](https://github.com/thomaspatrickpearl53-ctrl/hl-lua-addons/releases/download/sandbox-v1.6.0/sandbox-v1.6.0.zip) |
| Fieldrunner utility van 1.0.0 | An original six-seat van with a detailed cabin, custom wheels, suspension, running and brake lamps and a two-tone horn. Spawn it from the sandbox Vehicles tab. | `sandbox` | [detailed_van-v1.0.0.zip](https://github.com/thomaspatrickpearl53-ctrl/hl-lua-addons/releases/download/detailed_van-v1.0.0/detailed_van-v1.0.0.zip) |
| Realistic Graphics 1.0.0 | One screen shader for a more modern look: ambient occlusion, weapon contact shadows, sun rays, bloom, fog and filmic colour. Presets: `cl_realism_preset Subtle\|Realistic\|Cinematic`. | – | [realistic_graphics-v1.0.0.zip](https://github.com/thomaspatrickpearl53-ctrl/hl-lua-addons/releases/download/realistic_graphics-v1.0.0/realistic_graphics-v1.0.0.zip) |
| Half-Life 2 flashlight 1.0.0 | Replaces the flashlight's round glow with a Half-Life 2 style spotlight: sharp cone, soft rings, shadows and a slight lag as you turn. | – | [hl2_flashlight-v1.0.0.zip](https://github.com/thomaspatrickpearl53-ctrl/hl-lua-addons/releases/download/hl2_flashlight-v1.0.0/hl2_flashlight-v1.0.0.zip) |
| First-person body 1.0.0 | See your own body and legs in first person: walks, runs, crouches, jumps and turns in place. | – | [firstperson_body-v1.0.0.zip](https://github.com/thomaspatrickpearl53-ctrl/hl-lua-addons/releases/download/firstperson_body-v1.0.0/firstperson_body-v1.0.0.zip) |
| Cry of Fear Glock 1.0.0 | Glock 19 with slide lock, empty reloads and iron sights. In chat: `!give weapon_cof_glock` | – | [cof_glock-v1.0.0.zip](https://github.com/thomaspatrickpearl53-ctrl/hl-lua-addons/releases/download/cof_glock-v1.0.0/cof_glock-v1.0.0.zip) |
| Cry of Fear vehicle pack 1.0.0 | Aud, Vari, Foretag, police car and fire engine, with physical wheels. Imports its models from your own Cry of Fear install. | `sandbox` (comes with the game), Cry of Fear on Steam | [cof_vehicles-v1.0.0.zip](https://github.com/thomaspatrickpearl53-ctrl/hl-lua-addons/releases/download/cof_vehicles-v1.0.0/cof_vehicles-v1.0.0.zip) |

Every download is also on the [Releases](https://github.com/thomaspatrickpearl53-ctrl/hl-lua-addons/releases) page.

## How to install

1. Download the addon's ZIP.
2. Close Half-Life.
3. Open your Half-Life folder (in Steam: right-click Half-Life > Manage > Browse local files) and go into `hl_lua`.
4. Extract the ZIP there. Each ZIP contains an `addons` folder, so the addon lands in the right place:

   ```
   Half-Life\hl_lua\addons\<addon name>\addon.json
   ```

   If you end up with `addons\addons\...` or `addons\<name>\<name>\...`, move the folder up one level.
5. Start Half-Life: Lua.

**Disable** an addon: open `addons\<addon name>\addon.json` and set `"enabled": false`.
**Remove** an addon: delete its `addons\<addon name>` folder.
Restart the game after either change. Install anything listed under "Needs" yourself.

In multiplayer, everyone needs the same addons as the host.

## Making an addon

An addon ZIP should look like this:

```
addons/my_weapon/addon.json
addons/my_weapon/LICENSE.txt
addons/my_weapon/lua/weapons/weapon_my_weapon.lua
addons/my_weapon/models/my_weapon/...   (optional)
addons/my_weapon/sound/my_weapon/...    (optional)
```

Use a lowercase folder name and keep your models and sounds in folders named after the addon so they don't overwrite other addons. Don't include Half-Life's own files, other people's assets you don't have permission to share, DLLs or executables. The Lua API is described in `LUA.md` in your `hl_lua` folder.

Want yours listed here? [Submit it](https://github.com/thomaspatrickpearl53-ctrl/hl-lua-addons/issues/new?template=submit-addon.yml). The owner checks submissions before adding them. Garry's Mod addons don't work without changes.

Each addon keeps its creator's license.

Maintainer notes: [SETUP.md](SETUP.md).
