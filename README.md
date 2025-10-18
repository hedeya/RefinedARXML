# ARXML Editor

A professional-grade GUI editor for AUTOSAR XML (ARXML) files with comprehensive validation, cross-reference management, and diagram support.

## 🚀 Features

### Core Functionality
- **Multi-schema Support**: Load and edit ARXML files across multiple AUTOSAR releases (R20.11, R21.11, R22.11, R24.11)
- **Advanced Validation**: Two-tier validation with XSD compliance and semantic rule checking
- **Cross-Reference Management**: Full support for ARXML references with integrity checking
- **Visual Diagrams**: Interactive diagrams for SWC compositions and system topologies
- **Performance Optimized**: Lazy loading and indexing for large ARXML files
- **Professional UI**: Modern PySide6 interface with dockable panels and tree navigation

### Advanced Features
- **Schema Conversion**: Convert between different AUTOSAR releases
- **Deterministic Serialization**: Consistent XML output for better version control
- **Quick Fixes**: Automated fixes for common validation errors
- **Reference Navigation**: Jump to definitions and find all references
- **Search & Filter**: Powerful search across elements with type filtering
- **ECUC Support**: Full support for ECU Configuration (ECUC) elements

## 🏗️ Architecture

- **Core Engine**: Built on `autosar-data` for robust ARXML processing
- **UI Framework**: PySide6 for native cross-platform experience
- **Validation**: XSD + semantic rule-based validation system
- **Diagrams**: ELK layout integration for professional diagram rendering
- **Serialization**: Custom ARXML serializer with AUTOSAR naming conventions

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- Qt6 libraries (installed automatically with PySide6)

### Install from Source
```bash
# Clone the repository
git clone https://github.com/arxml-editor/arxml-editor.git
cd arxml-editor

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Run the Application
```bash
# Method 1: Using the launcher script
python run_editor.py

# Method 2: Using the module
python -m arxml_editor.main

# Method 3: Using the console script (after installation)
arxml-editor
```

## 🎯 Usage

### Basic Workflow
1. **Open ARXML files** through File > Open
2. **Navigate** using the package tree on the left
3. **Edit properties** in the center panel
4. **View diagrams** in the right panel
5. **Check validation** results in the bottom panel

### Key Features

#### Package Tree Navigation
- Hierarchical view of ARXML packages and elements
- Search and filter by element type
- Context menu for quick actions
- Expandable/collapsible tree structure

#### Property Editor
- Form-based editing of element properties
- Attribute management
- Content editing for text elements
- Reference visualization and navigation

#### Diagram View
- Interactive diagrams for different views:
  - **Hierarchy**: Parent-child relationships
  - **References**: Cross-reference connections
  - **Composition**: SWC composition diagrams
  - **System Topology**: System-level connections
- Auto-layout with ELK integration
- Zoom and pan controls
- Node selection and navigation

#### Validation Panel
- Real-time validation with error/warning/info levels
- Quick fixes for common issues
- Filter by validation level or rule
- Jump to error locations

### Advanced Usage

#### Schema Conversion
```python
# Convert between AUTOSAR releases
model.convert_to_release(AUTOSARRelease.R24_11)
```

#### Custom Validation Rules
```python
# Add custom validation rules
from arxml_editor.validation.rule_engine import RuleEngine, ValidationRule

rule_engine = RuleEngine()
custom_rule = ValidationRule(
    rule_id="CUSTOM001",
    name="Custom Rule",
    description="Custom validation rule",
    severity=RuleSeverity.WARNING,
    category="Custom",
    validator=my_custom_validator
)
rule_engine.add_rule(custom_rule)
```

#### Programmatic Access
```python
from arxml_editor.core.arxml_model import ARXMLModel

# Create model
model = ARXMLModel()

# Load file
model.load_file("example.arxml")

# Get element
element = model.get_element_by_path("/MyPackage/MyElement")

# Create new element
new_path = model.create_element("/MyPackage", "ELEMENT", "NewElement")

# Save file
model.save_file("output.arxml")
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=arxml_editor

# Run specific test file
pytest tests/test_arxml_model.py

# Run with verbose output
pytest -v
```

## 🔧 Development

### Code Style
```bash
# Format code
black arxml_editor/

# Sort imports
isort arxml_editor/

# Type checking
mypy arxml_editor/
```

### Project Structure
```
arxml_editor/
├── core/                   # Core ARXML processing
│   ├── arxml_model.py     # Main model class
│   ├── schema_manager.py  # Schema version management
│   ├── element_index.py   # Element indexing
│   └── reference_manager.py # Reference management
├── ui/                    # User interface
│   ├── main_window.py     # Main application window
│   ├── package_tree.py    # Package tree widget
│   ├── property_editor.py # Property editing
│   ├── diagram_view.py    # Diagram visualization
│   └── validation_panel.py # Validation results
├── validation/            # Validation system
│   ├── validator.py       # Main validator
│   ├── xsd_validator.py   # XSD validation
│   ├── semantic_validator.py # Semantic validation
│   └── rule_engine.py     # Rule-based validation
├── serialization/         # Serialization
│   ├── arxml_serializer.py # ARXML serialization
│   ├── naming_converter.py # Naming conventions
│   └── xml_formatter.py   # XML formatting
├── diagrams/              # Diagram rendering
│   └── elk_layout.py      # ELK layout engine
└── utils/                 # Utilities
    ├── naming_conventions.py # Naming rules
    ├── xml_utils.py       # XML utilities
    └── path_utils.py      # Path utilities
```

## 📋 Requirements

### Core Dependencies
- PySide6 >= 6.6.0 (Qt6 Python bindings)
- autosar-data >= 0.1.0 (ARXML processing)
- lxml >= 4.9.0 (XML processing)
- xmlschema >= 3.0.0 (XSD validation)
- networkx >= 3.0 (Graph algorithms)
- pydantic >= 2.0.0 (Data validation)

### Optional Dependencies
- elkjs (for advanced diagram layout)
- matplotlib (for diagram rendering)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- AUTOSAR Consortium for the ARXML specification
- Eclipse Foundation for the ELK layout engine
- Qt Company for the PySide6 framework
- The open-source community for various dependencies

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/arxml-editor/arxml-editor/issues)
- **Discussions**: [GitHub Discussions](https://github.com/arxml-editor/arxml-editor/discussions)
- **Documentation**: [Read the Docs](https://arxml-editor.readthedocs.io/)

## 🗺️ Roadmap

- [ ] Plugin system for custom validators
- [ ] Advanced diagram layouts (force-directed, hierarchical)
- [ ] ARXML diff and merge tools
- [ ] Batch processing capabilities
- [ ] Integration with AUTOSAR modeling tools
- [ ] Performance profiling and optimization
- [ ] Multi-language support
- [ ] Cloud-based collaboration features