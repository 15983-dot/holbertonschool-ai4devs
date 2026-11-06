async function fetchUserData(userIds) {
    if (!userIds || userIds.length === 0) {
        return [];
    }

    const fetchPromises = userIds.map(id => {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve({
                    id: id,
                    status: "active"
                });
            }, 100);
        });
    });

    return await Promise.all(fetchPromises);
}

// Async self-test wrapper
(async () => {
    const ids = [101, 102, 103];
    const result = await fetchUserData(ids);
    console.log("Fetched users:", result);
    
    if (result.length === 3 && result[0].id === 101 && result[2].id === 103) {
        console.log("All tests passed for bug5_fixed.js!");
    } else {
        console.error("Test failed for bug5_fixed.js");
    }
})();
