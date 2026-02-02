# 🚀 Polymarket Alpha Bot - Complete Setup

**Fresh, clean installation with only essential files!**

---

## 📦 What You're Getting

**5 Essential Files:**
1. `polymarket_alpha_bot.py` - The bot that scans markets
2. `dashboard_triple.html` - Beautiful 3-tab web interface
3. `LAUNCH_SINGLE.bat` - One-click launcher
4. `setup_nightly_single.bat` - Automation setup
5. `requirements.txt` - Python dependencies

**3 Documentation Files:**
6. `SETUP_GUIDE.md` - Quick start (you're reading it!)
7. `COST_OPTIMIZATION.md` - Why single bot saves money
8. `NIGHTLY_AUTOMATION_GUIDE.md` - How to automate

**Total: 8 files. Clean. Simple. Done.** ✨

---

## ⚡ Quick Start (5 Minutes)

### **Step 1: Install Python Dependencies**
```cmd
cd C:\your\bot\folder
pip install requests python-dateutil --break-system-packages
```

### **Step 2: Set API Key (Permanently)**
```powershell
[System.Environment]::SetEnvironmentVariable("PERPLEXITY_API_KEY", "pplx-your-key-here", "User")
```
**Then close and reopen terminal!**

### **Step 3: Test Run**
```cmd
LAUNCH_SINGLE.bat
```

**Dashboard opens automatically!** 🎉

### **Step 4: Setup Nightly Automation (Optional)**
```cmd
setup_nightly_single.bat
> Enter time: 06:00
```

**Done!** Bot runs every morning at 6 AM.

---

## 🎯 What This Bot Does

### **Scans Polymarket Markets**
- Fetches 400+ active prediction markets
- Scores each by profit potential
- Researches top 10 with AI (Perplexity)

### **Generates Reports**
- Creates `reports/original_latest.json`
- Creates `reports/serious_latest.json`
- Saves timestamped backups

### **Beautiful Dashboard**
- **3 Tabs:** All Markets, Serious, Meme
- **Sorted by profit** potential
- **Filter by verdict:** Strong Buy, Buy, Neutral, Pass
- **Auto-refresh:** Updates when bot runs

---

## 💰 Cost

**Per Run:** ~$0.05-0.10 (10 AI research calls)
**Daily:** ~$0.10
**Monthly:** ~$3
**Yearly:** ~$36

**Compare to:** One profitable trade pays for a year! 💎

---

## 📊 How to Use

### **Daily Workflow:**

**Morning:**
1. Open browser → `http://localhost:8000/dashboard.html`
2. Press F5 to refresh
3. See fresh opportunities sorted by profit
4. Execute top plays
5. Make money! 💰

**That's it!**

---

## 🎨 Dashboard Features

### **3 Tabs:**
- 📊 **All Markets** - Everything from the scan
- 🎯 **Serious** - Filtered (no meme markets)
- 🎪 **Meme** - GTA 6, Jesus, celebrities

### **Sorting:**
- Profit Potential (default)
- Confidence
- Edge %
- Liquidity

### **Filtering:**
- All Plays
- Strong Buy (high conviction)
- Buy (good opportunity)
- Neutral (maybe)
- Pass (skip)

### **Each Card Shows:**
- Market question
- Profit score
- Edge percentage
- Confidence level
- Recommended action (BUY YES/NO)
- Key findings
- Risk factors
- Direct trade link

---

## 🔧 File Structure

```
your-bot-folder/
│
├── polymarket_alpha_bot.py          ← The bot
├── dashboard_triple.html            ← The UI
├── LAUNCH_SINGLE.bat                ← Run this
├── setup_nightly_single.bat         ← Setup automation
├── requirements.txt                 ← Dependencies
│
├── SETUP_GUIDE.md                   ← This file
├── COST_OPTIMIZATION.md             ← Why single bot
├── NIGHTLY_AUTOMATION_GUIDE.md      ← Automation help
│
└── reports/                         ← Auto-generated
    ├── dashboard.html              (copied here)
    ├── original_latest.json        (bot data)
    ├── serious_latest.json         (same data, filtered)
    └── alpha_report_*.json         (timestamped backups)
```

---

## 💡 Pro Tips

### **Tip 1: Keep Server Running 24/7**
```cmd
# Terminal 1 - Leave open forever (just minimize)
cd reports
python -m http.server 8000

# Bookmark: http://localhost:8000/dashboard.html
# Just refresh each morning!
```

### **Tip 2: Focus on Top 3-5 Plays**
- Dashboard sorts by profit automatically
- Top card = highest profit potential
- Look for Edge > 10% + Confidence > 70%

### **Tip 3: Check Multiple Tabs**
- Start with All Markets
- Switch to Serious for filtered view
- Check Meme for guaranteed wins (e.g., "Jesus before GTA 6")

### **Tip 4: Use Filters**
- Click "Strong Buy" button
- See only high-conviction plays
- Execute these first

---

## 🎯 What Makes Money

**Look for ALL of these:**
- ✅ Profit Score > 70
- ✅ Edge > 10%
- ✅ Confidence > 70%
- ✅ Liquidity > $50k
- ✅ Verdict: STRONG_BUY or BUY

**Example good play:**
```
Market: Bitcoin reaches $100k by March?
Profit Score: 85.2
Edge: 15.3%
Confidence: 78%
Liquidity: $156k
Verdict: STRONG_BUY
→ BUY YES at 42%
```

**This is money!** 💰

---

## 🔍 Troubleshooting

### **Bot won't run?**
```cmd
# Check Python installed
python --version

# Check API key set
echo %PERPLEXITY_API_KEY%

# Reinstall dependencies
pip install requests python-dateutil --break-system-packages
```

### **Dashboard shows old data?**
```cmd
# Check reports folder
cd reports
dir *.json

# Should see files with today's date
# If not, run bot again:
cd ..
LAUNCH_SINGLE.bat
```

### **Automation not working?**
```cmd
# Verify task exists
schtasks /query /tn "Polymarket Alpha Bot - Single"

# Test run immediately
schtasks /run /tn "Polymarket Alpha Bot - Single"

# Check computer was ON at scheduled time
```

---

## 📞 Common Questions

**Q: Do I need to keep my computer on?**
A: Yes, or set it to wake for scheduled tasks.

**Q: Can I run manually instead of automation?**
A: Yes! Just run `LAUNCH_SINGLE.bat` whenever you want.

**Q: How often should I run it?**
A: Daily is good. Markets change fast!

**Q: What if I run out of API credits?**
A: Add payment method to Perplexity. First $5 is free.

**Q: Can I use this on Mac/Linux?**
A: Yes, but scripts need modification (use .sh instead of .bat).

**Q: Is this better than running both bots?**
A: Yes! Same results, 50% less cost. See COST_OPTIMIZATION.md

---

## ⚙️ Advanced: Customization

### **Change Number of Markets Researched**

Edit `polymarket_alpha_bot.py`, line ~300:
```python
# Change from 10 to whatever you want
max_research=10  # Default
```

### **Change Profit Score Weights**

Edit `dashboard_triple.html`, line ~805:
```javascript
// Current: Edge 50%, Confidence 30%, Liquidity 20%
const profitScore = (edge * 0.5) + (confidence * 0.3) + (liquidityFactor * 100 * 0.2);
```

### **Change Market Filters**

Edit `polymarket_alpha_bot.py`, line ~150:
```python
MIN_LIQUIDITY = 5000    # Minimum liquidity
MIN_VOLUME_24H = 1000   # Minimum volume
MIN_ALPHA_SCORE = 60    # Minimum alpha score
```

---

## 🚀 You're Ready!

**You now have:**
- ✅ Clean setup (8 files only)
- ✅ Cost-optimized (single bot)
- ✅ Beautiful dashboard
- ✅ Automation ready
- ✅ Everything you need to make money

**Next steps:**
1. Run `LAUNCH_SINGLE.bat` to test
2. Setup automation with `setup_nightly_single.bat`
3. Check dashboard each morning
4. Execute profitable trades
5. Make money! 💰

**Good luck hunting alpha!** 🎯📈
