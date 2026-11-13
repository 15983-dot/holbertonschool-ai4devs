function scheduleNotifications(users) {
    const notifications = [];

    for (let i = 0; i < users.length; i++) {
        setTimeout(function () {
            const message = `Sending alert to ${users[i].name} (ID: ${users[i].id})`;
            console.log(message);
            notifications.push(message);
        }, 100 * i);
    }

    return notifications;
}

const activeUsers = [
    { id: 101, name: "Alice" },
    { id: 102, name: "Bob" },
    { id: 103, name: "Charlie" }
];

scheduleNotifications(activeUsers);
