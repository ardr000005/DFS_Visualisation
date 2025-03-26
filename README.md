# 🌐 DFS Visualization

A **Streamlit** web application for **Depth First Search (DFS)** visualization with an interactive graph-building interface.

🔗 **Live Demo**: [DFS Visualization](https://dfsvisualisation.streamlit.app/)

## 🚀 Features

- **Add Nodes & Edges**: Create custom graphs interactively.
- **Graph Visualization**: Displays the graph using `streamlit_agraph`.
- **DFS Algorithm**: Step-by-step execution of DFS.
- **DFS Traversal Order**: Shows visited nodes in order.
- **Graph Statistics**: Displays node count, edge count, and connected components.
- **Reset & Clear Options**: Start fresh anytime.

## 🛠 Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/dfs-visualization.git
   cd dfs-visualization
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Run the application:
   ```sh
   streamlit run app.py
   ```

## 📂 Project Structure

```
📁 DFS_Visualization
│── 📄 app.py            # Main Streamlit application
│── 📄 requirements.txt   # Required dependencies
│── 📄 README.md          # Project documentation
```

## 📌 Dependencies

Ensure you have the following installed (automatically installed via `requirements.txt`):

- `streamlit`
- `networkx`
- `matplotlib`
- `streamlit-agraph`

## 🎯 How It Works

1. **Add Nodes**: Enter node names and click "Add Node".
2. **Add Edges**: Select two nodes to connect them with an edge.
3. **Run DFS**: Choose a starting node and execute DFS step by step.
4. **Reset/Restart**: Reset DFS progress or clear the graph.

## 💡 Contributing

Contributions are welcome! Feel free to open issues or create pull requests.

## 📜 License

This project is licensed under the **MIT License**.

---

⭐ **Star** this repo if you found it useful!

