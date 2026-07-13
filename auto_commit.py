import os
import datetime
import random
import subprocess
import sys
import time

FILE_NAME = "activity_log.txt"

COMMIT_MESSAGES = [
    "Refactor code structure", "Fix minor bug", "Update documentation",
    "Clean up unused variables", "Optimize performance", "Add comments for clarity",
    "Update dependencies", "Fix typo in comments", "Improve error handling",
    "Tweak UI styles", "Resolve merge conflicts", "Format code style",
    "Initial work on new feature", "WIP: API integration", "Hotfix: resolve crash"
]

ISSUE_TITLES = [
    "Bug: Memory leak in background process", "Feature Request: Add dark mode toggle",
    "Investigate high CPU usage", "Update outdated dependencies", 
    "Fix responsive layout on mobile", "Database query optimization needed",
    "Write unit tests for authentication module"
]

ISSUE_BODIES = [
    "This issue needs to be addressed before the next release.",
    "I will look into this when I have some free time this week.",
    "Reported by a user. Needs immediate attention.",
    "Just a reminder to clean up this part of the codebase."
]

def run_command(command, env=None):
    try:
        current_env = os.environ.copy()
        if env:
            current_env.update(env)
        subprocess.run(command, check=True, shell=False, capture_output=True, env=current_env)
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(command)}: {e}")
        sys.exit(1)

def human_behavior_decision():
    """الگوریتم تصمیم‌گیری بر اساس رفتار واقعی انسان‌ها"""
    today = datetime.datetime.now()
    
    # 1. شانس مرخصی یا مریضی (5% احتمال در هر روز)
    if random.randint(1, 100) <= 5:
        return False, "Taking a sick day or vacation! No coding today."

    # 2. بررسی روزهای هفته (0 دوشنبه است، 5 شنبه و 6 یکشنبه)
    is_weekend = today.weekday() >= 5
    is_friday = today.weekday() == 4

    if is_weekend:
        # آخر هفته‌ها انسان‌ها معمولا استراحت می‌کنند (فقط 15% شانس کار)
        work_chance = 15
    elif is_friday:
        # جمعه‌ها حس و حال کار کمتر است (60%)
        work_chance = 60
    else:
        # روزهای عادی وسط هفته شانس بالایی برای کار وجود دارد (85%)
        work_chance = 85

    if random.randint(1, 100) <= work_chance:
        return True, "Regular work day. Feeling productive."
    else:
        return False, "Just didn't feel like coding today. Taking it easy."

def generate_working_hours_times(num_commits):
    """تولید زمان‌های کامیت در بازه ساعات کاری طبیعی (مثلا 10 صبح تا 6 عصر)"""
    now = datetime.datetime.now()
    
    # تنظیم شروع کار از ساعت 10 صبح و پایان در 6 عصر
    start_work = now.replace(hour=10, minute=0, second=0, microsecond=0)
    end_work = now.replace(hour=18, minute=0, second=0, microsecond=0)
    
    if now < end_work:
        end_work = now # اگر هنوز به 6 عصر نرسیدیم، نهایتا تا همین الان کامیت بزند
        
    time_diff_seconds = int((end_work - start_work).total_seconds())
    if time_diff_seconds <= 0:
        time_diff_seconds = 3600 # حداقل یک ساعت بازه زمانی
        
    times = []
    for _ in range(num_commits):
        random_seconds = random.randint(0, time_diff_seconds)
        commit_time = start_work + datetime.timedelta(seconds=random_seconds)
        times.append(commit_time)
        
    # مرتب‌سازی زمان‌ها از صبح تا عصر تا در تاریخچه گیت منطقی باشد
    return sorted(times)

def manage_issues():
    """مدیریت تسک‌ها فقط وقتی انجام می‌شود که برنامه‌نویس در حال کار باشد"""
    if random.randint(1, 100) > 30: # 30% شانس رسیدگی به Issue ها در روز کاری
        return

    if random.randint(1, 100) <= 60:
        # ساخت Issue جدید
        title = f"{random.choice(ISSUE_TITLES)} (#{random.randint(100,999)})"
        body = random.choice(ISSUE_BODIES)
        cmd = ["gh", "issue", "create", "--title", title, "--body", body]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"Created a new issue: {title}")
        except Exception:
            pass
    else:
        # بستن یک Issue قدیمی
        cmd = ["gh", "issue", "list", "--state", "open", "--json", "number", "-q", ".[].number"]
        try:
            res = subprocess.run(cmd, check=True, capture_output=True, text=True)
            issue_numbers = res.stdout.strip().split('\n')
            if issue_numbers and issue_numbers[0]: 
                issue_to_close = random.choice(issue_numbers)
                subprocess.run(["gh", "issue", "close", str(issue_to_close)], check=True, capture_output=True)
                print(f"Closed issue #{issue_to_close}")
        except Exception:
            pass

def main():
    # مرحله اول: تصمیم‌گیری انسانی که آیا امروز کار کنیم یا نه؟
    will_work, reason = human_behavior_decision()
    print(f"Decision: {reason}")
    
    if not will_work:
        sys.exit(0) # خروج بدون ارور و بدون ثبت هیچ کامیتی

    # مرحله دوم: اگر قرار است کار کنیم، چند تا کامیت بزنیم؟
    # وزن‌ها: روز معمولی (1تا3 کامیت) پرکاربردتر است. روزهای سنگین (تا 12 کامیت) نادرتر هستند.
    weights = [45, 30, 15, 7, 3]
    categories = [(1, 2), (3, 5), (6, 8), (9, 10), (11, 12)]
    chosen_category = random.choices(categories, weights=weights, k=1)[0]
    num_commits = random.randint(chosen_category[0], chosen_category[1])
    
    print(f"Active day! Making {num_commits} commits during office hours.")

    # مدیریت Issue ها قبل از شروع کدنویسی
    manage_issues()

    commit_times = generate_working_hours_times(num_commits)

    for i in range(num_commits):
        commit_time = commit_times[i]
        formatted_time = commit_time.strftime('%Y-%m-%dT%H:%M:%S')
        
        env_vars = {
            'GIT_AUTHOR_DATE': formatted_time,
            'GIT_COMMITTER_DATE': formatted_time
        }
        
        commit_message = random.choice(COMMIT_MESSAGES)
        unique_id = random.randint(1000, 9999) 
        
        with open(FILE_NAME, "a") as file:
            file.write(f"Contribution logged at {formatted_time} (Hash: {unique_id})\n")
        
        run_command(["git", "add", FILE_NAME])
        run_command(["git", "commit", "-m", f"{commit_message} (#{unique_id})"], env=env_vars)
        
        time.sleep(0.1) # یک مکث کوتاه بین ثبت دستورات
        
    print("Workday finished successfully.")

if __name__ == "__main__":
    main()
