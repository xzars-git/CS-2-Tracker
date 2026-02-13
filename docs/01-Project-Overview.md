# 01 - Project Overview

**CS2 Trading Tracker - Complete PROJECT Goals & Features**

---

## 1.1 Project Goals

### Primary Goals:
- ✅ **Track CS2 inventory value** in real-time
- ✅ **Calculate accurate P&L** (Profit & Loss) for all trades
- ✅ **Sync 1+ year** of trade history automatically
- ✅ **Support multiple Steam accounts**
- ✅ **100% FREE** - No paid API services required

### Target Users:
- Active CS2 traders (10+ trades/week)
- Skin flippers (buy low, sell high)
- Long-term investors (track appreciation)
- Multi-account traders

---

## 1.2 Key Features Breakdown

### **Phase 1: MVP (Minimum Viable Product)**
*Timeline: Week 1-2*

1. **Steam OAuth login** ✅
2. **Fetch current inventory** ✅
3. **Display inventory value** (real-time prices from CSFloat) ✅
4. **Basic dashboard UI** ✅

**Goal:** User dapat login dan melihat inventory mereka dengan harga real-time.

---

### **Phase 2: Core Features**
*Timeline: Week 3-4*

5. **Trade history sync** (1 year back) ✅
6. **P&L calculation** (FIFO + unique token tracking) ✅
7. **Inventory value over time** (line chart) ✅
8. **Multi-account support** ✅

**Goal:** User dapat track profit/loss dari semua trade mereka.

---

### **Phase 3: Advanced Features**
*Timeline: Week 5-6*

9. **AI-based rate limiter** (avoid Steam ban) ✅
10. **Export data** (CSV/JSON) ✅
11. **Price alerts** (Discord/Email notifications) ⏳
12. **Mobile-responsive design** ✅

**Goal:** Polish aplikasi untuk production use.

---

### **Phase 4: Future Enhancements**
*Timeline: TBD*

- **Trade recommendations** (ML model)
- **Portfolio comparison** (vs market)
- **Advanced charts** (Plotly)
- **Dark mode**
- **Multi-language support**

---

## 1.3 Success Metrics

### Performance Targets:
- ⏱️ **Sync 1 year trade history** in <5 minutes
- 🔄 **Update inventory prices** every 5 minutes
- 🚫 **Zero API bans** (smart rate limiting)
- 👤 **Support up to 5 Steam accounts** per user
- ⚡ **Load dashboard** in <2 seconds

### Quality Targets:
- ✅ **100% accurate P&L** calculation
- ✅ **No data loss** during sync
- ✅ **Mobile-responsive** UI
- ✅ **Secure** authentication & data storage

---

## 1.4 Why This Project?

### Problem Statement:
❌ Existing CS2 trading trackers are:
- **Paid** (monthly subscriptions)
- **Limited** (only Steam Market, no CSFloat)
- **Inaccurate** (wrong P&L calculations)
- **Complex** to setup

### Our Solution:
✅ **100% Free** - No paid APIs  
✅ **Accurate** - Uses CSFloat real-time prices  
✅ **Advanced P&L** - FIFO + unique token matching  
✅ **Easy Setup** - Steam OAuth login  
✅ **Multi-account** - Track multiple Steam accounts  

---

## 1.5 Technical Highlights

### Free APIs Used:
1. **Steam Web API** - For inventory & trade history
2. **CSFloat** (scraping) - For real-time prices
3. **Steam Market** (fallback) - Backup pricing

### Unique Features:
- **FIFO Algorithm** for consumables (cases, keys)
- **Unique Token Matching** for skins (float, pattern)
- **Smart Rate Limiting** to avoid API bans
- **Daily Snapshots** for portfolio tracking

---

## Next Steps

✅ **Lanjut ke:** [`02-Tech-Stack.md`](02-Tech-Stack.md) - Pilih teknologi yang digunakan  
✅ **Alternative:** [`03-System-Architecture.md`](03-System-Architecture.md) - Pahami arsitektur sistem

---

**Good luck building your CS2 Tracker! 🚀**
