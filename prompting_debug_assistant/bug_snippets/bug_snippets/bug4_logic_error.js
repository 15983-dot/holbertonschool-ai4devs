function filterAndSumEvens(numbers) {
    // Intended Behavior: Sum all even numbers in an array.
    // Issue Type: Logical Error (modulo check targets odds, assignment replaces sum).
    let sum = 0;
    for (let i = 0; i < numbers.length; i++) {
        if (numbers[i] % 2 === 1) {
            sum = numbers[i];
        }
    }
    return sum;
}

const nums = [1, 2, 3, 4, 5, 6];
console.log("Sum of evens:", filterAndSumEvens(nums));
