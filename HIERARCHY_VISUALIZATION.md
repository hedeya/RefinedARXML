# ARXML Hierarchy Visualization

This document describes the new hierarchy visualization feature added to the ARXML Editor, which provides tree-based views showing parent-child relationships in ARXML structure.

## Features

### 1. **Dual View Interface**
- **Tree Widget**: Left panel showing hierarchical structure in a traditional tree format
- **Graphics View**: Right panel showing visual hierarchy with connected nodes
- **Synchronized Navigation**: Both views stay synchronized when selecting elements

### 2. **Interactive Hierarchy Visualization**
- **Expandable/Collapsible Nodes**: Click to expand or collapse hierarchy branches
- **Visual Connections**: Lines connecting parent and child nodes
- **Level-based Color Coding**: Different colors for different hierarchy levels
- **Element Type Indicators**: Visual indicators showing element types (AR-PACKAGE, ELEMENT, CONTAINER, etc.)

### 3. **Advanced Layout Options**
- **Auto Layout**: Automatic tree layout algorithm
- **Expand All/Collapse All**: Quick controls for managing large hierarchies
- **Zoom Controls**: Zoom in/out and fit-to-view functionality
- **Customizable Display**: Toggle element types and level indicators

### 4. **Navigation Features**
- **Element Selection**: Click on any node to select and view its properties
- **Context Menus**: Right-click for additional options
- **Search and Filter**: Find specific elements in the hierarchy
- **Breadcrumb Navigation**: Track your position in the hierarchy

## Usage

### Starting the Hierarchy View

1. **Launch the ARXML Editor**
2. **Load an ARXML file** using File → Open
3. **Open the Hierarchy View** using View → Hierarchy View
4. **Select an element** in the package tree to view its hierarchy

### Navigation

#### Tree Widget (Left Panel)
- **Click on items** to select elements
- **Expand/collapse** by clicking the arrow icons
- **Right-click** for context menu options

#### Graphics View (Right Panel)
- **Click on nodes** to select elements
- **Drag nodes** to reposition them (layout will auto-adjust)
- **Use mouse wheel** to zoom in/out
- **Right-click** for context menu options

### Toolbar Controls

- **Auto Layout**: Automatically arrange nodes in a tree structure
- **Expand All**: Expand all nodes in the hierarchy
- **Collapse All**: Collapse all nodes to show only the root
- **Zoom In/Out**: Adjust the zoom level
- **Fit to View**: Fit the entire hierarchy in the view
- **Show Types**: Toggle display of element types
- **Show Levels**: Toggle display of level indicators

## Visual Design

### Color Scheme
- **Level 0 (Root)**: Blue (#6496C8)
- **Level 1**: Green (#96C864)
- **Level 2**: Orange (#C89664)
- **Level 3**: Pink (#C86496)
- **Level 4+**: Purple (#9664C8)

### Node Appearance
- **Main Name**: Bold text at the top of each node
- **Element Type**: Smaller text below the name
- **Level Indicator**: Colored bar on the left side
- **Expand/Collapse**: Arrow indicator for expandable nodes

### Connection Lines
- **Parent-Child**: Gray lines connecting nodes
- **Visual Hierarchy**: Clear visual representation of relationships

## Technical Implementation

### Key Components

1. **HierarchyViewWidget**: Main widget containing both tree and graphics views
2. **HierarchyTreeNode**: Graphics item representing individual nodes
3. **HierarchyTreeScene**: Graphics scene managing the visual hierarchy
4. **Tree Widget**: Standard Qt tree widget for navigation

### Layout Algorithm

The hierarchy uses a recursive tree layout algorithm:
- **Root nodes** are positioned at the top
- **Child nodes** are positioned below their parents with indentation
- **Siblings** are arranged horizontally with proper spacing
- **Connections** are drawn between parent and child nodes

### Performance Optimizations

- **Lazy Loading**: Only visible nodes are fully rendered
- **Efficient Layout**: Layout algorithm runs only when needed
- **Memory Management**: Proper cleanup of graphics items
- **Smooth Interaction**: Responsive UI with minimal lag

## Example Usage

### Loading a Sample File

```python
# Load the hierarchy sample
arxml_model.load_file("examples/hierarchy_sample.arxml")

# Set the root element for hierarchy view
hierarchy_view.set_element("/AUTOSAR/AR-PACKAGES/AR-PACKAGE[1]")
```

### Programmatic Access

```python
# Get the hierarchy view widget
hierarchy_view = main_window.hierarchy_view

# Set a specific element
hierarchy_view.set_element("/path/to/element")

# Expand all nodes
hierarchy_view._expand_all()

# Apply auto layout
hierarchy_view._apply_auto_layout()
```

## Integration with Main Application

The hierarchy view is integrated into the main ARXML Editor as a dockable widget:

- **Dock Location**: Right dock area (alongside diagram view)
- **Menu Access**: View → Hierarchy View
- **Signal Integration**: Connected to element selection system
- **State Persistence**: Maintains state across file operations

## Future Enhancements

### Planned Features
- **Search and Filter**: Find specific elements in large hierarchies
- **Export Options**: Export hierarchy as image or PDF
- **Custom Layouts**: Additional layout algorithms (circular, radial, etc.)
- **Performance Improvements**: Better handling of very large hierarchies
- **Animation**: Smooth transitions when expanding/collapsing nodes

### Customization Options
- **Color Themes**: Multiple color schemes
- **Node Shapes**: Different shapes for different element types
- **Connection Styles**: Various line styles and colors
- **Font Settings**: Customizable text appearance

## Troubleshooting

### Common Issues

1. **Hierarchy not displaying**: Ensure an ARXML file is loaded and an element is selected
2. **Nodes not expanding**: Check if the element has children in the ARXML structure
3. **Layout issues**: Use the "Auto Layout" button to reset the arrangement
4. **Performance problems**: For very large hierarchies, try collapsing unused branches

### Debug Information

The hierarchy view provides status information in the bottom panel:
- **Node Count**: Number of nodes in the current hierarchy
- **Selection Status**: Currently selected element path
- **Layout Status**: Whether auto-layout is enabled

## Conclusion

The hierarchy visualization feature provides a powerful and intuitive way to explore ARXML file structures. It combines the familiarity of tree navigation with the visual appeal of connected diagrams, making it easier to understand complex ARXML hierarchies and navigate large files efficiently.

This feature is particularly useful for:
- **System Architects**: Understanding overall system structure
- **Developers**: Navigating complex ARXML files
- **Testers**: Verifying ARXML structure and relationships
- **Documentation**: Creating visual representations of ARXML structures