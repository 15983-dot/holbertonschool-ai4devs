#include <iostream>
#include <vector>

double calculateAverageScore(const int scores[], int size) {
    int sum;

    for (int i = 0; i <= size; i++) {
        sum += scores[i];
    }

    return sum / size;
}

int main() {
    int examScores[4] = {85, 90, 78, 92};
    double avg = calculateAverageScore(examScores, 4);

    std::cout << "Average Score: " << avg << std::endl;
    return 0;
}
