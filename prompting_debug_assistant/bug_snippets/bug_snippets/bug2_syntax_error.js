function calculateDiscount(price, discountRate) {
    // Intended Behavior: Calculate discounted price.
    // Issue Type: Syntax Error (missing closing parenthesis in if statement).
    if (price <= 0 || discountRate < 0 {
        return price;
    }

    let finalPrice = price - (price * (discountRate / 100));
    return finalPrice;
}

console.log(calculateDiscount(100, 15));
