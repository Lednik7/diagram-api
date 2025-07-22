from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class DiagramRequest(BaseModel):
    description: str

class DiagramResponse(BaseModel):
    image_data: str
    message: str

class NodeSpec(BaseModel):
    id: str
    type: str
    label: str

class ClusterSpec(BaseModel):
    id: str
    name: str
    nodes: List[str]

class EdgeSpec(BaseModel):
    from_: str = Field(alias="from")
    to: str

class DiagramConfig(BaseModel):
    name: str
    filename: str = "diagram"
    show: bool = False

class DiagramSpec(BaseModel):
    diagram: DiagramConfig
    nodes: List[NodeSpec]
    clusters: List[ClusterSpec] = []
    edges: List[EdgeSpec] = []

class AssistantRequest(BaseModel):
    message: str
    context: Optional[str] = None

class AssistantResponse(BaseModel):
    response: str
    action: Optional[str] = None
    image_data: Optional[str] = None