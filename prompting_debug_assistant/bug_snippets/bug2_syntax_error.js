function calculateAverage(numbers) {
    if (!numbers || numbers.length === 0) {
        return 0;
    }

    let sum = 0;
    for (let i = 0; i < numbers.length; i++) {
        sum += numbers[i]
    }

    // Bug: Missing closing parenthesis on console statement & syntax error in object mapping
    console.log("Calculated total sum:", sum;
    
    return sum / numbers.length;
}

const scores = [88, 92, 79, 95];
console.log("Average Score:", calculateAverage(scores));
