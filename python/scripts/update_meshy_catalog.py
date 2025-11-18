#!/usr/bin/env python3
"""
Scrapes Meshy's animation library documentation and generates:
1. tools/meshy/catalog/animations.json - Complete animation catalog
2. Updates tools/meshy/catalog/__init__.py with enums and catalog class
"""
import json
import re
from pathlib import Path
from typing import Dict, List, Any
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def generate_slug(name: str) -> str:
    """Generate Python-safe enum name from animation name
    
    Examples:
        "Walking_Woman" -> "WALKING_WOMAN"
        "90s Dance" -> "DANCE_90S"
        "T-Pose" -> "T_POSE"
    """
    # Remove special characters, replace spaces/hyphens with underscores
    slug = re.sub(r'[^\w\s-]', '', name)
    slug = re.sub(r'[-\s]+', '_', slug)
    
    # Convert to uppercase
    slug = slug.upper()
    
    # Move leading numbers to end (Python identifiers can't start with numbers)
    match = re.match(r'^(\d+)(.*)$', slug)
    if match:
        slug = f"{match.group(2)}_{match.group(1)}"
    
    # Remove leading/trailing underscores
    slug = slug.strip('_')
    
    # Ensure it's not empty
    if not slug:
        slug = "UNKNOWN"
    
    return slug


def organize_by_category(animations: List[Dict[str, Any]]) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
    """Organize animations by category and subcategory"""
    organized = {}
    
    for anim in animations:
        category = anim["category"]
        subcategory = anim["subcategory"]
        
        # Add slug
        anim["slug"] = generate_slug(anim["name"])
        
        if category not in organized:
            organized[category] = {}
        
        if subcategory not in organized[category]:
            organized[category][subcategory] = []
        
        organized[category][subcategory].append({
            "id": anim["id"],
            "name": anim["name"],
            "slug": anim["slug"],
            "category": category,
            "subcategory": subcategory
        })
    
    return organized


def main():
    print("🎬 Scraping Meshy Animation Library...")
    
    # Use Playwright to render JavaScript and get the table
    with sync_playwright() as p:
        print("  Launching browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("  Loading page...")
        page.goto("https://docs.meshy.ai/en/api/animation-library", wait_until="networkidle")
        
        # Wait for the table to be loaded
        print("  Waiting for table to render...")
        page.wait_for_selector("table", timeout=30000)
        
        # Get the rendered HTML
        html_content = page.content()
        browser.close()
    
    print(f"✓ Downloaded and rendered {len(html_content):,} bytes")
    
    # Parse the HTML table with BeautifulSoup
    soup = BeautifulSoup(html_content, 'lxml')
    table = soup.find('table')
    
    if not table:
        raise Exception("No table found in the page!")
    
    # Extract animations from table
    animations = []
    for row in table.find_all('tr')[1:]:  # Skip header row
        cells = row.find_all(['td', 'th'])
        if len(cells) >= 4:
            try:
                anim_id = cells[0].get_text(strip=True)
                if anim_id.isdigit():
                    animations.append({
                        "id": int(anim_id),
                        "name": cells[1].get_text(strip=True),
                        "category": cells[2].get_text(strip=True),
                        "subcategory": cells[3].get_text(strip=True)
                    })
            except (ValueError, IndexError):
                continue
    
    print(f"✓ Parsed {len(animations)} animations")
    
    if len(animations) < 500:
        print(f"⚠️  Warning: Expected 600+ animations, only found {len(animations)}")
    
    # Organize by category
    organized = organize_by_category(animations)
    
    # Print statistics
    print("\n📊 Animation Statistics:")
    total = 0
    for category, subcategories in sorted(organized.items()):
        cat_total = sum(len(anims) for anims in subcategories.values())
        total += cat_total
        print(f"  {category}: {cat_total}")
        for subcat, anims in sorted(subcategories.items()):
            print(f"    - {subcat}: {len(anims)}")
    print(f"\n  Total: {total} animations")
    
    # Create catalog directory
    catalog_dir = Path(__file__).parent.parent / "tools" / "meshy" / "catalog"
    catalog_dir.mkdir(exist_ok=True)
    
    # Write JSON
    json_path = catalog_dir / "animations.json"
    with open(json_path, "w") as f:
        json.dump({"categories": organized}, f, indent=2)
    
    print(f"\n✓ Wrote {json_path}")
    
    # Generate Python module
    generate_catalog_module(organized, catalog_dir)
    
    print("\n✅ Catalog generation complete!")


def generate_catalog_module(organized: Dict, catalog_dir: Path):
    """Generate __init__.py with AnimationCatalog class and enums"""
    
    # Collect all animations for master enum
    all_animations = []
    for category, subcategories in organized.items():
        for subcategory, anims in subcategories.items():
            all_animations.extend(anims)
    
    # Sort by ID to ensure consistent ordering
    all_animations.sort(key=lambda x: x["id"])
    
    # Generate category-specific enums
    category_enums = []
    for category, subcategories in sorted(organized.items()):
        # Create category enum name (e.g., "Walk And Run" -> "WalkAndRunAnimation")
        category_name = category.replace(" ", "").replace("&", "And")
        enum_name = f"{category_name}Animation"
        
        # Collect all animations in this category
        cat_animations = []
        for subcategory, anims in subcategories.items():
            cat_animations.extend(anims)
        cat_animations.sort(key=lambda x: x["id"])
        
        # Generate enum entries
        entries = []
        for anim in cat_animations:
            entries.append(f'    {anim["slug"]} = {anim["id"]}  # {anim["name"]}')
        
        category_enums.append(f'''
class {enum_name}(IntEnum):
    """Animation IDs for {category} category"""
{chr(10).join(entries)}
''')
    
    # Generate master AnimationId enum
    master_entries = []
    for anim in all_animations:
        master_entries.append(f'    {anim["slug"]} = {anim["id"]}  # {anim["name"]} ({anim["category"]} - {anim["subcategory"]})')
    
    # Generate complete module
    module_content = f'''"""
Meshy Animation Catalog
Auto-generated from https://docs.meshy.ai/en/api/animation-library

This module provides:
- AnimationCatalog: Query and lookup animations
- AnimationId: Master enum with all {len(all_animations)} animation IDs
- Category-specific enums: WalkAndRunAnimation, FightingAnimation, etc.

Usage:
    from tools.meshy.catalog import AnimationId, AnimationCatalog
    
    # Use type-safe enum instead of magic numbers
    anim_id = AnimationId.WALKING_WOMAN
    
    # Query the catalog
    catalog = AnimationCatalog()
    anim = catalog.get_by_id(4)
    print(anim["name"])  # "Attack"
"""
import json
from enum import IntEnum
from pathlib import Path
from typing import Dict, List, Optional, Any


class AnimationId(IntEnum):
    """Master enum with all Meshy animation IDs"""
{chr(10).join(master_entries)}

{chr(10).join(category_enums)}

class AnimationCatalog:
    """Query interface for Meshy animation library"""
    
    def __init__(self):
        catalog_path = Path(__file__).parent / "animations.json"
        with open(catalog_path) as f:
            self._data = json.load(f)
        
        # Build lookup indices
        self._by_id: Dict[int, Dict[str, Any]] = {{}}
        self._by_slug: Dict[str, Dict[str, Any]] = {{}}
        self._by_name: Dict[str, Dict[str, Any]] = {{}}
        
        for category, subcategories in self._data["categories"].items():
            for subcategory, animations in subcategories.items():
                for anim in animations:
                    self._by_id[anim["id"]] = anim
                    self._by_slug[anim["slug"].upper()] = anim
                    self._by_name[anim["name"].lower()] = anim
    
    def get_by_id(self, animation_id: int) -> Dict[str, Any]:
        """Get animation by ID
        
        Args:
            animation_id: Numeric animation ID
            
        Returns:
            Animation dict with id, name, slug, category, subcategory
            
        Raises:
            KeyError: If animation ID not found
        """
        if animation_id not in self._by_id:
            raise KeyError(f"Animation ID {{animation_id}} not found in catalog")
        return self._by_id[animation_id]
    
    def get_by_name(self, name: str) -> Dict[str, Any]:
        """Get animation by name (case-insensitive)
        
        Args:
            name: Animation name (e.g., "Walking Woman")
            
        Returns:
            Animation dict
            
        Raises:
            KeyError: If animation name not found
        """
        key = name.lower()
        if key not in self._by_name:
            raise KeyError(f"Animation name '{{name}}' not found in catalog")
        return self._by_name[key]
    
    def get_by_slug(self, slug: str) -> Dict[str, Any]:
        """Get animation by slug (case-insensitive)
        
        Args:
            slug: Animation slug (e.g., "WALKING_WOMAN" or "walking_woman")
            
        Returns:
            Animation dict
            
        Raises:
            KeyError: If animation slug not found
        """
        key = slug.upper()
        if key not in self._by_slug:
            raise KeyError(f"Animation slug '{{slug}}' not found in catalog")
        return self._by_slug[key]
    
    def get_by_category(self, category: str, subcategory: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all animations in a category or subcategory
        
        Args:
            category: Category name (e.g., "Walk And Run")
            subcategory: Optional subcategory filter (e.g., "Walking")
            
        Returns:
            List of animation dicts
            
        Raises:
            KeyError: If category not found
        """
        if category not in self._data["categories"]:
            raise KeyError(f"Category '{{category}}' not found")
        
        if subcategory:
            if subcategory not in self._data["categories"][category]:
                raise KeyError(f"Subcategory '{{subcategory}}' not found in category '{{category}}'")
            return self._data["categories"][category][subcategory]
        
        # Return all animations in category
        result = []
        for anims in self._data["categories"][category].values():
            result.extend(anims)
        return result
    
    def list_all(self) -> List[Dict[str, Any]]:
        """Get all animations"""
        return list(self._by_id.values())
    
    def list_categories(self) -> List[str]:
        """Get all category names"""
        return list(self._data["categories"].keys())
    
    def list_subcategories(self, category: str) -> List[str]:
        """Get all subcategory names for a category"""
        if category not in self._data["categories"]:
            raise KeyError(f"Category '{{category}}' not found")
        return list(self._data["categories"][category].keys())


__all__ = [
    "AnimationId",
    "AnimationCatalog",
{chr(10).join(f'    "{enum_name}",' for category, subcategories in sorted(organized.items()) for enum_name in [f"{category.replace(' ', '').replace('&', 'And')}Animation"])}
]
'''
    
    # Write __init__.py
    init_path = catalog_dir / "__init__.py"
    with open(init_path, "w") as f:
        f.write(module_content)
    
    print(f"✓ Wrote {init_path}")
    print(f"  - AnimationId enum with {len(all_animations)} entries")
    print(f"  - {len(category_enums)} category-specific enums")
    print(f"  - AnimationCatalog class with query methods")


if __name__ == "__main__":
    main()
