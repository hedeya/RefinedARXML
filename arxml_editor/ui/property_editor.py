"""
Property editor widget for ARXML elements.

Provides form-based editing of element properties, attributes, and content.
"""

from typing import Optional, Dict, Any, List
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QLineEdit,
    QTextEdit, QComboBox, QCheckBox, QPushButton, QGroupBox, QScrollArea,
    QTableWidget, QTableWidgetItem, QHeaderView, QSplitter, QTabWidget,
    QMessageBox, QDialog, QDialogButtonBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from ..core.arxml_model import ARXMLModel
from ..core.element_index import ElementInfo
from ..utils.xml_utils import XMLUtils
from ..utils.naming_conventions import ARXMLNamingConventions


class PropertyEditorWidget(QWidget):
    """Widget for editing ARXML element properties."""
    
    # Signals
    element_modified = Signal(str)  # Emits element path when modified
    
    def __init__(self, arxml_model: ARXMLModel):
        super().__init__()
        self.arxml_model = arxml_model
        self.current_element: Optional[ElementInfo] = None
        self.naming_conventions = ARXMLNamingConventions()
        
        self._setup_ui()
        self._setup_connections()
    
    def _setup_ui(self):
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create tab widget for different editing modes
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Properties tab
        self.properties_tab = self._create_properties_tab()
        self.tab_widget.addTab(self.properties_tab, "Properties")
        
        # Attributes tab
        self.attributes_tab = self._create_attributes_tab()
        self.tab_widget.addTab(self.attributes_tab, "Attributes")
        
        # Content tab
        self.content_tab = self._create_content_tab()
        self.tab_widget.addTab(self.content_tab, "Content")
        
        # References tab
        self.references_tab = self._create_references_tab()
        self.tab_widget.addTab(self.references_tab, "References")
        
        # Initially hide tabs until element is selected
        self.tab_widget.setVisible(False)
        
        # No element selected message
        self.no_element_label = QLabel("No element selected")
        self.no_element_label.setAlignment(Qt.AlignCenter)
        self.no_element_label.setStyleSheet("color: gray; font-style: italic;")
        layout.addWidget(self.no_element_label)
    
    def _create_properties_tab(self) -> QWidget:
        """Create the properties editing tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Scroll area for properties
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Properties form
        self.properties_form = QFormLayout()
        self.properties_form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        
        # Basic properties
        self.short_name_edit = QLineEdit()
        self.short_name_edit.setPlaceholderText("Enter SHORT-NAME")
        self.properties_form.addRow("SHORT-NAME:", self.short_name_edit)
        
        self.long_name_edit = QLineEdit()
        self.long_name_edit.setPlaceholderText("Enter LONG-NAME")
        self.properties_form.addRow("LONG-NAME:", self.long_name_edit)
        
        self.uuid_edit = QLineEdit()
        self.uuid_edit.setPlaceholderText("Enter UUID")
        self.properties_form.addRow("UUID:", self.uuid_edit)
        
        # Element type (read-only)
        self.element_type_label = QLabel()
        self.element_type_label.setStyleSheet("color: gray;")
        self.properties_form.addRow("Type:", self.element_type_label)
        
        # Path (read-only)
        self.path_label = QLabel()
        self.path_label.setStyleSheet("color: gray;")
        self.path_label.setWordWrap(True)
        self.properties_form.addRow("Path:", self.path_label)
        
        # File (read-only)
        self.file_label = QLabel()
        self.file_label.setStyleSheet("color: gray;")
        self.file_label.setWordWrap(True)
        self.properties_form.addRow("File:", self.file_label)
        
        # Properties container
        properties_widget = QWidget()
        properties_widget.setLayout(self.properties_form)
        scroll_area.setWidget(properties_widget)
        
        layout.addWidget(scroll_area)
        
        # Save button
        self.save_properties_button = QPushButton("Save Properties")
        self.save_properties_button.setEnabled(False)
        layout.addWidget(self.save_properties_button)
        
        return widget
    
    def _create_attributes_tab(self) -> QWidget:
        """Create the attributes editing tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Attributes table
        self.attributes_table = QTableWidget()
        self.attributes_table.setColumnCount(2)
        self.attributes_table.setHorizontalHeaderLabels(["Attribute", "Value"])
        
        # Configure table
        header = self.attributes_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        
        self.attributes_table.setAlternatingRowColors(True)
        self.attributes_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.attributes_table)
        
        # Attribute buttons
        button_layout = QHBoxLayout()
        
        self.add_attribute_button = QPushButton("Add Attribute")
        self.add_attribute_button.setEnabled(False)
        button_layout.addWidget(self.add_attribute_button)
        
        self.remove_attribute_button = QPushButton("Remove Attribute")
        self.remove_attribute_button.setEnabled(False)
        button_layout.addWidget(self.remove_attribute_button)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        return widget
    
    def _create_content_tab(self) -> QWidget:
        """Create the content editing tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Text content
        self.text_content_edit = QTextEdit()
        self.text_content_edit.setPlaceholderText("Enter text content...")
        self.text_content_edit.setMaximumHeight(150)
        layout.addWidget(QLabel("Text Content:"))
        layout.addWidget(self.text_content_edit)
        
        # Child elements
        layout.addWidget(QLabel("Child Elements:"))
        self.children_table = QTableWidget()
        self.children_table.setColumnCount(3)
        self.children_table.setHorizontalHeaderLabels(["Tag", "Content", "Type"])
        
        # Configure table
        header = self.children_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        self.children_table.setAlternatingRowColors(True)
        self.children_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.children_table)
        
        # Child element buttons
        child_button_layout = QHBoxLayout()
        
        self.add_child_button = QPushButton("Add Child")
        self.add_child_button.setEnabled(False)
        child_button_layout.addWidget(self.add_child_button)
        
        self.edit_child_button = QPushButton("Edit Child")
        self.edit_child_button.setEnabled(False)
        child_button_layout.addWidget(self.edit_child_button)
        
        self.remove_child_button = QPushButton("Remove Child")
        self.remove_child_button.setEnabled(False)
        child_button_layout.addWidget(self.remove_child_button)
        
        child_button_layout.addStretch()
        layout.addLayout(child_button_layout)
        
        return widget
    
    def _create_references_tab(self) -> QWidget:
        """Create the references tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # References to this element
        layout.addWidget(QLabel("References to this element:"))
        self.references_to_table = QTableWidget()
        self.references_to_table.setColumnCount(3)
        self.references_to_table.setHorizontalHeaderLabels(["Source", "Type", "Status"])
        
        header = self.references_to_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        self.references_to_table.setAlternatingRowColors(True)
        layout.addWidget(self.references_to_table)
        
        # References from this element
        layout.addWidget(QLabel("References from this element:"))
        self.references_from_table = QTableWidget()
        self.references_from_table.setColumnCount(3)
        self.references_from_table.setHorizontalHeaderLabels(["Target", "Type", "Status"])
        
        header = self.references_from_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        self.references_from_table.setAlternatingRowColors(True)
        layout.addWidget(self.references_from_table)
        
        return widget
    
    def _setup_connections(self):
        """Set up signal connections."""
        # Properties
        self.short_name_edit.textChanged.connect(self._on_property_changed)
        self.long_name_edit.textChanged.connect(self._on_property_changed)
        self.uuid_edit.textChanged.connect(self._on_property_changed)
        self.save_properties_button.clicked.connect(self._save_properties)
        
        # Attributes
        self.add_attribute_button.clicked.connect(self._add_attribute)
        self.remove_attribute_button.clicked.connect(self._remove_attribute)
        self.attributes_table.itemChanged.connect(self._on_attribute_changed)
        
        # Content
        self.text_content_edit.textChanged.connect(self._on_content_changed)
        self.add_child_button.clicked.connect(self._add_child_element)
        self.edit_child_button.clicked.connect(self._edit_child_element)
        self.remove_child_button.clicked.connect(self._remove_child_element)
        
        # References
        self.references_to_table.itemDoubleClicked.connect(self._go_to_reference)
        self.references_from_table.itemDoubleClicked.connect(self._go_to_reference)
    
    def set_element(self, path: str):
        """Set the current element to edit."""
        # Save current changes before switching
        if self.current_element:
            self._save_current_changes()
        
        element = self.arxml_model.get_element_by_path(path)
        if not element:
            self._clear_editor()
            return
        
        self.current_element = element
        self._populate_editor()
        self._update_references()
        
        # Show tabs and hide no-element message
        self.tab_widget.setVisible(True)
        self.no_element_label.setVisible(False)
    
    def _clear_editor(self):
        """Clear the editor when no element is selected."""
        self.current_element = None
        self.tab_widget.setVisible(False)
        self.no_element_label.setVisible(True)
        
        # Clear all fields
        self.short_name_edit.clear()
        self.long_name_edit.clear()
        self.uuid_edit.clear()
        self.element_type_label.clear()
        self.path_label.clear()
        self.file_label.clear()
        self.text_content_edit.clear()
        
        # Clear tables
        self.attributes_table.setRowCount(0)
        self.children_table.setRowCount(0)
        self.references_to_table.setRowCount(0)
        self.references_from_table.setRowCount(0)
        
        # Disable buttons
        self.save_properties_button.setEnabled(False)
        self.add_attribute_button.setEnabled(False)
        self.remove_attribute_button.setEnabled(False)
        self.add_child_button.setEnabled(False)
        self.edit_child_button.setEnabled(False)
        self.remove_child_button.setEnabled(False)
    
    def _populate_editor(self):
        """Populate editor with current element data."""
        if not self.current_element:
            return
        
        element = self.current_element
        
        # Basic properties
        self.short_name_edit.setText(element.short_name or "")
        self.long_name_edit.setText(XMLUtils.get_long_name(element.element))
        self.uuid_edit.setText(element.uuid or "")
        self.element_type_label.setText(element.element_type or "Unknown")
        self.path_label.setText(element.path)
        self.file_label.setText(element.file_path or "Unknown")
        
        # Text content
        text_content = element.element.text or ""
        self.text_content_edit.setText(text_content)
        
        # Attributes
        self._populate_attributes()
        
        # Child elements
        self._populate_children()
        
        # Enable buttons
        self.save_properties_button.setEnabled(True)
        self.add_attribute_button.setEnabled(True)
        self.remove_attribute_button.setEnabled(True)
        self.add_child_button.setEnabled(True)
        self.edit_child_button.setEnabled(True)
        self.remove_child_button.setEnabled(True)
    
    def _populate_attributes(self):
        """Populate attributes table."""
        if not self.current_element:
            return
        
        attributes = self.current_element.element.attrib
        self.attributes_table.setRowCount(len(attributes))
        
        for row, (attr_name, attr_value) in enumerate(attributes.items()):
            # Skip namespace attributes
            if attr_name.startswith('xmlns') or attr_name.startswith('xsi:'):
                continue
            
            name_item = QTableWidgetItem(attr_name)
            value_item = QTableWidgetItem(attr_value)
            
            self.attributes_table.setItem(row, 0, name_item)
            self.attributes_table.setItem(row, 1, value_item)
    
    def _populate_children(self):
        """Populate children table."""
        if not self.current_element:
            return
        
        children = list(self.current_element.element)
        self.children_table.setRowCount(len(children))
        
        for row, child in enumerate(children):
            tag_name = child.tag
            if '}' in tag_name:
                tag_name = tag_name.split('}', 1)[1]
            
            content = child.text or ""
            child_type = "Element" if len(child) > 0 else "Text"
            
            tag_item = QTableWidgetItem(tag_name)
            content_item = QTableWidgetItem(content)
            type_item = QTableWidgetItem(child_type)
            
            self.children_table.setItem(row, 0, tag_item)
            self.children_table.setItem(row, 1, content_item)
            self.children_table.setItem(row, 2, type_item)
    
    def _update_references(self):
        """Update references tables."""
        if not self.current_element:
            return
        
        # References to this element
        references_to = self.arxml_model.reference_manager.get_references_to(self.current_element.path)
        self.references_to_table.setRowCount(len(references_to))
        
        for row, ref in enumerate(references_to):
            source_item = QTableWidgetItem(ref.source_path)
            type_item = QTableWidgetItem(ref.reference_type.value)
            status_item = QTableWidgetItem("Valid" if ref.is_valid else "Invalid")
            
            if not ref.is_valid:
                status_item.setBackground(Qt.red)
            
            self.references_to_table.setItem(row, 0, source_item)
            self.references_to_table.setItem(row, 1, type_item)
            self.references_to_table.setItem(row, 2, status_item)
        
        # References from this element
        references_from = self.arxml_model.reference_manager.get_references_from(self.current_element.path)
        self.references_from_table.setRowCount(len(references_from))
        
        for row, ref in enumerate(references_from):
            target_item = QTableWidgetItem(ref.target_path)
            type_item = QTableWidgetItem(ref.reference_type.value)
            status_item = QTableWidgetItem("Valid" if ref.is_valid else "Invalid")
            
            if not ref.is_valid:
                status_item.setBackground(Qt.red)
            
            self.references_from_table.setItem(row, 0, target_item)
            self.references_from_table.setItem(row, 1, type_item)
            self.references_from_table.setItem(row, 2, status_item)
    
    def _on_property_changed(self):
        """Handle property change."""
        # Enable save button when properties change
        self.save_properties_button.setEnabled(True)
    
    def _on_attribute_changed(self, item):
        """Handle attribute change."""
        # Update element attribute
        if not self.current_element:
            return
        
        row = item.row()
        name_item = self.attributes_table.item(row, 0)
        value_item = self.attributes_table.item(row, 1)
        
        if not name_item or not value_item:
            return
            
        attr_name = name_item.text()
        attr_value = value_item.text()
        
        XMLUtils.set_element_attribute(self.current_element.element, attr_name, attr_value)
        
        # Mark as modified
        self.arxml_model.is_modified = True
        
        # Emit modification signal
        self.element_modified.emit(self.current_element.path)
    
    def _on_content_changed(self):
        """Handle content change."""
        if not self.current_element:
            return
        
        new_text = self.text_content_edit.toPlainText()
        XMLUtils.set_element_text(self.current_element.element, new_text)
        
        # Mark as modified
        self.arxml_model.is_modified = True
        
        # Emit modification signal
        self.element_modified.emit(self.current_element.path)
    
    def _save_current_changes(self):
        """Save current changes without user interaction."""
        if not self.current_element:
            return
        
        # Update SHORT-NAME
        new_short_name = self.short_name_edit.text()
        if new_short_name != self.current_element.short_name:
            XMLUtils.set_short_name(self.current_element.element, new_short_name)
            # Update index
            self.arxml_model.element_index.update_element(self.current_element.path, self.current_element.element)
        
        # Update LONG-NAME
        new_long_name = self.long_name_edit.text()
        current_long_name = XMLUtils.get_long_name(self.current_element.element)
        if new_long_name != current_long_name:
            XMLUtils.set_long_name(self.current_element.element, new_long_name)
        
        # Update UUID
        new_uuid = self.uuid_edit.text()
        if new_uuid != self.current_element.uuid:
            XMLUtils.set_element_attribute(self.current_element.element, "UUID", new_uuid)
            # Update index
            self.arxml_model.element_index.update_element(self.current_element.path, self.current_element.element)
        
        # Mark as modified
        self.arxml_model.is_modified = True
        
        # Emit modification signal
        self.element_modified.emit(self.current_element.path)

    def _save_properties(self):
        """Save property changes."""
        if not self.current_element:
            return
        
        self._save_current_changes()
        
        # Disable save button
        self.save_properties_button.setEnabled(False)
    
    def _add_attribute(self):
        """Add new attribute."""
        dialog = AttributeDialog(self)
        if dialog.exec() == QDialog.Accepted:
            attr_name, attr_value = dialog.get_attribute()
            
            # Add to table
            row = self.attributes_table.rowCount()
            self.attributes_table.insertRow(row)
            
            name_item = QTableWidgetItem(attr_name)
            value_item = QTableWidgetItem(attr_value)
            
            self.attributes_table.setItem(row, 0, name_item)
            self.attributes_table.setItem(row, 1, value_item)
            
            # Add to element
            if self.current_element:
                XMLUtils.set_element_attribute(self.current_element.element, attr_name, attr_value)
                self.element_modified.emit(self.current_element.path)
    
    def _remove_attribute(self):
        """Remove selected attribute."""
        current_row = self.attributes_table.currentRow()
        if current_row >= 0:
            attr_name = self.attributes_table.item(current_row, 0).text()
            
            # Remove from element
            if self.current_element and attr_name in self.current_element.element.attrib:
                del self.current_element.element.attrib[attr_name]
                self.element_modified.emit(self.current_element.path)
            
            # Remove from table
            self.attributes_table.removeRow(current_row)
    
    def _add_child_element(self):
        """Add child element."""
        dialog = ChildElementDialog(self)
        if dialog.exec() == QDialog.Accepted:
            tag_name, content = dialog.get_element()
            
            # Create child element
            child_element = XMLUtils.create_reference_element(content) if tag_name == "REF" else None
            if not child_element:
                child_element = XMLUtils.create_reference_element(content)
                child_element.tag = tag_name
            
            # Add to element
            if self.current_element:
                self.current_element.element.append(child_element)
                self.element_modified.emit(self.current_element.path)
                
                # Refresh children table
                self._populate_children()
    
    def _edit_child_element(self):
        """Edit selected child element."""
        current_row = self.children_table.currentRow()
        if current_row >= 0:
            # Get current values
            tag_name = self.children_table.item(current_row, 0).text()
            content = self.children_table.item(current_row, 1).text()
            
            dialog = ChildElementDialog(self, tag_name, content)
            if dialog.exec() == QDialog.Accepted:
                new_tag, new_content = dialog.get_element()
                
                # Update element
                if self.current_element:
                    children = list(self.current_element.element)
                    if current_row < len(children):
                        child = children[current_row]
                        child.tag = new_tag
                        XMLUtils.set_element_text(child, new_content)
                        self.element_modified.emit(self.current_element.path)
                        
                        # Refresh table
                        self._populate_children()
    
    def _remove_child_element(self):
        """Remove selected child element."""
        current_row = self.children_table.currentRow()
        if current_row >= 0 and self.current_element:
            children = list(self.current_element.element)
            if current_row < len(children):
                child = children[current_row]
                self.current_element.element.remove(child)
                self.element_modified.emit(self.current_element.path)
                
                # Refresh table
                self._populate_children()
    
    def _go_to_reference(self, item):
        """Go to referenced element."""
        if not item:
            return
        
        table = item.tableWidget()
        row = item.row()
        
        if table == self.references_to_table:
            # Go to source of reference
            source_path = table.item(row, 0).text()
        else:
            # Go to target of reference
            target_path = table.item(row, 0).text()
            target_element = self.arxml_model.element_index.get_element_by_path(target_path)
            if target_element:
                source_path = target_element.path
            else:
                return
        
        # Emit signal to navigate to element
        self.element_modified.emit(source_path)


class AttributeDialog(QDialog):
    """Dialog for adding/editing attributes."""
    
    def __init__(self, parent=None, attr_name="", attr_value=""):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Attribute")
        self.setModal(True)
        
        layout = QFormLayout(self)
        
        self.name_edit = QLineEdit(attr_name)
        self.value_edit = QLineEdit(attr_value)
        
        layout.addRow("Attribute Name:", self.name_edit)
        layout.addRow("Attribute Value:", self.value_edit)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def get_attribute(self):
        """Get attribute name and value."""
        return self.name_edit.text(), self.value_edit.text()


class ChildElementDialog(QDialog):
    """Dialog for adding/editing child elements."""
    
    def __init__(self, parent=None, tag_name="", content=""):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Child Element")
        self.setModal(True)
        
        layout = QFormLayout(self)
        
        self.tag_edit = QLineEdit(tag_name)
        self.content_edit = QTextEdit(content)
        self.content_edit.setMaximumHeight(100)
        
        layout.addRow("Tag Name:", self.tag_edit)
        layout.addRow("Content:", self.content_edit)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def get_element(self):
        """Get element tag and content."""
        return self.tag_edit.text(), self.content_edit.toPlainText()