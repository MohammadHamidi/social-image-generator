"""
Instagram Layout Types Module

This module provides all layout type implementations for the
Social Image Generator system.

Available layouts are registered automatically and can be accessed
via the layout registry.
"""

from .base import (
    LayoutEngine,
    TextLayoutEngine,
    PhotoLayoutEngine,
    CarouselLayoutEngine,
    register_layout,
    get_layout_engine,
    list_available_layouts,
    LAYOUT_REGISTRY
)

__all__ = [
    'LayoutEngine',
    'TextLayoutEngine',
    'PhotoLayoutEngine',
    'CarouselLayoutEngine',
    'register_layout',
    'get_layout_engine',
    'list_available_layouts',
    'LAYOUT_REGISTRY'
]

# Import all layout implementations to trigger registration
# Layouts will be auto-discovered and registered via @register_layout decorator

def import_layouts():
    """Import all layout modules to register them."""
    import os
    import importlib

    layouts_dir = os.path.dirname(__file__)

    # Get all .py files except __init__ and base
    for filename in os.listdir(layouts_dir):
        if filename.endswith('.py') and filename not in ('__init__.py', 'base.py'):
            module_name = filename[:-3]  # Remove .py
            try:
                # Import relative to layouts package
                importlib.import_module(f'layouts.{module_name}', package='src')
            except Exception as e:
                print(f"Warning: Could not import layout module {module_name}: {e}")
                import traceback
                traceback.print_exc()

# Auto-import all layouts
import_layouts()

# Also explicitly import known layouts to ensure they're registered
try:
    from . import headline_promo
except ImportError:
    pass  # Layout not available yet
