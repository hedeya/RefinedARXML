#!/usr/bin/env python3
"""
Debug script for hierarchy view issues.

This script tests the hierarchy view to see why it's only showing the top node.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_hierarchy_building():
    """Test hierarchy building logic."""
    print("Hierarchy View Debug Test")
    print("=" * 30)
    
    try:
        from arxml_editor.core.arxml_model import ARXMLModel
        from arxml_editor.ui.hierarchy_view import HierarchyViewWidget
        from PySide6.QtWidgets import QApplication
        
        # Create application
        app = QApplication(sys.argv)
        
        # Load sample ARXML
        sample_file = project_root / "examples" / "hierarchy_sample.arxml"
        if not sample_file.exists():
            print(f"❌ Sample file not found: {sample_file}")
            return 1
        
        print(f"📁 Loading sample file: {sample_file}")
        
        # Create model and load file
        model = ARXMLModel()
        success = model.load_file(sample_file)
        
        if not success:
            print("❌ Failed to load ARXML file")
            return 1
        
        print("✅ ARXML file loaded successfully")
        
        # Check element index
        print(f"📊 Total elements in index: {len(model.element_index._by_path)}")
        print(f"📊 Total children mappings: {len(model.element_index._children)}")
        
        # Get all elements and analyze their structure
        all_elements = model.element_index.get_all_elements()
        print(f"📊 Total elements: {len(all_elements)}")
        
        # Show first few elements with their parent info
        print("\n📋 First 10 elements:")
        for i, element in enumerate(all_elements[:10]):
            print(f"  {i+1}. {element.short_name} ({element.element_type})")
            print(f"     Path: {element.path}")
            print(f"     Parent: {element.parent_path}")
            children = model.element_index.get_children(element.path)
            print(f"     Children: {len(children)}")
            print()
        
        # Find elements with no parent (root elements)
        root_elements = [elem for elem in all_elements if elem.parent_path is None or elem.parent_path == ""]
        print(f"📊 Root elements (no parent): {len(root_elements)}")
        
        # Find elements that are AR-PACKAGE (likely root elements)
        package_elements = [elem for elem in all_elements if elem.element_type == "AR-PACKAGE"]
        print(f"📊 AR-PACKAGE elements: {len(package_elements)}")
        
        for i, element in enumerate(package_elements):
            print(f"  {i+1}. {element.short_name} ({element.element_type})")
            children = model.element_index.get_children(element.path)
            print(f"     Children: {len(children)}")
            for j, child in enumerate(children[:3]):  # Show first 3 children
                print(f"       {j+1}. {child.short_name} ({child.element_type})")
            if len(children) > 3:
                print(f"       ... and {len(children) - 3} more")
        
        # Test hierarchy view
        print("\n🔍 Testing hierarchy view...")
        hierarchy_view = HierarchyViewWidget(model)
        
        # Set the first root element
        if root_elements:
            first_root = root_elements[0]
            print(f"🎯 Setting element: {first_root.short_name}")
            hierarchy_view.set_element(first_root.path)
            
            # Check scene nodes
            scene = hierarchy_view.scene
            print(f"📊 Scene root nodes: {len(scene.root_nodes)}")
            print(f"📊 Scene all nodes: {len(scene.all_nodes)}")
            
            # Check tree widget
            tree_widget = hierarchy_view.tree_widget
            print(f"📊 Tree widget top level items: {tree_widget.topLevelItemCount()}")
            
            if tree_widget.topLevelItemCount() > 0:
                root_item = tree_widget.topLevelItem(0)
                print(f"📊 Root item children: {root_item.childCount()}")
                
                # Show first few children
                for i in range(min(3, root_item.childCount())):
                    child_item = root_item.child(i)
                    print(f"  {i+1}. {child_item.text(0)}")
        
        print("\n✅ Hierarchy debug test completed")
        return 0
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return 1

def main():
    """Main function."""
    return test_hierarchy_building()

if __name__ == "__main__":
    sys.exit(main())