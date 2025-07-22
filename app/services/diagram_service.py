import os
import json
import base64
import tempfile
import importlib
import logging
from diagrams import Diagram, Cluster
from app.models.schemas import DiagramSpec

logger = logging.getLogger(__name__)

class DiagramService:
    def __init__(self):
        logger.info("DiagramService initialized")
    
    def get_node_instance(self, type_path: str, label: str):
        """Create a node instance from type path"""
        provider, module, cls_name = type_path.split(".")
        mod = importlib.import_module(f"diagrams.{provider}.{module}")
        cls = getattr(mod, cls_name)
        return cls(label)
    
    def create_diagram_from_spec(self, spec: DiagramSpec) -> str:
        """Create diagram from JSON specification using the parser"""
        logger.info("Creating diagram from specification...")
        logger.info(f"Diagram name: {spec.diagram.name}")
        logger.info(f"Nodes count: {len(spec.nodes)}")
        logger.info(f"Clusters count: {len(spec.clusters)}")
        logger.info(f"Edges count: {len(spec.edges)}")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            diagram_path = os.path.join(temp_dir, spec.diagram.filename)
            logger.info(f"Diagram path: {diagram_path}")
            
            nodes_spec = {n.id: n for n in spec.nodes}
            clusters_spec = {c.id: c for c in spec.clusters}
            
            logger.info("Creating Diagram object...")
            with Diagram(
                spec.diagram.name,
                filename=diagram_path,
                outformat="png",
                show=spec.diagram.show
            ):
                node_instances = {}
                rendered_nodes = set()

                # Render clusters first
                logger.info("Rendering clusters...")
                for cluster in clusters_spec.values():
                    logger.info(f"Rendering cluster: {cluster.name}")
                    with Cluster(cluster.name):
                        for node_id in cluster.nodes:
                            node_data = nodes_spec[node_id]
                            logger.info(f"Creating node: {node_id} ({node_data.type})")
                            instance = self.get_node_instance(node_data.type, node_data.label)
                            node_instances[node_id] = instance
                            rendered_nodes.add(node_id)

                # Render standalone nodes
                logger.info("Rendering standalone nodes...")
                for node_id, node_data in nodes_spec.items():
                    if node_id not in rendered_nodes:
                        logger.info(f"Creating standalone node: {node_id} ({node_data.type})")
                        instance = self.get_node_instance(node_data.type, node_data.label)
                        node_instances[node_id] = instance

                # Render edges
                logger.info("Rendering edges...")
                for edge in spec.edges:
                    logger.info(f"Creating edge: {edge.from_} -> {edge.to}")
                    node_instances[edge.from_] >> node_instances[edge.to]
            
            # Read generated image
            image_path = f"{diagram_path}.png"
            logger.info(f"Looking for generated image at: {image_path}")
            
            if os.path.exists(image_path):
                file_size = os.path.getsize(image_path)
                logger.info(f"Found image file, size: {file_size} bytes")
                
                with open(image_path, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode()
                    logger.info(f"Encoded image to base64, length: {len(image_data)}")
                    return image_data
            else:
                logger.error(f"Image file not found at {image_path}")
                # List all files in temp directory
                files = os.listdir(temp_dir)
                logger.error(f"Files in temp dir: {files}")
                raise Exception("Failed to generate diagram")