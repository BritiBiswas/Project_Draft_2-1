import tkinter as tk
from tkinter import ttk, messagebox
import random
import math

class GeneMutationSimulator:
    NUCLEOTIDES = ['A', 'T', 'C', 'G']
    AMINO_ACIDS = {
        'ATA': 'I', 'ATC': 'I', 'ATT': 'I', 'ATG': 'M',
        'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACT': 'T',
        'AAC': 'N', 'AAT': 'N', 'AAA': 'K', 'AAG': 'K',
        'AGC': 'S', 'AGT': 'S', 'AGA': 'R', 'AGG': 'R',
        'CTA': 'L', 'CTC': 'L', 'CTG': 'L', 'CTT': 'L',
        'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCT': 'P',
        'CAC': 'H', 'CAT': 'H', 'CAA': 'Q', 'CAG': 'Q',
        'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGT': 'R',
        'GTA': 'V', 'GTC': 'V', 'GTG': 'V', 'GTT': 'V',
        'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCT': 'A',
        'GAC': 'D', 'GAT': 'D', 'GAA': 'E', 'GAG': 'E',
        'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGT': 'G',
        'TCA': 'S', 'TCC': 'S', 'TCG': 'S', 'TCT': 'S',
        'TTC': 'F', 'TTT': 'F', 'TTA': 'L', 'TTG': 'L',
        'TAC': 'Y', 'TAT': 'Y', 'TAA': '*', 'TAG': '*',
        'TGC': 'C', 'TGT': 'C', 'TGA': '*', 'TGG': 'W'
    }
    
    def __init__(self, target_sequence):
        self.target = target_sequence.upper()
        self.current = self._generate_random_sequence()
        self.generation = 0
        self.fitness_history = []
        self.mutation_path = []
        
    def _generate_random_sequence(self):
        return ''.join(random.choice(self.NUCLEOTIDES) for _ in range(len(self.target)))
    
    def calculate_fitness(self):
        """Calculate how similar current sequence is to target"""
        matches = sum(1 for a, b in zip(self.current, self.target) if a == b)
        return matches / len(self.target) * 100
    
    def translate_to_protein(self, sequence):
        """Translate DNA sequence to amino acid sequence"""
        protein = ""
        for i in range(0, len(sequence), 3):
            codon = sequence[i:i+3]
            if len(codon) == 3:
                protein += self.AMINO_ACIDS.get(codon, 'X')  # X for invalid codons
        return protein
    
    def mutate(self, mutation_rate=0.1):
        """Apply random mutations to the sequence"""
        new_sequence = []
        for i, nucleotide in enumerate(self.current):
            if random.random() < mutation_rate:
                # Slightly increase chance of mutating to target nucleotide
                if random.random() < 0.3 and self.target[i] != nucleotide:
                    new_sequence.append(self.target[i])
                else:
                    choices = [n for n in self.NUCLEOTIDES if n != nucleotide]
                    new_sequence.append(random.choice(choices))
            else:
                new_sequence.append(nucleotide)
                
        self.current = ''.join(new_sequence)
        self.generation += 1
        fitness = self.calculate_fitness()
        self.fitness_history.append(fitness)
        self.mutation_path.append(self.current)
        return fitness
    
    def reset(self, new_target=None):
        """Reset the simulation with a new target"""
        if new_target:
            self.target = new_target.upper()
        self.current = self._generate_random_sequence()
        self.generation = 0
        self.fitness_history = []
        self.mutation_path = []

class MutationSimulatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gene Mutation Simulator")
        self.geometry("1000x700")
        self.configure(bg="#2c3e50")
        
        # Initialize simulator
        self.simulator = GeneMutationSimulator("ATGCCCGAGTAATAG")  # Start with valid sequence
        
        # Create colorful theme
        self.colors = {
            'A': '#4CAF50',  # Green
            'T': '#E91E63',  # Pink
            'C': '#2196F3',  # Blue
            'G': '#FFC107',  # Yellow
            'background': '#2c3e50',
            'panel': '#34495e',
            'text': '#ecf0f1',
            'highlight': '#3498db',
            'match': '#4CAF50',  # Green for matches
            'mismatch': '#F44336',  # Red for mismatches
            'start': '#99FF99',  # Light green for start codon
            'stop': '#FF9999',   # Light red for stop codon
            'invalid': '#FF99FF' # Light magenta for invalid
        }
        
        # Create widgets
        self.create_widgets()
        self.update_display()
    
    def create_widgets(self):
        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background=self.colors['background'])
        style.configure('TLabel', background=self.colors['background'], foreground=self.colors['text'])
        style.configure('TButton', background=self.colors['highlight'], foreground='black', font=('Arial', 10, 'bold'))
        style.configure('Header.TLabel', background=self.colors['background'], 
                        foreground=self.colors['highlight'], font=('Arial', 16, 'bold'))
        style.configure('Panel.TFrame', background=self.colors['panel'], relief='raised', borderwidth=2)
        style.configure('Panel.TLabelframe', background=self.colors['panel'], foreground=self.colors['text'])
        style.configure('Panel.TLabelframe.Label', background=self.colors['panel'], foreground=self.colors['highlight'])
        
        # Main container
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = ttk.Frame(main_frame)
        header.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header, text="Gene Mutation Simulator", style='Header.TLabel').pack(side=tk.LEFT)
        ttk.Label(header, text="Explore DNA Mutations & Evolution", font=('Arial', 12)).pack(side=tk.LEFT, padx=10)
        
        # Create notebook for multiple views
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.simulation_tab = ttk.Frame(self.notebook, padding=10)
        self.analysis_tab = ttk.Frame(self.notebook, padding=10)
        self.education_tab = ttk.Frame(self.notebook, padding=10)
        
        self.notebook.add(self.simulation_tab, text="Simulation")
        self.notebook.add(self.analysis_tab, text="Analysis")
        self.notebook.add(self.education_tab, text="Genetics Concepts")
        
        # Build each tab
        self.build_simulation_tab()
        self.build_analysis_tab()
        self.build_education_tab()
    
    def build_simulation_tab(self):
        """Build the main simulation tab"""
        # Create two main panels
        left_panel = ttk.Frame(self.simulation_tab, style='Panel.TFrame')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_panel = ttk.Frame(self.simulation_tab, style='Panel.TFrame')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Left panel - DNA visualization
        dna_frame = ttk.LabelFrame(left_panel, text="DNA Sequence Visualization", style='Panel.TLabelframe')
        dna_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Target sequence
        ttk.Label(dna_frame, text="Target Sequence:", font=('Arial', 10, 'bold')).pack(anchor='w', padx=10, pady=(10, 5))
        self.target_display = ttk.Frame(dna_frame, height=40)
        self.target_display.pack(fill=tk.X, padx=10, pady=5)
        
        # Current sequence
        ttk.Label(dna_frame, text="Current Sequence:", font=('Arial', 10, 'bold')).pack(anchor='w', padx=10, pady=(10, 5))
        self.current_display = ttk.Frame(dna_frame, height=40)
        self.current_display.pack(fill=tk.X, padx=10, pady=5)
        
        # Match visualization
        ttk.Label(dna_frame, text="Sequence Comparison:", font=('Arial', 10, 'bold')).pack(anchor='w', padx=10, pady=(10, 5))
        self.match_canvas = tk.Canvas(dna_frame, height=60, bg='white')
        self.match_canvas.pack(fill=tk.X, padx=10, pady=5)
        
        # Protein translation
        ttk.Label(dna_frame, text="Protein Translation:", font=('Arial', 10, 'bold')).pack(anchor='w', padx=10, pady=(10, 5))
        protein_frame = ttk.Frame(dna_frame)
        protein_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(protein_frame, text="Target Protein:").pack(side=tk.LEFT, padx=(0, 10))
        self.target_protein_frame = ttk.Frame(protein_frame)
        self.target_protein_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(protein_frame, text="Current Protein:").pack(side=tk.LEFT, padx=(20, 10))
        self.current_protein_frame = ttk.Frame(protein_frame)
        self.current_protein_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Right panel - Controls and info
        control_frame = ttk.LabelFrame(right_panel, text="Simulation Controls", style='Panel.TLabelframe')
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Target sequence input
        ttk.Label(control_frame, text="Target Sequence:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.target_entry = ttk.Entry(control_frame, width=30, font=('Courier', 10))
        self.target_entry.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
        self.target_entry.insert(0, self.simulator.target)
        
        # Mutation rate
        ttk.Label(control_frame, text="Mutation Rate:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.mutation_rate = tk.DoubleVar(value=0.1)
        mutation_scale = ttk.Scale(control_frame, from_=0.01, to=0.5, variable=self.mutation_rate, 
                                  orient=tk.HORIZONTAL, length=200)
        mutation_scale.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        self.rate_label = ttk.Label(control_frame, text="0.10")
        self.rate_label.grid(row=1, column=2, padx=5)
        
        # Buttons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        ttk.Button(btn_frame, text="Mutate", command=self.run_mutation).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Auto Run (5 gens)", command=self.auto_run).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Reset", command=self.reset_simulation).pack(side=tk.LEFT, padx=5)
        
        # Stats
        stats_frame = ttk.LabelFrame(right_panel, text="Simulation Stats", style='Panel.TLabelframe')
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.generation_var = tk.StringVar(value="Generation: 0")
        ttk.Label(stats_frame, textvariable=self.generation_var, font=('Arial', 10)).pack(anchor='w', padx=10, pady=5)
        
        self.fitness_var = tk.StringVar(value="Fitness: 0.0%")
        ttk.Label(stats_frame, textvariable=self.fitness_var, font=('Arial', 10)).pack(anchor='w', padx=10, pady=5)
        
        # History panel
        history_frame = ttk.LabelFrame(right_panel, text="Mutation History", style='Panel.TLabelframe')
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        self.history_text = tk.Text(history_frame, height=8, wrap=tk.WORD, bg=self.colors['panel'], 
                                  fg=self.colors['text'], font=('Courier', 9))
        scrollbar = ttk.Scrollbar(history_frame, command=self.history_text.yview)
        self.history_text.config(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.history_text.insert(tk.END, "Mutation history will appear here...")
        self.history_text.config(state=tk.DISABLED)
        
        # Bind mutation rate changes
        self.mutation_rate.trace_add("write", self.update_rate_label)
    
    def build_analysis_tab(self):
        """Build the analysis tab"""
        # Create two panels
        left_panel = ttk.Frame(self.analysis_tab, style='Panel.TFrame')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_panel = ttk.Frame(self.analysis_tab, style='Panel.TFrame')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Fitness graph
        fitness_frame = ttk.LabelFrame(left_panel, text="Fitness Over Generations", style='Panel.TLabelframe')
        fitness_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.fitness_canvas = tk.Canvas(fitness_frame, bg='white')
        self.fitness_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.fitness_canvas.create_text(200, 100, text="Run simulation to see fitness graph", fill="gray")
        
        # Mutation details
        details_frame = ttk.LabelFrame(left_panel, text="Mutation Details", style='Panel.TLabelframe')
        details_frame.pack(fill=tk.BOTH, expand=True)
        
        self.details_text = tk.Text(details_frame, wrap=tk.WORD, bg=self.colors['panel'], 
                                  fg=self.colors['text'], font=('Courier', 9))
        scrollbar = ttk.Scrollbar(details_frame, command=self.details_text.yview)
        self.details_text.config(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.details_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.details_text.insert(tk.END, "Detailed mutation information will appear here...")
        self.details_text.config(state=tk.DISABLED)
        
        # DNA properties
        properties_frame = ttk.LabelFrame(right_panel, text="DNA Properties", style='Panel.TLabelframe')
        properties_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a canvas for DNA visualization
        self.dna_canvas = tk.Canvas(properties_frame, bg='white', height=200)
        self.dna_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.dna_canvas.create_text(150, 100, text="DNA visualization will appear here", fill="gray")
        
        # Nucleotide frequency
        freq_frame = ttk.LabelFrame(right_panel, text="Nucleotide Frequency", style='Panel.TLabelframe')
        freq_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.freq_canvas = tk.Canvas(freq_frame, bg='white', height=150)
        self.freq_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def build_education_tab(self):
        """Build the genetics concepts education tab"""
        # Create a scrolled text widget
        frame = ttk.Frame(self.education_tab, style='Panel.TFrame')
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a canvas for a scrollable frame
        canvas = tk.Canvas(frame, bg=self.colors['panel'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack everything
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add educational content
        content = [
            ("DNA Basics", [
                "• DNA (Deoxyribonucleic Acid) carries genetic instructions",
                "• Made of nucleotides: Adenine (A), Thymine (T), Cytosine (C), Guanine (G)",
                "• Base pairing: A-T and C-G",
                "• DNA sequence determines traits and protein synthesis"
            ]),
            ("Gene Mutations", [
                "• Mutations are changes in DNA sequence",
                "• Occur naturally during DNA replication",
                "• Types:",
                "  - Point mutations: Single nucleotide changes",
                "  - Insertions/Deletions: Add/Remove nucleotides",
                "• Effects: Beneficial, neutral, or harmful"
            ]),
            ("Protein Synthesis", [
                "• Central Dogma: DNA → RNA → Protein",
                "• Codons (3-nucleotide groups) code for amino acids",
                "• 20 amino acids form all proteins",
                "• Start codon: ATG (Methionine)",
                "• Stop codons: TAA, TAG, TGA"
            ]),
            ("Evolution & Natural Selection", [
                "• Mutations create genetic diversity",
                "• Natural selection favors beneficial mutations",
                "• Fitness: Measure of adaptation to environment",
                "• This simulator demonstrates evolutionary principles"
            ]),
            ("Simulation Concepts", [
                "• Fitness: Percentage match to target DNA",
                "• Mutation Rate: Probability of nucleotide change",
                "• Generations: Number of mutation cycles",
                "• Protein Translation: Shows biological impact"
            ])
        ]
        
        for title, items in content:
            ttk.Label(scrollable_frame, text=title, font=('Arial', 14, 'bold'), 
                     foreground=self.colors['highlight']).pack(anchor='w', padx=20, pady=(20, 5))
            
            for item in items:
                ttk.Label(scrollable_frame, text=item, font=('Arial', 11), wraplength=800).pack(anchor='w', padx=40, pady=2)
    
    def update_rate_label(self, *args):
        """Update mutation rate label"""
        self.rate_label.config(text=f"{self.mutation_rate.get():.2f}")
    
    def update_display(self):
        # Update sequence displays
        self.display_sequence(self.target_display, self.simulator.target)
        self.display_sequence(self.current_display, self.simulator.current)
        
        # Update match visualization
        self.update_match_visualization()
        
        # Update protein translation
        target_protein = self.simulator.translate_to_protein(self.simulator.target)
        current_protein = self.simulator.translate_to_protein(self.simulator.current)
        self.display_protein(self.target_protein_frame, target_protein)
        self.display_protein(self.current_protein_frame, current_protein)
        
        # Update stats
        fitness = self.simulator.calculate_fitness()
        self.generation_var.set(f"Generation: {self.simulator.generation}")
        self.fitness_var.set(f"Fitness: {fitness:.1f}%")
        
        # Update history
        self.update_history()
        
        # Update analysis tab
        self.update_fitness_graph()
        self.update_dna_visualization()
        self.update_frequency_chart()
        self.update_mutation_details()
    
    def display_sequence(self, parent, sequence):
        """Display DNA sequence with colored nucleotides"""
        # Clear previous display
        for widget in parent.winfo_children():
            widget.destroy()
        
        # Create a label for each nucleotide
        for i, nucleotide in enumerate(sequence):
            color = self.colors[nucleotide]
            label = tk.Label(parent, text=nucleotide, font=('Courier', 14, 'bold'), 
                           bg=color, fg='black', width=2, relief='raised', padx=2)
            label.pack(side=tk.LEFT, padx=1)
    
    def display_protein(self, parent, sequence):
        """Display protein sequence with color coding"""
        # Clear previous display
        for widget in parent.winfo_children():
            widget.destroy()
        
        # Create a label for each amino acid
        for aa in sequence:
            if aa == '*':  # Stop codon
                color = self.colors['stop']
            elif aa == 'M':  # Start codon
                color = self.colors['start']
            elif aa == 'X':  # Invalid codon
                color = self.colors['invalid']
            else:  # Regular amino acid
                color = 'white'
            
            label = tk.Label(parent, text=aa, font=('Courier', 10, 'bold'), 
                           bg=color, fg='black', relief='sunken', padx=2)
            label.pack(side=tk.LEFT, padx=1)
    
    def update_match_visualization(self):
        """Update the sequence comparison visualization"""
        self.match_canvas.delete("all")
        width = self.match_canvas.winfo_width()
        if width < 10 or len(self.simulator.target) == 0:
            return
            
        cell_width = width / len(self.simulator.target)
        
        for i, (curr, target) in enumerate(zip(self.simulator.current, self.simulator.target)):
            x0 = i * cell_width
            x1 = (i+1) * cell_width
            
            # Draw match indicator
            if curr == target:
                self.match_canvas.create_rectangle(x0, 0, x1, 30, fill=self.colors['match'], outline="")
            else:
                self.match_canvas.create_rectangle(x0, 0, x1, 30, fill=self.colors['mismatch'], outline="")
            
            # Draw nucleotide
            self.match_canvas.create_text((x0+x1)/2, 15, text=curr, 
                                        font=('Courier', 12, 'bold'), fill="white")
    
    def update_fitness_graph(self):
        """Update the fitness graph on the analysis tab - FIXED Y-AXIS LABEL"""
        self.fitness_canvas.delete("all")
        width = self.fitness_canvas.winfo_width()
        height = self.fitness_canvas.winfo_height()
        
        if width < 50 or height < 50 or len(self.simulator.fitness_history) < 2:
            return
        
        # Calculate graph area dimensions
        graph_height = height - 80  # From y=30 to y=height-50
        graph_width = width - 70    # From x=50 to x=width-20
        
        # Draw axes
        self.fitness_canvas.create_line(50, height-50, width-20, height-50, width=2)  # X-axis
        self.fitness_canvas.create_line(50, 30, 50, height-50, width=2)  # Y-axis (fixed to extend to top)
        
        # Add labels - FIXED Y-AXIS POSITION
        self.fitness_canvas.create_text(25, height/2, text="Fitness %", angle=90, anchor="center")  # Centered vertically
        self.fitness_canvas.create_text(width//2, height-25, text="Generation")
        
        # Add scale markers on Y-axis
        for percent in [0, 25, 50, 75, 100]:
            y_pos = height - 50 - (percent/100) * graph_height
            self.fitness_canvas.create_line(45, y_pos, 55, y_pos, width=1)
            self.fitness_canvas.create_text(40, y_pos, text=f"{percent}%", anchor="e")
        
        # Draw data points
        max_fitness = max(self.simulator.fitness_history + [100])
        x_step = graph_width / max(1, len(self.simulator.fitness_history)-1)
        y_scale = graph_height / max_fitness
        
        points = []
        for i, fitness in enumerate(self.simulator.fitness_history):
            x = 50 + i * x_step
            y = height - 50 - fitness * y_scale
            points.append((x, y))
            self.fitness_canvas.create_oval(x-3, y-3, x+3, y+3, fill=self.colors['highlight'])
        
        # Draw line connecting points
        if len(points) > 1:
            self.fitness_canvas.create_line(points, fill=self.colors['highlight'], width=2)
    
    def update_history(self):
        """Update mutation history display"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        
        if not self.simulator.mutation_path:
            self.history_text.insert(tk.END, "No mutations recorded yet")
        else:
            # Only show last 10 generations to avoid clutter
            start_index = max(0, len(self.simulator.mutation_path) - 10)
            for i in range(start_index, len(self.simulator.mutation_path)):
                seq = self.simulator.mutation_path[i]
                fitness = self.simulator.fitness_history[i] if i < len(self.simulator.fitness_history) else 0
                self.history_text.insert(tk.END, f"Gen {i+1}: {seq} (Fitness: {fitness:.1f}%)\n")
        
        self.history_text.config(state=tk.DISABLED)
        self.history_text.see(tk.END)
    
    def update_mutation_details(self):
        """Update mutation details in analysis tab"""
        self.details_text.config(state=tk.NORMAL)
        self.details_text.delete(1.0, tk.END)
        
        if len(self.simulator.mutation_path) < 2:
            self.details_text.insert(tk.END, "Perform mutations to see details")
            self.details_text.config(state=tk.DISABLED)
            return
            
        # Compare current and previous sequences
        current_seq = self.simulator.current
        prev_seq = self.simulator.mutation_path[-2] if len(self.simulator.mutation_path) > 1 else ""
        
        if not prev_seq:
            self.details_text.insert(tk.END, "No previous sequence to compare")
            self.details_text.config(state=tk.DISABLED)
            return
            
        # Find mutations
        mutations = []
        for i, (curr, prev) in enumerate(zip(current_seq, prev_seq)):
            if curr != prev:
                mutations.append(f"Position {i+1}: {prev} → {curr}")
                
        # Find protein changes
        prev_protein = self.simulator.translate_to_protein(prev_seq)
        curr_protein = self.simulator.translate_to_protein(current_seq)
        protein_changes = []
        
        for i, (prev_aa, curr_aa) in enumerate(zip(prev_protein, curr_protein)):
            if prev_aa != curr_aa:
                protein_changes.append(f"Amino acid {i+1}: {prev_aa} → {curr_aa}")
                
        # Display results
        if mutations:
            self.details_text.insert(tk.END, "DNA Mutations:\n")
            for mut in mutations:
                self.details_text.insert(tk.END, f"• {mut}\n")
                
            self.details_text.insert(tk.END, "\nProtein Changes:\n")
            for change in protein_changes:
                self.details_text.insert(tk.END, f"• {change}\n")
        else:
            self.details_text.insert(tk.END, "No mutations in this generation")
            
        self.details_text.config(state=tk.DISABLED)
    
    def update_dna_visualization(self):
        """Create a DNA strand visualization"""
        self.dna_canvas.delete("all")
        width = self.dna_canvas.winfo_width()
        height = self.dna_canvas.winfo_height()
        
        if width < 50 or height < 50:
            return
        
        # Draw DNA strands
        center_y = height // 2
        self.dna_canvas.create_line(50, center_y, width-50, center_y, fill="#7f8c8d", width=2)
        
        # Draw base pairs
        num_pairs = min(20, len(self.simulator.current))  # Limit to 20 pairs for visibility
        x_step = (width - 100) / (num_pairs - 1) if num_pairs > 1 else 0
        
        for i in range(num_pairs):
            x = 50 + i * x_step
            top_nt = self.simulator.current[i] if i < len(self.simulator.current) else "A"
            bottom_nt = self.get_complement(top_nt)
            
            # Draw connection lines
            self.dna_canvas.create_line(x, center_y - 30, x, center_y + 30, fill="#95a5a6", width=1)
            
            # Draw nucleotides
            self.draw_nucleotide(self.dna_canvas, x, center_y - 40, top_nt)
            self.draw_nucleotide(self.dna_canvas, x, center_y + 40, bottom_nt)
    
    def draw_nucleotide(self, canvas, x, y, nucleotide):
        """Draw a nucleotide at the specified position"""
        color = self.colors[nucleotide]
        canvas.create_oval(x-15, y-15, x+15, y+15, fill=color, outline="black")
        canvas.create_text(x, y, text=nucleotide, font=('Arial', 12, 'bold'))
    
    def get_complement(self, nucleotide):
        """Get complementary nucleotide"""
        complements = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        return complements.get(nucleotide, '?')
    
    def update_frequency_chart(self):
        """Update nucleotide frequency chart"""
        self.freq_canvas.delete("all")
        width = self.freq_canvas.winfo_width()
        height = self.freq_canvas.winfo_height()
        
        if width < 50 or height < 50 or not self.simulator.current:
            return
        
        # Count nucleotides
        counts = {'A': 0, 'T': 0, 'C': 0, 'G': 0}
        for nt in self.simulator.current:
            if nt in counts:
                counts[nt] += 1
        
        total = sum(counts.values())
        if total == 0:
            return
        
        # Normalize counts to percentages
        percents = {nt: count/total * 100 for nt, count in counts.items()}
        
        # Draw bars
        bar_width = 50
        spacing = 20
        x_pos = 50
        
        for nt in ['A', 'T', 'C', 'G']:
            bar_height = (percents[nt] / 100) * (height - 70)
            y_pos = height - 50 - bar_height
            
            # Draw bar
            self.freq_canvas.create_rectangle(
                x_pos, y_pos, 
                x_pos + bar_width, height - 50,
                fill=self.colors[nt], outline="black"
            )
            
            # Add label
            self.freq_canvas.create_text(
                x_pos + bar_width/2, height - 30, 
                text=f"{nt}\n{percents[nt]:.1f}%", 
                font=('Arial', 9), justify='center'
            )
            
            x_pos += bar_width + spacing
    
    def run_mutation(self):
        """Apply one mutation"""
        mutation_rate = self.mutation_rate.get()
        self.simulator.mutate(mutation_rate)
        self.update_display()
    
    def auto_run(self):
        """Run multiple mutations at once"""
        mutation_rate = self.mutation_rate.get()
        for _ in range(5):
            self.simulator.mutate(mutation_rate)
            self.update_display()
            self.update()  # Update the GUI
    
    def reset_simulation(self):
        """Reset the simulation with a new target"""
        target = self.target_entry.get().upper()
        if not all(n in GeneMutationSimulator.NUCLEOTIDES for n in target):
            messagebox.showerror("Invalid Sequence", 
                                "Sequence must contain only A, T, C, G nucleotides")
            return
            
        if len(target) < 6:
            messagebox.showerror("Invalid Sequence", 
                                "Sequence must be at least 6 nucleotides long")
            return
            
        self.simulator.reset(target)
        self.update_display()

if __name__ == "__main__":
    app = MutationSimulatorApp()
    app.mainloop()
