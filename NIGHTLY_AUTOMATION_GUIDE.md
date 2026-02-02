# 🌙 Nightly Automation Setup Guide

Get fresh alpha plays automatically every morning!

---

## ⚡ Quick Setup (Easiest)

**Just double-click this file:**
```
setup_nightly_schedule.bat
```

**It will ask:**
- What time to run? (Enter like: `06:00` or `18:30`)

**Done!** Bot runs automatically every day at that time.

---

## 🎯 What Happens Automatically

Every night (or morning) at your chosen time:

1. ✅ **Serious bot runs** (scans filtered markets)
2. ✅ **Original bot runs** (scans all markets)
3. ✅ **Reports generated** in `reports/` folder
4. ✅ **Dashboard data updated** (`serious_latest.json` + `original_latest.json`)
5. ✅ **Ready to view** when you wake up!

**You just open the dashboard and see fresh opportunities!**

---

## 📋 Two Setup Options

### **Option 1: Batch File** (Recommended)
```cmd
setup_nightly_schedule.bat
```
- Simplest
- No admin required
- Just works

### **Option 2: PowerShell** (More features)
```powershell
Right-click PowerShell → Run as Administrator
.\setup_nightly_schedule.ps1
```
- Fancier interface
- Better error handling
- Can parse times like "6:00 AM"

---

## ⏰ Recommended Schedule

### **Morning Person:**
- **Time:** 6:00 AM
- **Why:** Fresh data waiting when you wake up
- **Coffee + Alpha = Perfect morning** ☕

### **Night Owl:**
- **Time:** 11:00 PM (23:00)
- **Why:** Data ready before bed, review before sleep
- **Dream about profits** 💭

### **Workday:**
- **Time:** 8:00 AM
- **Why:** Data ready before market opens
- **Trade during lunch break** 📊

---

## 🔧 What You Need

**Before setting up automation:**

1. ✅ **API Key Set Permanently**
   ```powershell
   [System.Environment]::SetEnvironmentVariable("PERPLEXITY_API_KEY", "pplx-yourkey", "User")
   ```
   **Then restart terminal!**

2. ✅ **All Files in Same Folder**
   - LAUNCH_BOTH.bat
   - Both .py bot files
   - dashboard_triple.html
   - setup_nightly_schedule.bat (or .ps1)

3. ✅ **Computer Settings**
   - Computer must be **ON** at scheduled time
   - Or set to **wake from sleep** for scheduled tasks

---

## 📊 Viewing Automated Results

### **Option A: Always-On Dashboard**

**Keep server running 24/7:**
```cmd
REM Terminal 1 - Never close this
cd C:\path\to\bot\reports
python -m http.server 8000

REM Terminal 2 - Automation uses this
REM (Task Scheduler runs the bot here)
```

**Then:**
- Bookmark: `http://localhost:8000/dashboard.html`
- Just refresh browser each morning
- New data loads automatically!

### **Option B: Manual Dashboard Start**

**After bot runs automatically:**
```cmd
cd reports
python -m http.server 8000
start http://localhost:8000/dashboard.html
```

**Or** just run `LAUNCH_BOTH.bat` manually to see results + start server.

---

## 🎯 Complete Workflow

### **Setup (Once):**
1. Run `setup_nightly_schedule.bat`
2. Choose time (e.g., 6:00 AM)
3. Done!

### **Daily (Automatic):**
- 6:00 AM → Bot runs automatically
- 6:05 AM → Reports ready in `reports/` folder

### **Morning (You):**
- Open browser to dashboard
- Review top profit opportunities
- Execute trades
- Make money 💰

---

## 🔍 Verify It's Working

### **Test Run Immediately:**
```cmd
schtasks /run /tn "Polymarket Alpha Bot - Nightly"
```

This runs the task **right now** instead of waiting for scheduled time.

### **Check Task Status:**
```cmd
REM Open Task Scheduler
taskschd.msc
```

Look for: **"Polymarket Alpha Bot - Nightly"**
- Should show: "Ready" status
- Last Run Time: After you test it
- Next Run Time: Your scheduled time

### **Check Logs:**
Look in `reports/` folder:
- New files with today's timestamp = Working! ✅
- Old files only = Not running ❌

---

## ⚙️ Task Scheduler Settings

The automated task is configured to:

✅ **Run daily** at your chosen time
✅ **Run even if missed** (if computer was off)
✅ **Run only if network available** (needs internet for API)
✅ **Stop after 2 hours** (shouldn't take that long)
✅ **Run even on battery** (for laptops)

---

## 🛠️ Troubleshooting

### **Task doesn't run?**

**Check:**
1. Computer was ON at scheduled time?
2. API key is set permanently?
   ```cmd
   echo %PERPLEXITY_API_KEY%
   ```
3. Task exists?
   ```cmd
   schtasks /query /tn "Polymarket Alpha Bot - Nightly"
   ```

**Fix:**
- Set PC to not sleep during scheduled time
- Or enable "Wake computer to run task" in Task Scheduler

### **Bot runs but fails?**

**Check:**
1. API key has credits?
2. Python installed and in PATH?
3. All bot files exist?

**Test manually:**
```cmd
cd C:\path\to\bot
LAUNCH_BOTH.bat
```

If manual works but scheduled doesn't:
- Task might be using wrong directory
- Re-run setup script

### **No new data in dashboard?**

**Check:**
1. Reports folder has new files?
2. Files are `serious_latest.json` and `original_latest.json`?
3. Dashboard pointing to right location?

**Fix:**
```cmd
cd reports
dir *.json
```

Should see files with today's date.

---

## 📝 Useful Commands

```cmd
REM Test run now (don't wait for schedule)
schtasks /run /tn "Polymarket Alpha Bot - Nightly"

REM Check task status
schtasks /query /tn "Polymarket Alpha Bot - Nightly" /fo LIST /v

REM Disable task temporarily
schtasks /change /tn "Polymarket Alpha Bot - Nightly" /disable

REM Enable task
schtasks /change /tn "Polymarket Alpha Bot - Nightly" /enable

REM Delete task (removes automation)
schtasks /delete /tn "Polymarket Alpha Bot - Nightly" /f

REM View all tasks
taskschd.msc
```

---

## 🎊 Success Checklist

After setup, verify:

- [ ] Ran setup script (bat or ps1)
- [ ] Chose a time
- [ ] Task shows in Task Scheduler
- [ ] Tested with `/run` command
- [ ] Reports folder updated
- [ ] Dashboard loads new data
- [ ] API key is permanent (survived terminal restart)
- [ ] Computer settings allow task to run

---

## 💡 Pro Tips

### **Tip 1: Keep Dashboard Open**
- Bookmark `http://localhost:8000/dashboard.html`
- Leave tab open permanently
- Just refresh each morning (F5)

### **Tip 2: Phone Notifications**
Set up a simple email when task completes:
- Use Windows Task Scheduler "Send email" action
- Or use a script to ping your phone

### **Tip 3: Multiple Schedules**
Run bot at **multiple times**:
```cmd
REM Morning scan
setup_nightly_schedule.bat → 6:00 AM

REM Evening scan  
setup_nightly_schedule.bat → 6:00 PM
```

Run setup twice with different times = twice daily scans!

### **Tip 4: Weekend Skip**
Edit task in Task Scheduler:
- Triggers tab → Untick Saturday/Sunday
- Now only runs weekdays

---

## 🚀 Quick Start Summary

**Most people should just do this:**

1. **Setup (30 seconds):**
   ```
   Double-click: setup_nightly_schedule.bat
   Enter time: 06:00
   ```

2. **Test (1 minute):**
   ```cmd
   schtasks /run /tn "Polymarket Alpha Bot - Nightly"
   ```

3. **Verify (30 seconds):**
   ```cmd
   dir reports\*.json
   ```
   See today's files? ✅ Working!

4. **Enjoy!**
   - Go to sleep
   - Wake up to fresh alpha
   - Make money 💰

---

## 📞 Common Questions

**Q: Do I need to keep my computer on?**
A: Yes, or set it to wake for scheduled tasks.

**Q: Can I run it multiple times per day?**
A: Yes! Run setup script again with different time.

**Q: What if I'm traveling?**
A: Set task to disabled temporarily, re-enable when back.

**Q: Does it use a lot of API credits?**
A: ~$0.05-0.10 per run, so ~$3/month for daily runs.

**Q: Can I see the task running?**
A: Yes, a command window will appear briefly.

**Q: How do I stop automation?**
A: `schtasks /delete /tn "Polymarket Alpha Bot - Nightly" /f`

**Q: Can I change the time later?**
A: Yes, just run setup script again.

---

**You're now set up for fully automated alpha hunting!** 🎉

Wake up every morning to fresh opportunities, sorted by profit potential, ready to execute. 🌅💰
