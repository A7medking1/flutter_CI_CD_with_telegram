# 🚀 Flutter CI/CD Setup Guide
## Firebase App Distribution + Fastlane + Telegram

This guide will walk you through setting up a complete CI/CD pipeline that automatically builds your Flutter app, uploads it to Firebase App Distribution with **public access**, and sends a download link to your Telegram channel.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Firebase Setup](#firebase-setup)
3. [Telegram Bot Setup](#telegram-bot-setup)
4. [GitHub Secrets Configuration](#github-secrets-configuration)
5. [Testing the Workflow](#testing-the-workflow)
6. [Using with Multiple Projects](#using-with-multiple-projects)
7. [Troubleshooting](#troubleshooting)

---

## ✅ Prerequisites

- A Firebase project
- A GitHub repository with your Flutter app
- A Telegram account and channel/group
- GitHub Actions enabled in your repository

---

## 🔥 Firebase Setup

### Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Add project"** or select an existing project
3. Follow the setup wizard to create your project

### Step 2: Add Your Android App to Firebase

1. In Firebase Console, click the **Android icon** to add an Android app
2. Enter your Android package name (found in `android/app/build.gradle.kts`):
   ```kotlin
   applicationId = "com.example.tes_cicd_telegram"
   ```
3. Download the `google-services.json` file (if you haven't already)
4. Place it in `android/app/` directory
5. Note down your **Firebase App ID** - it looks like:
   ```
   1:123456789:android:abc123def456
   ```
   You can find this in:
   - Firebase Console → Project Settings → Your Apps → App ID
   - Or in `google-services.json` under `mobilesdk_app_id`

### Step 3: Create a Service Account

Firebase App Distribution requires a service account for authentication in CI/CD environments.

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your Firebase project from the dropdown
3. Navigate to **IAM & Admin → Service Accounts**
4. Click **"Create Service Account"**
5. Fill in the details:
   - **Name**: `firebase-app-distribution`
   - **Description**: `Service account for CI/CD Firebase App Distribution`
6. Click **"Create and Continue"**
7. Grant the following roles:
   - **Firebase App Distribution Admin**
   - **Service Account User**
8. Click **"Continue"** then **"Done"**

### Step 4: Create and Download the Service Account Key

1. In the Service Accounts list, find your newly created account
2. Click the **three dots** (⋮) → **"Manage keys"**
3. Click **"Add Key" → "Create new key"**
4. Select **JSON** format
5. Click **"Create"** - this downloads the JSON file
6. **Keep this file secure!** You'll use it in GitHub Secrets

### Step 5: Enable App Distribution API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **APIs & Services → Library**
3. Search for **"Firebase App Distribution API"**
4. Click on it and enable it
5. Also enable **"Firebase Management API"**

### Step 6: Configure Public Access (Important!)

By default, Firebase App Distribution requires testers to be invited. To make your releases publicly accessible:

**Option 1: Via Firebase Console**
1. Go to Firebase Console → App Distribution
2. After your first release appears, go to **Settings**
3. Look for **"Public access"** or **"Share links publicly"** option
4. Enable it for your app

**Option 2: Via the Download Link**
The public download link format is:
```
https://appdistribution.firebase.google.com/pub/i/<FIREBASE_APP_ID>
```
This link will show the latest release and allows anyone to download it without being added as a tester.

> **Note**: The first time someone accesses the link, they might need to accept Firebase's terms. After that, they can download directly.

---

## 💬 Telegram Bot Setup

### Step 1: Create a Telegram Bot

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot` command
3. Follow the instructions:
   - Choose a name for your bot (e.g., "My App CI/CD Bot")
   - Choose a username (must end in `bot`, e.g., "myapp_cicd_bot")
4. BotFather will give you a **bot token** - save it! It looks like:
   ```
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

### Step 2: Get Your Chat/Channel ID

**For a Group:**
1. Add your bot to the group
2. Send a message to the group
3. Visit this URL (replace `YOUR_BOT_TOKEN`):
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```
4. Look for `"chat":{"id":-123456789}` - this is your chat ID

**For a Channel:**
1. Add your bot as an administrator to the channel
2. Post a message in the channel
3. Visit the same URL as above
4. Look for `"chat":{"id":-100123456789}` - this is your channel ID
   (Channel IDs usually start with `-100`)

**Quick Method:**
1. Forward any message from your channel/group to [@userinfobot](https://t.me/userinfobot)
2. The bot will show you the chat ID

---

## 🔐 GitHub Secrets Configuration

You need to add 4 secrets to your GitHub repository:

### Step 1: Go to Repository Settings

1. Open your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**

### Step 2: Add Each Secret

#### Secret 1: `FIREBASE_SERVICE_ACCOUNT_JSON`
- **Name**: `FIREBASE_SERVICE_ACCOUNT_JSON`
- **Value**: Open the service account JSON file you downloaded and **paste the entire content**
  
  It should look like:
  ```json
  {
    "type": "service_account",
    "project_id": "your-project-id",
    "private_key_id": "...",
    "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-app-distribution@your-project.iam.gserviceaccount.com",
    ...
  }
  ```

#### Secret 2: `FIREBASE_APP_ID`
- **Name**: `FIREBASE_APP_ID`
- **Value**: Your Firebase App ID (e.g., `1:123456789:android:abc123def456`)

#### Secret 3: `TELEGRAM_BOT_TOKEN`
- **Name**: `TELEGRAM_BOT_TOKEN`
- **Value**: Your bot token from BotFather (e.g., `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### Secret 4: `TELEGRAM_CHAT_ID`
- **Name**: `TELEGRAM_CHAT_ID`
- **Value**: Your channel/group chat ID (e.g., `-100123456789`)

### Visual Confirmation

After adding all secrets, you should see:
```
FIREBASE_SERVICE_ACCOUNT_JSON  Updated X minutes ago
FIREBASE_APP_ID                Updated X minutes ago
TELEGRAM_BOT_TOKEN             Updated X minutes ago
TELEGRAM_CHAT_ID               Updated X minutes ago
```

---

## 🧪 Testing the Workflow

### Step 1: Make a Test Commit

1. Make any small change to your code
2. Commit with a descriptive message:
   ```bash
   git add .
   git commit -m "Test CI/CD pipeline"
   git push origin main
   ```

### Step 2: Monitor the Workflow

1. Go to your GitHub repository
2. Click **Actions** tab
3. You should see your workflow running
4. Click on the workflow run to see detailed logs

### Step 3: Verify Each Step

The workflow should complete these steps:
- ✅ Checkout code
- ✅ Setup Java
- ✅ Setup Flutter
- ✅ Setup Ruby & Fastlane
- ✅ Get version info
- ✅ Create service account file
- ✅ Build and upload with Fastlane
- ✅ Get Firebase download link
- ✅ Send link to Telegram
- ✅ Cleanup service account file

### Step 4: Check the Results

1. **Firebase Console**: Go to App Distribution → Releases - you should see your APK
2. **Telegram**: Check your channel/group for a formatted message with:
   - App name
   - Version number
   - Commit message
   - Public download link

### Step 5: Test the Download Link

1. Copy the link from the Telegram message
2. Open it in an **incognito/private browser** (to simulate a public user)
3. You should be able to download the APK without logging into Firebase
4. Install the APK on an Android device to verify it works

---

## 🔄 Using with Multiple Projects

This setup is designed to work with **10+ Flutter projects** using the **same Firebase project**. Here's how:

### Option 1: Shared Firebase Project with Different Apps

1. **Add each Flutter app to the same Firebase project:**
   - Firebase Console → Add Android app
   - Each app gets its own unique `FIREBASE_APP_ID`

2. **Use the same service account for all projects:**
   - The same `FIREBASE_SERVICE_ACCOUNT_JSON` works for all apps in the Firebase project

3. **Configure each GitHub repository:**
   - Copy the workflow files to each project
   - Set the same `FIREBASE_SERVICE_ACCOUNT_JSON` secret in each repo
   - Set different `FIREBASE_APP_ID` for each app
   - Optionally use different Telegram channels or the same one

### Option 2: Shared Configuration

If you want to avoid duplicating the service account JSON secret:

1. Create an **Organization secret** (if using GitHub Organizations)
2. Or use **repository variables** for non-sensitive data
3. Only the `FIREBASE_APP_ID` needs to be different per project

### App Name Configuration

Each project can customize the app name in the workflow:

```yaml
env:
  APP_NAME: "Your App Name Here"  # Change this per project
```

---

## 🔧 Troubleshooting

### Issue: "Failed to create service account file"

**Cause**: The JSON secret might not be properly formatted

**Solution**:
1. Re-copy the entire JSON file content
2. Make sure you copied the **complete** JSON (starts with `{` and ends with `}`)
3. Don't add any extra spaces or line breaks

### Issue: "Firebase upload failed - Permission denied"

**Cause**: Service account doesn't have the right permissions

**Solution**:
1. Go to Google Cloud Console → IAM & Admin
2. Find your service account
3. Ensure it has these roles:
   - Firebase App Distribution Admin
   - Service Account User
4. Try regenerating the service account key

### Issue: "Firebase API not enabled"

**Cause**: Required APIs are not enabled

**Solution**:
1. Go to Google Cloud Console → APIs & Services → Library
2. Enable:
   - Firebase App Distribution API
   - Firebase Management API
3. Wait a few minutes and try again

### Issue: Telegram notification failed

**Cause**: Wrong bot token or chat ID

**Solution**:
1. Verify the bot token by visiting:
   ```
   https://api.telegram.org/botYOUR_TOKEN/getMe
   ```
   Should return bot information
2. Verify the chat ID is correct (including the minus sign for groups/channels)
3. Ensure the bot is added as an administrator to the channel

### Issue: Download link shows "Access denied"

**Cause**: The release is not public

**Solution**:
1. Make sure you removed the `groups:` parameter in Fastlane (already done in our setup)
2. First release might not be public by default - check Firebase console settings
3. Use the public link format: `https://appdistribution.firebase.google.com/pub/i/<APP_ID>`

### Issue: Build fails at Flutter build step

**Cause**: Flutter/Java version mismatch or dependency issues

**Solution**:
1. Check the Flutter version in workflow matches your local version
2. Verify Java version is correct (17.0.10 for Flutter 3.35.1)
3. Check the build logs for specific errors
4. Try running `flutter clean && flutter pub get` locally first

### Issue: "Fastlane command not found"

**Cause**: Ruby/Bundler setup failed

**Solution**:
1. Check the workflow logs for Ruby installation errors
2. Verify `Gemfile` and `Gemfile.lock` exist in `android/` directory
3. Try adding explicit Bundler installation:
   ```yaml
   gem install bundler:2.4.22
   ```

### Getting Help

If you encounter issues:
1. Check the **GitHub Actions logs** for detailed error messages
2. Review the **Fastlane output** for Firebase-specific errors
3. Verify all secrets are correctly set
4. Test Fastlane locally first: `cd android && bundle exec fastlane test`

---

## 📁 Complete File Structure

After setup, your project should look like this:

```
your-flutter-project/
├── .github/
│   └── workflows/
│       └── ci.yml                          # GitHub Actions workflow
├── android/
│   ├── app/
│   │   ├── build.gradle.kts               # Contains applicationId
│   │   └── google-services.json           # Firebase config (gitignored)
│   ├── fastlane/
│   │   ├── Fastfile                       # Fastlane configuration
│   │   ├── Appfile                        # App-specific config
│   │   ├── Gemfile                        # Ruby dependencies
│   │   └── Gemfile.lock                   # Locked Ruby versions
│   └── firebase-service-account.json      # Only created in CI, never committed
├── .gitignore                              # Updated with Firebase/Fastlane entries
├── pubspec.yaml                            # Contains version number
└── SETUP_GUIDE.md                          # This file
```

**Files to NEVER commit:**
- `android/app/google-services.json` (optional, if sensitive)
- `android/firebase-service-account.json`
- Any `*-service-account*.json` files

These are already in your `.gitignore`!

---

## 🎉 Success!

If everything is set up correctly, every push to your `main` branch will:

1. ✅ Build your Flutter APK
2. ✅ Upload it to Firebase App Distribution (public)
3. ✅ Generate a public download link
4. ✅ Send a beautiful formatted message to Telegram with the link
5. ✅ Anyone can download the APK without Firebase login!

Your Telegram message will look like:

```
🚀 New Build Available!

📱 App: mini-soft-admin
🔖 Version: 1.0.1+1
📝 Changes: Test CI/CD pipeline

🔗 Download Link:
https://appdistribution.firebase.google.com/pub/i/1:xxx:android:xxx

✅ Click the link above to download and install the latest version
```

---

## 📚 Additional Resources

- [Firebase App Distribution Docs](https://firebase.google.com/docs/app-distribution)
- [Fastlane Docs](https://docs.fastlane.tools/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

**Need help?** Review the [Troubleshooting](#troubleshooting) section or check the GitHub Actions logs for detailed error messages.
