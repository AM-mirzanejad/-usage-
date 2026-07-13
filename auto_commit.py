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
    "Initial work on new feature", "WIP: API integration", "Hotfix: resolve crash",
    "Update README.md", "Remove dead code"
]

QUICK_FIX_MESSAGES = [
    "Oops, fix typo", "Missed a semicolon", "Fix linter error",
    "Quick formatting fix", "Forgot to save file before commit"
]

PR_COMMENTS = [
    "LGTM! 🚀", "Tested locally, everything works fine.", 
    "Great work on this feature.", "Code review passed. Merging now.",
    "Thanks for the fix!"
]

CO_AUTHORS = [
    "Co-authored-by: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>",
    "Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>"
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

BRANCH_NAMES = [
    "feature/dark-mode", "hotfix/memory-leak", "refactor/auth-module",
    "feature/api-integration", "bugfix/mobile-ui", "docs/update-readme"
]

def run_command(command, env=None):
    try:
        current_env = os.environ.copy()
        if env:
            current_env.update(env)
        subprocess.run(command, check=True, shell=False, capture_output=True, text=True, env=current_env)
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(command)}: {e.stderr}")
        sys.exit(1)

def human_behavior_decision():
    """الگوریتم تصمیم‌گیری با در نظر گرفتن شب‌بیداری‌ها و تعطیلات"""
    today = datetime.datetime.now()
    
    if random.randint(1, 100) <= 5:
        return False, "Taking a sick day or vacation! No coding today."

    is_weekend = today.weekday() >= 5
    is_friday = today.weekday() == 4

    if is_weekend:
        work_chance = 15
    elif is_friday:
        work_chance = 60
    else:
        work_chance = 85

    if random.randint(1, 100) <= work_chance:
        return True, "Regular work day. Feeling productive."
    else:
        return False, "Just didn't feel like coding today. Taking it easy."

def generate_working_hours_times(num_commits):
    now = datetime.datetime.now()
    
    # 10% احتمال دارد برنامه‌نویس شب‌بیدار (Night Owl) باشد
    is_night_owl = random.randint(1, 100) <= 10
    
    if is_night_owl:
        print("🦉 Night owl mode activated! Coding at midnight.")
        start_work = now.replace(hour=23, minute=0, second=0, microsecond=0) - datetime.timedelta(days=1)
        end_work = now.replace(hour=3, minute=0, second=0, microsecond=0)
    else:
        start_work = now.replace(hour=10, minute=0, second=0, microsecond=0)
        end_work = now.replace(hour=18, minute=0, second=0, microsecond=0)
    
    if now < end_work and not is_night_owl:
        end_work = now 
        
    time_diff_seconds = int((end_work - start_work).total_seconds())
    if time_diff_seconds <= 0:
        time_diff_seconds = 3600 
        
    times = []
    i = 0
    while i < num_commits:
        random_seconds = random.randint(0, time_diff_seconds)
        commit_time = start_work + datetime.timedelta(seconds=random_seconds)
        times.append((commit_time, False)) # False یعنی یک کامیت معمولی است
        
        # الگوی "کامیت جا مانده" (Quick Fix) - 15% شانس
        # یک کامیت دقیقا 1 دقیقه بعد از کامیت قبلی زده می شود تا خطاهای انسانی را نشان دهد
        if random.randint(1, 100) <= 15 and i + 1 < num_commits:
            quick_fix_time = commit_time + datetime.timedelta(seconds=random.randint(30, 120))
            times.append((quick_fix_time, True)) # True یعنی این یک کامیت سریع و رفع باگ است
            i += 1 # یک کامیت اضافه مصرف شد
            
        i += 1
        
    return sorted(times, key=lambda x: x[0])

def manage_issues():
    if random.randint(1, 100) > 30: 
        return

    if random.randint(1, 100) <= 60:
        title = f"{random.choice(ISSUE_TITLES)} (#{random.randint(100,999)})"
        body = random.choice(ISSUE_BODIES)
        run_command(["gh", "issue", "create", "--title", title, "--body", body])
        print(f"Created a new issue: {title}")
    else:
        try:
            res = subprocess.run(["gh", "issue", "list", "--state", "open", "--json", "number", "-q", ".[].number"], check=True, capture_output=True, text=True)
            issue_numbers = res.stdout.strip().split('\n')
            if issue_numbers and issue_numbers[0]: 
                issue_to_close = random.choice(issue_numbers)
                run_command(["gh", "issue", "close", str(issue_to_close)])
                print(f"Closed issue #{issue_to_close}")
        except Exception:
            pass

def manage_pull_requests_and_releases(unique_id):
    if random.randint(1, 100) <= 15:
        branch_name = f"{random.choice(BRANCH_NAMES)}-{unique_id}"
        pr_title = f"Implement {branch_name.split('/')[0]} for #{unique_id}"
        
        try:
            print(f"Starting Pull Request workflow on branch: {branch_name}")
            run_command(["git", "checkout", "-b", branch_name])
            
            with open(FILE_NAME, "a") as file:
                file.write(f"PR commit logged (Hash: {unique_id})\n")
            run_command(["git", "add", FILE_NAME])
            run_command(["git", "commit", "-m", f"Prepare code for {branch_name}"])
            
            run_command(["git", "push", "--set-upstream", "origin", branch_name])
            
            # ایجاد Pull Request
            run_command(["gh", "pr", "create", "--title", pr_title, "--body", "Automated PR created to fix the issue.", "--head", branch_name, "--base", "main"])
            time.sleep(3) 
            
            # ثبت یک کامنت برنامه نویسانه در PR قبل از مرج کردن (بسیار طبیعی)
            pr_comment = random.choice(PR_COMMENTS)
            run_command(["gh", "pr", "comment", branch_name, "--body", pr_comment])
            time.sleep(2)
            
            run_command(["gh", "pr", "merge", branch_name, "--merge", "--delete-branch"])
            print("Pull Request merged successfully! 🦈")
            
            run_command(["git", "checkout", "main"])
            run_command(["git", "pull", "origin", "main"])
        except Exception as e:
            print(f"PR flow failed, recovering... {e}")
            run_command(["git", "checkout", "main"])

    if random.randint(1, 100) <= 5:
        version = f"v{random.randint(1,5)}.{random.randint(0,9)}.{random.randint(0,9)}"
        try:
            print(f"Drafting a new release: {version}")
            run_command(["gh", "release", "create", version, "--title", f"Release {version}", "--notes", f"Bug fixes and performance improvements in {version}."])
        except Exception:
            pass

def main():
    will_work, reason = human_behavior_decision()
    print(f"Decision: {reason}")
    
    if not will_work:
        sys.exit(0)

    weights = [45, 30, 15, 7, 3]
    categories = [(1, 2), (3, 5), (6, 8), (9, 10), (11, 12)]
    chosen_category = random.choices(categories, weights=weights, k=1)[0]
    num_commits = random.randint(chosen_category[0], chosen_category[1])
    
    print(f"Active day! Preparing to make {num_commits} commits.")

    manage_issues()
    unique_id = random.randint(1000, 9999)
    manage_pull_requests_and_releases(unique_id)

    commit_data = generate_working_hours_times(num_commits)

    for i in range(num_commits):
        if i >= len(commit_data):
            break
            
        commit_time, is_quick_fix = commit_data[i]
        formatted_time = commit_time.strftime('%Y-%m-%dT%H:%M:%S')
        
        env_vars = {
            'GIT_AUTHOR_DATE': formatted_time,
            'GIT_COMMITTER_DATE': formatted_time
        }
        
        current_unique_id = random.randint(1000, 9999)
        
        # انتخاب پیام کامیت و بررسی اینکه آیا این یک کامیت "سوتی" است یا خیر
        if is_quick_fix:
            base_message = random.choice(QUICK_FIX_MESSAGES)
        else:
            base_message = random.choice(COMMIT_MESSAGES)
            
        # 20% شانس برای Pair Programming (اضافه کردن Co-author برای گرفتن بج Pair Extraordinaire)
        full_message = f"{base_message} (#{current_unique_id})"
        if random.randint(1, 100) <= 20:
            co_author = random.choice(CO_AUTHORS)
            full_message += f"\n\n{co_author}"
            print("👯 Pair Extraordinaire mode! Added a co-author.")
        
        with open(FILE_NAME, "a") as file:
            file.write(f"Contribution logged at {formatted_time} (Hash: {current_unique_id})\n")
        
        run_command(["git", "add", FILE_NAME])
        run_command(["git", "commit", "-m", full_message], env=env_vars)
        
        time.sleep(0.2)
        
    print("Workday finished successfully.")

if __name__ == "__main__":
    main()
