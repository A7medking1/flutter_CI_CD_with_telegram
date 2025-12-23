# 🔑 GitHub Secrets Quick Reference

This document provides a quick reference for all the GitHub Secrets you need to configure for the CI/CD pipeline.

## Required Secrets

Add these secrets to your GitHub repository:
**Settings → Secrets and variables → Actions → New repository secret**

### 1. FIREBASE_SERVICE_ACCOUNT_JSON

**Description**: Complete JSON content of the Firebase service account key file

**How to get it**:
1. Google Cloud Console → IAM & Admin → Service Accounts
2. Create service account with roles:
   - Firebase App Distribution Admin
   - Service Account User
3. Create key (JSON format)
4. Copy the **entire file content**

**Example value** (paste the complete JSON):
```json
{
  "type": "service_account",
  "project_id": "your-firebase-project",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-app-distribution@your-project.iam.gserviceaccount.com",
  "client_id": "123456789",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/..."
}
```

---

### 2. FIREBASE_APP_ID

**Description**: Your Firebase Android app ID

**How to get it**:
- **Method 1**: Firebase Console → Project Settings → Your Apps → App ID
- **Method 2**: In `android/app/google-services.json`, look for `mobilesdk_app_id`

**Format**: `1:PROJECT_NUMBER:android:APP_IDENTIFIER`

**Example value**:
```
1:469664748258:android:f4029842d3762afc5684bb
```

---

### 3. TELEGRAM_BOT_TOKEN

**Description**: Your Telegram bot authentication token

**How to get it**:
1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow instructions
3. Copy the token BotFather gives you

**Format**: `NUMBER:ALPHANUMERIC_STRING`

**Example value**:
```
123456789:ABCdefGHIjklMNOpqrsTUVwxyz-123456
```

**Verify it works** (replace with your token):
```
https://api.telegram.org/bot<YOUR_TOKEN>/getMe
```

---

### 4. TELEGRAM_CHAT_ID

**Description**: The ID of your Telegram channel or group

**How to get it**:

**For a Channel:**
1. Add your bot as administrator to the channel
2. Post a message in the channel
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Look for `"chat":{"id":-100123456789}`

**For a Group:**
1. Add your bot to the group
2. Send a message in the group
3. Visit the same URL above
4. Look for `"chat":{"id":-123456789}`

**Quick Method:**
Forward any message from your channel/group to [@userinfobot](https://t.me/userinfobot)

**Format**: Usually starts with `-` for groups/channels

**Example values**:
```
-100123456789    (for channels)
-123456789       (for groups)
```

---

## Verification Checklist

Before triggering your workflow, verify:

- [ ] All 4 secrets are added to GitHub
- [ ] `FIREBASE_SERVICE_ACCOUNT_JSON` is complete valid JSON
- [ ] `FIREBASE_APP_ID` matches your app in Firebase Console
- [ ] `TELEGRAM_BOT_TOKEN` works (test with `/getMe` endpoint)
- [ ] `TELEGRAM_CHAT_ID` is correct (bot is added to channel/group)
- [ ] Bot has admin rights in the channel (if using a channel)

---

## Testing Secrets Locally

You can test the setup locally before pushing to GitHub:

### Test Firebase Connection

```bash
cd android

# Set environment variables
export FIREBASE_APP_ID="your_app_id"
export FIREBASE_SERVICE_ACCOUNT_PATH="/path/to/service-account.json"
export RELEASE_NOTES="Test build"

# Run Fastlane
bundle exec fastlane firebase_distribution
```

### Test Telegram Bot

```bash
# Replace with your values
BOT_TOKEN="your_token"
CHAT_ID="your_chat_id"
MESSAGE="Test message"

curl -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -d chat_id="${CHAT_ID}" \
  -d text="${MESSAGE}"
```

---

## Security Notes

⚠️ **NEVER commit these secrets to your repository!**

- The `.gitignore` file is configured to exclude service account JSON files
- GitHub Secrets are encrypted and only accessible during workflow runs
- The service account file is created temporarily during CI/CD and deleted after use
- Keep your bot token secure - it allows full control of your bot

---

## Multi-Project Setup

If you're using the same Firebase project for multiple Flutter apps:

**Same across all projects:**
- ✅ `FIREBASE_SERVICE_ACCOUNT_JSON` (same service account)
- ✅ `TELEGRAM_BOT_TOKEN` (can use same bot)

**Different per project:**
- ❗ `FIREBASE_APP_ID` (each app has unique ID)
- ⚠️ `TELEGRAM_CHAT_ID` (optional - can use same or different channels)

**Tip**: For GitHub Organizations, create organization-level secrets for shared values!

---

## Troubleshooting

### "Invalid service account"
- Verify the JSON is complete and valid
- Ensure service account has Firebase App Distribution Admin role
- Check that Firebase APIs are enabled in Google Cloud Console

### "Invalid bot token"
- Test the token with: `https://api.telegram.org/bot<TOKEN>/getMe`
- Make sure you copied the full token from BotFather
- No spaces or extra characters

### "Chat not found"
- Verify the chat ID is correct (including the minus sign)
- Make sure the bot is added to the channel/group
- For channels, bot needs administrator rights

---

For detailed setup instructions, see [SETUP_GUIDE.md](./SETUP_GUIDE.md)
