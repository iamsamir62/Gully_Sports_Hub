// your_template.js

// ... (existing WebSocket connection code)

// Function to create a match request dropdown
function createMatchRequestDropdown(matchRequestData) {
    const dropdown = document.createElement('div');
    dropdown.classList.add('match-request-dropdown');

    // Display team name and sender username
    const message = document.createElement('p');
    message.textContent = `${matchRequestData.sender_username} has requested a match with your team!`;
    dropdown.appendChild(message);

    // Buttons for accept, reject, and pending
    const acceptButton = document.createElement('button');
    acceptButton.textContent = 'Accept';
    acceptButton.addEventListener('click', () => onAcceptMatchClicked(matchRequestData.team_id));
    dropdown.appendChild(acceptButton);

    const rejectButton = document.createElement('button');
    rejectButton.textContent = 'Reject';
    rejectButton.addEventListener('click', () => onRejectMatchClicked(matchRequestData.team_id));
    dropdown.appendChild(rejectButton);

    const pendingButton = document.createElement('button');
    pendingButton.textContent = 'Pending';
    pendingButton.addEventListener('click', () => onPendingMatchClicked(matchRequestData.team_id));
    dropdown.appendChild(pendingButton);

    return dropdown;
}

// Function to handle the accept button click
function onAcceptMatchClicked(teamId) {
    // Implement logic for accepting the match request
    console.log(`Accepted match request for team ${teamId}`);
    // Update UI or perform other actions as needed
}

// Function to handle the reject button click
function onRejectMatchClicked(teamId) {
    // Implement logic for rejecting the match request
    console.log(`Rejected match request for team ${teamId}`);
    // Update UI or perform other actions as needed
}

// Function to handle the pending button click
function onPendingMatchClicked(teamId) {
    // Implement logic for marking the match request as pending
    console.log(`Marked match request as pending for team ${teamId}`);
    // Update UI or perform other actions as needed
}

// Display the notification dropdown when the bell icon is clicked
document.getElementById('notification-dropdown').addEventListener('click', function() {
    const dropdownContent = document.getElementById('notification-dropdown-content');
    dropdownContent.style.display = (dropdownContent.style.display === 'none') ? 'block' : 'none';
});
