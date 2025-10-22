#!/usr/bin/env python3
"""
Test script to verify the hierarchy view fix.

This script tests that the hierarchy view now shows the full hierarchy
instead of just the top node.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_hierarchy_fix():
    """Test that the hierarchy fix is working."""
    print("Hierarchy View Fix Test")
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
        
        # Create hierarchy view
        hierarchy_view = HierarchyViewWidget(model)
        
        # Get the first AR-PACKAGE element
        all_elements = model.element_index.get_all_elements()
        package_elements = [elem for elem in all_elements if elem.element_type == "AR-PACKAGE"]
        
        if not package_elements:
            print("❌ No AR-PACKAGE elements found")
            return 1
        
        first_package = package_elements[0]
        print(f"🎯 Testing with element: {first_package.short_name}")
        
        # Set the element
        hierarchy_view.set_element(first_package.path)
        
        # Check the results immediately after setting
        scene = hierarchy_view.scene
        tree_widget = hierarchy_view.tree_widget
        
        print(f"\n📊 Immediate results after set_element:")
        print(f"  Scene root nodes: {len(scene.root_nodes)}")
        print(f"  Scene all nodes: {len(scene.all_nodes)}")
        print(f"  Tree widget top level items: {tree_widget.topLevelItemCount()}")
        
        # Check visibility immediately
        visible_nodes = [node for node in scene.all_nodes.values() if node.isVisible()]
        print(f"  Visible nodes immediately: {len(visible_nodes)}")
        
        # Force a scene update
        scene.update()
        
        # Check visibility after update
        visible_nodes_after = [node for node in scene.all_nodes.values() if node.isVisible()]
        print(f"  Visible nodes after update: {len(visible_nodes_after)}")
        
        print(f"\n📊 Results:")
        print(f"  Scene root nodes: {len(scene.root_nodes)}")
        print(f"  Scene all nodes: {len(scene.all_nodes)}")
        print(f"  Tree widget top level items: {tree_widget.topLevelItemCount()}")
        
        # Check if we have more than just the root node
        if len(scene.all_nodes) > 1:
            print("✅ SUCCESS: Multiple nodes found in scene")
        else:
            print("❌ FAILURE: Only root node found in scene")
            return 1
        
        # Check tree widget
        if tree_widget.topLevelItemCount() > 0:
            root_item = tree_widget.topLevelItem(0)
            if root_item.childCount() > 0:
                print("✅ SUCCESS: Tree widget has child items")
            else:
                print("❌ FAILURE: Tree widget has no child items")
                return 1
        
        # Check visibility
        visible_nodes = [node for node in scene.all_nodes.values() if node.isVisible()]
        print(f"  Visible nodes: {len(visible_nodes)}")
        
        if len(visible_nodes) > 1:
            print("✅ SUCCESS: Multiple nodes are visible")
        else:
            print("❌ FAILURE: Only one node is visible")
            return 1
        
        # Show hierarchy structure
        print(f"\n🌳 Hierarchy Structure:")
        if scene.root_nodes:
            root_node = scene.root_nodes[0]
            print(f"  Root: {root_node.element_info.short_name}")
            print(f"  Children: {len(root_node.children_nodes)}")
            
            for i, child in enumerate(root_node.children_nodes):
                print(f"    {i+1}. {child.element_info.short_name} ({child.element_info.element_type})")
                if child.children_nodes:
                    print(f"       Children: {len(child.children_nodes)}")
                    for j, grandchild in enumerate(child.children_nodes[:3]):
                        print(f"         {j+1}. {grandchild.element_info.short_name} ({grandchild.element_info.element_type})")
                    if len(child.children_nodes) > 3:
                        print(f"         ... and {len(child.children_nodes) - 3} more")
        
        print("\n✅ Hierarchy view fix test completed successfully!")
        return 0
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return 1

def main():
    """Main function."""
    return test_hierarchy_fix()

if __name__ == "__main__":
    sys.exit(main())