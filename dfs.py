import streamlit as st
import networkx as nx
from streamlit_agraph import agraph, Node, Edge, Config

# Initialize session state
def initialize_state():
    if "graph" not in st.session_state:
        st.session_state.graph = nx.Graph()
    if "node_positions" not in st.session_state:
        st.session_state.node_positions = {}
    if "dfs_steps" not in st.session_state:
        st.session_state.dfs_steps = []
    if "current_step" not in st.session_state:
        st.session_state.current_step = 0
    if "visited" not in st.session_state:
        st.session_state.visited = set()
    if "stack" not in st.session_state:
        st.session_state.stack = []
    if "dfs_result" not in st.session_state:
        st.session_state.dfs_result = []
    if "node_colors" not in st.session_state:
        st.session_state.node_colors = {}
    if "node_text_colors" not in st.session_state:
        st.session_state.node_text_colors = {}

initialize_state()

# UI Configuration
st.set_page_config(layout="wide", page_title="DFS Visualizer")
st.title("🌐 Interactive Depth First Search (DFS) Visualizer")

# CSS for better styling
st.markdown("""
<style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 8px 16px;
        border: none;
        border-radius: 4px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .highlight {
        background-color: #fffacd;
        padding: 2px 4px;
        border-radius: 3px;
    }
    body {
        color: #333333;
        background-color: #f5f5f5;
    }
</style>
""", unsafe_allow_html=True)

# Color scheme
COLOR_SCHEME = {
    "default": {"fill": "#4682B4", "text": "white"},       # Steel Blue
    "start": {"fill": "#FF6347", "text": "white"},         # Tomato
    "visited": {"fill": "#32CD32", "text": "white"},       # Lime Green
    "stack": {"fill": "#FFD700", "text": "black"},         # Gold
    "current": {"fill": "#9370DB", "text": "white"},       # Medium Purple
    "edge": "#808080"                                      # Gray
}

# Sidebar for graph controls
with st.sidebar:
    st.header("📊 Graph Controls")
    
    # Node management
    with st.expander("➕ Add Node", expanded=True):
        new_node = st.text_input("Node name:", key="new_node")
        if st.button("Add Node"):
            if new_node and new_node not in st.session_state.graph:
                st.session_state.graph.add_node(new_node)
                st.session_state.node_colors[new_node] = COLOR_SCHEME["default"]["fill"]
                st.session_state.node_text_colors[new_node] = COLOR_SCHEME["default"]["text"]
                st.success(f"Node '{new_node}' added!")
            elif new_node in st.session_state.graph:
                st.error(f"Node '{new_node}' already exists!")
    
    # Edge management
    if len(st.session_state.graph.nodes) > 1:
        with st.expander("🔗 Add Edge", expanded=True):
            cols = st.columns(2)
            with cols[0]:
                node1 = st.selectbox("From:", list(st.session_state.graph.nodes))
            with cols[1]:
                node2 = st.selectbox("To:", list(st.session_state.graph.nodes))
            
            if st.button("Connect Nodes"):
                if node1 != node2:
                    st.session_state.graph.add_edge(node1, node2)
                    st.success(f"Edge {node1}-{node2} created!")
                else:
                    st.error("Cannot connect a node to itself!")
    
    # Graph management
    with st.expander("⚙ Graph Settings", expanded=False):
        if st.button("Clear Graph", key="clear_graph"):
            st.session_state.graph = nx.Graph()
            st.session_state.node_positions = {}
            st.session_state.dfs_steps = []
            st.session_state.dfs_result = []
            st.session_state.node_colors = {}
            st.session_state.node_text_colors = {}
            st.success("Graph cleared!")
        
        if st.button("Generate Random Graph", key="random_graph"):
            st.session_state.graph = nx.erdos_renyi_graph(6, 0.3)
            # Convert node labels to strings
            st.session_state.graph = nx.relabel_nodes(st.session_state.graph, lambda x: str(x))
            st.session_state.node_colors = {node: COLOR_SCHEME["default"]["fill"] for node in st.session_state.graph.nodes}
            st.session_state.node_text_colors = {node: COLOR_SCHEME["default"]["text"] for node in st.session_state.graph.nodes}
            st.success("Random graph generated!")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Graph Visualization")
    
    # Convert to agraph format
    nodes = [
        Node(
            id=str(node),
            label=str(node),
            color=st.session_state.node_colors.get(node, COLOR_SCHEME["default"]["fill"]),
            size=25,
            font={"size": 14, "color": st.session_state.node_text_colors.get(node, COLOR_SCHEME["default"]["text"])},
            shape="circle"
        ) 
        for node in st.session_state.graph.nodes
    ]
    
    edges = [
        Edge(
            source=str(node1),
            target=str(node2),
            width=2,
            color=COLOR_SCHEME["edge"]
        ) 
        for node1, node2 in st.session_state.graph.edges
    ]
    
    config = Config(
        width=700,
        height=500,
        directed=False,
        nodeHighlightBehavior=True,
        highlightColor="#F7A7A6",
        collapsible=False,
        node={'labelProperty': 'label'},
        link={'highlightColor': '#ff0000'},
        backgroundColor="#f5f5f5"
    )
    
    if nodes:
        agraph(nodes=nodes, edges=edges, config=config)
    else:
        st.info("Add nodes to visualize the graph")

with col2:
    st.subheader("⚡ DFS Controls")
    
    if st.session_state.graph.nodes:
        start_node = st.selectbox(
            "Select start node:", 
            list(st.session_state.graph.nodes),
            key="start_node"
        )
        
        cols = st.columns(2)
        with cols[0]:
            if st.button("Run DFS", key="run_dfs"):
                st.session_state.dfs_steps = []
                st.session_state.dfs_result = []
                st.session_state.visited = set()
                st.session_state.stack = [start_node]
                st.session_state.current_step = 0
                
                # Reset all node colors
                for node in st.session_state.graph.nodes:
                    st.session_state.node_colors[node] = COLOR_SCHEME["default"]["fill"]
                    st.session_state.node_text_colors[node] = COLOR_SCHEME["default"]["text"]
                
                # Color the start node
                st.session_state.node_colors[start_node] = COLOR_SCHEME["start"]["fill"]
                st.session_state.node_text_colors[start_node] = COLOR_SCHEME["start"]["text"]
                st.success(f"DFS started from node '{start_node}'")
        
        with cols[1]:
            if st.button("Reset DFS", key="reset_dfs"):
                st.session_state.dfs_steps = []
                st.session_state.dfs_result = []
                st.session_state.visited = set()
                st.session_state.stack = []
                st.session_state.current_step = 0
                for node in st.session_state.graph.nodes:
                    st.session_state.node_colors[node] = COLOR_SCHEME["default"]["fill"]
                    st.session_state.node_text_colors[node] = COLOR_SCHEME["default"]["text"]
                st.success("DFS reset!")
        
        # Step through DFS
        if st.session_state.stack or st.session_state.dfs_steps:
            if st.button("Next Step", key="next_step"):
                if st.session_state.stack:
                    node = st.session_state.stack.pop()
                    if node not in st.session_state.visited:
                        st.session_state.visited.add(node)
                        st.session_state.dfs_result.append(node)
                        
                        # Mark as visited
                        st.session_state.node_colors[node] = COLOR_SCHEME["visited"]["fill"]
                        st.session_state.node_text_colors[node] = COLOR_SCHEME["visited"]["text"]
                        
                        step_desc = f"Visited node: {node}"
                        st.session_state.dfs_steps.append(step_desc)
                        
                        neighbors = sorted(st.session_state.graph.neighbors(node), reverse=True)
                        for neighbor in neighbors:
                            if neighbor not in st.session_state.visited and neighbor not in st.session_state.stack:
                                st.session_state.stack.append(neighbor)
                                st.session_state.node_colors[neighbor] = COLOR_SCHEME["stack"]["fill"]
                                st.session_state.node_text_colors[neighbor] = COLOR_SCHEME["stack"]["text"]
                                st.session_state.dfs_steps.append(f"Added to stack: {neighbor}")
                        
                        st.session_state.current_step += 1
                else:
                    st.info("DFS completed!")
    
    # Display DFS progress
    if st.session_state.dfs_steps:
        st.subheader("🔍 DFS Steps")
        
        current_step = st.session_state.current_step
        if current_step < len(st.session_state.dfs_steps):
            st.markdown(f"*Current Step:* <span class='highlight'>{st.session_state.dfs_steps[current_step]}</span>", 
                       unsafe_allow_html=True)
        
        with st.expander("View all steps"):
            for i, step in enumerate(st.session_state.dfs_steps):
                if i == current_step:
                    st.markdown(f"➔ *{step}*")
                else:
                    st.write(f"- {step}")
    
    # Display DFS result
    if st.session_state.dfs_result:
        st.subheader("📜 DFS Traversal Order")
        st.write(" → ".join(str(node) for node in st.session_state.dfs_result))

# Graph statistics
if st.session_state.graph.nodes:
    with st.expander("📈 Graph Statistics", expanded=False):
        cols = st.columns(3)
        cols[0].metric("Nodes", len(st.session_state.graph.nodes))
        cols[1].metric("Edges", len(st.session_state.graph.edges))
        cols[2].metric("Components", nx.number_connected_components(st.session_state.graph))
        
        if st.checkbox("Show adjacency list"):
            st.json({str(node): [str(n) for n in st.session_state.graph.neighbors(node)] 
                    for node in st.session_state.graph.nodes})