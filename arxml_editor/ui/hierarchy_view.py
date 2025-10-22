"""
Hierarchy view widget for ARXML tree-based visualization.

Provides interactive tree-based views showing parent-child relationships in ARXML structure.
"""

from typing import Optional, List, Dict, Any, Tuple, Set
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGraphicsView, QGraphicsScene,
    QGraphicsItem, QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem,
    QPushButton, QComboBox, QLabel, QSlider, QCheckBox, QGroupBox,
    QMenu, QMessageBox, QDialog, QFormLayout, QLineEdit, QTreeWidget,
    QTreeWidgetItem, QSplitter, QScrollArea, QFrame
)
from PySide6.QtCore import Qt, Signal, QRectF, QPointF, QTimer, QSize
from PySide6.QtGui import QPen, QBrush, QColor, QFont, QPainter, QPainterPath, QAction

from ..core.arxml_model import ARXMLModel
from ..core.element_index import ElementInfo
from ..core.reference_manager import ReferenceInfo


class HierarchyTreeNode(QGraphicsRectItem):
    """Represents a node in the hierarchy tree."""
    
    def __init__(self, element_info: ElementInfo, x: float = 0, y: float = 0, 
                 width: float = 150, height: float = 60, level: int = 0):
        super().__init__(x, y, width, height)
        
        self.element_info = element_info
        self.level = level
        self.is_expanded = True
        self.children_nodes: List['HierarchyTreeNode'] = []
        self.parent_node: Optional['HierarchyTreeNode'] = None
        
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        
        # Visual properties based on level
        self._setup_visual_properties()
        self._create_content()
    
    def _setup_visual_properties(self):
        """Set up visual properties based on hierarchy level."""
        # Color scheme based on level
        colors = [
            QColor(100, 150, 200),   # Level 0 - Root
            QColor(150, 200, 100),   # Level 1
            QColor(200, 150, 100),   # Level 2
            QColor(200, 100, 150),   # Level 3
            QColor(150, 100, 200),   # Level 4+
        ]
        
        level_color = colors[min(self.level, len(colors) - 1)]
        
        # Set visual properties
        self.setBrush(QBrush(level_color.lighter(180)))
        self.setPen(QPen(level_color.darker(120), 2))
        
        # Add level indicator
        if self.level > 0:
            level_rect = QGraphicsRectItem(0, 0, 8, self.rect().height(), self)
            level_rect.setBrush(QBrush(level_color))
            level_rect.setPen(QPen(Qt.NoPen))
    
    def _create_content(self):
        """Create text content for the node."""
        # Main name
        short_name = self.element_info.short_name or self.element_info.element_type or "Unnamed"
        self.name_item = QGraphicsTextItem(short_name, self)
        self.name_item.setDefaultTextColor(QColor(0, 0, 0))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.name_item.setFont(font)
        
        # Element type
        element_type = self.element_info.element_type or "Unknown"
        self.type_item = QGraphicsTextItem(element_type, self)
        self.type_item.setDefaultTextColor(QColor(100, 100, 100))
        type_font = QFont()
        type_font.setPointSize(8)
        self.type_item.setFont(type_font)
        
        # Position text elements
        self._position_text()
        
        # Add expand/collapse indicator
        if self.element_info.element_type in ["AR-PACKAGE", "ELEMENT", "CONTAINER"]:
            self.expand_indicator = QGraphicsTextItem("▼" if self.is_expanded else "▶", self)
            self.expand_indicator.setDefaultTextColor(QColor(50, 50, 50))
            expand_font = QFont()
            expand_font.setPointSize(8)
            self.expand_indicator.setFont(expand_font)
            self.expand_indicator.setPos(5, 5)
    
    def _position_text(self):
        """Position text elements within the node."""
        rect = self.rect()
        name_rect = self.name_item.boundingRect()
        type_rect = self.type_item.boundingRect()
        
        # Center the name
        name_x = max(15, (rect.width() - name_rect.width()) / 2)
        self.name_item.setPos(name_x, 8)
        
        # Center the type below the name
        type_x = max(15, (rect.width() - type_rect.width()) / 2)
        self.type_item.setPos(type_x, 25)
    
    def add_child(self, child_node: 'HierarchyTreeNode'):
        """Add a child node."""
        child_node.parent_node = self
        child_node.level = self.level + 1
        self.children_nodes.append(child_node)
        child_node._setup_visual_properties()
    
    def remove_child(self, child_node: 'HierarchyTreeNode'):
        """Remove a child node."""
        if child_node in self.children_nodes:
            self.children_nodes.remove(child_node)
            child_node.parent_node = None
    
    def toggle_expansion(self):
        """Toggle the expansion state."""
        self.is_expanded = not self.is_expanded
        if hasattr(self, 'expand_indicator'):
            self.expand_indicator.setPlainText("▼" if self.is_expanded else "▶")
    
    def get_all_descendants(self) -> List['HierarchyTreeNode']:
        """Get all descendant nodes."""
        descendants = []
        for child in self.children_nodes:
            descendants.append(child)
            descendants.extend(child.get_all_descendants())
        return descendants
    
    def itemChange(self, change, value):
        """Handle item changes."""
        if change == QGraphicsItem.ItemPositionChange:
            # Update child positions when this node moves
            self._update_children_positions()
        return super().itemChange(change, value)
    
    def _update_children_positions(self):
        """Update positions of child nodes."""
        if not self.is_expanded:
            return
        
        # This will be handled by the layout algorithm
        pass


class HierarchyTreeScene(QGraphicsScene):
    """Custom graphics scene for hierarchy tree visualization."""
    
    # Signals
    node_selected = Signal(str)  # Emits element path when node is selected
    node_expanded = Signal(str, bool)  # Emits element path and expansion state
    
    def __init__(self):
        super().__init__()
        self.root_nodes: List[HierarchyTreeNode] = []
        self.all_nodes: Dict[str, HierarchyTreeNode] = {}
        self.layout_timer = QTimer()
        self.layout_timer.timeout.connect(self._apply_tree_layout)
        self.layout_timer.setSingleShot(True)
        
        # Layout parameters
        self.node_spacing_x = 200
        self.node_spacing_y = 100
        self.level_indent = 50
    
    def add_root_node(self, element_info: ElementInfo) -> HierarchyTreeNode:
        """Add a root node to the hierarchy."""
        node = HierarchyTreeNode(element_info, level=0)
        self.root_nodes.append(node)
        self.all_nodes[element_info.path] = node
        self.addItem(node)
        return node
    
    def add_child_node(self, parent_path: str, element_info: ElementInfo) -> Optional[HierarchyTreeNode]:
        """Add a child node to an existing parent."""
        parent_node = self.all_nodes.get(parent_path)
        if not parent_node:
            return None
        
        child_node = HierarchyTreeNode(element_info, level=parent_node.level + 1)
        parent_node.add_child(child_node)
        self.all_nodes[element_info.path] = child_node
        self.addItem(child_node)
        
        # Add visual connection
        self._add_connection_line(parent_node, child_node)
        
        return child_node
    
    def _add_connection_line(self, parent: HierarchyTreeNode, child: HierarchyTreeNode):
        """Add a visual connection line between parent and child."""
        # This will be handled by the layout algorithm
        pass
    
    def get_node(self, path: str) -> Optional[HierarchyTreeNode]:
        """Get a node by its path."""
        return self.all_nodes.get(path)
    
    def expand_node(self, path: str, expanded: bool = True):
        """Expand or collapse a node."""
        node = self.all_nodes.get(path)
        if node:
            node.is_expanded = expanded
            node.toggle_expansion()
            self._update_visibility()
            self._apply_tree_layout()
    
    def _update_visibility(self):
        """Update visibility of nodes based on expansion state."""
        for node in self.all_nodes.values():
            # Hide if any parent is collapsed
            should_show = True
            current = node.parent_node
            while current:
                if not current.is_expanded:
                    should_show = False
                    break
                current = current.parent_node
            
            node.setVisible(should_show)
    
    def _apply_tree_layout(self):
        """Apply tree layout algorithm."""
        if not self.root_nodes:
            return
        
        print(f"Debug: Applying layout to {len(self.root_nodes)} root nodes")
        
        # Clear existing connections
        self._clear_connections()
        
        # Apply layout starting from root nodes
        y_offset = 50
        for root in self.root_nodes:
            print(f"Debug: Layout root node {root.element_info.short_name}, visible: {root.isVisible()}")
            y_offset = self._layout_subtree(root, 50, y_offset)
    
    def _layout_subtree(self, node: HierarchyTreeNode, x: float, y: float) -> float:
        """Layout a subtree starting from the given node."""
        if not node.isVisible():
            return y
        
        # Position the current node
        node.setPos(x, y)
        
        if not node.is_expanded or not node.children_nodes:
            return y + self.node_spacing_y
        
        # Layout children
        child_y = y + self.node_spacing_y
        child_x = x + self.level_indent
        
        for child in node.children_nodes:
            child_y = self._layout_subtree(child, child_x, child_y)
            # Add connection line
            self._add_connection_line(node, child)
        
        return child_y
    
    def _add_connection_line(self, parent: HierarchyTreeNode, child: HierarchyTreeNode):
        """Add a connection line between parent and child."""
        # Calculate connection points
        parent_rect = parent.rect()
        child_rect = child.rect()
        
        # Parent connection point (bottom center)
        parent_x = parent.x() + parent_rect.width() / 2
        parent_y = parent.y() + parent_rect.height()
        
        # Child connection point (top center)
        child_x = child.x() + child_rect.width() / 2
        child_y = child.y()
        
        # Create connection line
        line = QGraphicsLineItem(parent_x, parent_y, child_x, child_y)
        line.setPen(QPen(QColor(100, 100, 100), 1, Qt.SolidLine))
        self.addItem(line)
    
    def _clear_connections(self):
        """Clear all connection lines."""
        # Remove all line items
        items_to_remove = []
        for item in self.items():
            if isinstance(item, QGraphicsLineItem):
                items_to_remove.append(item)
        
        for item in items_to_remove:
            self.removeItem(item)
    
    def clear_hierarchy(self):
        """Clear all nodes and connections."""
        self.clear()
        self.root_nodes.clear()
        self.all_nodes.clear()


class HierarchyViewWidget(QWidget):
    """Widget for displaying ARXML hierarchy tree visualization."""
    
    # Signals
    element_selected = Signal(str)  # Emits element path when selected in hierarchy
    
    def __init__(self, arxml_model: ARXMLModel):
        super().__init__()
        self.arxml_model = arxml_model
        self.current_element: Optional[ElementInfo] = None
        
        self._setup_ui()
        self._setup_connections()
    
    def _setup_ui(self):
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Toolbar
        self._create_toolbar(layout)
        
        # Split view for tree and graphics
        splitter = QSplitter(Qt.Horizontal)
        
        # Tree widget for navigation
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabel("ARXML Structure")
        self.tree_widget.setMaximumWidth(300)
        splitter.addWidget(self.tree_widget)
        
        # Graphics view for hierarchy visualization
        self.scene = HierarchyTreeScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setDragMode(QGraphicsView.RubberBandDrag)
        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        # Use full viewport updates to avoid partial buffer commits that can
        # cause Wayland buffer-size mismatches on some compositors when the
        # window is maximized and the scene is updated heavily.
        try:
            self.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        except Exception:
            # QGraphicsView may not expose the mode on some bindings; ignore.
            pass
        
        splitter.addWidget(self.view)
        splitter.setSizes([300, 700])
        
        layout.addWidget(splitter)
        
        # Status label
        self.status_label = QLabel("No hierarchy loaded")
        self.status_label.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(self.status_label)
    
    def _create_toolbar(self, layout: QVBoxLayout):
        """Create hierarchy toolbar."""
        toolbar_layout = QHBoxLayout()
        
        # Layout controls
        self.auto_layout_button = QPushButton("Auto Layout")
        self.auto_layout_button.setEnabled(False)
        toolbar_layout.addWidget(self.auto_layout_button)
        
        self.expand_all_button = QPushButton("Expand All")
        self.expand_all_button.setEnabled(False)
        toolbar_layout.addWidget(self.expand_all_button)
        
        self.collapse_all_button = QPushButton("Collapse All")
        self.collapse_all_button.setEnabled(False)
        toolbar_layout.addWidget(self.collapse_all_button)
        
        # Zoom controls
        self.zoom_in_button = QPushButton("Zoom In")
        self.zoom_in_button.setEnabled(False)
        toolbar_layout.addWidget(self.zoom_in_button)
        
        self.zoom_out_button = QPushButton("Zoom Out")
        self.zoom_out_button.setEnabled(False)
        toolbar_layout.addWidget(self.zoom_out_button)
        
        self.fit_button = QPushButton("Fit to View")
        self.fit_button.setEnabled(False)
        toolbar_layout.addWidget(self.fit_button)
        
        toolbar_layout.addStretch()
        
        # Display options
        self.show_types_checkbox = QCheckBox("Show Types")
        self.show_types_checkbox.setChecked(True)
        toolbar_layout.addWidget(self.show_types_checkbox)
        
        self.show_levels_checkbox = QCheckBox("Show Levels")
        self.show_levels_checkbox.setChecked(True)
        toolbar_layout.addWidget(self.show_levels_checkbox)
        
        # Types selector merged from the former Type pane
        self.type_selector = QComboBox()
        self.type_selector.addItem("All Types")
        self.type_selector.setMaximumWidth(180)
        toolbar_layout.addWidget(self.type_selector)
        
        # Option to show full component/package hierarchy
        self.show_full_hierarchy_checkbox = QCheckBox("Show full hierarchy")
        self.show_full_hierarchy_checkbox.setChecked(False)
        toolbar_layout.addWidget(self.show_full_hierarchy_checkbox)
        
        layout.addLayout(toolbar_layout)
    
    def _setup_connections(self):
        """Set up signal connections."""
        # Toolbar buttons
        self.auto_layout_button.clicked.connect(self._apply_auto_layout)
        self.expand_all_button.clicked.connect(self._expand_all)
        self.collapse_all_button.clicked.connect(self._collapse_all)
        self.zoom_in_button.clicked.connect(self._zoom_in)
        self.zoom_out_button.clicked.connect(self._zoom_out)
        self.fit_button.clicked.connect(self._fit_to_view)
        
        # Display options
        self.show_types_checkbox.toggled.connect(self._toggle_types)
        self.show_levels_checkbox.toggled.connect(self._toggle_levels)
        self.type_selector.currentTextChanged.connect(self._on_type_selector_changed)
        self.show_full_hierarchy_checkbox.toggled.connect(self._on_full_hierarchy_toggled)
        
        # Scene signals
        self.scene.node_selected.connect(self._on_node_selected)
        self.scene.node_expanded.connect(self._on_node_expanded)
        
        # Tree widget signals
        self.tree_widget.itemClicked.connect(self._on_tree_item_clicked)
        self.tree_widget.itemExpanded.connect(self._on_tree_item_expanded)
        self.tree_widget.itemCollapsed.connect(self._on_tree_item_collapsed)
        
        # Context menu
        self.view.customContextMenuRequested.connect(self._show_context_menu)
    
    def set_element(self, path: str):
        """Set the current element and build hierarchy."""
        element = self.arxml_model.get_element_by_path(path)
        if not element:
            self._clear_hierarchy()
            return
        
        self.current_element = element

        # Populate type selector from model (merge of Type pane)
        self._populate_type_selector()

        self._build_hierarchy()
        self._populate_tree_widget()

    def _populate_type_selector(self):
        """Populate the type selector with available element types from the model."""
        types = set()
        for elem in self.arxml_model.element_index.get_all_elements():
            if elem.element_type:
                types.add(elem.element_type)

        current = self.type_selector.currentText()
        self.type_selector.blockSignals(True)
        self.type_selector.clear()
        self.type_selector.addItem("All Types")
        for t in sorted(types):
            self.type_selector.addItem(t)
        # restore previous if exists
        idx = self.type_selector.findText(current)
        if idx >= 0:
            self.type_selector.setCurrentIndex(idx)
        self.type_selector.blockSignals(False)
    
    def _build_hierarchy(self):
        """Build the hierarchy visualization."""
        if not self.current_element:
            return
        
        self.scene.clear_hierarchy()
        # If user requested full hierarchy, start from top-level packages
        if self.show_full_hierarchy_checkbox.isChecked():
            # build roots from all top-level elements (parent_path empty)
            root_elements = [e for e in self.arxml_model.element_index.get_all_elements() if not e.parent_path]
            for elem in root_elements:
                root_node = self.scene.add_root_node(elem)
                self._build_subtree(root_node, elem)
        else:
            # Start with the current element as root
            root_node = self.scene.add_root_node(self.current_element)
            # Build the complete hierarchy under the current element
            self._build_subtree(root_node, self.current_element)
        
        # Ensure all nodes are visible initially (they should be expanded by default)
        visible_count = 0
        for node in self.scene.all_nodes.values():
            node.setVisible(True)
            if node.isVisible():
                visible_count += 1
        
        print(f"Debug: Set {visible_count} nodes to visible out of {len(self.scene.all_nodes)}")
        
        # Defer layout slightly to allow the window and compositor to settle
        # (prevents rapid buffer reconfiguration on Wayland which can lead
        # to protocol errors when the surface is maximized).
        def _deferred_layout():
            try:
                self.scene._apply_tree_layout()
            except Exception:
                logging.getLogger(__name__).exception("Hierarchy layout failed")

        # Disable viewport updates while building the scene to reduce stress on
        # the compositor and avoid resizing artifacts.
        try:
            self.view.setUpdatesEnabled(False)
        except Exception:
            pass

        QTimer.singleShot(150, lambda: (_deferred_layout(), self.view.setUpdatesEnabled(True)))
        
        # Enable toolbar buttons
        self.auto_layout_button.setEnabled(True)
        self.expand_all_button.setEnabled(True)
        self.collapse_all_button.setEnabled(True)
        self.zoom_in_button.setEnabled(True)
        self.zoom_out_button.setEnabled(True)
        self.fit_button.setEnabled(True)
        
        # Update status
        node_count = len(self.scene.all_nodes)
        self.status_label.setText(f"Hierarchy: {node_count} nodes")
    
    def _build_subtree(self, parent_node: HierarchyTreeNode, element: ElementInfo):
        """Build a subtree starting from the given element."""
        # Optionally filter by the selected type
        selected_type = self.type_selector.currentText() if hasattr(self, 'type_selector') else "All Types"
        children = self.arxml_model.element_index.get_children(element.path)
        if selected_type and selected_type != "All Types":
            children = [c for c in children if c.element_type == selected_type]
        print(f"Debug: Building subtree for {element.short_name}, found {len(children)} children")
        
        for child in children:
            child_node = self.scene.add_child_node(element.path, child)
            if child_node:
                print(f"Debug: Added child {child.short_name}, visible: {child_node.isVisible()}")
                # Recursively build children
                self._build_subtree(child_node, child)
    
    def _populate_tree_widget(self):
        """Populate the tree widget with ARXML structure."""
        self.tree_widget.clear()
        
        if not self.current_element:
            return
        
        # Build tree widget items
        root_item = self._create_tree_item(self.current_element)
        self.tree_widget.addTopLevelItem(root_item)
        self._populate_tree_subtree(root_item, self.current_element)
        
        # Expand first level
        root_item.setExpanded(True)
    
    def _create_tree_item(self, element: ElementInfo) -> QTreeWidgetItem:
        """Create a tree widget item for an element."""
        short_name = element.short_name or element.element_type or "Unnamed"
        element_type = element.element_type or "Unknown"
        
        item = QTreeWidgetItem([short_name, element_type])
        item.setData(0, Qt.UserRole, element.path)
        
        # Set icon based on element type
        from PySide6.QtWidgets import QStyle
        if element.element_type == "AR-PACKAGE":
            item.setIcon(0, self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon))
        elif element.element_type in ["ELEMENT", "CONTAINER"]:
            item.setIcon(0, self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon))
        else:
            item.setIcon(0, self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
        
        return item
    
    def _populate_tree_subtree(self, parent_item: QTreeWidgetItem, element: ElementInfo):
        """Populate tree widget subtree."""
        children = self.arxml_model.element_index.get_children(element.path)
        
        for child in children:
            child_item = self._create_tree_item(child)
            parent_item.addChild(child_item)
            self._populate_tree_subtree(child_item, child)
    
    def _apply_auto_layout(self):
        """Apply automatic layout to the hierarchy."""
        self.scene._apply_tree_layout()
    
    def _expand_all(self):
        """Expand all nodes in the hierarchy."""
        for node in self.scene.all_nodes.values():
            self.scene.expand_node(node.element_info.path, True)
        self.tree_widget.expandAll()
    
    def _collapse_all(self):
        """Collapse all nodes in the hierarchy."""
        for node in self.scene.all_nodes.values():
            self.scene.expand_node(node.element_info.path, False)
        self.tree_widget.collapseAll()
    
    def _zoom_in(self):
        """Zoom in on the view."""
        self.view.scale(1.2, 1.2)
    
    def _zoom_out(self):
        """Zoom out of the view."""
        self.view.scale(0.8, 0.8)
    
    def _fit_to_view(self):
        """Fit the entire hierarchy to the view."""
        self.view.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
    
    def _toggle_types(self, show: bool):
        """Toggle display of element types."""
        for node in self.scene.all_nodes.values():
            if hasattr(node, 'type_item'):
                node.type_item.setVisible(show)
    
    def _toggle_levels(self, show: bool):
        """Toggle display of level indicators."""
        for node in self.scene.all_nodes.values():
            if hasattr(node, 'expand_indicator'):
                node.expand_indicator.setVisible(show)
    
    def _on_node_selected(self, path: str):
        """Handle node selection."""
        self.element_selected.emit(path)
    
    def _on_node_expanded(self, path: str, expanded: bool):
        """Handle node expansion."""
        # Update tree widget
        self._update_tree_item_expansion(path, expanded)

    def _on_type_selector_changed(self, text: str):
        """Handle type selection change - rebuild hierarchy with filter."""
        # Rebuild current hierarchy view using the newly selected type
        self._build_hierarchy()
        self._populate_tree_widget()

    def _on_full_hierarchy_toggled(self, checked: bool):
        """Handle full-hierarchy toggle - rebuild view."""
        # Rebuild to either show all top-level roots or only the selected element subtree
        self._build_hierarchy()
        self._populate_tree_widget()
    
    def _on_tree_item_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle tree item click."""
        path = item.data(0, Qt.UserRole)
        if path:
            # Select corresponding node in graphics view
            node = self.scene.get_node(path)
            if node:
                self.scene.clearSelection()
                node.setSelected(True)
                self.element_selected.emit(path)
    
    def _on_tree_item_expanded(self, item: QTreeWidgetItem):
        """Handle tree item expansion."""
        path = item.data(0, Qt.UserRole)
        if path:
            self.scene.expand_node(path, True)
    
    def _on_tree_item_collapsed(self, item: QTreeWidgetItem):
        """Handle tree item collapse."""
        path = item.data(0, Qt.UserRole)
        if path:
            self.scene.expand_node(path, False)
    
    def _update_tree_item_expansion(self, path: str, expanded: bool):
        """Update tree item expansion state."""
        # Find and update the corresponding tree item
        for i in range(self.tree_widget.topLevelItemCount()):
            item = self.tree_widget.topLevelItem(i)
            self._update_tree_item_recursive(item, path, expanded)
    
    def _update_tree_item_recursive(self, item: QTreeWidgetItem, path: str, expanded: bool):
        """Recursively update tree item expansion."""
        if item.data(0, Qt.UserRole) == path:
            item.setExpanded(expanded)
            return
        
        for i in range(item.childCount()):
            self._update_tree_item_recursive(item.child(i), path, expanded)
    
    def _show_context_menu(self, position):
        """Show context menu for the view."""
        menu = QMenu(self)
        
        expand_action = QAction("Expand", self)
        expand_action.triggered.connect(self._expand_selected)
        menu.addAction(expand_action)
        
        collapse_action = QAction("Collapse", self)
        collapse_action.triggered.connect(self._collapse_selected)
        menu.addAction(collapse_action)
        
        menu.addSeparator()
        
        layout_action = QAction("Auto Layout", self)
        layout_action.triggered.connect(self._apply_auto_layout)
        menu.addAction(layout_action)
        
        menu.exec(self.view.mapToGlobal(position))
    
    def _expand_selected(self):
        """Expand selected nodes."""
        selected_items = self.scene.selectedItems()
        for item in selected_items:
            if isinstance(item, HierarchyTreeNode):
                self.scene.expand_node(item.element_info.path, True)
    
    def _collapse_selected(self):
        """Collapse selected nodes."""
        selected_items = self.scene.selectedItems()
        for item in selected_items:
            if isinstance(item, HierarchyTreeNode):
                self.scene.expand_node(item.element_info.path, False)
    
    def _clear_hierarchy(self):
        """Clear the hierarchy display."""
        self.scene.clear_hierarchy()
        self.tree_widget.clear()
        self.status_label.setText("No hierarchy loaded")
        
        # Disable toolbar buttons
        self.auto_layout_button.setEnabled(False)
        self.expand_all_button.setEnabled(False)
        self.collapse_all_button.setEnabled(False)
        self.zoom_in_button.setEnabled(False)
        self.zoom_out_button.setEnabled(False)
        self.fit_button.setEnabled(False)