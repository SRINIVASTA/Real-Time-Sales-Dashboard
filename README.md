Real-Time Sales Dashboard with Streamlit
This project demonstrates how to build and deploy a live, real-time sales dashboard using Python, Streamlit, and Pandas. The application simulates live sales events and visualizes key metrics as they happen, all within a simple, web-based interface. The entire application is self-contained and designed to be easily deployed on Streamlit Community Cloud directly from a GitHub repository.
✅ Features
Real-Time Data Simulation: Generates a continuous stream of mock sales data to mimic live events.
Live Metrics: Visualizes key performance indicators (KPIs) that update in real time, including:
Total Units Sold
Total Revenue
Dynamic Charts: Utilizes Plotly to create dynamic, auto-updating charts for:
Revenue over time (Line Chart)
Product performance by units sold (Bar Chart)
Interactive Data Table: Displays the raw, incoming sales data in a sortable table.
Zero Database Dependency: Uses Streamlit's session_state and Pandas DataFrames to manage data in-memory, simplifying setup and deployment.
One-Click Deployment: Ready to be deployed on Streamlit Community Cloud with minimal configuration.
🛠️ Technologies Used
Streamlit: The core framework for building the interactive web application.
Pandas: Used for efficient data manipulation and storage in memory.
Plotly Express: For creating rich, interactive visualizations.
GitHub: For version control and hosting the application code.
Streamlit Community Cloud: For deploying the application live on the web.
