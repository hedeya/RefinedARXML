"""
Package tree widget for ARXML navigation.

Provides hierarchical view of ARXML packages and elements with search and filtering.
"""

from typing import Optional, List, Dict, Any
from PySide6.QtWidgets import (
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QHBoxLayout, QWidget,
    QLineEdit, QPushButton, QComboBox, QLabel, QMenu, QHeaderView
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction

from ..core.arxml_model import ARXMLModel
from ..core.element_index import ElementInfo


class PackageTreeWidget(QWidget):
    """Widget for displaying ARXML package hierarchy."""
    
    # Signals
    element_selected = Signal(str)  # Emits element path when selected
    element_double_clicked = Signal(str)  # Emits element path when double-clicked
    
    def __init__(self, arxml_model: ARXMLModel):
        super().__init__()
        self.arxml_model = arxml_model
        self.tree_items: Dict[str, QTreeWidgetItem] = {}
        self.filtered_elements: List[ElementInfo] = []
        
        self._setup_ui()
        self._setup_connections()
    
    def _setup_ui(self):
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Search and filter controls
        self._create_search_controls(layout)
        
        # Tree widget
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Name", "Type", "Path"])
        self.tree_widget.setAlternatingRowColors(True)
        self.tree_widget.setRootIsDecorated(True)
        self.tree_widget.setSortingEnabled(False)
        
        # Configure header
        header = self.tree_widget.header()
        header.setStretchLastSection(False)
        # Allow the user to resize the 'Name' column interactively instead
        # of forcing it to always stretch. This enables moving the separator
        # between 'Name' and 'Type' to adjust column allocation.
        header.setSectionResizeMode(0, QHeaderView.Interactive)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        # Allow moving columns if desired
        try:
            header.setSectionsMovable(True)
        except Exception:
            pass
        
        layout.addWidget(self.tree_widget)
        
        # Context menu
        self.tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
    
    def _create_search_controls(self, layout: QVBoxLayout):
        """Create search and filter controls."""
        controls_layout = QHBoxLayout()
        
        # Search box
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search elements...")
        controls_layout.addWidget(self.search_edit)
        
        # Clear search button
        self.clear_button = QPushButton("Clear")
        self.clear_button.setMaximumWidth(60)
        controls_layout.addWidget(self.clear_button)
        
        # Filter by type
        self.type_filter = QComboBox()
        self.type_filter.addItem("All Types")
        self.type_filter.setMaximumWidth(120)
        controls_layout.addWidget(self.type_filter)
        
        layout.addLayout(controls_layout)
    
    def _setup_connections(self):
        """Set up signal connections."""
        # Tree selection
        self.tree_widget.itemSelectionChanged.connect(self._on_selection_changed)
        self.tree_widget.itemDoubleClicked.connect(self._on_item_double_clicked)
        
        # Search
        self.search_edit.textChanged.connect(self._on_search_changed)
        self.clear_button.clicked.connect(self._clear_search)
        
        # Type filter
        self.type_filter.currentTextChanged.connect(self._on_type_filter_changed)
        
        # Context menu
        self.tree_widget.customContextMenuRequested.connect(self._show_context_menu)
    
    def refresh(self):
        """Refresh the tree with current model data."""
        self.tree_widget.clear()
        self.tree_items.clear()
        self.filtered_elements.clear()
        
        if not self.arxml_model.current_file:
            return
        
        # Get all elements
        all_elements = self.arxml_model.element_index.get_all_elements()
        self.filtered_elements = all_elements.copy()
        
        # Update type filter
        self._update_type_filter()
        
        # Build tree
        self._build_tree()
        
        # Apply current filters
        self._apply_filters()
    
    def _build_tree(self):
        """Build the tree structure from elements."""
        # Group elements by parent path
        elements_by_parent = {}
        root_elements = []
        
        for element in self.filtered_elements:
            if element.parent_path is None or element.parent_path == "":
                root_elements.append(element)
            else:
                if element.parent_path not in elements_by_parent:
                    elements_by_parent[element.parent_path] = []
                elements_by_parent[element.parent_path].append(element)
        
        # Create root items
        for element in root_elements:
            item = self._create_tree_item(element)
            self.tree_widget.addTopLevelItem(item)
            self.tree_items[element.path] = item
        
        # Create child items recursively
        self._create_child_items(root_elements, elements_by_parent)
    
    def _create_child_items(self, parent_elements: List[ElementInfo], 
                           elements_by_parent: Dict[str, List[ElementInfo]]):
        """Create child items recursively."""
        for parent_element in parent_elements:
            parent_item = self.tree_items.get(parent_element.path)
            if not parent_item:
                continue
            
            children = elements_by_parent.get(parent_element.path, [])
            for child_element in children:
                child_item = self._create_tree_item(child_element)
                parent_item.addChild(child_item)
                self.tree_items[child_element.path] = child_item
                
                # Recursively create grandchildren
                grandchildren = elements_by_parent.get(child_element.path, [])
                if grandchildren:
                    self._create_child_items([child_element], elements_by_parent)
    
    def _create_tree_item(self, element: ElementInfo) -> QTreeWidgetItem:
        """Create a tree item for an element."""
        item = QTreeWidgetItem()
        
        # Set display data
        display_name = element.short_name or element.element_type or "Unnamed"
        item.setText(0, display_name)
        item.setText(1, element.element_type or "Unknown")
        item.setText(2, element.path)
        
        # Set tooltip
        tooltip = f"Path: {element.path}\nType: {element.element_type}"
        if element.uuid:
            tooltip += f"\nUUID: {element.uuid}"
        item.setToolTip(0, tooltip)
        
        # Set icon based on element type
        self._set_item_icon(item, element)
        
        # Store element reference
        item.setData(0, Qt.UserRole, element)
        
        return item
    
    def _set_item_icon(self, item: QTreeWidgetItem, element: ElementInfo):
        """Set icon for tree item based on element type."""
        # This would use actual icons in a full implementation
        # For now, we'll use text indicators
        icon_text = ""
        
        if element.element_type == "AUTOSAR":
            icon_text = "🏠"
        elif element.element_type == "AR-PACKAGE":
            icon_text = "📦"
        elif element.element_type == "ELEMENT":
            icon_text = "📄"
        elif element.element_type == "CONTAINER":
            icon_text = "📋"
        elif element.element_type == "PARAMETER":
            icon_text = "⚙️"
        elif element.is_reference:
            icon_text = "🔗"
        else:
            icon_text = "📝"
        
        # In a real implementation, you'd set an actual icon here
        # item.setIcon(0, icon)
    
    def _update_type_filter(self):
        """Update the type filter dropdown."""
        current_text = self.type_filter.currentText()
        self.type_filter.clear()
        self.type_filter.addItem("All Types")
        
        # Get unique element types
        types = set()
        for element in self.filtered_elements:
            if element.element_type:
                types.add(element.element_type)
        
        # Add types to filter
        for element_type in sorted(types):
            self.type_filter.addItem(element_type)
        
        # Restore selection if possible
        index = self.type_filter.findText(current_text)
        if index >= 0:
            self.type_filter.setCurrentIndex(index)
    
    def _apply_filters(self):
        """Apply current search and type filters."""
        search_text = self.search_edit.text().lower()
        type_filter = self.type_filter.currentText()
        
        # Show/hide items based on filters
        for i in range(self.tree_widget.topLevelItemCount()):
            self._apply_filters_recursive(self.tree_widget.topLevelItem(i), search_text, type_filter)
    
    def _apply_filters_recursive(self, item: QTreeWidgetItem, search_text: str, type_filter: str):
        """Apply filters recursively to tree items."""
        element = item.data(0, Qt.UserRole)
        if not element:
            return
        
        # Check if item matches filters
        matches_search = not search_text or search_text in element.short_name.lower()
        matches_type = type_filter == "All Types" or element.element_type == type_filter
        
        # Show/hide item
        item.setHidden(not (matches_search and matches_type))
        
        # Apply to children
        for i in range(item.childCount()):
            self._apply_filters_recursive(item.child(i), search_text, type_filter)
    
    def _on_selection_changed(self):
        """Handle tree selection change."""
        current_item = self.tree_widget.currentItem()
        if current_item:
            element = current_item.data(0, Qt.UserRole)
            if element:
                self.element_selected.emit(element.path)
    
    def _on_item_double_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle item double-click."""
        element = item.data(0, Qt.UserRole)
        if element:
            self.element_double_clicked.emit(element.path)
    
    def _on_search_changed(self, text: str):
        """Handle search text change."""
        self._apply_filters()
    
    def _on_type_filter_changed(self, text: str):
        """Handle type filter change."""
        self._apply_filters()
    
    def _clear_search(self):
        """Clear search text."""
        self.search_edit.clear()
    
    def _show_context_menu(self, position):
        """Show context menu for tree item."""
        item = self.tree_widget.itemAt(position)
        if not item:
            return
        
        element = item.data(0, Qt.UserRole)
        if not element:
            return
        
        menu = QMenu(self)
        
        # Navigate actions
        go_to_def_action = QAction("Go to Definition", self)
        go_to_def_action.triggered.connect(lambda: self._go_to_definition(element))
        menu.addAction(go_to_def_action)
        
        find_refs_action = QAction("Find References", self)
        find_refs_action.triggered.connect(lambda: self._find_references(element))
        menu.addAction(find_refs_action)
        
        menu.addSeparator()
        
        # Edit actions
        edit_action = QAction("Edit Properties", self)
        edit_action.triggered.connect(lambda: self.element_selected.emit(element.path))
        menu.addAction(edit_action)
        
        delete_action = QAction("Delete Element", self)
        delete_action.triggered.connect(lambda: self._delete_element(element))
        menu.addAction(delete_action)
        
        menu.addSeparator()
        
        # View actions
        expand_all_action = QAction("Expand All", self)
        expand_all_action.triggered.connect(self._expand_all)
        menu.addAction(expand_all_action)
        
        collapse_all_action = QAction("Collapse All", self)
        collapse_all_action.triggered.connect(self._collapse_all)
        menu.addAction(collapse_all_action)
        
        menu.exec(self.tree_widget.mapToGlobal(position))
    
    def _go_to_definition(self, element: ElementInfo):
        """Go to definition of referenced element."""
        if element.is_reference:
            from ..utils.xml_utils import XMLUtils
            ref_value, dest = XMLUtils.get_reference_value(element.element)
            if ref_value:
                if dest == "DEST":
                    # Path reference
                    target_element = self.arxml_model.element_index.get_element_by_path(ref_value)
                    if target_element:
                        self._select_element_by_path(target_element.path)
                else:
                    # UUID reference
                    target_element = self.arxml_model.element_index.get_element_by_uuid(ref_value)
                    if target_element:
                        self._select_element_by_path(target_element.path)
    
    def _find_references(self, element: ElementInfo):
        """Find references to element."""
        references = self.arxml_model.reference_manager.get_references_to(element.path)
        
        if references:
            # Show references in a dialog or panel
            ref_paths = [ref.source_path for ref in references]
            self.status_message = f"Found {len(references)} references to {element.short_name}"
            # In a full implementation, you'd show this in a dedicated panel
        else:
            self.status_message = f"No references found to {element.short_name}"
    
    def _delete_element(self, element: ElementInfo):
        """Delete element after confirmation."""
        from PySide6.QtWidgets import QMessageBox
        
        reply = QMessageBox.question(
            self, "Delete Element",
            f"Are you sure you want to delete '{element.short_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success = self.arxml_model.delete_element(element.path)
            if success:
                self.refresh()
    
    def _expand_all(self):
        """Expand all tree items."""
        self.tree_widget.expandAll()
    
    def _collapse_all(self):
        """Collapse all tree items."""
        self.tree_widget.collapseAll()
    
    def _select_element_by_path(self, path: str):
        """Select element by path."""
        item = self.tree_items.get(path)
        if item:
            self.tree_widget.setCurrentItem(item)
            self.tree_widget.scrollToItem(item)
    
    def get_selected_element(self) -> Optional[ElementInfo]:
        """Get currently selected element."""
        current_item = self.tree_widget.currentItem()
        if current_item:
            return current_item.data(0, Qt.UserRole)
        return None
    
    def expand_to_path(self, path: str):
        """Expand tree to show specific path."""
        # Find the item and expand its parents
        item = self.tree_items.get(path)
        if item:
            # Expand all parents
            parent = item.parent()
            while parent:
                parent.setExpanded(True)
                parent = parent.parent()
            
            # Select the item
            self.tree_widget.setCurrentItem(item)
            self.tree_widget.scrollToItem(item)