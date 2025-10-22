#!/usr/bin/env python3
"""
Visual test for hierarchy view to debug display issues.

This script creates a simple window to test the hierarchy view visually.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_hierarchy_visual():
    """Test hierarchy view visually."""
    print("Hierarchy Visual Test")
    print("=" * 25)
    
    try:
        from arxml_editor.core.arxml_model import ARXMLModel
        from arxml_editor.ui.hierarchy_view import HierarchyViewWidget
        from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton
        from PySide6.QtCore import Qt
        
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
        
        # Create main window
        main_window = QMainWindow()
        main_window.setWindowTitle("Hierarchy View Visual Test")
        main_window.setGeometry(100, 100, 1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        main_window.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Add instructions
        instructions = QLabel("""
Hierarchy View Visual Test

This window shows the hierarchy view. You should see:
1. A tree widget on the left with the ARXML structure
2. A graphics view on the right showing the visual hierarchy
3. Both should show the full hierarchy, not just the top node

If you only see the top node, there's a display issue.
        """)
        instructions.setStyleSheet("padding: 10px; background-color: #f0f0f0;")
        layout.addWidget(instructions)
        
        # Create hierarchy view
        hierarchy_view = HierarchyViewWidget(model)
        layout.addWidget(hierarchy_view)
        
        # Add test buttons
        button_layout = QVBoxLayout()
        
        test_button = QPushButton("Test Hierarchy View")
        test_button.clicked.connect(lambda: test_hierarchy_functionality(hierarchy_view, model))
        button_layout.addWidget(test_button)
        
        expand_button = QPushButton("Expand All")
        expand_button.clicked.connect(lambda: hierarchy_view.expand_all())
        button_layout.addWidget(expand_button)
        
        layout.addLayout(button_layout)
        
        # Set the first root element
        all_elements = model.element_index.get_all_elements()
        package_elements = [elem for elem in all_elements if elem.element_type == "AR-PACKAGE"]
        
        if package_elements:
            first_package = package_elements[0]
            print(f"🎯 Setting element: {first_package.short_name}")
            hierarchy_view.set_element(first_package.path)
        
        # Show window
        main_window.show()
        
        print("✅ Test window created")
        print("Check the hierarchy view for proper display")
        print("Close the window to continue...")
        
        return app.exec()
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return 1

def test_hierarchy_functionality(hierarchy_view, model):
    """Test hierarchy view functionality."""
    print("\n🔍 Testing hierarchy functionality...")
    
    # Check scene
    scene = hierarchy_view.scene
    print(f"Scene root nodes: {len(scene.root_nodes)}")
    print(f"Scene all nodes: {len(scene.all_nodes)}")
    
    # Check tree widget
    tree_widget = hierarchy_view.tree_widget
    print(f"Tree widget top level items: {tree_widget.topLevelItemCount()}")
    
    if tree_widget.topLevelItemCount() > 0:
        root_item = tree_widget.topLevelItem(0)
        print(f"Root item text: {root_item.text(0)}")
        print(f"Root item children: {root_item.childCount()}")
        
        # Count total items recursively
        total_items = count_tree_items(root_item)
        print(f"Total tree items: {total_items}")
    
    # Check if nodes are visible
    visible_nodes = [node for node in scene.all_nodes.values() if node.isVisible()]
    print(f"Visible nodes: {len(visible_nodes)}")
    
    # Check layout
    if scene.root_nodes:
        root_node = scene.root_nodes[0]
        print(f"Root node position: ({root_node.x()}, {root_node.y()})")
        print(f"Root node size: {root_node.rect().size()}")
        print(f"Root node is expanded: {root_node.is_expanded}")

def count_tree_items(item):
    """Count total items in tree recursively."""
    count = 1  # Count the item itself
    for i in range(item.childCount()):
        count += count_tree_items(item.child(i))
    return count

def main():
    """Main function."""
    return test_hierarchy_visual()

if __name__ == "__main__":
    sys.exit(main())