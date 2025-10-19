"""
Diagram view widget for ARXML visualizations.

Provides interactive diagrams for SWC compositions, system topologies, and reference relationships.
"""

from typing import Optional, List, Dict, Any, Tuple
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGraphicsView, QGraphicsScene,
    QGraphicsItem, QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem,
    QPushButton, QComboBox, QLabel, QSlider, QCheckBox, QGroupBox,
    QMenu, QMessageBox, QDialog, QFormLayout, QLineEdit
)
from PySide6.QtCore import Qt, Signal, QRectF, QPointF, QTimer
from PySide6.QtGui import QPen, QBrush, QColor, QFont, QPainter, QPainterPath, QAction

from ..core.arxml_model import ARXMLModel
from ..core.element_index import ElementInfo
from ..core.reference_manager import ReferenceInfo


class DiagramNode(QGraphicsRectItem):
    """Represents a node in the diagram."""
    
    def __init__(self, element_info: ElementInfo, x: float = 0, y: float = 0, 
                 width: float = 120, height: float = 80):
        super().__init__(x, y, width, height)
        self.element_info = element_info
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        
        # Visual properties
        self.setBrush(QBrush(QColor(200, 220, 255)))
        self.setPen(QPen(QColor(100, 150, 200), 2))
        
        # Calculate text dimensions
        short_name = element_info.short_name or element_info.element_type or "Unnamed"
        element_type = element_info.element_type or "Unknown"
        
        # Create text items with proper sizing
        self.text_item = QGraphicsTextItem(short_name, self)
        self.text_item.setDefaultTextColor(QColor(0, 0, 0))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.text_item.setFont(font)
        
        # Center the text horizontally
        text_rect = self.text_item.boundingRect()
        text_x = (width - text_rect.width()) / 2
        self.text_item.setPos(max(5, text_x), 10)
        
        # Add type label
        self.type_item = QGraphicsTextItem(element_type, self)
        self.type_item.setDefaultTextColor(QColor(100, 100, 100))
        type_font = QFont()
        type_font.setPointSize(8)
        self.type_item.setFont(type_font)
        
        # Center the type text horizontally
        type_rect = self.type_item.boundingRect()
        type_x = (width - type_rect.width()) / 2
        self.type_item.setPos(max(5, type_x), 35)
        
        # Adjust node size based on text content
        max_text_width = max(text_rect.width(), type_rect.width()) + 20
        if max_text_width > width:
            self.setRect(x, y, max_text_width, height)
    
    def itemChange(self, change, value):
        """Handle item changes."""
        if change == QGraphicsItem.ItemPositionChange:
            # Notify parent about position change
            if hasattr(self.scene(), 'node_moved'):
                self.scene().node_moved.emit(self.element_info.path, value)
        return super().itemChange(change, value)


class DiagramEdge(QGraphicsLineItem):
    """Represents an edge/connection in the diagram."""
    
    def __init__(self, source_node: DiagramNode, target_node: DiagramNode, 
                 reference_info: Optional[ReferenceInfo] = None):
        super().__init__()
        self.source_node = source_node
        self.target_node = target_node
        self.reference_info = reference_info
        
        # Visual properties
        self.setPen(QPen(QColor(150, 150, 150), 2))
        self.update_position()
    
    def update_position(self):
        """Update line position based on node positions."""
        if self.source_node and self.target_node:
            source_center = self.source_node.rect().center()
            target_center = self.target_node.rect().center()
            self.setLine(source_center.x(), source_center.y(), 
                        target_center.x(), target_center.y())


class DiagramScene(QGraphicsScene):
    """Custom graphics scene for ARXML diagrams."""
    
    # Signals
    node_selected = Signal(str)  # Emits element path when node is selected
    node_moved = Signal(str, QPointF)  # Emits element path and new position
    
    def __init__(self):
        super().__init__()
        self.nodes: Dict[str, DiagramNode] = {}
        self.edges: List[DiagramEdge] = []
        self.layout_timer = QTimer()
        self.layout_timer.timeout.connect(self._apply_layout)
        self.layout_timer.setSingleShot(True)
    
    def add_node(self, element_info: ElementInfo, x: float = 0, y: float = 0) -> DiagramNode:
        """Add a node to the diagram."""
        node = DiagramNode(element_info, x, y)
        self.nodes[element_info.path] = node
        self.addItem(node)
        return node
    
    def add_edge(self, source_path: str, target_path: str, reference_info: Optional[ReferenceInfo] = None) -> DiagramEdge:
        """Add an edge between nodes."""
        source_node = self.nodes.get(source_path)
        target_node = self.nodes.get(target_path)
        
        if source_node and target_node:
            edge = DiagramEdge(source_node, target_node, reference_info)
            self.edges.append(edge)
            self.addItem(edge)
            return edge
        return None
    
    def remove_node(self, path: str):
        """Remove a node and its edges."""
        if path in self.nodes:
            node = self.nodes[path]
            
            # Remove connected edges
            edges_to_remove = [edge for edge in self.edges 
                             if edge.source_node == node or edge.target_node == node]
            for edge in edges_to_remove:
                self.removeItem(edge)
                self.edges.remove(edge)
            
            # Remove node
            self.removeItem(node)
            del self.nodes[path]
    
    def clear_diagram(self):
        """Clear all nodes and edges."""
        self.clear()
        self.nodes.clear()
        self.edges.clear()
    
    def get_selected_node(self) -> Optional[DiagramNode]:
        """Get currently selected node."""
        selected_items = self.selectedItems()
        for item in selected_items:
            if isinstance(item, DiagramNode):
                return item
        return None
    
    def apply_auto_layout(self):
        """Apply automatic layout to nodes."""
        self.layout_timer.start(100)  # Delay to avoid excessive updates
    
    def _apply_layout(self):
        """Apply layout algorithm."""
        if not self.nodes:
            return
        
        # Improved grid layout with better spacing
        nodes = list(self.nodes.values())
        if len(nodes) == 1:
            # Center single node
            nodes[0].setPos(200, 150)
        else:
            # Calculate optimal grid dimensions
            cols = int(len(nodes) ** 0.5) + 1
            rows = (len(nodes) + cols - 1) // cols
            
            # Calculate spacing based on node size
            node_width = 120
            node_height = 80
            horizontal_spacing = node_width + 50
            vertical_spacing = node_height + 50
            
            # Center the grid
            start_x = 50
            start_y = 50
            
            for i, node in enumerate(nodes):
                row = i // cols
                col = i % cols
                x = start_x + col * horizontal_spacing
                y = start_y + row * vertical_spacing
                node.setPos(x, y)
        
        # Update edge positions
        for edge in self.edges:
            edge.update_position()


class DiagramViewWidget(QWidget):
    """Widget for displaying ARXML diagrams."""
    
    # Signals
    element_selected = Signal(str)  # Emits element path when selected in diagram
    
    def __init__(self, arxml_model: ARXMLModel):
        super().__init__()
        self.arxml_model = arxml_model
        self.current_element: Optional[ElementInfo] = None
        self.diagram_type = "hierarchy"  # hierarchy, references, composition
        
        self._setup_ui()
        self._setup_connections()
    
    def _setup_ui(self):
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Toolbar
        self._create_toolbar(layout)
        
        # Graphics view
        self.scene = DiagramScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setDragMode(QGraphicsView.RubberBandDrag)
        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        
        layout.addWidget(self.view)
        
        # Status label
        self.status_label = QLabel("No diagram loaded")
        self.status_label.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(self.status_label)
    
    def _create_toolbar(self, layout: QVBoxLayout):
        """Create diagram toolbar."""
        toolbar_layout = QHBoxLayout()
        
        # Diagram type selector
        self.diagram_type_combo = QComboBox()
        self.diagram_type_combo.addItems(["Hierarchy", "References", "Composition", "System Topology"])
        self.diagram_type_combo.setCurrentText("Hierarchy")
        toolbar_layout.addWidget(QLabel("Type:"))
        toolbar_layout.addWidget(self.diagram_type_combo)
        
        # Layout button
        self.layout_button = QPushButton("Auto Layout")
        self.layout_button.setEnabled(False)
        toolbar_layout.addWidget(self.layout_button)
        
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
        
        # Show/hide options
        self.show_labels_checkbox = QCheckBox("Show Labels")
        self.show_labels_checkbox.setChecked(True)
        toolbar_layout.addWidget(self.show_labels_checkbox)
        
        self.show_types_checkbox = QCheckBox("Show Types")
        self.show_types_checkbox.setChecked(True)
        toolbar_layout.addWidget(self.show_types_checkbox)
        
        layout.addLayout(toolbar_layout)
    
    def _setup_connections(self):
        """Set up signal connections."""
        # Diagram type change
        self.diagram_type_combo.currentTextChanged.connect(self._on_diagram_type_changed)
        
        # Toolbar buttons
        self.layout_button.clicked.connect(self._apply_auto_layout)
        self.zoom_in_button.clicked.connect(self._zoom_in)
        self.zoom_out_button.clicked.connect(self._zoom_out)
        self.fit_button.clicked.connect(self._fit_to_view)
        
        # Show/hide options
        self.show_labels_checkbox.toggled.connect(self._toggle_labels)
        self.show_types_checkbox.toggled.connect(self._toggle_types)
        
        # Scene signals
        self.scene.node_selected.connect(self._on_node_selected)
        self.scene.node_moved.connect(self._on_node_moved)
        
        # Context menu
        self.view.customContextMenuRequested.connect(self._show_context_menu)
    
    def set_element(self, path: str):
        """Set the current element and update diagram."""
        element = self.arxml_model.get_element_by_path(path)
        if not element:
            self._clear_diagram()
            return
        
        self.current_element = element
        self._update_diagram()
    
    def _update_diagram(self):
        """Update diagram based on current element and type."""
        if not self.current_element:
            return
        
        self.scene.clear_diagram()
        
        diagram_type = self.diagram_type_combo.currentText().lower().replace(" ", "_")
        
        if diagram_type == "hierarchy":
            self._create_hierarchy_diagram()
        elif diagram_type == "references":
            self._create_references_diagram()
        elif diagram_type == "composition":
            self._create_composition_diagram()
        elif diagram_type == "system_topology":
            self._create_system_topology_diagram()
        
        # Enable toolbar buttons
        self.layout_button.setEnabled(True)
        self.zoom_in_button.setEnabled(True)
        self.zoom_out_button.setEnabled(True)
        self.fit_button.setEnabled(True)
        
        # Update status
        node_count = len(self.scene.nodes)
        edge_count = len(self.scene.edges)
        self.status_label.setText(f"Diagram: {node_count} nodes, {edge_count} edges")
    
    def _create_hierarchy_diagram(self):
        """Create hierarchy diagram showing parent-child relationships."""
        if not self.current_element:
            return
        
        # Add current element and its children with tree layout
        self._add_element_hierarchy(self.current_element, 0, 0)
        
        # Apply layout
        self.scene.apply_auto_layout()
    
    def _create_references_diagram(self):
        """Create references diagram showing reference relationships."""
        if not self.current_element:
            return
        
        # Add current element
        current_node = self.scene.add_node(self.current_element, 0, 0)
        
        # Add references to this element
        references_to = self.arxml_model.reference_manager.get_references_to(self.current_element.path)
        for i, ref in enumerate(references_to):
            source_element = self.arxml_model.element_index.get_element_by_path(ref.source_path)
            if source_element:
                source_node = self.scene.add_node(source_element, -200, i * 100)
                self.scene.add_edge(ref.source_path, self.current_element.path, ref)
        
        # Add references from this element
        references_from = self.arxml_model.reference_manager.get_references_from(self.current_element.path)
        for i, ref in enumerate(references_from):
            target_element = self.arxml_model.element_index.get_element_by_path(ref.target_path)
            if target_element:
                target_node = self.scene.add_node(target_element, 200, i * 100)
                self.scene.add_edge(self.current_element.path, ref.target_path, ref)
        
        # Apply layout
        self.scene.apply_auto_layout()
    
    def _create_composition_diagram(self):
        """Create composition diagram for SWC compositions."""
        if not self.current_element:
            return
        
        # Find composition elements
        composition_elements = self._find_composition_elements(self.current_element)
        
        # Add elements to diagram
        for i, element in enumerate(composition_elements):
            self.scene.add_node(element, i * 150, 0)
        
        # Add composition relationships
        self._add_composition_relationships(composition_elements)
        
        # Apply layout
        self.scene.apply_auto_layout()
    
    def _create_system_topology_diagram(self):
        """Create system topology diagram."""
        if not self.current_element:
            return
        
        # Find system elements
        system_elements = self._find_system_elements(self.current_element)
        
        # Add elements to diagram
        for i, element in enumerate(system_elements):
            self.scene.add_node(element, i * 200, 0)
        
        # Add connections
        self._add_system_connections(system_elements)
        
        # Apply layout
        self.scene.apply_auto_layout()
    
    def _add_element_hierarchy(self, element: ElementInfo, x: float, y: float, level: int = 0):
        """Add element and its children to hierarchy diagram."""
        # Add current element
        node = self.scene.add_node(element, x, y)
        
        # Add children with better spacing
        children = self.arxml_model.element_index.get_children(element.path)
        if children:
            # Calculate spacing for children
            child_spacing = 200
            total_width = (len(children) - 1) * child_spacing
            start_x = x - total_width / 2
            
            for i, child in enumerate(children):
                child_x = start_x + i * child_spacing
                child_y = y + 120
                self._add_element_hierarchy(child, child_x, child_y, level + 1)
    
    def _find_composition_elements(self, element: ElementInfo) -> List[ElementInfo]:
        """Find elements that are part of a composition."""
        # This is a simplified implementation
        # In practice, you'd look for specific AUTOSAR composition patterns
        composition_elements = [element]
        
        # Add children that are part of composition
        children = self.arxml_model.element_index.get_children(element.path)
        for child in children:
            if child.element_type in ["ELEMENT", "CONTAINER", "PARAMETER"]:
                composition_elements.append(child)
        
        return composition_elements
    
    def _find_system_elements(self, element: ElementInfo) -> List[ElementInfo]:
        """Find system-level elements."""
        # This is a simplified implementation
        system_elements = [element]
        
        # Add related system elements
        children = self.arxml_model.element_index.get_children(element.path)
        for child in children:
            if child.element_type in ["AR-PACKAGE", "ELEMENT"]:
                system_elements.append(child)
        
        return system_elements
    
    def _add_composition_relationships(self, elements: List[ElementInfo]):
        """Add composition relationships to diagram."""
        # Add relationships based on references
        for element in elements:
            references = self.arxml_model.reference_manager.get_references_from(element.path)
            for ref in references:
                target_element = self.arxml_model.element_index.get_element_by_path(ref.target_path)
                if target_element and target_element in elements:
                    self.scene.add_edge(element.path, ref.target_path, ref)
    
    def _add_system_connections(self, elements: List[ElementInfo]):
        """Add system connections to diagram."""
        # Add connections based on references
        for element in elements:
            references = self.arxml_model.reference_manager.get_references_from(element.path)
            for ref in references:
                target_element = self.arxml_model.element_index.get_element_by_path(ref.target_path)
                if target_element and target_element in elements:
                    self.scene.add_edge(element.path, ref.target_path, ref)
    
    def _clear_diagram(self):
        """Clear the diagram."""
        self.scene.clear_diagram()
        self.current_element = None
        self.status_label.setText("No diagram loaded")
        
        # Disable toolbar buttons
        self.layout_button.setEnabled(False)
        self.zoom_in_button.setEnabled(False)
        self.zoom_out_button.setEnabled(False)
        self.fit_button.setEnabled(False)
    
    def _on_diagram_type_changed(self, diagram_type: str):
        """Handle diagram type change."""
        self._update_diagram()
    
    def _apply_auto_layout(self):
        """Apply automatic layout."""
        self.scene.apply_auto_layout()
    
    def _zoom_in(self):
        """Zoom in the view."""
        self.view.scale(1.2, 1.2)
    
    def _zoom_out(self):
        """Zoom out the view."""
        self.view.scale(0.8, 0.8)
    
    def _fit_to_view(self):
        """Fit diagram to view."""
        self.view.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
    
    def _toggle_labels(self, show: bool):
        """Toggle node labels visibility."""
        for node in self.scene.nodes.values():
            node.text_item.setVisible(show)
    
    def _toggle_types(self, show: bool):
        """Toggle node type labels visibility."""
        for node in self.scene.nodes.values():
            node.type_item.setVisible(show)
    
    def _on_node_selected(self, path: str):
        """Handle node selection."""
        self.element_selected.emit(path)
    
    def _on_node_moved(self, path: str, position: QPointF):
        """Handle node movement."""
        # Update edge positions
        for edge in self.scene.edges:
            edge.update_position()
    
    def _show_context_menu(self, position):
        """Show context menu for diagram."""
        item = self.scene.itemAt(self.view.mapToScene(position))
        if not item or not isinstance(item, DiagramNode):
            return
        
        menu = QMenu(self)
        
        # Navigate actions
        go_to_action = QAction("Go to Element", self)
        go_to_action.triggered.connect(lambda: self.element_selected.emit(item.element_info.path))
        menu.addAction(go_to_action)
        
        # Edit actions
        edit_action = QAction("Edit Properties", self)
        edit_action.triggered.connect(lambda: self.element_selected.emit(item.element_info.path))
        menu.addAction(edit_action)
        
        # View actions
        center_action = QAction("Center on Node", self)
        center_action.triggered.connect(lambda: self._center_on_node(item))
        menu.addAction(center_action)
        
        menu.exec(self.view.mapToGlobal(position))
    
    def _center_on_node(self, node: DiagramNode):
        """Center view on specific node."""
        self.view.centerOn(node)