import os

gradle_path = "android/app/build.gradle"
gradle_path = "android/app/build.gradle.kts"

if not os.path.exists(gradle_path):
    print(f"لم يتم العثور على: {gradle_path}")
    print("تأكد أنك في مجلد Flutter project الصحيح")
