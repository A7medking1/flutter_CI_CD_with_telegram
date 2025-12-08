#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت تلقائي لإنشاء Android Keystore و Code Signing
يعمل تلقائياً عند رفع المشروع لأول مرة

الاستخدام:
    python setup_keystore.py
"""

import os
import json
import sys
from pathlib import Path
import subprocess

# ============================================
# الإعدادات - عدلها حسب رغبتك
# ============================================

CONFIG = {
    # معلومات الشركة/المطور
    "company_name": "testComp",
    "developer_name": "ahmed nasr",
    "organization": "testComp",
    "city": "Cairo",
    "state": "Cairo",
    "country": "EG",

    # إعدادات الـ Keystore
    "keystore_dir": "necessary_files",
    "keystore_name": "upload-keystore.jks",
    "key_alias": "upload",
    "validity_days": 10000,  # ~27 سنة
    "password": "123456",
}


# ============================================
# دوال مساعدة
# ============================================

def print_header(text):
    """طباعة عنوان منسق"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_success(text):
    """طباعة رسالة نجاح"""
    print(f"✅ {text}")


def print_error(text):
    """طباعة رسالة خطأ"""
    print(f"❌ {text}")


def print_info(text):
    """طباعة معلومة"""
    print(f"ℹ️  {text}")


def check_keytool():
    """التحقق من وجود keytool على Windows أو macOS أو Linux"""
    # أولاً نحاول نلاقي keytool في PATH الحالي
    import shutil

    keytool_path = shutil.which("keytool")

    # لو مش موجود نحاول نبحث في مواقع الـ JDK الشائعة على Windows
    if not keytool_path:
        possible_paths = [
            r"C:\Program Files\Java\jdk-21\bin\keytool.exe",
            r"C:\Program Files\Java\jdk-22\bin\keytool.exe",
            r"C:\Program Files\Java\jdk-20\bin\keytool.exe",
            r"C:\Program Files\Java\jdk-17\bin\keytool.exe",
        ]
        for p in possible_paths:
            if os.path.exists(p):
                os.environ["PATH"] += ";" + os.path.dirname(p)
                keytool_path = p
                print(f"✅ تم العثور على keytool في: {p}")
                break

    # لو بعد كل ده لسه مش موجود
    if not keytool_path:
        print("❌ لم يتم العثور على keytool. تأكد من تثبيت JDK أو تعديل PATH.")
        return False

    # الآن نجرب تشغيله فعلاً للتأكد من أنه يعمل
    try:
        subprocess.run([keytool_path, "-help"], capture_output=True, text=True, check=True)
        return True
    except Exception as e:
        print(f"⚠️ خطأ أثناء محاولة تشغيل keytool: {e}")
        return False


def create_directory(path):
    """إنشاء مجلد إذا لم يكن موجود"""
    Path(path).mkdir(parents=True, exist_ok=True)
    print_success(f"تم إنشاء المجلد: {path}")


def keystore_exists(keystore_path):
    """التحقق من وجود Keystore"""
    return Path(keystore_path).exists()


def generate_keystore(config):
    """إنشاء Keystore جديد"""
    keystore_path = os.path.join(config["keystore_dir"], config["keystore_name"])

    keystore_password = config["password"]
    key_password = config["password"]

    print_info("جاري إنشاء Keystore...")

    # أمر keytool
    dname = (
        f"CN={config['developer_name']}, "
        f"OU={config['organization']}, "
        f"O={config['company_name']}, "
        f"L={config['city']}, "
        f"ST={config['state']}, "
        f"C={config['country']}"
    )

    cmd = [
        "keytool",
        "-genkey",
        "-v",
        "-keystore", keystore_path,
        "-keyalg", "RSA",
        "-keysize", "2048",
        "-validity", str(config["validity_days"]),
        "-alias", config["key_alias"],
        "-storepass", keystore_password,
        "-keypass", key_password,
        "-dname", dname,
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        print_success(f"تم إنشاء Keystore: {keystore_path}")
        return keystore_password, key_password
    except subprocess.CalledProcessError as e:
        print_error(f"فشل إنشاء Keystore: {e.stderr}")
        sys.exit(1)


def create_key_properties(config, keystore_password, key_password):
    """إنشاء ملف key.properties"""
    key_properties_path = os.path.join(config["keystore_dir"], "key.properties")

    content = f"""# Android Keystore Configuration
# تم الإنشاء تلقائياً بواسطة setup_keystore.py
# لا تشارك هذا الملف مع أحد!

storePassword={keystore_password}
keyPassword={key_password}
keyAlias={config['key_alias']}
storeFile=../necessary_files/{config['keystore_name']}
"""

    with open(key_properties_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print_success(f"تم إنشاء: {key_properties_path}")


def create_key_properties_template(config):
    """إنشاء template لـ key.properties"""
    template_path = os.path.join(config["keystore_dir"], "key.properties")

    content = """# Android Keystore Configuration Template
# انسخ هذا الملف إلى key.properties وأضف كلمات المرور الخاصة بك
# لا تضف key.properties إلى Git!

storePassword=YOUR_KEYSTORE_PASSWORD
keyPassword=YOUR_KEY_PASSWORD
keyAlias=upload
storeFile=../necessary_files/upload-keystore.jks
"""

    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print_success(f"تم إنشاء: {template_path}")


def create_keystore_info(config, keystore_password, key_password):
    """إنشاء ملف معلومات الـ Keystore"""
    info_path = os.path.join(config["keystore_dir"], "keystore-info.txt")

    from datetime import datetime

    content = f"""{'=' * 60}
معلومات Android Keystore
{'=' * 60}

📁 ملف الـ Keystore: {config['keystore_name']}
🔑 Key Alias: {config['key_alias']}
🔒 Keystore Password: {keystore_password}
🔐 Key Password: {key_password}
⏰ صلاحية: {config['validity_days']} يوم (~27 سنة)

{'=' * 60}
معلومات المطور
{'=' * 60}

👤 الاسم: {config['developer_name']}
🏢 الشركة: {config['company_name']}
🏛️ المنظمة: {config['organization']}
🌍 المدينة: {config['city']}, {config['state']}, {config['country']}

{'=' * 60}
ملاحظات مهمة
{'=' * 60}

⚠️  احفظ هذا الملف في مكان آمن!
⚠️  لا تشارك كلمات المرور مع أحد!
⚠️  لا تضف الـ Keystore إلى Git!
⚠️  إذا فقدت الـ Keystore، لن تستطيع تحديث التطبيق على Play Store!
⚠️  اعمل نسخة احتياطية من الـ Keystore!

{'=' * 60}
تاريخ الإنشاء
{'=' * 60}

📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'=' * 60}
"""

    with open(info_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print_success(f"تم إنشاء: {info_path}")


def create_github_secrets_guide(config, keystore_password, key_password):
    """إنشاء دليل لإضافة Secrets إلى GitHub"""
    guide_path = os.path.join(config["keystore_dir"], "github-secrets-guide.txt")

    keystore_path = os.path.join(config["keystore_dir"], config["keystore_name"])

    # تحويل Keystore إلى Base64
    import base64
    with open(keystore_path, 'rb') as f:
        keystore_base64 = base64.b64encode(f.read()).decode('utf-8')

    content = f"""{'=' * 60}
دليل إضافة GitHub Secrets
{'=' * 60}

اذهب إلى:
Settings → Secrets and variables → Actions → New repository secret

أضف هذه الـ Secrets:

{'=' * 60}
1. ANDROID_KEYSTORE_BASE64
{'=' * 60}
القيمة:
{keystore_base64}

{'=' * 60}
2. ANDROID_KEY_ALIAS
{'=' * 60}
القيمة:
{config['key_alias']}

{'=' * 60}
3. ANDROID_KEY_PASSWORD
{'=' * 60}
القيمة:
{key_password}

{'=' * 60}
4. ANDROID_STORE_PASSWORD
{'=' * 60}
القيمة:
{keystore_password}

{'=' * 60}
خطوات سريعة
{'=' * 60}

1. افتح repository على GitHub
2. Settings → Secrets and variables → Actions
3. اضغط "New repository secret"
4. انسخ والصق كل secret من الأعلى
5. احفظ

✅ انتهى!

{'=' * 60}
"""

    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print_success(f"تم إنشاء: {guide_path}")


def update_android_build_gradle():
    """تحديث android/app/build.gradle أو build.gradle.kts تلقائيًا"""
    import os, re

    gradle_paths = [
        "android/app/build.gradle",
        "android/app/build.gradle.kts"
    ]

    gradle_path = next((p for p in gradle_paths if os.path.exists(p)), None)
    if not gradle_path:
        print("❌ لم يتم العثور على build.gradle أو build.gradle.kts")
        return False

    print(f"📄 جاري قراءة الملف: {gradle_path}")
    is_kts = gradle_path.endswith(".kts")

    with open(gradle_path, "r", encoding="utf-8") as f:
        original_content = f.read()

    # -------------------------------
    # للكوتلن DSL (.kts)
    # -------------------------------
    if is_kts:
        print("⚙️ تعديل build.gradle.kts ...")

        content = original_content

        # ✅ إضافة import في الأعلى لو غير موجود
        if "import java.util.Properties" not in content:
            content = (
                    "import java.util.Properties\n"
                    "import java.io.FileInputStream\n\n" + content
            )
            print("✓ تم إضافة import في أعلى الملف")

        # ✅ حذف أي release قديم
        content = re.sub(
            r'buildTypes\s*\{[^}]*release\s*\{[^}]*\}[^}]*\}',
            '',
            content,
            flags=re.DOTALL
        )

        # ✅ إضافة كود keystore لو غير موجود
        if "keystorePropertiesFile" not in content:
            keystore_block = """
// ============================================
// تحميل إعدادات Android Keystore (Kotlin DSL)
// ============================================
val keystorePropertiesFile = rootProject.file("../ness_files/key.properties")
val keystoreProperties = Properties()

if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(FileInputStream(keystorePropertiesFile))
}
"""
            # أضفه قبل android {
            content = content.replace("android {", keystore_block + "\nandroid {", 1)
            print("✓ تم إضافة إعدادات keystore")

        # ✅ إضافة signingConfigs و buildTypes مضبوطين
        build_block = """
    // ============================================
    // إعدادات التوقيع (Kotlin DSL)
    // ============================================
    signingConfigs {
        create("release") {
            if (keystorePropertiesFile.exists()) {
                keyAlias = keystoreProperties["keyAlias"] as String
                keyPassword = keystoreProperties["keyPassword"] as String
                storeFile = file(keystoreProperties["storeFile"] as String)
                storePassword = keystoreProperties["storePassword"] as String
            }
        }
    }

    buildTypes {
        getByName("release") {
            signingConfig = signingConfigs.getByName("release")
        }
    }
"""
        # أضف بعد defaultConfig
        content = re.sub(
            r'(defaultConfig\s*\{[^}]*\})',
            r'\1\n' + build_block,
            content,
            flags=re.DOTALL
        )

        # حفظ النسخة الجديدة
        backup_path = gradle_path + ".backup"
        with open(backup_path, "w", encoding="utf-8") as f:
            f.write(original_content)
        with open(gradle_path, "w", encoding="utf-8") as f:
            f.write(content)

        print("🎯 build.gradle.kts تم تحديثه بنجاح ✓")
        return True

    # -------------------------------
    # للـ Groovy DSL (build.gradle)
    # -------------------------------
    else:
        print("⚙️ تعديل build.gradle (Groovy DSL) ...")

        content = original_content

        # حذف release القديم
        content = re.sub(
            r'buildTypes\s*\{[^}]*release\s*\{[^}]*\}[^}]*\}',
            '',
            content,
            flags=re.DOTALL
        )

        keystore_loader = """
// ============================================
// تحميل إعدادات Android Keystore (Groovy DSL)
// ============================================
def keystoreProperties = new Properties()
def keystorePropertiesFile = rootProject.file('../ness_files/key.properties')
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
}
"""
        if "keystorePropertiesFile" not in content:
            content = content.replace("android {", keystore_loader + "\nandroid {", 1)
            print("✓ تم إضافة إعدادات keystore")

        build_block = """
    signingConfigs {
        release {
            if (keystorePropertiesFile.exists()) {
                keyAlias keystoreProperties['keyAlias']
                keyPassword keystoreProperties['keyPassword']
                storeFile keystoreProperties['storeFile'] ? file(keystoreProperties['storeFile']) : null
                storePassword keystoreProperties['storePassword']
            }
        }
    }

    buildTypes {
        release {
            signingConfig signingConfigs.release
        }
    }
"""
        content = re.sub(
            r'(defaultConfig\s*\{[^}]*\})',
            r'\1\n' + build_block,
            content,
            flags=re.DOTALL
        )

        backup_path = gradle_path + ".backup"
        with open(backup_path, "w", encoding="utf-8") as f:
            f.write(original_content)
        with open(gradle_path, "w", encoding="utf-8") as f:
            f.write(content)

        print("🎯 build.gradle تم تحديثه بنجاح ✓")
        return True


# def update_android_build_gradle():
#     """تحديث android/app/build.gradle أو build.gradle.kts تلقائيًا"""
#
#     gradle_paths = [
#         "android/app/build.gradle",
#         "android/app/build.gradle.kts"
#     ]
#
#     gradle_path = next((p for p in gradle_paths if os.path.exists(p)), None)
#
#     if not gradle_path:
#         print("❌ لم يتم العثور على build.gradle أو build.gradle.kts")
#         print("ℹ️ تأكد أنك داخل مجلد Flutter الصحيح")
#         return False
#
#     print(f"📄 جاري قراءة الملف: {gradle_path}")
#     is_kts = gradle_path.endswith(".kts")
#
#     with open(gradle_path, 'r', encoding='utf-8') as f:
#         original_content = f.read()
#
#     # لو الملف محدث بالفعل
#     if "keystoreProperties" in original_content and "signingConfigs" in original_content:
#         print("ℹ️ build.gradle محدث بالفعل ✓")
#         return True
#
#     content = original_content
#
#     # ============================================
#     # 1️⃣ لو الملف KTS أضف import في أول سطر
#     # ============================================
#     if is_kts:
#         imports_block = "import java.util.Properties\nimport java.io.FileInputStream\n\n"
#
#         # لو مش مضاف بالفعل
#         if "import java.util.Properties" not in content:
#             # أضفه قبل plugins { لو موجود، وإلا في أول الملف
#             if "plugins {" in content:
#                 content = re.sub(r'(^\s*)(plugins\s*\{)', imports_block + r'\1\2', content, count=1)
#                 print("✓ تم إضافة import قبل plugins {")
#             else:
#                 content = imports_block + content
#                 print("✓ تم إضافة import في أول الملف")
#
#     # ============================================
#     # 2️⃣ تحميل keystore properties
#     # ============================================
#     if is_kts:
#         keystore_loader = """
# // ============================================
# // تحميل إعدادات Android Keystore (Kotlin DSL)
# // ============================================
# val keystorePropertiesFile = rootProject.file("../ness_files/key.properties")
# val keystoreProperties = Properties()
#
# if (keystorePropertiesFile.exists()) {
#     keystoreProperties.load(FileInputStream(keystorePropertiesFile))
# }
#
# """
#     else:
#         keystore_loader = """
# // ============================================
# // تحميل إعدادات Android Keystore (Groovy DSL)
# // ============================================
# def keystoreProperties = new Properties()
# def keystorePropertiesFile = rootProject.file('../ness_files/key.properties')
# if (keystorePropertiesFile.exists()) {
#     keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
# }
#
# """
#
#     if 'android {' in content:
#         content = content.replace('android {', keystore_loader + 'android {', 1)
#         print("✓ تم إضافة تحميل keystore properties")
#     else:
#         print("✗ لم يتم العثور على android {")
#         return False
#
#     # ============================================
#     # 3️⃣ إضافة signingConfigs block
#     # ============================================
#     if is_kts:
#         signing_configs = """
#     // ============================================
#     // إعدادات التوقيع (Kotlin DSL)
#     // ============================================
#     signingConfigs {
#         create("release") {
#             if (keystorePropertiesFile.exists()) {
#                 keyAlias = keystoreProperties["keyAlias"] as String
#                 keyPassword = keystoreProperties["keyPassword"] as String
#                 storeFile = file(keystoreProperties["storeFile"] as String)
#                 storePassword = keystoreProperties["storePassword"] as String
#             }
#         }
#     }
#     """
#     else:
#         signing_configs = """
#     // ============================================
#     // إعدادات التوقيع (Groovy DSL)
#     // ============================================
#     signingConfigs {
#         release {
#             if (keystorePropertiesFile.exists()) {
#                 keyAlias keystoreProperties['keyAlias']
#                 keyPassword keystoreProperties['keyPassword']
#                 storeFile keystoreProperties['storeFile'] ? file(keystoreProperties['storeFile']) : null
#                 storePassword keystoreProperties['storePassword']
#             }
#         }
#     }
#     """
#
#     if 'buildTypes {' in content:
#         content = content.replace('buildTypes {', signing_configs + '\n    buildTypes {', 1)
#         print("✓ تم إضافة signingConfigs block")
#     else:
#         print("⚠ لم يتم العثور على buildTypes")
#         return False
#
#     # ============================================
#     # 4️⃣ تحديث release buildType
#     # ============================================
#     print("🔧 جاري تعديل release block...")
#
#     if is_kts:
#         if 'getByName("release")' in content:
#             content = re.sub(
#                 r'signingConfig\s*=\s*signingConfigs\.getByName\(".*?"\)',
#                 'signingConfig = signingConfigs.getByName("release")',
#                 content
#             )
#         else:
#             content = re.sub(
#                 r'(buildTypes\s*\{)',
#                 r'\1\n        getByName("release") {\n            signingConfig = signingConfigs.getByName("release")\n        }',
#                 content,
#                 count=1
#             )
#     else:
#         if 'signingConfig signingConfigs.' in content:
#             content = re.sub(
#                 r'signingConfig\s+signingConfigs\.\w+',
#                 'signingConfig signingConfigs.release',
#                 content
#             )
#         else:
#             content = re.sub(
#                 r'(release\s*\{)',
#                 r'\1\n            signingConfig signingConfigs.release',
#                 content,
#                 count=1
#             )
#
#     print("✓ تم تحديث release buildType")
#
#     # ============================================
#     # 5️⃣ حفظ النسخة الجديدة ونسخة احتياطية
#     # ============================================
#     backup_path = f"{gradle_path}.backup"
#     with open(backup_path, 'w', encoding='utf-8') as f:
#         f.write(original_content)
#     print(f"💾 تم حفظ نسخة احتياطية: {backup_path}")
#
#     with open(gradle_path, 'w', encoding='utf-8') as f:
#         f.write(content)
#
#     print("=" * 60)
#     print("🎉 تم تعديل build.gradle بنجاح!")
#     print("=" * 60)
#     return True


# def update_android_build_gradle():
#     """تحديث android/app/build.gradle أو build.gradle.kts تلقائيًا"""
#     # نحاول نحدد أي ملف Gradle موجود
#     gradle_paths = [
#         "android/app/build.gradle",
#         "android/app/build.gradle.kts"
#     ]
#
#     gradle_path = None
#     for path in gradle_paths:
#         if os.path.exists(path):
#             gradle_path = path
#             break
#
#     # لو مفيش أي ملف منهم
#     if not gradle_path:
#         print("❌ لم يتم العثور على build.gradle أو build.gradle.kts")
#         print("ℹ️ تأكد أنك داخل مجلد مشروع Flutter الصحيح")
#         return False
#
#     print(f"📄 جاري قراءة الملف: {gradle_path}")
#
#     is_kts = gradle_path.endswith(".kts")
#
#     with open(gradle_path, 'r', encoding='utf-8') as f:
#         original_content = f.read()
#
#     # التحقق إذا كان التكوين موجود بالفعل
#     if "keystoreProperties" in original_content and "signingConfigs" in original_content:
#         print_info("build.gradle محدث بالفعل ✓")
#         return True
#
#     print_info("جاري تعديل build.gradle...")
#     content = original_content
#
#     # ============================================
#     # الخطوة 1: إضافة تحميل keystore properties
#     # ============================================
#
#     if is_kts:
#         keystore_loader = """
#             // ============================================
#             // تحميل إعدادات Android Keystore (Kotlin DSL)
#             # // تم الإضافة تلقائياً بواسطة setup_keystore.py
#             // ============================================
#             import java.util.Properties
#             import java.io.FileInputStream
#
#             val keystorePropertiesFile = rootProject.file("../necessary_files/key.properties")
#             val keystoreProperties = Properties()
#
#             if (keystorePropertiesFile.exists()) {
#                 keystoreProperties.load(FileInputStream(keystorePropertiesFile))
#             }
#
#             """
#     else:
#         keystore_loader = """
#             // ============================================
#             // تحميل إعدادات Android Keystore (Groovy DSL)
#             # // تم الإضافة تلقائياً بواسطة setup_keystore.py
#             // ============================================
#             def keystoreProperties = new Properties()
#             def keystorePropertiesFile = rootProject.file('../necessary_files/key.properties')
#             if (keystorePropertiesFile.exists()) {
#                 keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
#             }
#
#             """
#         # أضف قبل "android {"
#     import re
#
#     # ابحث عن android { مع مراعاة المسافات
#     android_pattern = r'(\napply.*\n.*\n)(android\s*\{)'
#
#     if re.search(android_pattern, content):
#         content = re.sub(
#             android_pattern,
#             r'\1' + keystore_loader + r'\2',
#             content,
#             count=1
#         )
#         print_success("✓ تم إضافة: تحميل keystore properties")
#     else:
#         # محاولة بديلة: ابحث عن android { مباشرة
#         if 'android {' in content:
#             content = content.replace('android {', keystore_loader + 'android {', 1)
#             print_success("✓ تم إضافة: تحميل keystore properties (طريقة بديلة)")
#         else:
#             print_error("✗ لم يتم العثور على 'android {' في build.gradle")
#             return False
#
#     # ============================================
#     # الخطوة 2: إضافة signingConfigs
#     # ============================================
#     if is_kts:
#         signing_configs = """
#     // ============================================
#     // إعدادات التوقيع (Kotlin DSL)
#     #     // تم الإضافة تلقائياً بواسطة setup_keystore.py
#     // ============================================
#     signingConfigs {
#         create("release") {
#             if (keystorePropertiesFile.exists()) {
#                 keyAlias = keystoreProperties["keyAlias"] as String
#                 keyPassword = keystoreProperties["keyPassword"] as String
#                 storeFile = file(keystoreProperties["storeFile"] as String)
#                 storePassword = keystoreProperties["storePassword"] as String
#             }
#         }
#     }
#     """
#     else:
#         signing_configs = """
#     // ============================================
#     // إعدادات التوقيع (Groovy DSL)
#     #     // تم الإضافة تلقائياً بواسطة setup_keystore.py
#     // ============================================
#     signingConfigs {
#         release {
#             if (keystorePropertiesFile.exists()) {
#                 keyAlias keystoreProperties['keyAlias']
#                 keyPassword keystoreProperties['keyPassword']
#                 storeFile keystoreProperties['storeFile'] ? file(keystoreProperties['storeFile']) : null
#                 storePassword keystoreProperties['storePassword']
#             }
#         }
#     }
#     """
#
#     # ابحث عن defaultConfig { وأضف بعدها
#     default_config_pattern = r'(defaultConfig\s*\{[^}]*\})'
#
#     if re.search(default_config_pattern, content, re.DOTALL):
#         # أضف signingConfigs بعد defaultConfig block
#         content = re.sub(
#             r'(\n\s*\})\s*\n(\s*)(buildTypes|\n)',
#             r'\1\n\n' + signing_configs + r'\2\3',
#             content,
#             count=1
#         )
#         print_success("✓ تم إضافة: signingConfigs block")
#     else:
#         print("⚠ لم يتم العثور على defaultConfig، جاري المحاولة بطريقة أخرى...")
#
#         # محاولة بديلة: أضف قبل buildTypes
#         if 'buildTypes {' in content:
#             content = content.replace('buildTypes {', signing_configs + '    buildTypes {', 1)
#             print_success("✓ تم إضافة: signingConfigs block (طريقة بديلة)")
#         else:
#             print_error("✗ لم يتم العثور على 'buildTypes'")
#             return False
#     # ============================================
#     # الخطوة 3: تحديث release buildType (تصحيح regex)
#     # ============================================
#
#     print_info("جاري تحديث release block...")
#
#     # الأنماط المحتملة لـ release block
#     release_patterns = [
#         r'getByName\("release"\)\s*\{',  # Kotlin DSL
#         r'release\s*\{'  # Groovy DSL
#     ]
#
#     found_release = False
#     for pattern in release_patterns:
#         match = re.search(pattern, content)
#         if match:
#             found_release = True
#
#             # نحذف أي signingConfig قديم سواء فيه debug أو غيره
#             if is_kts:
#                 # Kotlin DSL
#                 content = re.sub(
#                     r'signingConfig\s*=\s*signingConfigs\.getByName\(".*?"\)',
#                     'signingConfig = signingConfigs.getByName("release")',
#                     content
#                 )
#             else:
#                 # Groovy DSL
#                 content = re.sub(
#                     r'signingConfig\s+signingConfigs\.\w+',
#                     'signingConfig signingConfigs.release',
#                     content
#                 )
#
#             print_success("✓ تم تحديث signingConfig داخل release block")
#
#             # لو مفيش signingConfig إطلاقًا، ضيفه
#             if not re.search(r'signingConfig', content):
#                 content = re.sub(
#                     pattern,
#                     lambda m: m.group(0) + (
#                         '\n            signingConfig = signingConfigs.getByName("release")'
#                         if is_kts else '\n            signingConfig signingConfigs.release'
#                     ),
#                     content,
#                     count=1
#                 )
#                 print_success("✓ تم إضافة signingConfig داخل release block")
#
#     if not found_release:
#         print("⚠️ لم يتم العثور على release block داخل buildTypes")
#     # ============================================
#     # الخطوة 5: حفظ الملف المعدل
#     # ============================================
#
#     # إنشاء نسخة احتياطية
#     backup_path = f"{gradle_path}.backup"
#     with open(backup_path, 'w', encoding='utf-8') as f:
#         f.write(original_content)
#     print_info(f"✓ تم إنشاء نسخة احتياطية: {backup_path}")
#
#     # حفظ الملف المعدل
#     with open(gradle_path, 'w', encoding='utf-8') as f:
#         f.write(content)
#
#     print_success("=" * 60)
#     print_success("🎉 تم تعديل build.gradle بنجاح!")
#     print_success("=" * 60)
#     print_info("التعديلات المضافة:")
#     print_info("  ✓ تحميل keystore properties")
#     print_info("  ✓ signingConfigs block")
#     print_info("  ✓ ربط release build بالتوقيع")
#     print_info("  ✓ minifyEnabled و shrinkResources")
#     print_info("")
#     print_info("النسخة الاحتياطية: android/app/build.gradle.backup")
#
#     return True


def check_and_backup_firebase_files():
    """التحقق من ملفات Firebase ونسخها إلى necessary_files"""
    print_header("🔥 التحقق من ملفات Firebase")

    firebase_files = {
        "android": {
            "path": "android/app/google-services.json",
            "name": "google-services.json",
            "description": "Android Firebase Config"
        },
        "ios": {
            "path": "ios/Runner/GoogleService-Info.plist",
            "name": "GoogleService-Info.plist",
            "description": "iOS Firebase Config"
        }
    }

    found_files = []

    for platform, info in firebase_files.items():
        file_path = info["path"]

        if os.path.exists(file_path):
            print_success(f"تم العثور على: {info['description']}")

            # نسخ الملف إلى necessary_files
            dest_path = os.path.join(CONFIG["keystore_dir"], info["name"])

            try:
                import shutil
                shutil.copy2(file_path, dest_path)
                print_success(f"✓ تم نسخ: {info['name']} → necessary_files/")
                found_files.append({
                    "platform": platform,
                    "name": info["name"],
                    "original": file_path,
                    "backup": dest_path
                })
            except Exception as e:
                print_error(f"فشل نسخ {info['name']}: {e}")
        else:
            print_info(f"غير موجود: {info['description']}")

    if found_files:
        print_success(f"تم نسخ {len(found_files)} من ملفات Firebase")

        # إنشاء ملف معلومات Firebase البسيط
        create_firebase_info_simple(found_files)

        # تحديث .gitignore لحماية ملفات Firebase
        update_gitignore_for_firebase()

        return True
    else:
        print_info("لم يتم العثور على ملفات Firebase")
        print_info("إذا كنت تستخدم Firebase، تأكد من:")
        print_info("  • تشغيل: flutterfire configure")
        print_info("  • وجود الملفات في المسارات الصحيحة")
        return False


def create_firebase_info_simple(files):
    """إنشاء ملف معلومات Firebase بسيط"""
    info_path = os.path.join(CONFIG["keystore_dir"], "firebase-info.txt")

    from datetime import datetime

    content = f"""{'=' * 60}
نسخ احتياطي لملفات Firebase
{'=' * 60}

تم نسخ ملفات Firebase التالية إلى مجلد necessary_files:

"""

    for file_info in files:
        content += f"""
Platform: {file_info['platform'].upper()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 اسم الملف: {file_info['name']}
📍 المسار الأصلي: {file_info['original']}
💾 النسخة الاحتياطية: {file_info['backup']}

"""

    content += f"""
{'=' * 60}
ملاحظات مهمة
{'=' * 60}

⚠️  هذه الملفات تحتوي على API Keys خاصة بـ Firebase
⚠️  تم إضافتها إلى .gitignore تلقائياً (محمية من Git)
⚠️  احفظ نسخة احتياطية في مكان آمن

{'=' * 60}
تاريخ النسخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'=' * 60}
"""

    with open(info_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print_success(f"تم إنشاء: {info_path}")


def update_gitignore_for_firebase():
    """تحديث .gitignore لحماية ملفات Firebase"""
    firebase_ignore_lines = [
        "\n# Firebase configuration files backup",
        f"{CONFIG['keystore_dir']}/google-services.json",
        f"{CONFIG['keystore_dir']}/GoogleService-Info.plist",
        f"{CONFIG['keystore_dir']}/firebase-info.txt",
    ]

    gitignore_path = ".gitignore"

    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            existing_content = f.read()

        # أضف فقط السطور غير الموجودة
        lines_to_add = [line for line in firebase_ignore_lines
                        if line.strip() and line not in existing_content]

        if lines_to_add:
            with open(gitignore_path, 'a', encoding='utf-8') as f:
                f.write('\n'.join(lines_to_add))
            print_success("✓ تم تحديث .gitignore لحماية ملفات Firebase")

    # تحديث necessary_files/.gitignore أيضاً
    ness_gitignore_path = os.path.join(CONFIG["keystore_dir"], ".gitignore")

    if os.path.exists(ness_gitignore_path):
        with open(ness_gitignore_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if "google-services.json" not in content:
            with open(ness_gitignore_path, 'a', encoding='utf-8') as f:
                f.write("\n# Firebase configuration files\n")
                f.write("google-services.json\n")
                f.write("GoogleService-Info.plist\n")
                f.write("firebase-info.txt\n")
            print_success("✓ تم تحديث necessary_files/.gitignore")


def check_firebase_connection():
    """التحقق من اتصال المشروع بـ Firebase"""
    print_header("🔍 فحص اتصال Firebase")

    # التحقق من pubspec.yaml
    pubspec_path = "pubspec.yaml"

    if not os.path.exists(pubspec_path):
        print("pubspec.yaml غير موجود!")
        return False

    with open(pubspec_path, 'r', encoding='utf-8') as f:
        pubspec_content = f.read()

    # البحث عن Firebase packages
    firebase_packages = [
        "firebase_core",
        "firebase_auth",
        "firebase_analytics",
        "firebase_messaging",
        "cloud_firestore",
        "firebase_storage"
    ]

    found_packages = [pkg for pkg in firebase_packages if pkg in pubspec_content]

    if found_packages:
        print_success(f"تم العثور على {len(found_packages)} من حزم Firebase:")
        for pkg in found_packages:
            print_info(f"  • {pkg}")
        return True
    else:
        print_info("لم يتم العثور على حزم Firebase في pubspec.yaml")
        return False
    """إنشاء ملف JSON للتأكد من اكتمال الإعداد"""
    setup_path = os.path.join(config["keystore_dir"], ".setup_complete")

    from datetime import datetime

    data = {
        "setup_completed": True,
        "setup_date": datetime.now().isoformat(),
        "keystore_name": config["keystore_name"],
        "key_alias": config["key_alias"],
        "version": "1.0"
    }

    with open(setup_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print_success("تم إنشاء: .setup_complete")


# ============================================
# البرنامج الرئيسي
# ============================================

def main():
    print_header("🔐 إعداد Android Keystore التلقائي")

    # التحقق من وجود keytool
    print_info("جاري التحقق من keytool...")
    if not check_keytool():
        print_error("keytool غير موجود!")
        print_info("تأكد من تثبيت Java JDK")
        print_info("Windows: أضف Java/bin إلى PATH")
        sys.exit(1)
    print_success("keytool موجود ✓")

    # إنشاء المجلد
    print_info(f"جاري إنشاء المجلد: {CONFIG['keystore_dir']}")
    create_directory(CONFIG["keystore_dir"])

    # التحقق من وجود Keystore
    keystore_path = os.path.join(CONFIG["keystore_dir"], CONFIG["keystore_name"])

    if keystore_exists(keystore_path):
        print_info("Keystore موجود بالفعل!")
        response = input("هل تريد إنشاء واحد جديد؟ (سيحذف القديم) [y/N]: ")
        if response.lower() != 'y':
            print_info("تم الإلغاء")
            sys.exit(0)
        os.remove(keystore_path)

    # إنشاء Keystore
    print_header("📦 إنشاء Keystore")
    keystore_password, key_password = generate_keystore(CONFIG)

    # إنشاء الملفات المساعدة
    print_header("📝 إنشاء الملفات المساعدة")
    create_key_properties(CONFIG, keystore_password, key_password)
    create_key_properties_template(CONFIG)
    create_keystore_info(CONFIG, keystore_password, key_password)
    create_github_secrets_guide(CONFIG, keystore_password, key_password)
    # create_setup_complete_json(CONFIG)

    # تحديث .gitignore
    print_header("🔒 تحديث .gitignore")
    # update_gitignore(CONFIG)
    # create_necessary_files_gitignore(CONFIG)

    # التحقق من Firebase ونسخ الملفات
    firebase_connected = check_firebase_connection()
    firebase_files = []

    if firebase_connected:
        has_firebase = check_and_backup_firebase_files()
        if has_firebase:

            # إضافة Firebase للـ GitHub Secrets guide
            firebase_files_info = []
            if os.path.exists(os.path.join(CONFIG["keystore_dir"], "google-services.json")):
                firebase_files_info.append({
                    "platform": "android",
                    "name": "google-services.json",
                    "backup": os.path.join(CONFIG["keystore_dir"], "google-services.json")
                })
            if os.path.exists(os.path.join(CONFIG["keystore_dir"], "GoogleService-Info.plist")):
                firebase_files_info.append({
                    "platform": "ios",
                    "name": "GoogleService-Info.plist",
                    "backup": os.path.join(CONFIG["keystore_dir"], "GoogleService-Info.plist")
                })

    # تحديث build.gradle
    print_header("🔧 تحديث Android Build Configuration")
    gradle_success = update_android_build_gradle()

    if not gradle_success:
        print("⚠️  فشل تحديث build.gradle!")
        print_info("يمكنك تعديله يدوياً لاحقاً")
        print_info("راجع: build.gradle (مثال) في الملف المرفق")

    # النتيجة النهائية
    print_header("✅ اكتمل الإعداد!")
    print_success("تم إنشاء جميع الملفات بنجاح!")

    print("\n" + "=" * 60)
    print("📋 الخطوات التالية:")
    print("=" * 60)
    print("1. راجع الملفات في:", CONFIG["keystore_dir"])
    print("2. افتح: keystore-info.txt (احفظ كلمات المرور)")
    print("3. افتح: github-secrets-guide.txt (انسخ الـ secrets)")
    print("4. أضف الـ secrets إلى GitHub")

    if firebase_connected and has_firebase:
        print("5. 🔥 راجع: firebase-info.txt (ملفات Firebase محفوظة)")
        print("6. لاستعادة Firebase: شغل restore_firebase.sh/.bat")
        print("7. لا تضف الملفات الحساسة إلى Git!")
        print("8. اعمل نسخة احتياطية من الـ Keystore!")
    else:
        print("5. لا تضف الملفات الحساسة إلى Git!")
        print("6. اعمل نسخة احتياطية من الـ Keystore!")

    print("=" * 60)

    print("\n" + "=" * 60)
    print("⚠️  تحذيرات مهمة:")
    print("=" * 60)
    print("• لا تفقد الـ Keystore! ستحتاجه لتحديث التطبيق")
    print("• اعمل نسخة احتياطية في مكان آمن")
    print("• لا تشارك كلمات المرور مع أحد")
    print("• تأكد من إضافة الـ secrets إلى GitHub")

    if firebase_connected and has_firebase:
        print("• 🔥 ملفات Firebase محمية من Git تلقائياً")
        print("• 🔥 استخدم سكريبتات الاستعادة عند الحاجة")

    print("=" * 60)

    # ملخص الملفات المنشأة
    print("\n" + "=" * 60)
    print("📦 الملفات المنشأة:")
    print("=" * 60)
    print("✓ upload-keystore.jks")
    print("✓ key.properties")
    print("✓ keystore-info.txt")
    print("✓ github-secrets-guide.txt")
    print("✓ key.properties")
    print("✓ .gitignore")
    print("✓ android/app/build.gradle (معدل)")
    print("✓ android/app/build.gradle.backup")

    if firebase_connected and has_firebase:
        print("\n🔥 ملفات Firebase:")
        if os.path.exists(os.path.join(CONFIG["keystore_dir"], "google-services.json")):
            print("✓ google-services.json (نسخة احتياطية)")
        if os.path.exists(os.path.join(CONFIG["keystore_dir"], "GoogleService-Info.plist")):
            print("✓ GoogleService-Info.plist (نسخة احتياطية)")
        print("✓ firebase-info.txt")
        print("✓ restore_firebase.sh")
        print("✓ restore_firebase.bat")

    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ تم الإلغاء بواسطة المستخدم")
        sys.exit(1)
    except Exception as e:
        print_error(f"خطأ غير متوقع: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
