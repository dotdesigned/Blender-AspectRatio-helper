# Blender-AspectRatio-helper

A lightweight Blender add-on for quickly applying cinema and video aspect-ratio resolution presets directly inside Blender's **Output Properties → Format** panel.

## Version

**v1.1.5**

**Maintainer:** dotdesigned

**License:** GNU General Public License v3.0 (GPL-3.0)

**Blender:** 5.2 LTS

---

## Features

* Embedded directly into Blender's **Output Properties → Format** panel.
* Separate **Resolution** and **Format** selectors.
* Resolution tiers:

   8K ,  6K ,  5K ,  4K ,  3K ,  2K ,  1080p , 720p
* Format options:
  * Standard
  * Cinema DCP
  * UHD
  * IMAX GT 1.43:1
  * IMAX Digital 1.90:1
* Format-specific resolution filtering.
* Cinema DCP support for 4K and 2K.
* Aspect-ratio presets with friendly labels such as:
4:5 • 5:4 • 4:3 • 5:3 • 16:9 • 1.85 • 1.90 • 2.00 • 2.35 • 2.37 • 2.39 • 2.40 • 2.44

* Practical use-case tooltips for aspect-ratio buttons.
* **Flip X/Y** resolution control.
* Flipped aspect-ratio labels update automatically.
* Aspect-ratio selection persists when changing resolution tiers.
* **Custom** indicator activates when Blender's native Resolution X/Y values are manually changed.
* Ctrl + mouse-wheel cycling for Resolution and Format selectors.
* Blender 5.2 registration compatibility fix.

---

## Installation

### Blender Add-on Installation

1. Download `Aspect_Ratio_Helper_v1.1.5.zip`.
2. Open Blender.
3. Go to **Edit → Preferences → Add-ons**.
4. Click **Install from Disk**.
5. Select `Aspect_Ratio_Helper_v1.1.5.zip`.
6. Enable **Aspect Ratio Helper**.

The add-on will appear in:

**Output Properties → Format**

### Blender 5.2

This release includes a compatibility fix for Blender 5.2's restricted add-on registration context.

---

## Usage

Open:

**Properties → Output Properties → Format**

The Aspect Ratio Helper appears inside Blender's native Format panel.

Use:

* **Resolution** to choose the resolution tier.
* **Format** to choose Standard, Cinema DCP, UHD, or IMAX.
* The aspect-ratio buttons to apply a specific framing.
* **Flip X/Y** to swap the current resolution dimensions.
* **Custom** to indicate that the current dimensions do not match a preset.

---

## Resolution Presets

The Standard format provides resolution tiers from **8K through 720p**.

Available tiers:

| Tier  |
| ----- |
| 8K    |
| 6K    |
| 5K    |
| 4K    |
| 3K    |
| 2K    |
| 1080p |
| 720p  |

Other formats expose only their supported resolution tiers.

---

## Cinema DCP

Cinema DCP presets include:

### 4K

* Flat — 1.85:1
* Scope — 2.39:1
* Full Container — 1.90:1

### 2K

* Flat — 1.85:1
* Scope — 2.39:1
* Full Container — 1.90:1

---

## IMAX

The add-on includes:

* **IMAX GT — 1.43:1**
* **IMAX Digital — 1.90:1**

The Resolution selector determines the available IMAX resolution tier, while the aspect-ratio control applies the corresponding IMAX ratio.

---
## Source

The preset dimensions are based on the Firehouse Aspect Ratio Cheat Sheet:

(https://www.wearethefirehouse.com/aspect-ratio-cheat-sheet)

imax ratios were added manually.

---

## License

Aspect Ratio Helper is free and open-source software licensed under the **GNU General Public License v3.0**.


---

## Maintainer

**dotdesigned**

Aspect Ratio Helper — v1.1.5

