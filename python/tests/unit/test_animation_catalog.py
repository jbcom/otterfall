"""Unit tests for AnimationCatalog"""
import pytest
from mesh_toolkit.catalog import AnimationCatalog, AnimationId


class TestAnimationCatalog:
    """Test animation catalog lookups and enums"""
    
    @pytest.fixture
    def catalog(self):
        """Create catalog instance"""
        return AnimationCatalog()
    
    def test_catalog_loads_all_animations(self, catalog):
        """Test that catalog loads all 678 animations"""
        all_animations = catalog.list_all()
        assert len(all_animations) == 678
    
    def test_get_by_id_valid(self, catalog):
        """Test lookup by valid animation ID"""
        # ID 4 = Attack
        animation = catalog.get_by_id(4)
        assert animation["id"] == 4
        assert animation["name"] == "Attack"
        assert animation["category"] == "Fighting"
        assert animation["subcategory"] == "AttackingwithWeapon"
    
    def test_get_by_id_invalid_raises(self, catalog):
        """Test lookup by invalid ID raises KeyError"""
        with pytest.raises(KeyError, match="Animation with ID 9999 not found"):
            catalog.get_by_id(9999)
    
    def test_get_by_name_valid(self, catalog):
        """Test lookup by animation name"""
        animation = catalog.get_by_name("Attack")
        assert animation["id"] == 4
        assert animation["name"] == "Attack"
    
    def test_get_by_name_invalid_raises(self, catalog):
        """Test lookup by invalid name raises KeyError"""
        with pytest.raises(KeyError, match="Animation with name 'NonexistentAnimation' not found"):
            catalog.get_by_name("NonexistentAnimation")
    
    def test_get_by_slug_valid(self, catalog):
        """Test lookup by slug"""
        animation = catalog.get_by_slug("ATTACK")
        assert animation["id"] == 4
        assert animation["slug"] == "ATTACK"
    
    def test_get_by_slug_invalid_raises(self, catalog):
        """Test lookup by invalid slug raises KeyError"""
        with pytest.raises(KeyError, match="Animation with slug 'INVALID_SLUG' not found"):
            catalog.get_by_slug("INVALID_SLUG")
    
    def test_get_by_category(self, catalog):
        """Test filtering by category"""
        fighting_anims = catalog.get_by_category("Fighting")
        assert len(fighting_anims) > 0
        assert all(anim["category"] == "Fighting" for anim in fighting_anims)
    
    def test_get_by_category_and_subcategory(self, catalog):
        """Test filtering by category and subcategory"""
        attack_anims = catalog.get_by_category("Fighting", "AttackingwithWeapon")
        assert len(attack_anims) > 0
        assert all(
            anim["category"] == "Fighting" and 
            anim["subcategory"] == "AttackingwithWeapon"
            for anim in attack_anims
        )
    
    def test_list_categories(self, catalog):
        """Test listing all categories"""
        categories = catalog.list_categories()
        expected_categories = {"Fighting", "WalkAndRun", "DailyActions", "BodyMovements", "Dancing"}
        assert set(categories) == expected_categories
    
    def test_list_subcategories(self, catalog):
        """Test listing subcategories for a category"""
        fighting_subcats = catalog.list_subcategories("Fighting")
        assert "AttackingwithWeapon" in fighting_subcats
        assert "GettingHit" in fighting_subcats
        assert "Dying" in fighting_subcats
    
    def test_animation_id_enum_attack(self):
        """Test AnimationId enum for Attack"""
        assert AnimationId.ATTACK == 4
    
    def test_animation_id_enum_idle(self):
        """Test AnimationId enum for Idle"""
        assert AnimationId.IDLE == 0
    
    def test_animation_id_enum_walking_woman(self):
        """Test AnimationId enum for Walking_Woman"""
        assert AnimationId.WALKING_WOMAN == 1
    
    def test_animation_id_enum_has_all_animations(self):
        """Test that AnimationId enum has all 689 animations"""
        # Count enum members
        enum_count = len([member for member in dir(AnimationId) if not member.startswith('_')])
        assert enum_count == 689
    
    def test_no_fallback_logic_on_missing(self, catalog):
        """Test that missing animations raise exceptions, not fallback to defaults"""
        # This ensures deterministic behavior - no silent failures
        with pytest.raises(KeyError):
            catalog.get_by_id(-1)
        
        with pytest.raises(KeyError):
            catalog.get_by_name("")
        
        with pytest.raises(KeyError):
            catalog.get_by_slug("")
