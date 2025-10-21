"""
Main window for ARXML Editor.

Provides the main application interface with dockable panels and menu system.
"""

import sys
import logging
from pathlib import Path
from typing import Optional, List
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QMenuBar, QMenu, QToolBar, QStatusBar, QFileDialog, QMessageBox,
    QDockWidget, QApplication, QProgressBar, QLabel
)
from PySide6.QtCore import Qt, QTimer, Signal, QThread
from PySide6.QtGui import QAction, QIcon, QKeySequence

from .package_tree import PackageTreeWidget
from .property_editor import PropertyEditorWidget
from .diagram_view import DiagramViewWidget
from .hierarchy_view import HierarchyViewWidget
from .validation_panel import ValidationPanelWidget
from ..core.arxml_model import ARXMLModel
from ..core.schema_manager import AUTOSARRelease


class MainWindow(QMainWindow):
    """Main application window."""
    
    # Signals
    file_opened = Signal(str)
    file_saved = Signal(str)
    element_selected = Signal(str)
    validation_completed = Signal(list)
    
    def __init__(self):
        super().__init__()
        self.arxml_model = ARXMLModel()
        self.current_file: Optional[Path] = None
        self.is_modified = False
        
        self._setup_ui()
        self._setup_connections()
        self._setup_menu()
        self._setup_toolbar()
        self._setup_status_bar()
        
        # Set window properties
        self.setWindowTitle("ARXML Editor")
        self._setup_window_geometry()
        
        # Show welcome message
        self._show_welcome_message()
    
    def _setup_ui(self):
        """Set up the main UI layout."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create splitter for resizable panels
        self.splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.splitter)
        
        # Create dockable widgets
        self._create_dock_widgets()
        
        # Add widgets to splitter
        self.splitter.addWidget(self.package_tree)
        self.splitter.addWidget(self.property_editor)
        self.splitter.addWidget(self.diagram_view)
        
        # Set splitter proportions
        self.splitter.setSizes([300, 400, 700])
    
    def _create_dock_widgets(self):
        """Create dockable widgets."""
        # Package tree (left dock)
        self.package_tree = PackageTreeWidget(self.arxml_model)
        self.package_tree_dock = QDockWidget("AR Packages", self)
        self.package_tree_dock.setWidget(self.package_tree)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.package_tree_dock)
        
        # Property editor (center)
        self.property_editor = PropertyEditorWidget(self.arxml_model)
        
        # Diagram view (right) - hidden by default
        self.diagram_view = DiagramViewWidget(self.arxml_model)
        self.diagram_dock = QDockWidget("Diagram View", self)
        self.diagram_dock.setWidget(self.diagram_view)
        self.addDockWidget(Qt.RightDockWidgetArea, self.diagram_dock)
        self.diagram_dock.hide()  # Hide by default
        
        # Hierarchy view (additional dock) - moved to left for easier navigation
        self.hierarchy_view = HierarchyViewWidget(self.arxml_model)
        self.hierarchy_dock = QDockWidget("Hierarchy View", self)
        self.hierarchy_dock.setWidget(self.hierarchy_view)
        # Place hierarchy dock on the left alongside the package tree
        self.addDockWidget(Qt.LeftDockWidgetArea, self.hierarchy_dock)
        
        # Validation panel (bottom)
        self.validation_panel = ValidationPanelWidget(self.arxml_model)
        self.validation_dock = QDockWidget("Validation", self)
        self.validation_dock.setWidget(self.validation_panel)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.validation_dock)
    
    def _setup_connections(self):
        """Set up signal connections."""
        # File operations
        self.file_opened.connect(self._on_file_opened)
        self.file_saved.connect(self._on_file_saved)
        
        # Element selection
        self.package_tree.element_selected.connect(self._on_element_selected)
        self.element_selected.connect(self.property_editor.set_element)
        self.element_selected.connect(self.diagram_view.set_element)
        self.element_selected.connect(self.hierarchy_view.set_element)
        
        # Diagram toggle actions are already connected in their creation
        
        # Validation
        self.validation_completed.connect(self.validation_panel.update_errors)
        
        # Model changes
        self.arxml_model.is_modified = True
        self._update_window_title()
    
    def _setup_menu(self):
        """Set up menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        # New
        new_action = QAction("&New", self)
        new_action.setShortcut(QKeySequence.New)
        new_action.triggered.connect(self._new_file)
        file_menu.addAction(new_action)
        
        # Open
        open_action = QAction("&Open...", self)
        open_action.setShortcut(QKeySequence.Open)
        open_action.triggered.connect(self._open_file)
        file_menu.addAction(open_action)
        
        # Save
        save_action = QAction("&Save", self)
        save_action.setShortcut(QKeySequence.Save)
        save_action.triggered.connect(self._save_file)
        file_menu.addAction(save_action)
        
        # Save As
        save_as_action = QAction("Save &As...", self)
        save_as_action.setShortcut(QKeySequence.SaveAs)
        save_as_action.triggered.connect(self._save_file_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # Export
        export_menu = file_menu.addMenu("&Export")
        
        # Export to different schema versions
        for release in AUTOSARRelease:
            export_action = QAction(f"Export as {release.value}", self)
            export_action.triggered.connect(lambda checked, r=release: self._export_as_schema(r))
            export_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        # Exit
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        # Undo/Redo (placeholder)
        undo_action = QAction("&Undo", self)
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.setEnabled(False)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("&Redo", self)
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.setEnabled(False)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        # Find
        find_action = QAction("&Find...", self)
        find_action.setShortcut(QKeySequence.Find)
        find_action.triggered.connect(self._show_find_dialog)
        edit_menu.addAction(find_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        # Toggle dock widgets
        view_menu.addAction(self.package_tree_dock.toggleViewAction())
        
        # Diagram view toggle with custom action
        self.diagram_toggle_action = QAction("&Diagram View", self)
        self.diagram_toggle_action.setCheckable(True)
        self.diagram_toggle_action.setChecked(False)
        self.diagram_toggle_action.triggered.connect(self._sync_diagram_toggle)
        view_menu.addAction(self.diagram_toggle_action)
        
        view_menu.addAction(self.hierarchy_dock.toggleViewAction())
        view_menu.addAction(self.validation_dock.toggleViewAction())
        
        # Tools menu
        tools_menu = menubar.addMenu("&Tools")
        
        # Validate
        validate_action = QAction("&Validate", self)
        validate_action.triggered.connect(self._validate_model)
        tools_menu.addAction(validate_action)
        
        # Schema conversion
        schema_menu = tools_menu.addMenu("&Schema Conversion")
        for release in AUTOSARRelease:
            convert_action = QAction(f"Convert to {release.value}", self)
            convert_action.triggered.connect(lambda checked, r=release: self._convert_schema(r))
            schema_menu.addAction(convert_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        # About
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _setup_toolbar(self):
        """Set up toolbar."""
        toolbar = self.addToolBar("Main")
        
        # File operations
        toolbar.addAction(self._create_action("New", "document-new", self._new_file))
        toolbar.addAction(self._create_action("Open", "document-open", self._open_file))
        toolbar.addAction(self._create_action("Save", "document-save", self._save_file))
        
        toolbar.addSeparator()
        
        # Validation
        toolbar.addAction(self._create_action("Validate", "checkmark", self._validate_model))
        
        toolbar.addSeparator()
        
        # View operations
        toolbar.addAction(self._create_action("Find", "edit-find", self._show_find_dialog))
        
        toolbar.addSeparator()
        
        # Diagram view toggle
        self.diagram_toolbar_action = self._create_action("Diagram View", "view-preview", self._sync_diagram_toggle)
        self.diagram_toolbar_action.setCheckable(True)
        self.diagram_toolbar_action.setChecked(False)
        toolbar.addAction(self.diagram_toolbar_action)
    
    def _setup_status_bar(self):
        """Set up status bar."""
        self.status_bar = self.statusBar()
        
        # File status
        self.file_status_label = QLabel("No file loaded")
        self.status_bar.addWidget(self.file_status_label)
        
        # Schema version
        self.schema_label = QLabel("")
        self.status_bar.addPermanentWidget(self.schema_label)
        
        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
    
    def _create_action(self, text: str, icon_name: str, callback):
        """Create a toolbar action."""
        action = QAction(text, self)
        action.triggered.connect(callback)
        return action
    
    def _new_file(self):
        """Create a new ARXML file."""
        if self._check_unsaved_changes():
            self.arxml_model.clear()
            self.current_file = None
            self.is_modified = False
            self._update_window_title()
            self._update_status_bar()
            self.package_tree.refresh()
    
    def _open_file(self):
        """Open an ARXML file."""
        if self._check_unsaved_changes():
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Open ARXML File", "", "ARXML Files (*.arxml);;All Files (*)"
            )
            if file_path:
                self._load_file(Path(file_path))
    
    def _save_file(self):
        """Save current file."""
        if self.current_file:
            self._save_to_file(self.current_file)
        else:
            self._save_file_as()
    
    def _save_file_as(self):
        """Save file with new name."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save ARXML File", "", "ARXML Files (*.arxml);;All Files (*)"
        )
        if file_path:
            self._save_to_file(Path(file_path))
    
    def _export_as_schema(self, target_schema: AUTOSARRelease):
        """Export current model to different schema version."""
        if not self.current_file:
            QMessageBox.warning(self, "Export", "No file loaded to export.")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, f"Export as {target_schema.value}", 
            f"{self.current_file.stem}_{target_schema.value.replace('-', '_')}.arxml",
            "ARXML Files (*.arxml);;All Files (*)"
        )
        if file_path:
            self._save_to_file(Path(file_path), target_schema)
    
    def _load_file(self, file_path: Path, validate_first: bool = True):
        """Load ARXML file.

        validate_first: when True perform a lightweight well-formedness check
        before launching the background load thread. This avoids attempting
        to fully parse obviously malformed files at startup and produces a
        gentler warning instead of a blocking critical dialog.
        """
        self._show_progress("Loading file...")

        # Optional lightweight validation to catch common parse errors early
        if validate_first:
            try:
                import xml.etree.ElementTree as ET
                # Use iterparse to quickly check basic well-formedness without
                # building the full tree in the main thread.
                iterator = ET.iterparse(str(file_path), events=("start",))
                # consume one event to trigger any ParseError early
                next(iterator, None)
            except ET.ParseError as pe:
                logging.getLogger(__name__).warning(
                    "Quick-parse failed for %s: %s", file_path, pe
                )
                self._hide_progress()
                # Show a non-fatal warning and avoid starting the heavy load
                self.status_bar.showMessage(f"Failed to load (not well-formed): {file_path.name}", 8000)
                QMessageBox.warning(
                    self,
                    "Invalid ARXML",
                    f"File is not well-formed XML and was not loaded:\n{file_path}\n\nParse error: {pe}"
                )
                return
            except Exception as e:
                # Any IO or unexpected error should be logged but not crash
                logging.getLogger(__name__).warning(
                    "Could not pre-validate file %s: %s", file_path, e
                )

        # Load in background thread to avoid UI freezing
        self.load_thread = LoadFileThread(file_path, self.arxml_model)
        self.load_thread.file_loaded.connect(self._on_file_loaded)
        self.load_thread.error_occurred.connect(self._on_load_error)
        self.load_thread.start()
    
    def _save_to_file(self, file_path: Path, target_schema: Optional[AUTOSARRelease] = None):
        """Save model to file."""
        self._show_progress("Saving file...")
        
        # Check if this is a Save As operation (different from current file)
        is_save_as = self.current_file != file_path
        
        success = self.arxml_model.save_file(file_path, target_schema)
        self._hide_progress()
        
        if success:
            self.current_file = file_path
            self.is_modified = False
            self._update_window_title()
            self._update_status_bar()
            self.file_saved.emit(str(file_path))
            
            # Show appropriate status message
            if is_save_as:
                self.status_bar.showMessage(f"File saved as: {file_path.name}", 5000)
            else:
                self.status_bar.showMessage(f"File saved: {file_path.name}", 3000)
        else:
            QMessageBox.critical(self, "Save Error", f"Failed to save file: {file_path}")
    
    def _on_file_loaded(self, file_path: Path, success: bool):
        """Handle file loaded signal."""
        self._hide_progress()
        
        if success:
            self.current_file = file_path
            self.is_modified = False
            self._update_window_title()
            self._update_status_bar()
            # Refresh package tree so UI widgets have the latest model
            self.package_tree.refresh()

            # If nothing is selected yet, preselect the first root element so
            # the property editor, diagram and hierarchy panes populate on load.
            try:
                current_selected = self.package_tree.get_selected_element()
                if not current_selected:
                    all_elements = self.arxml_model.element_index.get_all_elements()
                    # Root elements have no parent_path or an empty parent_path
                    root_elements = [e for e in all_elements if not e.parent_path]
                    if root_elements:
                        # Choose the first root element (stable ordering not guaranteed)
                        root_path = root_elements[0].path
                        self.package_tree.expand_to_path(root_path)
            except Exception:
                # Be defensive: do not let UI population errors break loading
                logging.getLogger(__name__).exception("Failed to preselect root element")

            self.file_opened.emit(str(file_path))
            self.status_bar.showMessage(f"File loaded: {file_path.name}", 3000)
        else:
            # Show a non-fatal warning for load failures (parsing/indexing issues)
            logging.getLogger(__name__).warning("Failed to load file: %s", file_path)
            self.status_bar.showMessage(f"Failed to load file: {file_path.name}", 5000)
            QMessageBox.warning(self, "Load Error", f"Failed to load file: {file_path}")
    
    def _on_load_error(self, error_message: str):
        """Handle load error."""
        self._hide_progress()
        # Log and display a non-fatal warning so startup isn't blocked by a modal
        logging.getLogger(__name__).warning("Load error: %s", error_message)
        self.status_bar.showMessage("Error loading file", 5000)
        QMessageBox.warning(self, "Load Error", error_message)
    
    def _on_file_opened(self, file_path: str):
        """Handle file opened signal."""
        pass  # Implement if needed
    
    def _on_file_saved(self, file_path: str):
        """Handle file saved signal."""
        pass  # Implement if needed
    
    def _on_element_selected(self, path: str):
        """Handle element selection."""
        self.element_selected.emit(path)
    
    def _toggle_diagram_view(self):
        """Toggle diagram view visibility."""
        if self.diagram_dock.isVisible():
            self.diagram_dock.hide()
            self.diagram_toggle_action.setChecked(False)
            self.diagram_toolbar_action.setChecked(False)
        else:
            self.diagram_dock.show()
            self.diagram_toggle_action.setChecked(True)
            self.diagram_toolbar_action.setChecked(True)
    
    def _sync_diagram_toggle(self):
        """Sync diagram toggle actions between menu and toolbar."""
        is_checked = self.sender().isChecked()
        self.diagram_toggle_action.setChecked(is_checked)
        self.diagram_toolbar_action.setChecked(is_checked)
        
        if is_checked:
            self.diagram_dock.show()
        else:
            self.diagram_dock.hide()
    
    def _setup_window_geometry(self):
        """Set up window geometry with multi-monitor support."""
        try:
            # Get available screens
            screens = QApplication.screens()
            if len(screens) > 1:
                # Use the primary screen
                primary_screen = QApplication.primaryScreen()
                screen_geometry = primary_screen.availableGeometry()
                
                # Set window size based on screen size
                width = min(1400, screen_geometry.width() - 100)
                height = min(900, screen_geometry.height() - 100)
                x = screen_geometry.x() + 50
                y = screen_geometry.y() + 50
                
                self.setGeometry(x, y, width, height)
            else:
                # Single screen - use default geometry
                self.setGeometry(100, 100, 1400, 900)
                
        except Exception as e:
            # Fallback to default geometry
            self.setGeometry(100, 100, 1400, 900)
    
    def changeEvent(self, event):
        """Handle window state changes."""
        from PySide6.QtCore import QEvent
        
        if event.type() == QEvent.WindowStateChange:
            # Handle window state changes (maximize, minimize, etc.)
            try:
                # Ensure the window is properly positioned after state changes
                if self.isMaximized():
                    # Window is maximized - ensure it's visible
                    self.raise_()
                    self.activateWindow()
            except Exception:
                # Ignore errors during state changes
                pass
        
        super().changeEvent(event)
    
    def _validate_model(self):
        """Validate the current model."""
        self._show_progress("Validating...")
        
        # Run validation in background
        self.validation_thread = ValidationThread(self.arxml_model)
        self.validation_thread.validation_completed.connect(self._on_validation_completed)
        self.validation_thread.start()
    
    def _on_validation_completed(self, errors):
        """Handle validation completion."""
        self._hide_progress()
        self.validation_completed.emit(errors)
        
        error_count = len([e for e in errors if e.level.value == "error"])
        warning_count = len([e for e in errors if e.level.value == "warning"])
        
        self.status_bar.showMessage(
            f"Validation complete: {error_count} errors, {warning_count} warnings", 5000
        )
    
    def _convert_schema(self, target_schema: AUTOSARRelease):
        """Convert current model to different schema."""
        if not self.current_file:
            QMessageBox.warning(self, "Schema Conversion", "No file loaded to convert.")
            return
        
        if self.arxml_model.can_convert_schema(target_schema):
            reply = QMessageBox.question(
                self, "Schema Conversion",
                f"Convert current model to {target_schema.value}?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                # Update model schema
                self.arxml_model.files[self.current_file].schema_version = target_schema
                self.is_modified = True
                self._update_window_title()
                self._update_status_bar()
        else:
            QMessageBox.warning(
                self, "Schema Conversion",
                f"Cannot convert to {target_schema.value}. Schema not supported."
            )
    
    def _show_find_dialog(self):
        """Show find dialog."""
        # Placeholder - implement find dialog
        QMessageBox.information(self, "Find", "Find dialog not implemented yet.")
    
    def _show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self, "About ARXML Editor",
            "ARXML Editor v0.1.0\n\n"
            "Professional AUTOSAR XML Editor with advanced validation,\n"
            "cross-reference management, and visual diagram support.\n\n"
            "Built with PySide6 and autosar-data."
        )
    
    def _show_welcome_message(self):
        """Show welcome message."""
        QMessageBox.information(
            self, "Welcome to ARXML Editor",
            "Welcome to ARXML Editor!\n\n"
            "To get started:\n"
            "1. Open an ARXML file using File > Open\n"
            "2. Navigate the package tree on the left\n"
            "3. Edit properties in the center panel\n"
            "4. View diagrams on the right\n"
            "5. Check validation results at the bottom"
        )
    
    def _check_unsaved_changes(self) -> bool:
        """Check for unsaved changes and prompt user."""
        if self.is_modified:
            reply = QMessageBox.question(
                self, "Unsaved Changes",
                "You have unsaved changes. Do you want to save them?",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if reply == QMessageBox.Save:
                self._save_file()
                return True
            elif reply == QMessageBox.Discard:
                return True
            else:
                return False
        return True
    
    def _update_window_title(self):
        """Update window title with current file and modification status."""
        if self.current_file:
            title = f"ARXML Editor - {self.current_file.name}"
            if self.is_modified:
                title += " *"
        else:
            title = "ARXML Editor - Untitled"
        
        self.setWindowTitle(title)
    
    def _update_status_bar(self):
        """Update status bar information."""
        if self.current_file:
            self.file_status_label.setText(f"File: {self.current_file.name}")
            
            # Get schema version
            schema_version = self.arxml_model.files[self.current_file].schema_version
            if schema_version:
                self.schema_label.setText(f"Schema: {schema_version.value}")
            else:
                self.schema_label.setText("Schema: Unknown")
        else:
            self.file_status_label.setText("No file loaded")
            self.schema_label.setText("")
    
    def _show_progress(self, message: str):
        """Show progress bar."""
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.status_bar.showMessage(message)
    
    def _hide_progress(self):
        """Hide progress bar."""
        self.progress_bar.setVisible(False)
    
    def closeEvent(self, event):
        """Handle window close event."""
        if self._check_unsaved_changes():
            event.accept()
        else:
            event.ignore()


class LoadFileThread(QThread):
    """Thread for loading ARXML files."""
    
    file_loaded = Signal(Path, bool)
    error_occurred = Signal(str)
    
    def __init__(self, file_path: Path, arxml_model: ARXMLModel):
        super().__init__()
        self.file_path = file_path
        self.arxml_model = arxml_model
    
    def run(self):
        """Load file in background thread."""
        try:
            success = self.arxml_model.load_file(self.file_path)
            self.file_loaded.emit(self.file_path, success)
        except Exception as e:
            self.error_occurred.emit(str(e))


class ValidationThread(QThread):
    """Thread for running validation."""
    
    validation_completed = Signal(list)
    
    def __init__(self, arxml_model: ARXMLModel):
        super().__init__()
        self.arxml_model = arxml_model
    
    def run(self):
        """Run validation in background thread."""
        try:
            from ..validation.validator import ARXMLValidator
            validator = ARXMLValidator(
                self.arxml_model.schema_manager,
                self.arxml_model.element_index,
                self.arxml_model.reference_manager
            )
            errors = validator.validate_all()
            self.validation_completed.emit(errors)
        except Exception as e:
            # Return error as validation result
            from ..validation.types import ValidationError, ValidationLevel
            error = ValidationError(
                path="",
                message=f"Validation failed: {str(e)}",
                level=ValidationLevel.ERROR
            )
            self.validation_completed.emit([error])