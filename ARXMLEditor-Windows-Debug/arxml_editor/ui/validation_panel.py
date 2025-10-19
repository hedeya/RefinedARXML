"""
Validation panel widget for ARXML validation results.

Displays validation errors, warnings, and provides quick fixes.
"""

from typing import List, Optional, Dict, Any
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem,
    QPushButton, QLabel, QComboBox, QTextEdit, QSplitter, QGroupBox,
    QHeaderView, QMessageBox, QDialog, QDialogButtonBox, QFormLayout,
    QLineEdit, QCheckBox, QProgressBar
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QColor, QFont, QIcon

from ..core.arxml_model import ARXMLModel
from ..validation.types import ValidationError, ValidationLevel


class ValidationErrorItem(QTreeWidgetItem):
    """Custom tree item for validation errors."""
    
    def __init__(self, error: ValidationError):
        super().__init__()
        self.error = error
        self._setup_item()
    
    def _setup_item(self):
        """Set up the item display."""
        # Set text based on error level
        level_text = {
            ValidationLevel.ERROR: "ERROR",
            ValidationLevel.WARNING: "WARNING", 
            ValidationLevel.INFO: "INFO"
        }.get(self.error.level, "UNKNOWN")
        
        self.setText(0, level_text)
        self.setText(1, self.error.path)
        self.setText(2, self.error.message)
        
        # Set colors based on level
        if self.error.level == ValidationLevel.ERROR:
            self.setForeground(0, QColor(200, 0, 0))
            self.setForeground(1, QColor(200, 0, 0))
            self.setForeground(2, QColor(200, 0, 0))
        elif self.error.level == ValidationLevel.WARNING:
            self.setForeground(0, QColor(200, 100, 0))
            self.setForeground(1, QColor(200, 100, 0))
            self.setForeground(2, QColor(200, 100, 0))
        else:
            self.setForeground(0, QColor(0, 100, 200))
            self.setForeground(1, QColor(0, 100, 200))
            self.setForeground(2, QColor(0, 100, 200))
        
        # Set tooltip
        tooltip = f"Path: {self.error.path}\nMessage: {self.error.message}"
        if self.error.rule_id:
            tooltip += f"\nRule: {self.error.rule_id}"
        if self.error.line_number:
            tooltip += f"\nLine: {self.error.line_number}"
        if self.error.column_number:
            tooltip += f"\nColumn: {self.error.column_number}"
        
        self.setToolTip(0, tooltip)
        self.setToolTip(1, tooltip)
        self.setToolTip(2, tooltip)


class ValidationPanelWidget(QWidget):
    """Widget for displaying validation results."""
    
    # Signals
    error_selected = Signal(str)  # Emits error path when selected
    quick_fix_applied = Signal(str)  # Emits error path when quick fix is applied
    
    def __init__(self, arxml_model: ARXMLModel):
        super().__init__()
        self.arxml_model = arxml_model
        self.current_errors: List[ValidationError] = []
        self.validation_timer = QTimer()
        self.validation_timer.timeout.connect(self._run_validation)
        self.validation_timer.setSingleShot(True)
        
        self._setup_ui()
        self._setup_connections()
    
    def _setup_ui(self):
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Toolbar
        self._create_toolbar(layout)
        
        # Main content splitter
        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)
        
        # Error list
        self._create_error_list(splitter)
        
        # Error details
        self._create_error_details(splitter)
        
        # Set splitter proportions
        splitter.setSizes([400, 300])
    
    def _create_toolbar(self, layout: QVBoxLayout):
        """Create validation toolbar."""
        toolbar_layout = QHBoxLayout()
        
        # Validate button
        self.validate_button = QPushButton("Validate")
        self.validate_button.setEnabled(False)
        toolbar_layout.addWidget(self.validate_button)
        
        # Clear button
        self.clear_button = QPushButton("Clear")
        self.clear_button.setEnabled(False)
        toolbar_layout.addWidget(self.clear_button)
        
        toolbar_layout.addWidget(QLabel("Filter:"))
        
        # Level filter
        self.level_filter = QComboBox()
        self.level_filter.addItems(["All Levels", "Errors", "Warnings", "Info"])
        self.level_filter.setCurrentText("All Levels")
        toolbar_layout.addWidget(self.level_filter)
        
        # Rule filter
        self.rule_filter = QComboBox()
        self.rule_filter.addItems(["All Rules"])
        toolbar_layout.addWidget(self.rule_filter)
        
        toolbar_layout.addStretch()
        
        # Statistics
        self.stats_label = QLabel("No validation results")
        self.stats_label.setStyleSheet("color: gray; font-style: italic;")
        toolbar_layout.addWidget(self.stats_label)
        
        layout.addLayout(toolbar_layout)
    
    def _create_error_list(self, parent: QSplitter):
        """Create error list widget."""
        error_group = QGroupBox("Validation Results")
        error_layout = QVBoxLayout(error_group)
        
        # Error tree
        self.error_tree = QTreeWidget()
        self.error_tree.setHeaderLabels(["Level", "Path", "Message"])
        self.error_tree.setAlternatingRowColors(True)
        self.error_tree.setSelectionMode(QTreeWidget.SingleSelection)
        self.error_tree.setSortingEnabled(True)
        
        # Configure tree widget columns
        self.error_tree.setColumnWidth(0, 100)  # Level column
        self.error_tree.setColumnWidth(1, 200)  # Path column
        # Message column will stretch to fill remaining space
        
        error_layout.addWidget(self.error_tree)
        
        # Error actions
        action_layout = QHBoxLayout()
        
        self.quick_fix_button = QPushButton("Quick Fix")
        self.quick_fix_button.setEnabled(False)
        action_layout.addWidget(self.quick_fix_button)
        
        self.go_to_button = QPushButton("Go to Error")
        self.go_to_button.setEnabled(False)
        action_layout.addWidget(self.go_to_button)
        
        self.ignore_button = QPushButton("Ignore")
        self.ignore_button.setEnabled(False)
        action_layout.addWidget(self.ignore_button)
        
        action_layout.addStretch()
        error_layout.addLayout(action_layout)
        
        parent.addWidget(error_group)
    
    def _create_error_details(self, parent: QSplitter):
        """Create error details widget."""
        details_group = QGroupBox("Error Details")
        details_layout = QVBoxLayout(details_group)
        
        # Error details text
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setMaximumHeight(200)
        details_layout.addWidget(self.details_text)
        
        # Quick fix details
        self.quick_fix_group = QGroupBox("Quick Fix")
        quick_fix_layout = QVBoxLayout(self.quick_fix_group)
        
        self.quick_fix_text = QTextEdit()
        self.quick_fix_text.setReadOnly(True)
        self.quick_fix_text.setMaximumHeight(100)
        quick_fix_layout.addWidget(self.quick_fix_text)
        
        self.apply_fix_button = QPushButton("Apply Fix")
        self.apply_fix_button.setEnabled(False)
        quick_fix_layout.addWidget(self.apply_fix_button)
        
        details_layout.addWidget(self.quick_fix_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        details_layout.addWidget(self.progress_bar)
        
        parent.addWidget(details_group)
    
    def _setup_connections(self):
        """Set up signal connections."""
        # Toolbar buttons
        self.validate_button.clicked.connect(self._run_validation)
        self.clear_button.clicked.connect(self._clear_results)
        self.level_filter.currentTextChanged.connect(self._apply_filters)
        self.rule_filter.currentTextChanged.connect(self._apply_filters)
        
        # Error list
        self.error_tree.itemSelectionChanged.connect(self._on_error_selected)
        self.error_tree.itemDoubleClicked.connect(self._on_error_double_clicked)
        
        # Action buttons
        self.quick_fix_button.clicked.connect(self._show_quick_fix)
        self.go_to_button.clicked.connect(self._go_to_error)
        self.ignore_button.clicked.connect(self._ignore_error)
        self.apply_fix_button.clicked.connect(self._apply_quick_fix)
    
    def update_errors(self, errors: List[ValidationError]):
        """Update validation results."""
        self.current_errors = errors
        self._populate_error_tree()
        self._update_statistics()
        self._update_rule_filter()
        
        # Enable/disable buttons
        self.validate_button.setEnabled(True)
        self.clear_button.setEnabled(len(errors) > 0)
    
    def _populate_error_tree(self):
        """Populate error tree with current errors."""
        self.error_tree.clear()
        
        for error in self.current_errors:
            item = ValidationErrorItem(error)
            self.error_tree.addTopLevelItem(item)
        
        # Apply current filters
        self._apply_filters()
    
    def _update_statistics(self):
        """Update validation statistics."""
        if not self.current_errors:
            self.stats_label.setText("No validation results")
            return
        
        error_count = len([e for e in self.current_errors if e.level == ValidationLevel.ERROR])
        warning_count = len([e for e in self.current_errors if e.level == ValidationLevel.WARNING])
        info_count = len([e for e in self.current_errors if e.level == ValidationLevel.INFO])
        
        self.stats_label.setText(f"Errors: {error_count}, Warnings: {warning_count}, Info: {info_count}")
    
    def _update_rule_filter(self):
        """Update rule filter dropdown."""
        current_rule = self.rule_filter.currentText()
        self.rule_filter.clear()
        self.rule_filter.addItem("All Rules")
        
        # Get unique rule IDs
        rule_ids = set()
        for error in self.current_errors:
            if error.rule_id:
                rule_ids.add(error.rule_id)
        
        # Add rules to filter
        for rule_id in sorted(rule_ids):
            self.rule_filter.addItem(rule_id)
        
        # Restore selection if possible
        index = self.rule_filter.findText(current_rule)
        if index >= 0:
            self.rule_filter.setCurrentIndex(index)
    
    def _apply_filters(self):
        """Apply current filters to error tree."""
        level_filter = self.level_filter.currentText()
        rule_filter = self.rule_filter.currentText()
        
        # Show/hide items based on filters
        for i in range(self.error_tree.topLevelItemCount()):
            item = self.error_tree.topLevelItem(i)
            error = item.error
            
            # Level filter
            level_matches = (level_filter == "All Levels" or 
                           (level_filter == "Errors" and error.level == ValidationLevel.ERROR) or
                           (level_filter == "Warnings" and error.level == ValidationLevel.WARNING) or
                           (level_filter == "Info" and error.level == ValidationLevel.INFO))
            
            # Rule filter
            rule_matches = (rule_filter == "All Rules" or error.rule_id == rule_filter)
            
            # Show/hide item
            item.setHidden(not (level_matches and rule_matches))
    
    def _on_error_selected(self):
        """Handle error selection."""
        current_item = self.error_tree.currentItem()
        if current_item and isinstance(current_item, ValidationErrorItem):
            error = current_item.error
            
            # Update details
            self._update_error_details(error)
            
            # Enable action buttons
            self.quick_fix_button.setEnabled(error.quick_fix is not None)
            self.go_to_button.setEnabled(True)
            self.ignore_button.setEnabled(True)
            
            # Emit selection signal
            self.error_selected.emit(error.path)
        else:
            self._clear_error_details()
            self.quick_fix_button.setEnabled(False)
            self.go_to_button.setEnabled(False)
            self.ignore_button.setEnabled(False)
    
    def _on_error_double_clicked(self, item: QTreeWidgetItem, column: int):
        """Handle error double-click."""
        if isinstance(item, ValidationErrorItem):
            self._go_to_error()
    
    def _update_error_details(self, error: ValidationError):
        """Update error details display."""
        details = f"Path: {error.path}\n"
        details += f"Level: {error.level.value.upper()}\n"
        details += f"Message: {error.message}\n"
        
        if error.rule_id:
            details += f"Rule: {error.rule_id}\n"
        
        if error.line_number:
            details += f"Line: {error.line_number}\n"
        
        if error.column_number:
            details += f"Column: {error.column_number}\n"
        
        self.details_text.setText(details)
        
        # Update quick fix
        if error.quick_fix:
            self.quick_fix_text.setText("Quick fix available. Click 'Apply Fix' to use it.")
            self.apply_fix_button.setEnabled(True)
        else:
            self.quick_fix_text.setText("No quick fix available for this error.")
            self.apply_fix_button.setEnabled(False)
    
    def _clear_error_details(self):
        """Clear error details display."""
        self.details_text.clear()
        self.quick_fix_text.clear()
        self.apply_fix_button.setEnabled(False)
    
    def _run_validation(self):
        """Run validation on current model."""
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        
        # Run validation in background
        self.validation_timer.start(100)  # Small delay to show progress
    
    def _run_validation_actual(self):
        """Actual validation execution."""
        try:
            from ..validation.validator import ARXMLValidator
            validator = ARXMLValidator(
                self.arxml_model.schema_manager,
                self.arxml_model.element_index,
                self.arxml_model.reference_manager
            )
            errors = validator.validate_all()
            self.update_errors(errors)
        except Exception as e:
            # Show error in validation results
            from ..validation.types import ValidationError, ValidationLevel
            error = ValidationError(
                path="",
                message=f"Validation failed: {str(e)}",
                level=ValidationLevel.ERROR
            )
            self.update_errors([error])
        finally:
            self.progress_bar.setVisible(False)
    
    def _clear_results(self):
        """Clear validation results."""
        self.current_errors.clear()
        self.error_tree.clear()
        self._clear_error_details()
        self._update_statistics()
        
        # Disable buttons
        self.clear_button.setEnabled(False)
        self.quick_fix_button.setEnabled(False)
        self.go_to_button.setEnabled(False)
        self.ignore_button.setEnabled(False)
    
    def _show_quick_fix(self):
        """Show quick fix dialog."""
        current_item = self.error_tree.currentItem()
        if isinstance(current_item, ValidationErrorItem):
            error = current_item.error
            if error.quick_fix:
                dialog = QuickFixDialog(error, self)
                if dialog.exec() == QDialog.Accepted:
                    self._apply_quick_fix()
    
    def _go_to_error(self):
        """Navigate to error location."""
        current_item = self.error_tree.currentItem()
        if isinstance(current_item, ValidationErrorItem):
            error = current_item.error
            self.error_selected.emit(error.path)
    
    def _ignore_error(self):
        """Ignore selected error."""
        current_item = self.error_tree.currentItem()
        if isinstance(current_item, ValidationErrorItem):
            error = current_item.error
            
            # Remove from current errors
            if error in self.current_errors:
                self.current_errors.remove(error)
                self._populate_error_tree()
                self._update_statistics()
    
    def _apply_quick_fix(self):
        """Apply quick fix to selected error."""
        current_item = self.error_tree.currentItem()
        if isinstance(current_item, ValidationErrorItem):
            error = current_item.error
            if error.quick_fix:
                try:
                    error.quick_fix()
                    self.quick_fix_applied.emit(error.path)
                    
                    # Remove fixed error from list
                    if error in self.current_errors:
                        self.current_errors.remove(error)
                        self._populate_error_tree()
                        self._update_statistics()
                    
                    QMessageBox.information(self, "Quick Fix", "Quick fix applied successfully.")
                except Exception as e:
                    QMessageBox.critical(self, "Quick Fix Error", f"Failed to apply quick fix: {str(e)}")


class QuickFixDialog(QDialog):
    """Dialog for showing quick fix details."""
    
    def __init__(self, error: ValidationError, parent=None):
        super().__init__(parent)
        self.error = error
        self.setWindowTitle("Quick Fix")
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # Error details
        layout.addWidget(QLabel(f"Error: {error.message}"))
        layout.addWidget(QLabel(f"Path: {error.path}"))
        
        # Quick fix description
        layout.addWidget(QLabel("Quick Fix Description:"))
        self.description_text = QTextEdit()
        self.description_text.setReadOnly(True)
        self.description_text.setMaximumHeight(100)
        self.description_text.setText("This quick fix will automatically resolve the validation error.")
        layout.addWidget(self.description_text)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)