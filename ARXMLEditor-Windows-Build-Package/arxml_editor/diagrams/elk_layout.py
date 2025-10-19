"""
ELK (Eclipse Layout Kernel) integration for automatic diagram layout.

Provides automatic layout algorithms for ARXML diagrams.
"""

from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json


class LayoutAlgorithm(Enum):
    """Available layout algorithms."""
    LAYERED = "layered"
    FORCE = "force"
    STRESS = "stress"
    RECTPACKING = "rectpacking"
    TREE = "tree"


@dataclass
class LayoutNode:
    """Represents a node in the layout."""
    id: str
    width: float = 100.0
    height: float = 60.0
    x: float = 0.0
    y: float = 0.0
    properties: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.properties is None:
            self.properties = {}


@dataclass
class LayoutEdge:
    """Represents an edge in the layout."""
    id: str
    source: str
    target: str
    properties: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.properties is None:
            self.properties = {}


@dataclass
class LayoutOptions:
    """Layout configuration options."""
    algorithm: LayoutAlgorithm = LayoutAlgorithm.LAYERED
    direction: str = "DOWN"  # UP, DOWN, LEFT, RIGHT
    spacing: float = 50.0
    node_spacing: float = 20.0
    edge_spacing: float = 10.0
    layer_spacing: float = 50.0
    crossing_minimization: str = "LAYER_SWEEP"
    node_placement: str = "SIMPLE"
    edge_routing: str = "ORTHOGONAL"


class ELKLayoutEngine:
    """ELK layout engine for automatic diagram layout."""
    
    def __init__(self):
        self.options = LayoutOptions()
        self._elk_available = self._check_elk_availability()
    
    def _check_elk_availability(self) -> bool:
        """Check if ELK is available."""
        try:
            # Try to import elkjs (JavaScript ELK port)
            import subprocess
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (ImportError, subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def layout_diagram(self, nodes: List[LayoutNode], edges: List[LayoutEdge], 
                      options: Optional[LayoutOptions] = None) -> Tuple[List[LayoutNode], List[LayoutEdge]]:
        """Apply layout to diagram nodes and edges."""
        if not self._elk_available:
            return self._fallback_layout(nodes, edges, options)
        
        layout_options = options or self.options
        
        try:
            return self._elk_layout(nodes, edges, layout_options)
        except Exception:
            # Fallback to simple layout if ELK fails
            return self._fallback_layout(nodes, edges, layout_options)
    
    def _elk_layout(self, nodes: List[LayoutNode], edges: List[LayoutEdge], 
                   options: LayoutOptions) -> Tuple[List[LayoutNode], List[LayoutEdge]]:
        """Apply ELK layout using Node.js elkjs."""
        import subprocess
        import tempfile
        import os
        
        # Create ELK graph structure
        elk_graph = {
            "id": "root",
            "layoutOptions": self._get_elk_options(options),
            "children": [
                {
                    "id": node.id,
                    "width": node.width,
                    "height": node.height,
                    "properties": node.properties
                }
                for node in nodes
            ],
            "edges": [
                {
                    "id": edge.id,
                    "sources": [edge.source],
                    "targets": [edge.target],
                    "properties": edge.properties
                }
                for edge in edges
            ]
        }
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as input_file:
            json.dump(elk_graph, input_file)
            input_path = input_file.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as output_file:
            output_path = output_file.name
        
        try:
            # Run ELK layout
            elk_script = f"""
            const ELK = require('elkjs');
            const fs = require('fs');
            
            const elk = new ELK();
            const input = JSON.parse(fs.readFileSync('{input_path}', 'utf8'));
            
            elk.layout(input)
                .then(result => {{
                    fs.writeFileSync('{output_path}', JSON.stringify(result, null, 2));
                }})
                .catch(err => {{
                    console.error('ELK layout failed:', err);
                    process.exit(1);
                }});
            """
            
            # Write and run ELK script
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as script_file:
                script_file.write(elk_script)
                script_path = script_file.name
            
            result = subprocess.run(['node', script_path], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                raise Exception(f"ELK layout failed: {result.stderr}")
            
            # Read layout result
            with open(output_path, 'r') as f:
                layout_result = json.load(f)
            
            # Update node positions
            node_positions = {}
            for child in layout_result.get('children', []):
                node_positions[child['id']] = (child.get('x', 0), child.get('y', 0))
            
            # Update nodes with new positions
            for node in nodes:
                if node.id in node_positions:
                    node.x, node.y = node_positions[node.id]
            
            return nodes, edges
            
        finally:
            # Clean up temporary files
            try:
                os.unlink(input_path)
                os.unlink(output_path)
                os.unlink(script_path)
            except OSError:
                pass
    
    def _get_elk_options(self, options: LayoutOptions) -> Dict[str, Any]:
        """Get ELK layout options."""
        elk_options = {
            "elk.algorithm": options.algorithm.value,
            "elk.direction": options.direction,
            "elk.spacing.nodeNode": str(options.node_spacing),
            "elk.spacing.edgeNode": str(options.edge_spacing),
            "elk.spacing.edgeEdge": str(options.edge_spacing),
            "elk.layered.spacing.nodeNodeBetweenLayers": str(options.layer_spacing),
            "elk.layered.crossingMinimization.strategy": options.crossing_minimization,
            "elk.layered.nodePlacement.strategy": options.node_placement,
            "elk.edgeRouting": options.edge_routing
        }
        
        return elk_options
    
    def _fallback_layout(self, nodes: List[LayoutNode], edges: List[LayoutEdge], 
                        options: Optional[LayoutOptions] = None) -> Tuple[List[LayoutNode], List[LayoutEdge]]:
        """Fallback layout when ELK is not available."""
        layout_options = options or self.options
        
        if layout_options.algorithm == LayoutAlgorithm.TREE:
            return self._tree_layout(nodes, edges, layout_options)
        elif layout_options.algorithm == LayoutAlgorithm.FORCE:
            return self._force_layout(nodes, edges, layout_options)
        else:
            return self._grid_layout(nodes, edges, layout_options)
    
    def _grid_layout(self, nodes: List[LayoutNode], edges: List[LayoutEdge], 
                    options: LayoutOptions) -> Tuple[List[LayoutNode], List[LayoutEdge]]:
        """Simple grid layout."""
        if not nodes:
            return nodes, edges
        
        # Calculate grid dimensions
        cols = int(len(nodes) ** 0.5) + 1
        spacing = options.spacing
        
        for i, node in enumerate(nodes):
            row = i // cols
            col = i % cols
            node.x = col * (node.width + spacing)
            node.y = row * (node.height + spacing)
        
        return nodes, edges
    
    def _tree_layout(self, nodes: List[LayoutNode], edges: List[LayoutEdge], 
                    options: LayoutOptions) -> Tuple[List[LayoutNode], List[LayoutEdge]]:
        """Tree layout algorithm."""
        if not nodes:
            return nodes, edges
        
        # Build adjacency list
        children = {}
        parents = {}
        roots = set()
        
        for edge in edges:
            if edge.source not in children:
                children[edge.source] = []
            children[edge.source].append(edge.target)
            parents[edge.target] = edge.source
        
        # Find root nodes (nodes with no parents)
        for node in nodes:
            if node.id not in parents:
                roots.add(node.id)
        
        # If no roots found, use first node
        if not roots:
            roots.add(nodes[0].id)
        
        # Layout tree recursively
        spacing = options.spacing
        for root in roots:
            self._layout_tree_node(root, children, nodes, 0, 0, spacing, options)
        
        return nodes, edges
    
    def _layout_tree_node(self, node_id: str, children: Dict[str, List[str]], 
                         nodes: List[LayoutNode], x: float, y: float, 
                         spacing: float, options: LayoutOptions):
        """Layout a single tree node and its children."""
        # Find node object
        node = next((n for n in nodes if n.id == node_id), None)
        if not node:
            return
        
        # Set position
        node.x = x
        node.y = y
        
        # Layout children
        child_ids = children.get(node_id, [])
        if not child_ids:
            return
        
        # Calculate child positions
        child_width = max(n.width for n in nodes if n.id in child_ids)
        child_height = max(n.height for n in nodes if n.id in child_ids)
        
        start_x = x - (len(child_ids) - 1) * (child_width + spacing) / 2
        child_y = y + node.height + spacing
        
        for i, child_id in enumerate(child_ids):
            child_x = start_x + i * (child_width + spacing)
            self._layout_tree_node(child_id, children, nodes, child_x, child_y, spacing, options)
    
    def _force_layout(self, nodes: List[LayoutNode], edges: List[LayoutEdge], 
                     options: LayoutOptions) -> Tuple[List[LayoutNode], List[LayoutEdge]]:
        """Force-directed layout algorithm."""
        if not nodes:
            return nodes, edges
        
        # Initialize positions randomly
        import random
        for node in nodes:
            node.x = random.uniform(0, 500)
            node.y = random.uniform(0, 500)
        
        # Force-directed iterations
        iterations = 100
        temperature = 1.0
        cooling_rate = 0.95
        
        for _ in range(iterations):
            # Calculate forces
            forces = {node.id: (0.0, 0.0) for node in nodes}
            
            # Repulsive forces between all nodes
            for i, node1 in enumerate(nodes):
                for j, node2 in enumerate(nodes):
                    if i != j:
                        dx = node1.x - node2.x
                        dy = node1.y - node2.y
                        distance = (dx * dx + dy * dy) ** 0.5
                        
                        if distance > 0:
                            force = 1000.0 / (distance * distance)
                            fx = force * dx / distance
                            fy = force * dy / distance
                            
                            forces[node1.id] = (forces[node1.id][0] + fx, forces[node1.id][1] + fy)
            
            # Attractive forces for connected nodes
            for edge in edges:
                source_node = next((n for n in nodes if n.id == edge.source), None)
                target_node = next((n for n in nodes if n.id == edge.target), None)
                
                if source_node and target_node:
                    dx = target_node.x - source_node.x
                    dy = target_node.y - source_node.y
                    distance = (dx * dx + dy * dy) ** 0.5
                    
                    if distance > 0:
                        force = distance / 100.0
                        fx = force * dx / distance
                        fy = force * dy / distance
                        
                        forces[source_node.id] = (forces[source_node.id][0] + fx, forces[source_node.id][1] + fy)
                        forces[target_node.id] = (forces[target_node.id][0] - fx, forces[target_node.id][1] - fy)
            
            # Apply forces
            for node in nodes:
                force_x, force_y = forces[node.id]
                node.x += force_x * temperature
                node.y += force_y * temperature
                
                # Keep nodes within bounds
                node.x = max(0, min(node.x, 1000))
                node.y = max(0, min(node.y, 1000))
            
            # Cool down
            temperature *= cooling_rate
        
        return nodes, edges
    
    def get_available_algorithms(self) -> List[LayoutAlgorithm]:
        """Get list of available layout algorithms."""
        if self._elk_available:
            return list(LayoutAlgorithm)
        else:
            return [LayoutAlgorithm.GRID, LayoutAlgorithm.TREE, LayoutAlgorithm.FORCE]
    
    def is_elk_available(self) -> bool:
        """Check if ELK is available."""
        return self._elk_available