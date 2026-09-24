bl_info = {
    "name": "Aspect Ratio Helper",
    "author": "dotdesigned",
    "maintainer": "dotdesigned",
    "version": (1, 1, 5),
    "blender": (3, 6, 0),
    "location": "Output Properties > Format",
    "description": "Quickly apply cinema and video aspect-ratio resolution presets.",
    "category": "Render",
}

import bpy
from bpy.app.handlers import persistent
from bpy.types import Operator, Panel, PropertyGroup
from bpy.props import EnumProperty, PointerProperty, BoolProperty


# Presets sourced from the Firehouse Aspect Ratio Cheat Sheet:
# https://www.wearethefirehouse.com/aspect-ratio-cheat-sheet

PRESETS = {
    "CINEMA_DCP_4K": {
        "label": "Cinema DCP 4K",
        "items": [
            ("Flat (1.85)", 3996, 2160),
            ("Scope (2.39)", 4096, 1716),
            ("Full Container (1.90)", 4096, 2160),
        ],
    },
    "8K": {
        "label": "8K",
        "items": [
            ("0.80 (4:5)", 3686, 4608),
            ("1.25 (5:4)", 5760, 4608),
            ("1.33 (4:3)", 6144, 4608),
            ("1.66 (5:3)", 7680, 4608),
            ("1.78 (16:9)", 8192, 4608),
            ("1.85", 8192, 4428),
            ("1.90", 8192, 4320),
            ("2.00", 8192, 4096),
            ("2.35", 8192, 3486),
            ("2.37", 8192, 3456),
            ("2.39", 8192, 3428),
            ("2.40", 8192, 3414),
            ("2.44", 8192, 3356),
        ],
    },
    "6K": {
        "label": "6K",
        "items": [
            ("0.80 (4:5)", 2764, 3456),
            ("1.25 (5:4)", 4320, 3456),
            ("1.33 (4:3)", 4608, 3456),
            ("1.66 (5:3)", 5760, 3456),
            ("1.78 (16:9)", 6144, 3456),
            ("1.85", 6144, 3320),
            ("1.90", 6144, 3234),
            ("2.00", 6144, 3072),
            ("2.35", 6144, 2614),
            ("2.37", 6144, 2592),
            ("2.39", 6144, 2570),
            ("2.40", 6144, 2560),
            ("2.44", 6144, 2518),
        ],
    },
    "4K": {
        "label": "4K",
        "items": [
            ("0.80 (4:5)", 1842, 2304),
            ("1.25 (5:4)", 2880, 2304),
            ("1.33 (4:3)", 3072, 2304),
            ("1.66 (5:3)", 3840, 2304),
            ("1.78 (16:9)", 4096, 2304),
            ("1.85", 4096, 2214),
            ("1.90", 4096, 2160),
            ("2.00", 4096, 2048),
            ("2.35", 4096, 1742),
            ("2.37", 4096, 1728),
            ("2.39", 4096, 1716),
            ("2.40", 4096, 1706),
            ("2.44", 4096, 1678),
        ],
    },
    "3K": {
        "label": "3K",
        "items": [
            ("0.80 (4:5)", 1382, 1728),
            ("1.25 (5:4)", 2160, 1728),
            ("1.33 (4:3)", 2304, 1728),
            ("1.66 (5:3)", 2880, 1728),
            ("1.78 (16:9)", 3072, 1728),
            ("1.85", 3072, 1660),
            ("1.90", 3072, 1620),
            ("2.00", 3072, 1536),
            ("2.35", 3072, 1306),
            ("2.37", 3072, 1296),
            ("2.39", 3072, 1284),
            ("2.40", 3072, 1280),
            ("2.44", 3072, 1259),
        ],
    },
    "2K": {
        "label": "2K",
        "items": [
            ("0.80 (4:5)", 922, 1152),
            ("1.25 (5:4)", 1440, 1152),
            ("1.33 (4:3)", 1536, 1152),
            ("1.66 (5:3)", 1920, 1152),
            ("1.78 (16:9)", 2048, 1152),
            ("1.85", 2048, 1106),
            ("1.90", 2048, 1078),
            ("2.00", 2048, 1024),
            ("2.35", 2048, 870),
            ("2.37", 2048, 864),
            ("2.39", 2048, 858),
            ("2.40", 2048, 852),
            ("2.44", 2048, 838),
        ],
    },
    "CINEMA_DCP_2K": {
        "label": "Cinema DCP 2K",
        "items": [
            ("Flat (1.85)", 1998, 1080),
            ("Scope (2.39)", 2048, 858),
            ("Full Container (1.90)", 2048, 1080),
        ],
    },
    "8K_UHD": {
        "label": "8K UHD",
        "items": [
            ("0.80 (4:5)", 2765, 3456),
            ("1.25 (5:4)", 5400, 3456),
            ("1.33 (4:3)", 5760, 3456),
            ("1.66 (5:3)", 7200, 3456),
            ("1.78 (16:9)", 7680, 4320),
            ("1.85", 7680, 4150),
            ("1.90", 7680, 4042),
            ("2.00", 7680, 3840),
            ("2.35", 7680, 3268),
            ("2.37", 7680, 3240),
            ("2.39", 7680, 3214),
            ("2.40", 7680, 3200),
            ("2.44", 7680, 3148),
        ],
    },
    "5K": {
        "label": "5K",
        "items": [
            ("0.80 (4:5)", 2304, 2880),
            ("1.25 (5:4)", 3600, 2880),
            ("1.33 (4:3)", 3840, 2880),
            ("1.66 (5:3)", 4800, 2880),
            ("1.78 (16:9)", 5120, 2880),
            ("1.85", 5120, 2768),
            ("1.90", 5120, 2700),
            ("2.00", 5120, 2560),
            ("2.35", 5120, 2178),
            ("2.37", 5120, 2160),
            ("2.39", 5120, 2142),
            ("2.40", 5120, 2136),
            ("2.44", 5120, 2098),
        ],
    },
    "4K_UHD": {
        "label": "4K UHD",
        "items": [
            ("0.80 (4:5)", 1728, 2160),
            ("1.25 (5:4)", 2700, 2160),
            ("1.33 (4:3)", 2880, 2160),
            ("1.66 (5:3)", 3600, 2160),
            ("1.78 (16:9)", 3840, 2160),
            ("1.85", 3840, 2076),
            ("1.90", 3840, 2020),
            ("2.00", 3840, 1920),
            ("2.35", 3840, 1634),
            ("2.37", 3840, 1620),
            ("2.39", 3840, 1606),
            ("2.40", 3840, 1600),
            ("2.44", 3840, 1574),
        ],
    },
    "3K_UHD": {
        "label": "3K UHD",
        "items": [
            ("0.80 (4:5)", 1296, 1620),
            ("1.25 (5:4)", 2024, 1620),
            ("1.33 (4:3)", 2160, 1620),
            ("1.66 (5:3)", 2700, 1620),
            ("1.78 (16:9)", 2880, 1620),
            ("1.85", 2880, 1556),
            ("1.90", 2880, 1516),
            ("2.00", 2880, 1440),
            ("2.35", 2880, 1226),
            ("2.37", 2880, 1216),
            ("2.39", 2880, 1204),
            ("2.40", 2880, 1200),
            ("2.44", 2880, 1180),
        ],
    },
    "1080P": {
        "label": "1080p",
        "items": [
            ("0.80 (4:5)", 864, 1080),
            ("1.25 (5:4)", 1350, 1080),
            ("1.33 (4:3)", 1440, 1080),
            ("1.66 (5:3)", 1800, 1080),
            ("1.78 (16:9)", 1920, 1080),
            ("1.85", 1920, 1038),
            ("1.90", 1920, 1010),
            ("2.00", 1920, 960),
            ("2.35", 1920, 816),
            ("2.37", 1920, 810),
            ("2.39", 1920, 802),
            ("2.40", 1920, 800),
            ("2.44", 1920, 786),
        ],
    },
    "720P": {
        "label": "720p",
        "items": [
            ("0.80 (4:5)", 576, 720),
            ("1.25 (5:4)", 900, 720),
            ("1.33 (4:3)", 960, 720),
            ("1.66 (5:3)", 1200, 720),
            ("1.78 (16:9)", 1280, 720),
            ("1.85", 1280, 692),
            ("1.90", 1280, 674),
            ("2.00", 1280, 640),
            ("2.35", 1280, 544),
            ("2.37", 1280, 540),
            ("2.39", 1280, 536),
            ("2.40", 1280, 532),
            ("2.44", 1280, 524),
        ],
    },
}




RATIO_LABELS = {
    "0.80": "4:5",
    "1.25": "5:4",
    "1.33": "4:3",
    "1.66": "5:3",
    "1.78": "16:9",
    "1.85": "1.85",
    "1.90": "1.90",
    "2.00": "2.00",
    "2.35": "2.35",
    "2.37": "2.37",
    "2.39": "2.39",
    "2.40": "2.40",
    "2.44": "2.44",
    "1.43": "1.43",
}

RATIO_USE_CASES = {
    "0.80": "Portrait photography • Social • Editorial",
    "1.25": "Photo prints • Editorial • Near-square photography",
    "1.33": "Classic TV • Photography • Presentations",
    "1.66": "European widescreen • Photography • Cinema",
    "1.78": "TV • YouTube • Games • Modern web video",
    "1.85": "Theatrical cinema • Traditional widescreen",
    "1.90": "Digital IMAX • Large-format cinema",
    "2.00": "Modern cinema • Streaming • Premium video",
    "2.35": "Anamorphic cinema • Very wide compositions",
    "2.37": "Anamorphic • Widescreen cinema",
    "2.39": "CinemaScope • Theatrical • Anamorphic cinema",
    "2.40": "Modern anamorphic • Ultra-wide cinema",
    "2.44": "Ultra-wide • Stylized cinematic compositions",
    "1.43": "IMAX GT • IMAX 70mm • Large-format cinema",
}



def _ratio_value(label):
    return label.split(" ")[0]


def _ratio_label(label):
    return RATIO_LABELS.get(_ratio_value(label), _ratio_value(label))


# Category hierarchy used by the selector menu.
# Additional IMAX presets. These are intentionally separate from the
# Firehouse table because 1.43:1 is an IMAX GT format rather than a
# Firehouse aspect-ratio preset.
IMAX_PRESETS = {
    "IMAX_GT": {
        "label": "IMAX GT — 1.43:1",
        # Keep every tier at the exact same mathematical 1.43:1 ratio.
        # The pixel dimensions are intentionally slightly non-standard at
        # some tiers because integer raster sizes cannot all be exact 1.43:1
        # while also matching conventional 8K/6K/5K/4K/3K/2K dimensions.
        # Exact ratio is more important here because Blender's camera framing
        # responds to the output aspect ratio.
        "items": (
            ("1.43", 6578, 4600),
            ("1.43", 5005, 3500),
            ("1.43", 4290, 3000),
            ("1.43", 3575, 2500),
            ("1.43", 2860, 2000),
            ("1.43", 2145, 1500),
        ),
    },
    "IMAX_DIGITAL": {
        "label": "IMAX Digital — 1.90:1",
        # Exact 1.90:1 (19:10) at every tier, again prioritizing stable
        # camera framing over preserving the rounded delivery dimensions of
        # individual IMAX examples.
        "items": (
            ("1.90", 8170, 4300),
            ("1.90", 6080, 3200),
            ("1.90", 5130, 2700),
            ("1.90", 4104, 2160),
            ("1.90", 3078, 1620),
            ("1.90", 2052, 1080),
        ),
    },
}



PRESETS.update(IMAX_PRESETS)

# Resolution stays independent from format. The user first chooses the
# resolution tier, then chooses the output format family.
RESOLUTION_ITEMS = (
    ("8K", "8K", "8K resolution tier"),
    ("6K", "6K", "6K resolution tier"),
    ("5K", "5K", "5K resolution tier"),
    ("4K", "4K", "4K resolution tier"),
    ("3K", "3K", "3K resolution tier"),
    ("2K", "2K", "2K resolution tier"),
    ("1080P", "1080p", "1080p resolution tier"),
    ("720P", "720p", "720p resolution tier"),
)

FORMAT_ITEMS = (
    ("STANDARD", "Standard", "Firehouse standard aspect-ratio presets"),
    ("DCP", "Cinema DCP", "Digital Cinema Package formats"),
    ("UHD", "UHD", "Ultra HD aspect-ratio presets"),
    ("IMAX_GT", "IMAX GT — 1.43:1", "IMAX GT / IMAX 70mm / 1.43:1"),
    ("IMAX_DIGITAL", "IMAX Digital — 1.90:1", "Digital IMAX / 1.90:1"),
)

FORMAT_LABELS = dict((key, label) for key, label, _description in FORMAT_ITEMS)

# Resolution tiers supported by each format.
FORMAT_RESOLUTIONS = {
    "STANDARD": ("8K", "6K", "5K", "4K", "3K", "2K", "1080P", "720P"),
    "DCP": ("4K", "2K"),
    "UHD": ("8K", "4K", "3K"),
    "IMAX_GT": ("8K", "6K", "5K", "4K", "3K", "2K"),
    "IMAX_DIGITAL": ("8K", "6K", "5K", "4K", "3K", "2K"),
}


def _nearest_supported_resolution(resolution, supported):
    """Return the closest supported resolution tier to the current choice."""
    if resolution in supported:
        return resolution

    order = [key for key, _label, _description in RESOLUTION_ITEMS]
    try:
        position = order.index(resolution)
    except ValueError:
        return supported[0]

    return min(
        supported,
        key=lambda key: abs(order.index(key) - position),
    )


def _category_for_selection(resolution, format_family):
    """Resolve the independent Resolution + Format selectors to a preset."""
    if resolution not in FORMAT_RESOLUTIONS.get(format_family, ()):
        return None

    if format_family == "STANDARD":
        return resolution

    if format_family == "DCP":
        return {
            "4K": "CINEMA_DCP_4K",
            "2K": "CINEMA_DCP_2K",
        }.get(resolution)

    if format_family == "UHD":
        return {
            "8K": "8K_UHD",
            "4K": "4K_UHD",
            "3K": "3K_UHD",
        }.get(resolution)

    if format_family in {"IMAX_GT", "IMAX_DIGITAL"}:
        return format_family

    return None


def _ratio_index_for_resolution(resolution):
    """Return the IMAX tier index for the selected resolution."""
    tiers = ("8K", "6K", "5K", "4K", "3K", "2K")
    try:
        return tiers.index(resolution)
    except ValueError:
        return None


def _apply_ratio(scene, category, index):
    """Apply the Firehouse preset exactly as published, without re-orienting it."""
    data = PRESETS.get(category)
    if not data:
        return False

    try:
        _, width, height = data["items"][int(index)]
    except (IndexError, ValueError, TypeError):
        return False

    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.resolution_percentage = 100
    return True


def flip_resolution(scene):
    """Flip the current render resolution while preserving the active preset."""
    if not scene:
        return False

    settings = scene.render
    settings.resolution_x, settings.resolution_y = (
        settings.resolution_y,
        settings.resolution_x,
    )
    settings.resolution_percentage = 100

    if hasattr(scene, "arh_props"):
        props = scene.arh_props
        props.flipped = not props.flipped
        props.custom_active = False
        props.expected_x = settings.resolution_x
        props.expected_y = settings.resolution_y

    return True


def _matching_ratio_index(scene, category):
    """Return the preset index matching the current render dimensions,
    including a deliberately flipped X/Y orientation."""
    data = PRESETS.get(category)
    if not data or not scene:
        return None

    width = scene.render.resolution_x
    height = scene.render.resolution_y

    for index, (_label, preset_width, preset_height) in enumerate(data["items"]):
        if width == preset_width and height == preset_height:
            return index
        if width == preset_height and height == preset_width:
            return index

    return None


def _display_ratio_label(label, flipped=False):
    """Display the selected ratio in the current orientation.

    X:Y labels are directional and reverse after Flip X/Y.
    Decimal cinema labels remain the same named standard after flipping;
    only the underlying render dimensions are swapped.
    """
    display = _ratio_label(label)

    if not flipped:
        return display

    ratio_key = _ratio_value(label)
    return {
        "0.80": "5:4",
        "1.25": "4:5",
        "1.33": "3:4",
        "1.66": "3:5",
        "1.78": "9:16",
    }.get(ratio_key, display)


def _is_custom_resolution(scene, category):
    """True when the current render dimensions are not a preset in this format."""
    return _matching_ratio_index(scene, category) is None


class ARHProperties(PropertyGroup):
    resolution: EnumProperty(
        name="Resolution",
        description="Choose the output resolution tier",
        items=RESOLUTION_ITEMS,
        default="4K",
    )
    format: EnumProperty(
        name="Format",
        description="Choose the output format",
        items=FORMAT_ITEMS,
        default="STANDARD",
    )
    flipped: BoolProperty(
        name="Flipped",
        description="The current preset is vertically oriented after using Flip X/Y",
        default=False,
    )
    selected_ratio: bpy.props.IntProperty(
        name="Selected Ratio",
        description="Currently selected aspect-ratio preset index",
        default=4,
    )
    custom_active: BoolProperty(
        name="Custom",
        description="The user manually changed the native render Resolution X/Y values",
        default=False,
    )
    expected_x: bpy.props.IntProperty(default=0, options={"HIDDEN"})
    expected_y: bpy.props.IntProperty(default=0, options={"HIDDEN"})


def _ratio_key_for_index(category, index):
    """Return the ratio key for a preset index."""
    data = PRESETS.get(category)
    if not data:
        return None
    try:
        return _ratio_value(data["items"][int(index)][0])
    except (IndexError, ValueError, TypeError):
        return None


def _find_ratio_index(category, ratio_key):
    """Find a preset index by ratio key, preserving ratio when resolution changes."""
    data = PRESETS.get(category)
    if not data:
        return None

    for index, (label, _width, _height) in enumerate(data["items"]):
        if _ratio_value(label) == ratio_key:
            return index
    return None


def _ensure_scene_state(scene):
    """Initialize add-on state lazily, outside Blender's restricted register context."""
    props = getattr(scene, "arh_props", None)
    if props is None:
        return None

    if props.expected_x == 0 or props.expected_y == 0:
        props.expected_x = scene.render.resolution_x
        props.expected_y = scene.render.resolution_y

    category = _category_for_selection(props.resolution, props.format)
    if props.format in {"IMAX_GT", "IMAX_DIGITAL"}:
        tier = _ratio_index_for_resolution(props.resolution)
        if tier is not None:
            props.selected_ratio = tier
    elif props.selected_ratio < 0 or props.selected_ratio >= len(PRESETS.get(category, {}).get("items", ())):
        props.selected_ratio = 0

    return props


def _set_expected_dimensions(scene):
    """Mark the current render dimensions as intentionally controlled by the addon."""
    props = getattr(scene, "arh_props", None)
    if props is None:
        return
    props.expected_x = scene.render.resolution_x
    props.expected_y = scene.render.resolution_y
    props.custom_active = False


@persistent
def _arh_track_manual_resolution_changes(scene, depsgraph):
    """Detect native Resolution X/Y edits without misclassifying addon actions.

    The addon records the dimensions it intentionally applied. If Blender later
    reports different dimensions and the addon did not update its expected
    values, the user changed Resolution X/Y manually, so Custom becomes active.
    """
    props = getattr(scene, "arh_props", None)
    if props is None:
        return

    current_x = scene.render.resolution_x
    current_y = scene.render.resolution_y

    if props.expected_x == 0 or props.expected_y == 0:
        _ensure_scene_state(scene)
        props.expected_x = current_x
        props.expected_y = current_y
        return

    if (current_x, current_y) != (props.expected_x, props.expected_y):
        props.custom_active = True
        props.flipped = False


class ARH_OT_set_resolution(Operator):
    bl_idname = "arh.set_resolution"
    bl_label = "Set Resolution"
    bl_options = {"INTERNAL"}

    resolution: bpy.props.StringProperty()

    @classmethod
    def description(cls, context, properties):
        return f"Set resolution to {properties.resolution}"

    def execute(self, context):
        props = context.scene.arh_props
        old_category = _category_for_selection(props.resolution, props.format)
        old_ratio = _ratio_key_for_index(old_category, props.selected_ratio)

        props.resolution = self.resolution

        # Resolution is the primary selector. If the current format does not
        # exist at the newly selected tier, fall back to Standard.
        if self.resolution not in FORMAT_RESOLUTIONS.get(props.format, ()):
            props.format = "STANDARD"

        new_category = _category_for_selection(props.resolution, props.format)

        if props.format in {"IMAX_GT", "IMAX_DIGITAL"}:
            new_index = _ratio_index_for_resolution(props.resolution)
            if new_index is not None:
                props.selected_ratio = new_index
        elif old_ratio is not None:
            new_index = _find_ratio_index(new_category, old_ratio)
            if new_index is not None:
                props.selected_ratio = new_index
            else:
                props.selected_ratio = 0
        else:
            props.selected_ratio = 0

        # Changing the selector does not constitute a manual X/Y edit.
        props.custom_active = False
        props.flipped = False

        return {"FINISHED"}


class ARH_OT_set_format(Operator):
    bl_idname = "arh.set_format"
    bl_label = "Set Format"
    bl_options = {"INTERNAL"}

    format_family: bpy.props.StringProperty()

    @classmethod
    def description(cls, context, properties):
        return FORMAT_LABELS.get(properties.format_family, "Choose a format")

    def execute(self, context):
        props = context.scene.arh_props
        if self.format_family not in FORMAT_LABELS:
            return {"CANCELLED"}

        old_category = _category_for_selection(props.resolution, props.format)
        old_ratio = _ratio_key_for_index(old_category, props.selected_ratio)

        props.format = self.format_family

        # If the chosen format does not support the current resolution tier,
        # move to the closest supported tier.
        supported = FORMAT_RESOLUTIONS[self.format_family]
        if props.resolution not in supported:
            props.resolution = _nearest_supported_resolution(props.resolution, supported)

        new_category = _category_for_selection(props.resolution, props.format)

        if props.format in {"IMAX_GT", "IMAX_DIGITAL"}:
            new_index = _ratio_index_for_resolution(props.resolution)
            props.selected_ratio = 0 if new_index is None else new_index
        elif old_ratio is not None:
            new_index = _find_ratio_index(new_category, old_ratio)
            props.selected_ratio = 0 if new_index is None else new_index
        else:
            props.selected_ratio = 0

        props.custom_active = False
        props.flipped = False
        return {"FINISHED"}


class ARH_OT_set_ratio(Operator):
    bl_idname = "arh.set_ratio"
    bl_label = "Set Aspect Ratio"
    bl_options = {"REGISTER", "UNDO"}

    category: bpy.props.StringProperty()
    index: bpy.props.IntProperty()

    @classmethod
    def description(cls, context, properties):
        """Build a useful Blender tooltip from the actual button preset."""
        try:
            data = PRESETS[properties.category]
            index = int(properties.index)
            label, width, height = data["items"][index]

            display_ratio = _ratio_label(label)
            ratio_key = _ratio_value(label)
            use_case = RATIO_USE_CASES.get(ratio_key)
            if use_case is None:
                use_case = RATIO_USE_CASES.get(display_ratio, "General-purpose framing")

            if properties.category in {"CINEMA_DCP_4K", "CINEMA_DCP_2K"}:
                dcp_use_cases = (
                    "Standard theatrical widescreen • General-purpose cinema framing",
                    "Anamorphic widescreen • Cinematic / epic compositions",
                    "Full DCP container • Digital cinema / IMAX-compatible framing",
                )
                use_case = dcp_use_cases[index]
            elif properties.category == "IMAX_GT":
                use_case = "IMAX GT • IMAX 70mm • Large-format cinema"
            elif properties.category == "IMAX_DIGITAL":
                use_case = "Digital IMAX • Large-format cinema"

            return f"{display_ratio} • {width} × {height} px\n{use_case}"
        except (KeyError, IndexError, TypeError, ValueError, AttributeError):
            return "Apply this aspect-ratio preset"

    def execute(self, context):
        props = context.scene.arh_props
        category = _category_for_selection(props.resolution, props.format)
        if not category:
            self.report(
                {"ERROR"},
                f"{FORMAT_LABELS.get(props.format, 'Format')} is not available at {props.resolution}",
            )
            return {"CANCELLED"}

        index = self.index
        if props.format in {"IMAX_GT", "IMAX_DIGITAL"}:
            index = _ratio_index_for_resolution(props.resolution)
            if index is None:
                self.report({"ERROR"}, "Choose an IMAX resolution from 8K to 2K")
                return {"CANCELLED"}

        if not _apply_ratio(context.scene, category, index):
            self.report({"ERROR"}, "Invalid aspect-ratio preset")
            return {"CANCELLED"}

        props.selected_ratio = index
        props.custom_active = False

        # If the user has deliberately flipped the current preset, apply the
        # selected ratio in that same orientation (for example 16:9 -> 9:16).
        if props.flipped:
            settings = context.scene.render
            settings.resolution_x, settings.resolution_y = (
                settings.resolution_y,
                settings.resolution_x,
            )
            settings.resolution_percentage = 100

        _set_expected_dimensions(context.scene)
        props.flipped = bool(props.flipped)
        return {"FINISHED"}


class ARH_OT_set_custom(Operator):
    bl_idname = "arh.set_custom"
    bl_label = "Custom"
    bl_description = (
        "Custom resolution is active when the current render dimensions "
        "do not match a preset"
    )
    bl_options = {"INTERNAL"}

    def execute(self, context):
        # Custom is a state indicator rather than a preset. The actual custom
        # dimensions are whatever the user has entered in Blender's native
        # Resolution X/Y fields.
        return {"FINISHED"}


class ARH_OT_flip_resolution(Operator):
    bl_idname = "arh.flip_resolution"
    bl_label = "Flip Resolution"
    bl_description = "Swap the current Resolution X and Y values"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        if not flip_resolution(context.scene):
            self.report({"ERROR"}, "Unable to flip resolution")
            return {"CANCELLED"}

        return {"FINISHED"}


class ARH_OT_ctrl_scroll(Operator):
    bl_idname = "arh.ctrl_scroll"
    bl_label = "Cycle Aspect Ratio Helper Menu"
    bl_options = {"INTERNAL"}

    direction: bpy.props.IntProperty(default=1)

    @classmethod
    def poll(cls, context):
        return context.area is not None and context.area.type == "PROPERTIES"

    def invoke(self, context, event):
        props = context.scene.arh_props
        x = event.mouse_region_x
        split = context.region.width * 0.60

        if x < split:
            resolution_keys = [
                key for key, _label, _description in RESOLUTION_ITEMS
                if key in FORMAT_RESOLUTIONS.get(props.format, ())
            ]
            if not resolution_keys:
                return {"CANCELLED"}
            current = resolution_keys.index(props.resolution)
            new_resolution = resolution_keys[(current + self.direction) % len(resolution_keys)]
            bpy.ops.arh.set_resolution(resolution=new_resolution)
        else:
            format_keys = [key for key, _label, _description in FORMAT_ITEMS]
            current = format_keys.index(props.format)
            new_format = format_keys[(current + self.direction) % len(format_keys)]
            bpy.ops.arh.set_format(format_family=new_format)

        context.area.tag_redraw()
        return {"FINISHED"}


class ARH_MT_resolution(bpy.types.Menu):
    bl_idname = "ARH_MT_resolution"
    bl_label = "Resolution"

    def draw(self, context):
        layout = self.layout
        props = context.scene.arh_props

        # Resolution choices are filtered by the currently selected format.
        # Each format therefore exposes only the tiers for which we have
        # actual presets, while Standard exposes the complete 8K-to-720p list.
        supported = FORMAT_RESOLUTIONS.get(props.format, ())
        for key, label, _description in RESOLUTION_ITEMS:
            if key not in supported:
                continue

            op = layout.operator(
                "arh.set_resolution",
                text=label,
                icon="CHECKMARK" if key == props.resolution else "NONE",
            )
            op.resolution = key


class ARH_MT_format(bpy.types.Menu):
    bl_idname = "ARH_MT_format"
    bl_label = "Format"

    def draw(self, context):
        layout = self.layout
        props = context.scene.arh_props

        # Only resolutions supported by the selected format are shown in the
        # Resolution menu. Selecting a format also snaps the current tier to
        # the closest supported one when necessary.
        for key, label, _description in FORMAT_ITEMS:
            op = layout.operator(
                "arh.set_format",
                text=label,
                icon="CHECKMARK" if key == props.format else "NONE",
            )
            op.format_family = key


def draw_aspect_ratio_helper(self, context):
    """Compact aspect-ratio helper embedded in Blender's Format panel."""
    scene = context.scene
    props = scene.arh_props
    layout = self.layout

    # Header: Resolution and Format are now independent selectors.
    row = layout.row(align=True)
    row.label(text="Aspect Ratio", icon="SCENE_DATA")
    row.menu(
        "ARH_MT_resolution",
        text=props.resolution,
    )
    row.menu(
        "ARH_MT_format",
        text=FORMAT_LABELS[props.format],
    )

    # Current resolution + simple X/Y flip button.
    row = layout.row(align=True)
    row.alignment = "RIGHT"
    row.label(
        text=f"{scene.render.resolution_x} × {scene.render.resolution_y}",
        icon="FULLSCREEN_ENTER",
    )
    row.operator(
        "arh.flip_resolution",
        text="Flip X/Y",
        icon="ARROW_LEFTRIGHT",
    )

    category = _category_for_selection(props.resolution, props.format)
    if not category:
        layout.label(
            text="Choose a compatible resolution for this format",
            icon="INFO",
        )
        return

    data = PRESETS[category]

    # IMAX is intentionally a single ratio button because Resolution already
    # selects the 8K/6K/5K/4K/3K/2K tier.
    if props.format in {"IMAX_GT", "IMAX_DIGITAL"}:
        index = _ratio_index_for_resolution(props.resolution)
        if index is None:
            return
        label, _width, _height = data["items"][index]
        row = layout.row(align=True)
        button = row.operator(
            "arh.set_ratio",
            text=_display_ratio_label(label, props.flipped),
            emboss=True,
            depress=(not props.custom_active and props.selected_ratio == index),
        )
        button.category = category
        button.index = index

        row.operator(
            "arh.set_custom",
            text="Custom",
            emboss=True,
            depress=props.custom_active,
        )
        return

    grid = layout.grid_flow(
        row_major=True,
        columns=4,
        even_columns=True,
        even_rows=True,
        align=True,
    )

    for idx, (label, width, height) in enumerate(data["items"]):
        button = grid.operator(
            "arh.set_ratio",
            text=_display_ratio_label(label, props.flipped),
            emboss=True,
            depress=(not props.custom_active and props.selected_ratio == idx),
        )
        button.category = category
        button.index = idx

    grid.operator(
        "arh.set_custom",
        text="Custom",
        emboss=True,
        depress=props.custom_active,
    )



_addon_keymaps = []


classes = (
    ARHProperties,
    ARH_OT_set_resolution,
    ARH_OT_set_format,
    ARH_OT_set_ratio,
    ARH_OT_set_custom,
    ARH_OT_flip_resolution,
    ARH_OT_ctrl_scroll,
    ARH_MT_resolution,
    ARH_MT_format,
)


def _get_format_panel():
    return getattr(bpy.types, "RENDER_PT_format", None)


def register():
    # Safe to run repeatedly from Blender's Text Editor.
    if hasattr(bpy.types.Scene, "arh_props"):
        del bpy.types.Scene.arh_props

    for cls in classes:
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.arh_props = PointerProperty(type=ARHProperties)

    if _arh_track_manual_resolution_changes not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(_arh_track_manual_resolution_changes)

    format_panel = _get_format_panel()
    if format_panel is not None:
        try:
            format_panel.remove(draw_aspect_ratio_helper)
        except Exception:
            pass
        format_panel.append(draw_aspect_ratio_helper)

    # Ctrl + mouse wheel cycles the selector under the cursor in the
    # Properties editor. This supplements Blender's normal menu scrolling.
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name="Aspect Ratio Helper", space_type="PROPERTIES", region_type="WINDOW")
        for event_type, direction in (("WHEELUPMOUSE", 1), ("WHEELDOWNMOUSE", -1)):
            kmi = km.keymap_items.new("arh.ctrl_scroll", event_type, "PRESS", ctrl=True)
            kmi.properties.direction = direction
            _addon_keymaps.append((km, kmi))


def unregister():
    try:
        bpy.app.handlers.depsgraph_update_post.remove(_arh_track_manual_resolution_changes)
    except ValueError:
        pass

    for km, kmi in _addon_keymaps:
        try:
            km.keymap_items.remove(kmi)
        except Exception:
            pass
    _addon_keymaps.clear()

    format_panel = _get_format_panel()
    if format_panel is not None:
        try:
            format_panel.remove(draw_aspect_ratio_helper)
        except Exception:
            pass

    if hasattr(bpy.types.Scene, "arh_props"):
        del bpy.types.Scene.arh_props

    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass


if __name__ == "__main__":
    register()
