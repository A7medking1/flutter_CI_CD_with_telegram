# 🚀 Flutter CI/CD with Firebase App Distribution & Telegram

Automated Flutter build pipeline using **Fastlane**, **Firebase App Distribution**, and **Telegram notifications** with public download links.

![Flutter](https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white)
![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)
![Fastlane](https://img.shields.io/badge/Fastlane-00F200?style=for-the-badge&logo=fastlane&logoColor=black)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)

---

## ✨ Features

- 📱 **Automated APK Builds** - Triggered on every push
- 🔥 **Firebase App Distribution** - Public download links (no tester registration)
- 💎 **Fastlane Integration** - Professional build automation
- 📢 **Telegram Notifications** - Formatted messages with download links
- 🔐 **Service Account Auth** - Secure Firebase authentication
- 🔄 **Multi-Project Support** - Same Firebase project for 10+ apps
- 🧹 **Auto Cleanup** - No credentials left behind

---

## 📦 What Happens Automatically

Every push to your configured branch:
1. ✅ Flutter APK builds in release mode
2. ✅ Uploads to Firebase App Distribution
3. ✅ Generates public download link
4. ✅ Sends formatted notification to Telegram with link
5. ✅ Cleans up temporary credentials

**Telegram Message Example:**
```
🚀 New Build Available!

📱 App: YourApp
🔖 Version: 1.0.1+1
📝 Changes: Your commit message

🔗 Download Link:
https://appdistribution.firebase.google.com/pub/i/...

✅ Click the link above to download and install
```

---

## 🔧 Quick Setup (30 minutes)

### 1️⃣ Firebase Setup (15 min)

**A. Create Service Account:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your Firebase project
3. **IAM & Admin → Service Accounts → Create Service Account**
4. Name: `firebase-app-distribution`
5. Grant roles:
   - `Firebase App Distribution Admin`
   - `Service Account User`
6. Create key (JSON format) → Download it

**B. Enable APIs:**
1. **APIs & Services → Library**
2. Enable:
   - Firebase App Distribution API
   - Firebase Management API

**C. Get Firebase App ID:**
- Firebase Console → Project Settings → Your Apps
- Copy the App ID (format: `1:xxxxx:android:xxxxx`)

### 2️⃣ Telegram Setup (5 min)

**A. Create Bot:**
1. Open Telegram, search [@BotFather](https://t.me/BotFather)
2. Send `/newbot` and follow instructions
3. Copy the **bot token**

**B. Get Chat ID:**
1. Send a message to your bot
2. Visit: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
3. Find `"chat":{"id":123456789}`
4. Copy the **chat ID**

**For channels:** Add bot as admin first, ID will be `-100xxxxxxx`

### 3️⃣ GitHub Secrets (5 min)

Go to **GitHub Repo → Settings → Secrets → Actions → New secret**

Add these 4 secrets:

| Secret Name | Value | Where to Get |
|------------|-------|--------------|
| `FIREBASE_SERVICE_ACCOUNT_JSON` | Complete JSON file content | Service account JSON file |
| `FIREBASE_APP_ID` | `1:xxxxx:android:xxxxx` | Firebase Console |
| `TELEGRAM_BOT_TOKEN` | `123456789:ABCdef...` | @BotFather |
| `TELEGRAM_CHAT_ID` | `123456789` or `-100xxx` | getUpdates API |

> **Important:** For `FIREBASE_SERVICE_ACCOUNT_JSON`:
> - Open the downloaded JSON file
> - Copy **all content** (Ctrl+A, Ctrl+C)
> - Paste it as the secret value (yes, the entire JSON)

### 4️⃣ Test It! (5 min)

```bash
git add .
git commit -m "Test Firebase CI/CD"
git push
```

Then:
1. Go to **GitHub → Actions** tab
2. Watch the workflow run
3. Check Telegram for your notification
4. Download APK from the Firebase link

---

## 📁 Project Structure

```
your-flutter-project/
├── .github/
│   └── workflows/
│       └── ci.yml                    # GitHub Actions workflow
├── android/
│   ├── app/
│   │   └── build.gradle.kts          # Contains applicationId
│   ├── fastlane/
│   │   ├── Fastfile                  # Fastlane build configuration
│   │   ├── Appfile                   # App settings
│   │   ├── Gemfile                   # Ruby dependencies
│   │   └── Gemfile.lock
│   └── firebase-service-account.json # ⚠️ Never committed (created in CI only)
├── .gitignore                         # Updated to exclude credentials
├── pubspec.yaml                       # App version
├── SETUP_GUIDE.md                     # Detailed setup instructions
└── GITHUB_SECRETS.md                  # Secrets reference
```

---

## 🎯 How It Works

### GitHub Actions Workflow

```yaml
Trigger: Push to branch
    ↓
Checkout code
    ↓
Setup: Java + Flutter + Ruby + Fastlane
    ↓
Create service account file (temporary)
    ↓
Run Fastlane → Build APK + Upload to Firebase
    ↓
Extract public download link
    ↓
Send Telegram notification with link
    ↓
Cleanup service account file
```

### Fastlane Lane

```ruby
1. flutter clean
2. flutter pub get
3. flutter build apk --release
4. firebase_app_distribution (with service account)
5. Success! ✅
```

---

## 🔐 Security Features

- ✅ **Service account JSON** stored in GitHub Secrets (encrypted)
- ✅ **Temporary file** created during workflow, deleted after
- ✅ **Credentials never committed** to repository
- ✅ **Gitignore rules** prevent accidental commits
- ✅ **Public links only** - no sensitive data exposed

---

## 🌍 Public Access

Downloads work **without Firebase login**:
- ✅ No tester registration required
- ✅ Anyone with link can download
- ✅ First-time: Accept Firebase ToS
- ✅ After that: Direct downloads

Link format:
```
https://appdistribution.firebase.google.com/pub/i/<FIREBASE_APP_ID>
```

---

## 🔄 Multi-Project Usage

Use the **same Firebase project** for multiple Flutter apps:

1. **Same for all projects:**
   - `FIREBASE_SERVICE_ACCOUNT_JSON` (same account)
   - Optionally same `TELEGRAM_BOT_TOKEN`

2. **Different per project:**
   - `FIREBASE_APP_ID` (each app has unique ID)
   - Optionally different `TELEGRAM_CHAT_ID`

Just copy the workflow files and configure secrets!

---

## ⚙️ Configuration

### Change App Name

Edit `.github/workflows/ci.yml`:
```yaml
env:
  APP_NAME: "YourAppName"  # ← Change this
```

### Change Trigger Branch

Edit `.github/workflows/ci.yml`:
```yaml
on:
  push:
    branches: [ main ]  # ← Change this
```

### Customize Release Notes

Edit workflow step:
```yaml
RELEASE_NOTES: |
  🚀 Version: ${{ steps.version.outputs.VERSION }}
  📝 ${{ steps.version.outputs.COMMIT_MSG }}
  # Add custom notes here
```

---

## 🆘 Troubleshooting

### "Invalid service account"
- ✅ Check JSON is complete (starts with `{`, ends with `}`)
- ✅ Verify service account has correct roles
- ✅ Ensure Firebase APIs are enabled

### "Chat not found" (Telegram)
- ✅ Bot must be started (send a message first)
- ✅ For channels: Bot needs admin rights
- ✅ Check chat ID includes minus sign if group/channel

### "APK not found"
- ✅ Check APK path in Fastfile (should be `../../build/...`)
- ✅ Verify Flutter build completed successfully

### "Firebase API not enabled"
- ✅ Enable Firebase App Distribution API
- ✅ Enable Firebase Management API
- ✅ Wait 1-2 minutes for APIs to activate

### Platform Lock Error (Ruby)
- ✅ Workflow includes `bundle lock --add-platform` fix
- ✅ Removes `bundler-cache: true` if causing issues

**For detailed help:** See `SETUP_GUIDE.md` Troubleshooting section

---

## 📊 Workflow Status

Monitor your builds:
- **GitHub Actions**: Check status and logs
- **Firebase Console**: View releases and analytics
- **Telegram**: Instant notifications on completion

---

## 📚 Documentation Files

| File | Description |
|------|-------------|
| `SETUP_GUIDE.md` | Complete setup walkthrough with screenshots |
| `GITHUB_SECRETS.md` | Quick reference for all secrets |
| `android/fastlane/Fastfile` | Fastlane configuration (commented) |
| `.github/workflows/ci.yml` | GitHub Actions workflow |

---

## 🚀 Quick Commands

**Test Fastlane locally:**
```bash
cd android
export FIREBASE_APP_ID="your_app_id"
export FIREBASE_SERVICE_ACCOUNT_PATH="/path/to/service-account.json"
export RELEASE_NOTES="Test build"
bundle exec fastlane firebase_distribution
```

**Test Telegram bot:**
```bash
curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" \
  -d chat_id="<CHAT_ID>" \
  -d text="Test message"
```

---

## 📈 Next Steps

After successful setup:
1. ✅ Commit and push to trigger first build
2. ✅ Monitor GitHub Actions for completion
3. ✅ Check Firebase Console for uploaded APK
4. ✅ Verify Telegram notification received
5. ✅ Test download link in incognito browser
6. ✅ Install APK and verify it works

---

## 🎉 Success!

Your Flutter CI/CD pipeline is ready! Every push will now:
- Build your app automatically
- Upload to Firebase with public link
- Notify you via Telegram
- Keep your credentials secure

**Happy Building! 🚀**

---

## 📝 License

This CI/CD setup is open source. Customize and use as needed for your projects.

---

**Questions?** Check the detailed guides:
- 📖 [SETUP_GUIDE.md](./SETUP_GUIDE.md) - Full setup instructions
- 🔑 [GITHUB_SECRETS.md](./GITHUB_SECRETS.md) - Secrets configuration
- 🔧 Workflow logs in GitHub Actions
