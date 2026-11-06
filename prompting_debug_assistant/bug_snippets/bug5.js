function fetchUserData(userIds) {
    let users = [];

    for (var i = 0; i < userIds.length; i++) {
        // Simulating async network request call
        setTimeout(function() {
            users.push({
                id: userIds[i], // Bug: `var i` evaluates after loop termination (undefined index)
                status: "active"
            });
        }, 100);
    }

    // Bug: Returns empty array synchronously before async timeouts complete
    return users;
}

const ids = [101, 102, 103];
const result = fetchUserData(ids);
console.log("Fetched users:", result);
