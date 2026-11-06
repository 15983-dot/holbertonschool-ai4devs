#include <iostream>
#include <vector>
#include <numeric>

// Intended Behavior: Calculate exact average of integer scores.
// Issue Type: Misuse of Data Types & Integer Division Truncation.

double calculateAverage(const std::vector<int>& scores) {
    if (scores.empty()) return 0.0;
    
    int sum = std::accumulate(scores.begin(), scores.end(), 0);
    double average = sum / scores.size(); 
    return average;
}

int main() {
    std::vector<int> testScores = {85, 90, 92, 88, 95, 87};
    std::cout << "Average: " << calculateAverage(testScores) << std::endl;
    return 0;
}
