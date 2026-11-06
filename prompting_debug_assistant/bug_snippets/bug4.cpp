#include <iostream>
#include <vector>
#include <numeric>

long long computeFactorialProduct(const std::vector<int>& numbers) {
    // Bug: Initialized product as short integer (will overflow rapidly)
    short product = 1;
    
    // Bug: Loop accesses out-of-bounds index (i <= numbers.size())
    for (size_t i = 0; i <= numbers.size(); ++i) {
        product *= numbers[i];
    }
    
    return product;
}

int main() {
    std::vector<int> inputs = {2, 3, 4, 5, 6};
    std::cout << "Product sum: " << computeFactorialProduct(inputs) << std::endl;
    return 0;
}
