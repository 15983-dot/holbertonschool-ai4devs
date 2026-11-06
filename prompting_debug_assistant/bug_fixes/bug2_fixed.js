function calculateAverage(numbers) {
    if (!numbers || numbers.length === 0) {
        return 0;
    }

    let sum = 0;
    for (let i = 0; i < numbers.length; i++) {
        sum += numbers[i];
    }

    console.log("Calculated total sum:", sum);
    return sum / numbers.length;
}

// Internal verification execution
const scores = [88, 92, 79, 95];
console.log("Average Score:", calculateAverage(scores));
