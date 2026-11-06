#include <iostream>
#include <vector>
#include <cassert>

long long computeFactorialProduct(const std::vector<int>& numbers) {
    if (numbers.empty()) {
        return 0;
    }

    long long product = 1;
    for (int num : numbers) {
        product *= num;
    }
    
    return product;
}

int main() {
    std::vector<int> inputs = {2, 3, 4, 5, 6};
    long long result = computeFactorialProduct(inputs);
    
    std::cout << "Product sum: " << result << std::endl;
    assert(result == 720);
    std::cout << "All tests passed for bug4_fixed.cpp!" << std::endl;
    return 0;
}
