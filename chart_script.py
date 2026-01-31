# Create a comprehensive system architecture diagram for Synova AI
diagram_code = """
flowchart TD
    %% Core orchestrator in center
    Core[Synova AI Core<br/>Central Orchestrator]
    
    %% Core modules
    QEP[Quantum Echo Prediction<br/>QAOA, Quantum SVM, VQC]
    NSF[Neuro-Symbiotic Fusion<br/>Knowledge Graphs, Symbolic AI]
    TWE[Temporal Weave Engine<br/>Pattern Recognition, Context]
    ESG[Ethical Singularity Guardian<br/>Bias Detection, Safety]
    MRI[Mind Resonance Interface<br/>EEG Processing, Neural Decode]
    SEC[Self Evolution Core<br/>Meta-Learning, Genetic Alg]
    BPM[Behavioral Predict Matrix<br/>Pattern Analysis, User Model]
    
    %% Platform deployment
    Android[Android Platform]
    iOS[iOS Platform] 
    PC[PC Platform]
    
    %% Core connections (orchestrator to all modules)
    Core --> QEP
    Core --> NSF
    Core --> TWE
    Core --> ESG
    Core --> MRI
    Core --> SEC
    Core --> BPM
    
    %% Inter-module data flow connections
    QEP -.-> NSF
    NSF -.-> TWE
    TWE -.-> BPM
    ESG -.-> SEC
    MRI -.-> BPM
    
    %% Safety validation paths
    ESG --> Core
    ESG --> SEC
    
    %% User interaction points
    MRI --> Core
    BPM --> Core
    
    %% Platform connections
    Core --> Android
    Core --> iOS
    Core --> PC
    
    %% Styling for different module types
    classDef orchestrator fill:#1FB8CD,stroke:#13343B,stroke-width:3px,color:#fff
    classDef quantum fill:#DB4545,stroke:#B4413C,stroke-width:2px,color:#fff
    classDef hybrid fill:#2E8B57,stroke:#13343B,stroke-width:2px,color:#fff
    classDef temporal fill:#5D878F,stroke:#13343B,stroke-width:2px,color:#fff
    classDef safety fill:#D2BA4C,stroke:#964325,stroke-width:2px,color:#000
    classDef neural fill:#B4413C,stroke:#13343B,stroke-width:2px,color:#fff
    classDef evolution fill:#964325,stroke:#13343B,stroke-width:2px,color:#fff
    classDef prediction fill:#944454,stroke:#13343B,stroke-width:2px,color:#fff
    classDef platform fill:#B3E5EC,stroke:#5D878F,stroke-width:2px,color:#000
    
    %% Apply styles
    class Core orchestrator
    class QEP quantum
    class NSF hybrid
    class TWE temporal
    class ESG safety
    class MRI neural
    class SEC evolution
    class BPM prediction
    class Android,iOS,PC platform
"""

# Create the mermaid diagram with standard filename
png_path, svg_path = create_mermaid_diagram(diagram_code, 'chart.png', 'chart.svg', width=1400, height=1000)
print(f"Created diagram at: {png_path} and {svg_path}")