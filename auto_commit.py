import os
import datetime
import random
import subprocess
import sys
import time

FILE_NAME = "activity_log.txt"

# لیستی از پیام‌های طبیعی تا کسی شک نکند که ربات در حال کامیت است
COMMIT_MESSAGES = [
    "Refactor code structure",
    "Fix minor bug",
    "Update documentation",
    "Clean up unused variables",
    "Optimize performance",
    "Add comments for clarity",
    "Update dependencies",
    "Fix typo in comments",
    "Improve error handling",
    "Tweak UI styles",
    "Resolve merge conflicts",
    "Format code style"
]

def run_command(command, env=None):
    """اجرای مستقیم دستورات خط فرمان با قابلیت دریافت متغیرهای محیطی برای دستکاری زمان"""
    try:
        current_env = os.environ.copy()
        if env:
            current_env.update(env) # اضافه کردن زمان جعلی به متغیرهای سیستمی
        subprocess.run(command, check=True, shell=False, capture_output=True, env=current_env)
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(command)}: {e}")
        sys.exit(1)

def generate_random_times(num_commits):
    """تولید زمان‌های تصادفی در طول یک روز (مثلاً بین ساعت ۹ صبح تا ۸ شب)"""
    now = datetime.datetime.now()
    # شروع بازه کاری: ۹ صبح امروز
    start_time = now.replace(hour=9, minute=0, second=0, microsecond=0)
    # پایان بازه کاری: ۸ شب امروز
    end_time = now.replace(hour=20, minute=0, second=0, microsecond=0)
    
    # اگر اسکریپت زودتر از ۸ شب اجرا شد، پایان بازه را همین الان در نظر می‌گیریم
    if now < end_time:
        end_time = now
        
    time_diff_seconds = int((end_time - start_time).total_seconds())
    
    times = []
    for _ in range(num_commits):
        # انتخاب یک ثانیه کاملاً تصادفی در طول روز کاری
        random_seconds = random.randint(0, time_diff_seconds)
        commit_time = start_time + datetime.timedelta(seconds=random_seconds)
        times.append(commit_time)
        
    # مرتب‌سازی زمان‌ها از صبح تا شب تا ترتیب تاریخچه گیت به هم نریزد (بسیار مهم)
    return sorted(times)

def main():
    # 1. تصمیم‌گیری برای اینکه آیا امروز فعالیتی داشته باشیم یا نه (۷۵٪ روزها فعال)
    if random.randint(1, 100) > 75:
        print("Decision: Rest day! No commits will be made today.")
        sys.exit(0)
        
    # 2. تعیین تعداد کامیت‌ها برای ساخت رنگ‌های مختلف
    weights = [40, 30, 20, 10]
    categories = [(1, 3), (4, 7), (8, 11), (12, 15)]
    chosen_category = random.choices(categories, weights=weights, k=1)[0]
    num_commits = random.randint(chosen_category[0], chosen_category[1])
    
    print(f"Active day! Making {num_commits} commits randomly spread across the day.")

    # 3. گرفتن زمان‌های جعلیِ مرتب شده برای امروز
    commit_times = generate_random_times(num_commits)

    with open(FILE_NAME, "a") as f:
        pass

    # 4. حلقه ثبت کامیت‌ها با زمان و پیام متفاوت
    for i in range(num_commits):
        commit_time = commit_times[i]
        # فرمت استاندارد زمان برای گیت
        formatted_time = commit_time.strftime('%Y-%m-%dT%H:%M:%S')
        
        # این دو متغیر محیطی، به گیت می‌گویند تاریخ اصلی را نادیده بگیر و این تاریخ را ثبت کن
        env_vars = {
            'GIT_AUTHOR_DATE': formatted_time,
            'GIT_COMMITTER_DATE': formatted_time
        }
        
        # انتخاب یک پیام برنامه‌نویسانه تصادفی
        commit_message = random.choice(COMMIT_MESSAGES)
        unique_id = random.randint(1000, 9999) 
        
        with open(FILE_NAME, "a") as file:
            file.write(f"Contribution logged at {formatted_time} (Hash: {unique_id})\n")
        
        run_command(["git", "add", FILE_NAME])
        run_command(["git", "commit", "-m", f"{commit_message} (#{unique_id})"], env=env_vars)
        
        time.sleep(0.2)
        
    print("All simulated commits generated beautifully!")

if __name__ == "__main__":
    main()
