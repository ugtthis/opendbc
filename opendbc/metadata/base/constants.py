"""
Constants used throughout the metadata framework.

This module defines constants such as column names, star ratings, and support types.
"""

# Column definitions for documentation tables
COLUMNS = {
    "MAKE": "Make",
    "MODEL": "Model",
    "PACKAGE": "Supported Package",
    "LONGITUDINAL": "ACC",
    "FSR_LONGITUDINAL": "No ACC accel below",
    "FSR_STEERING": "No ALC below",
    "STEERING_TORQUE": "Steering Torque",
    "AUTO_RESUME": "Resume from stop",
    "HARDWARE": "Hardware Needed",
    "VIDEO": "Video"
}

# Extra cars column definitions
EXTRA_CARS_COLUMNS = {
    "MAKE": "Make",
    "MODEL": "Model",
    "PACKAGE": "Package",
    "SUPPORT": "Support Level"
}

# Star rating definitions
STARS = {
    "full": "★",
    "half": "½",
    "empty": "☆"
}

# Support type definitions
SUPPORT_TYPES = {
    "upstream": {
        "name": "Upstream",
        "description": "Actively maintained by comma, plug-and-play in release versions of openpilot",
        "link": "#upstream"
    },
    "review": {
        "name": "Under review",
        "description": "Dashcam, but planned for official support after safety validation",
        "link": "#under-review"
    },
    "dashcam": {
        "name": "Dashcam mode",
        "description": "Dashcam, but may be drivable in a community fork",
        "link": "#dashcam"
    },
    "community": {
        "name": "Community",
        "description": "Not upstream, but available in a custom community fork, not validated by comma",
        "link": "#community"
    },
    "custom": {
        "name": "Custom",
        "description": "Upstream, but don't have a harness available or need an unusual custom install",
        "link": "#custom"
    },
    "incompatible": {
        "name": "Not compatible",
        "description": "Known fundamental incompatibility such as Flexray or hydraulic power steering",
        "link": "#incompatible"
    }
}

# Documentation formatting templates
DOCUMENTATION_TEMPLATES = {
    "star_icon": '<span class="star-icon {}">{}</span>',
    "video_icon": '<a href="{}" target="_blank"><img src="{}"></a>',
    "footnote_tag": '<sup>{}</sup>'
}

# Conversion constants
MS_TO_MPH = 2.23694  # Convert m/s to mph
GOOD_TORQUE_THRESHOLD = 1.8  # Threshold for "good" steering torque