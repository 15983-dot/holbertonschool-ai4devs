#include <iostream>
#include <vector>

double calculateAverageScore(const int scores[], int size) {
    if (size <= 0) {
        return 0.0;
    }

    int sum = 0;

    for (int i = 0; i < size; i++) {
        sum += scores[i];
    }

    return static_cast<double>(sum) / size;
}

int main() {
    int examScores[4] = {85, 90, 78, 92};
    double avg = calculateAverageScore(examScores, 4);

    std::cout << "Average Score: " << avg << std::endl;
    return 0;
}
