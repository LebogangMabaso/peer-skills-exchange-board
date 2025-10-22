function splitSkills(skillsString) {
    if (!skillsString) return [];
    var skills = skillsString.split(',');
    var result = [];
    for (var i = 0; i < skills.length; i++) {
        var skill = skills[i].trim();
        if (skill) {
            result.push(skill);
        }
    }
    return result;
}

document.getElementById('addUserForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const skillsOffered = splitSkills(document.getElementById('skillsOffered').value);
    const skillsNeeded = splitSkills(document.getElementById('skillsNeeded').value);
    
    fetch('/api/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: name,
            email: email,
            skills_offered: skillsOffered,
            skills_needed: skillsNeeded
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('addUserMessage').innerHTML = '<p class="error">' + data.error + '</p>';
        } else {
            document.getElementById('addUserMessage').innerHTML = '<p class="success">User added successfully!</p>';
            document.getElementById('addUserForm').reset();
            loadUsers();
        }
    })
    .catch(error => {
        document.getElementById('addUserMessage').innerHTML = '<p class="error">Error: ' + error + '</p>';
    });
});

function loadUsers() {
    fetch('/api/users')
        .then(response => response.json())
        .then(users => {
            let html = '';
            for (let i = 0; i < users.length; i++) {
                const user = users[i];
                html += '<div class="user-card">';
                html += '<strong>ID: ' + user.user_id + ' - ' + user.name + '</strong> (' + user.email + ')<br>';
                if (user.skills_offered && user.skills_offered.length > 0) {
                    html += 'Offers: ' + user.skills_offered.join(', ') + '<br>';
                }
                if (user.skills_needed && user.skills_needed.length > 0) {
                    html += 'Needs: ' + user.skills_needed.join(', ');
                }
                html += '</div>';
            }
            document.getElementById('usersList').innerHTML = html;
        })
        .catch(error => {
            document.getElementById('usersList').innerHTML = '<p class="error">Error loading users</p>';
        });
}

function findMatches() {
    const userId = document.getElementById('matchUserId').value;
    if (!userId) {
        alert('Please enter a user ID');
        return;
    }

    fetch('/api/users/' + userId + '/matches')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('matchesList').innerHTML = '<p class="error">' + data.error + '</p>';
                return;
            }
            
            let html = '';
            if (data.length === 0) {
                html = '<p>No matches found</p>';
            } else {
                for (let i = 0; i < data.length; i++) {
                    const match = data[i];
                    html += '<div class="user-card">';
                    html += '<strong>' + match.user.name + '</strong> - Score: ' + match.score.toFixed(2) + '<br>';
                    if (match.can_learn.length > 0) {
                        html += 'You can learn: ' + match.can_learn.join(', ') + '<br>';
                    }
                    if (match.can_teach.length > 0) {
                        html += 'You can teach: ' + match.can_teach.join(', ') + '<br>';
                    }
                    if (match.mutual) {
                        html += '<strong style="color: green;">Mutual exchange possible!</strong>';
                    }
                    html += '</div>';
                }
            }
            document.getElementById('matchesList').innerHTML = html;
        })
        .catch(error => {
            document.getElementById('matchesList').innerHTML = '<p class="error">Error finding matches</p>';
        });
}

loadUsers();

