// CS2 Tracker Browser Extension - Auto Import Script

document.getElementById('importBtn').addEventListener('click', async () => {
    const userId = document.getElementById('userId').value;
    const statusDiv = document.getElementById('status');
    const importBtn = document.getElementById('importBtn');

    // Validate user ID
    if (!userId || userId.length === 0) {
        statusDiv.textContent = '⚠️ Please enter your User ID';
        statusDiv.className = 'status error';
        return;
    }

    // Save user ID for future use
    chrome.storage.local.set({ userId: userId });

    // Disable button
    importBtn.disabled = true;
    statusDiv.textContent = '⏳ Extracting cookies...';
    statusDiv.className = 'status';

    try {
        // Get Steam cookies
        const cookies = await getSteamCookies();

        if (!cookies) {
            throw new Error('Could not extract Steam cookies. Make sure you are logged into Steam.');
        }

        statusDiv.textContent = '📡 Sending to CS2 Tracker...';

        // Send to our API
        const response = await fetch(`http://localhost:8000/api/import/steam-market?user_id=${userId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                cookies: cookies,
                count: 500
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Import failed');
        }

        const result = await response.json();

        // Show success
        statusDiv.textContent = `✅ Imported ${result.imported} transactions!`;
        statusDiv.className = 'status success';

        // Show detailed results
        setTimeout(() => {
            statusDiv.textContent = `✅ Success!\nImported: ${result.imported}\nSkipped: ${result.skipped}\nTotal: ${result.total}`;
        }, 1000);

    } catch (error) {
        console.error('Import error:', error);
        statusDiv.textContent = `❌ Error: ${error.message}`;
        statusDiv.className = 'status error';
    } finally {
        importBtn.disabled = false;
    }
});

// Load saved user ID
chrome.storage.local.get(['userId'], (result) => {
    if (result.userId) {
        document.getElementById('userId').value = result.userId;
    }
});

// Function to get Steam cookies
async function getSteamCookies() {
    try {
        // Get cookies from steamcommunity.com
        const sessionId = await chrome.cookies.get({
            url: 'https://steamcommunity.com',
            name: 'sessionid'
        });

        const steamLoginSecure = await chrome.cookies.get({
            url: 'https://steamcommunity.com',
            name: 'steamLoginSecure'
        });

        const steamCountry = await chrome.cookies.get({
            url: 'https://steamcommunity.com',
            name: 'steamCountry'
        });

        // Check if we got the essential cookies
        if (!sessionId || !steamLoginSecure) {
            console.error('Missing essential cookies');
            return null;
        }

        // Format as cookie string
        let cookieString = `sessionid=${sessionId.value}; steamLoginSecure=${steamLoginSecure.value}`;

        if (steamCountry) {
            cookieString += `; steamCountry=${steamCountry.value}`;
        }

        return cookieString;

    } catch (error) {
        console.error('Error getting cookies:', error);
        return null;
    }
}

// Auto-import on extension load (if user ID is saved)
chrome.storage.local.get(['userId', 'autoImport'], async (result) => {
    if (result.userId && result.autoImport) {
        // Trigger auto-import
        document.getElementById('userId').value = result.userId;
        // Small delay to let UI load
        setTimeout(() => {
            document.getElementById('importBtn').click();
        }, 500);
    }
});
