# Changelog

## [1.1.5] — Stable / Blender 5.2 Fix

- Fixed Blender 5.2 add-on installation/enabling failure caused by accessing `bpy.data.scenes` from the restricted `register()` context.
- Scene state is now initialized lazily when a normal scene context is available.
- No aspect-ratio preset behavior was intentionally changed.
