// Gene Mutation Pathway Optimizer in C++
// Features: Trie for storage, Graph for mutation links, BFS for shortest path, Edit Distance for suggestions, File I/O, DOT Export

#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <queue>
#include <string>
#include <algorithm>
#include <climits>
using namespace std;

//---------------------------------- TRIE STRUCTURE (Gene Storage) ----------------------------------
struct TrieNode {
    unordered_map<char, TrieNode*> children;
    bool isEnd = false;
};

class Trie {
public:
    TrieNode* root;
    Trie() { root = new TrieNode(); }

    void insert(const string& word) {
        TrieNode* node = root;
        for (char ch : word) {
            if (!node->children[ch]) node->children[ch] = new TrieNode();
            node = node->children[ch];
        }
        node->isEnd = true;
    }

    bool search(const string& word) {
        TrieNode* node = root;
        for (char ch : word) {
            if (!node->children[ch]) return false;
            node = node->children[ch];
        }
        return node->isEnd;
    }
};

//---------------------------------- MUTATION GRAPH BUILDING ----------------------------------
unordered_map<string, vector<string>> adjList;

bool isOneMutation(const string& a, const string& b) {
    if (a.size() != b.size()) return false;
    int diff = 0;
    for (int i = 0; i < a.size(); ++i) {
        if (a[i] != b[i]) diff++;
        if (diff > 1) return false;
    }
    return diff == 1;
}

void buildGraph(const vector<string>& genes) {
    for (int i = 0; i < genes.size(); ++i) {
        for (int j = i + 1; j < genes.size(); ++j) {
            if (isOneMutation(genes[i], genes[j])) {
                adjList[genes[i]].push_back(genes[j]);
                adjList[genes[j]].push_back(genes[i]);
            }
        }
    }
}

//---------------------------------- BFS SHORTEST PATH SEARCH (FIXED) ----------------------------------
vector<string> bfs(const string& start, const string& end) {
    if (start == end) return {start};

    unordered_map<string, string> parent;
    unordered_set<string> visited;
    queue<string> q;
    q.push(start);
    visited.insert(start);

    while (!q.empty()) {
        string cur = q.front(); q.pop();
        if (cur == end) break;

        for (const string& next : adjList[cur]) {
            if (!visited.count(next)) {
                visited.insert(next);
                parent[next] = cur;
                q.push(next);
            }
        }
    }

    if (!visited.count(end)) return {};

    vector<string> path;
    for (string at = end; at != start; at = parent[at])
        path.push_back(at);
    path.push_back(start);
    reverse(path.begin(), path.end());
    return path;
}

//---------------------------------- EDIT DISTANCE (Suggestions) ----------------------------------
int editDist(const string& a, const string& b) {
    int m = a.size(), n = b.size();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1));

    for (int i = 0; i <= m; ++i) {
        for (int j = 0; j <= n; ++j) {
            if (i == 0) dp[i][j] = j;
            else if (j == 0) dp[i][j] = i;
            else if (a[i - 1] == b[j - 1]) dp[i][j] = dp[i - 1][j - 1];
            else dp[i][j] = 1 + min({ dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1] });
        }
    }
    return dp[m][n];
}

string suggestGene(const string& input, const vector<string>& genes) {
    int minDist = INT_MAX;
    string best = "";
    for (const string& gene : genes) {
        int dist = editDist(input, gene);
        if (dist < minDist) {
            minDist = dist;
            best = gene;
        }
    }
    return best;
}

//---------------------------------- EXPORT TO GRAPHVIZ DOT FILE (FIXED) ----------------------------------
void exportDot(const string& filename) {
    ofstream out(filename);
    out << "graph MutationGraph {\n";
    for (auto& entry : adjList) {
        const string& from = entry.first;
        const vector<string>& toList = entry.second;
        for (const string& to : toList) {
            if (from < to)
                out << "  \"" << from << "\" -- \"" << to << "\";\n";
        }
    }
    out << "}";
    out.close();
    cout << "\n[+] Graph exported to " << filename << "\n";
}

//---------------------------------- MAIN INTERFACE ----------------------------------
int main() {
    Trie geneTrie;
    vector<string> genes;
    string filename = "genes.txt";
    ifstream fin(filename);

    if (!fin.is_open()) {
        cerr << "\n[!] Error: Could not open file " << filename << endl;
        cerr << "Please ensure the file exists in the same directory as the program.\n";
        return 1;
    }

    string line;
    while (getline(fin, line)) {
        if (!line.empty() && line.back() == '\r') line.pop_back();
        if (!line.empty()) {
            genes.push_back(line);
            geneTrie.insert(line);
        }
    }
    fin.close();

    if (genes.empty()) {
        cerr << "\n[!] Error: No genes found in file. Please add gene sequences to 'genes.txt'\n";
        return 1;
    }

    cout << "Successfully loaded " << genes.size() << " genes from file\n";
    buildGraph(genes);

    string start, end;
    cout << "\nEnter start gene: "; cin >> start;
    cout << "Enter end gene: "; cin >> end;

    transform(start.begin(), start.end(), start.begin(), ::toupper);
    transform(end.begin(), end.end(), end.begin(), ::toupper);

    if (!geneTrie.search(start)) {
        cout << "\n[!] Start gene not found. Did you mean: " << suggestGene(start, genes) << "?\n";
        return 0;
    }
    if (!geneTrie.search(end)) {
        cout << "\n[!] End gene not found. Did you mean: " << suggestGene(end, genes) << "?\n";
        return 0;
    }

    vector<string> path = bfs(start, end);

    if (path.empty()) {
        cout << "\n[!] No valid mutation path from " << start << " to " << end << ".\n";
    } else {
        cout << "\n[✔] Shortest mutation path (" << path.size() - 1 << " mutations):\n";
        for (size_t i = 0; i < path.size(); ++i) {
            cout << path[i];
            if (i < path.size() - 1) cout << " -> ";
        }
        cout << "\n";
    }

    exportDot("mutation_graph.dot");
    cout << "\nProgram completed successfully.\n";
    return 0;
}
