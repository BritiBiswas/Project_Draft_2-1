#include <iostream>
#include <unordered_map>
#include <vector>
#include <queue>
#include <fstream>
#include <algorithm>
using namespace std;

struct Gene {
    string sequence;
    int cost;
};

unordered_map<string, vector<pair<string, int>>> mutationMap;
vector<Gene> mutationHistory;

void loadHistory() {
    ifstream file("gene_history.txt");
    if (!file) return;
    Gene g;
    while (file >> g.sequence >> g.cost) {
        mutationHistory.push_back(g);
    }
    file.close();
}

void saveHistory() {
    ofstream file("gene_history.txt");
    for (auto &g : mutationHistory)
        file << g.sequence << " " << g.cost << endl;
    file.close();
}

vector<string> generateMutations(string gene) {
    vector<string> mutations;
    string bases = "ACGT";

    // Point mutation
    for (int i = 0; i < gene.length(); i++) {
        for (char base : bases) {
            if (gene[i] != base) {
                string mutated = gene;
                mutated[i] = base;
                mutations.push_back(mutated);
            }
        }
    }

    // Insertion
    for (int i = 0; i <= gene.length(); i++) {
        for (char base : bases) {
            string mutated = gene;
            mutated.insert(mutated.begin() + i, base);
            mutations.push_back(mutated);
        }
    }

    // Deletion
    for (int i = 0; i < gene.length(); i++) {
        string mutated = gene;
        mutated.erase(mutated.begin() + i);
        mutations.push_back(mutated);
    }

    return mutations;
}

int getMutationCost(string from, string to) {
    int cost = 0;
    if (from.length() != to.length()) cost += 2;
    for (int i = 0; i < min(from.length(), to.length()); i++)
        if (from[i] != to[i]) cost++;
    return cost;
}

void buildMutationMap(string gene) {
    vector<string> muts = generateMutations(gene);
    for (string m : muts) {
        int cost = getMutationCost(gene, m);
        mutationMap[gene].push_back({m, cost});
    }
}

vector<string> findBestMutationPath(string start, string target) {
    unordered_map<string, string> parent;
    unordered_map<string, bool> visited;
    queue<string> q;
    q.push(start);
    visited[start] = true;

    while (!q.empty()) {
        string curr = q.front(); q.pop();
        if (curr == target) break;

        buildMutationMap(curr);
        for (auto &mut : mutationMap[curr]) {
            string nextGene = mut.first;
            if (!visited[nextGene]) {
                visited[nextGene] = true;
                parent[nextGene] = curr;
                q.push(nextGene);
            }
        }
    }

    vector<string> path;
    if (!visited[target]) {
        cout << "\n❌ No mutation path found.\n";
        return path;
    }

    for (string at = target; at != start; at = parent[at])
        path.push_back(at);
    path.push_back(start);
    reverse(path.begin(), path.end());
    return path;
}

void optimizeMutation() {
    string start, target;
    cout << "Enter Start Gene: ";
    cin >> start;
    cout << "Enter Target Gene: ";
    cin >> target;

    vector<string> path = findBestMutationPath(start, target);
    if (!path.empty()) {
        cout << "\n✅ Optimized Mutation Path:\n";
        int totalCost = 0;
        for (int i = 0; i < path.size(); i++) {
            cout << path[i];
            if (i < path.size() - 1) {
                int cost = getMutationCost(path[i], path[i+1]);
                cout << " --(" << cost << ")--> ";
                totalCost += cost;
            }
        }
        cout << "\nTotal Mutation Cost: " << totalCost << endl;

        mutationHistory.push_back({target, totalCost});
        saveHistory();
    }
}

void showHistory() {
    cout << "\n📜 Mutation History:\n";
    for (auto &g : mutationHistory) {
        cout << "Sequence: " << g.sequence << " | Cost: " << g.cost << endl;
    }
}

void showMenu() {
    cout << "\n==============================\n";
    cout << "🔬 Gene Mutation Optimizer 🔬\n";
    cout << "==============================\n";
    cout << "1. Optimize Gene Mutation\n";
    cout << "2. View Mutation History\n";
    cout << "3. Exit\n";
    cout << "==============================\n";
    cout << "Choose an option: ";
}

int main() {
    loadHistory();
    while (true) {
        showMenu();
        int choice;
        cin >> choice;
        switch (choice) {
            case 1: optimizeMutation(); break;
            case 2: showHistory(); break;
            case 3: cout << "Goodbye!\n"; return 0;
            default: cout << "Invalid option!\n";
        }
    }
}
