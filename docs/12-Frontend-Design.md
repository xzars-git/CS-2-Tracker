# 12 - Frontend Design

**CS2 Trading Tracker - Dashboard UI Design**

---

## 12.1 Dashboard Layout Wireframe

```
┌─────────────────────────────────────────────────────────────────┐
│  Header                                                          │
│  [Logo]  CS2 Tracker          [Sync] [Accounts ▾] [Logout]      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Stats Cards                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Total Value  │  │ Total P&L    │  │ Total Items  │          │
│  │   $1,234.56  │  │   +$234.56   │  │     142      │          │
│  │   ↑ 12.5%    │  │   ↑ 45.2%    │  │   ↑ 5        │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Inventory Value Over Time                                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                                                          │    │
│  │    [Line Chart: Value vs Date]                          │    │
│  │                                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Current Inventory                                               │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ [Search]  [Filter: All ▾]  [Sort: Value ▾]              │    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │ [Icon] AK-47 | Slate (FT)         Float: 0.164  $7.30   │    │
│  │ [Icon] Glock-18 | Fade (FN)       Float: 0.008  $450.00 │    │
│  │ [Icon] Sticker | device           -              $5.20   │    │
│  │ ...                                                      │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 12.2 HTML Structure

### `frontend/index.html`:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CS2 Tracker - Dashboard</title>
    
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Alpine.js CDN -->
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <!-- Axios CDN -->
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
</head>
<body class="bg-gray-100" x-data="dashboardData()">
    <!-- Header -->
    <header class="bg-white shadow">
        <div class="container mx-auto px-4 py-4 flex justify-between items-center">
            <h1 class="text-2xl font-bold text-gray-800">CS2 Tracker</h1>
            <div class="flex space-x-4">
                <button @click="syncInventory()" 
                        class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                    Sync
                </button>
                <button class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600">
                    Logout
                </button>
            </div>
        </div>
    </header>

    <!-- Stats Cards -->
    <div class="container mx-auto px-4 py-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <!-- Total Value Card -->
            <div class="bg-white p-6 rounded-lg shadow">
                <h3 class="text-gray-500 text-sm">Total Value</h3>
                <p class="text-3xl font-bold text-gray-800" x-text="'$' + totalValue.toFixed(2)"></p>
                <p class="text-green-500 text-sm">↑ 12.5%</p>
            </div>
            
            <!-- Total P&L Card -->
            <div class="bg-white p-6 rounded-lg shadow">
                <h3 class="text-gray-500 text-sm">Total P&L</h3>
                <p class="text-3xl font-bold" 
                   :class="totalPnL >= 0 ? 'text-green-600' : 'text-red-600'"
                   x-text="(totalPnL >= 0 ? '+$' : '-$') + Math.abs(totalPnL).toFixed(2)"></p>
            </div>
            
            <!-- Total Items Card -->
            <div class="bg-white p-6 rounded-lg shadow">
                <h3 class="text-gray-500 text-sm">Total Items</h3>
                <p class="text-3xl font-bold text-gray-800" x-text="inventory.length"></p>
            </div>
        </div>
    </div>

    <!-- Chart -->
    <div class="container mx-auto px-4 py-4">
        <div class="bg-white p-6 rounded-lg shadow">
            <h2 class="text-xl font-bold text-gray-800 mb-4">Inventory Value Over Time</h2>
            <canvas id="valueChart"></canvas>
        </div>
    </div>

    <!-- Inventory Table -->
    <div class="container mx-auto px-4 py-4">
        <div class="bg-white p-6 rounded-lg shadow">
            <h2 class="text-xl font-bold text-gray-800 mb-4">Current Inventory</h2>
            
            <!-- Loading State -->
            <div x-show="loading" class="text-center py-8">
                <p class="text-gray-500">Loading...</p>
            </div>
            
            <!-- Inventory List -->
            <div x-show="!loading">
                <template x-for="item in inventory" :key="item.asset_id">
                    <div class="flex items-center justify-between py-3 border-b">
                        <div class="flex items-center space-x-4">
                            <img :src="'https://community.cloudflare.steamstatic.com/economy/image/' + item.icon_url" 
                                 class="w-16 h-16" alt="">
                            <div>
                                <p class="font-semibold" x-text="item.name"></p>
                                <p class="text-sm text-gray-500" x-text="'Float: ' + (item.float_value || 'N/A')"></p>
                            </div>
                        </div>
                        <p class="text-lg font-bold text-green-600" x-text="'$' + (item.current_price || 0).toFixed(2)"></p>
                    </div>
                </template>
            </div>
        </div>
    </div>

    <!-- JavaScript -->
    <script src="js/dashboard.js"></script>
</body>
</html>
```

---

## 12.3 Alpine.js Dashboard Logic

### `frontend/js/dashboard.js`:
```javascript
function dashboardData() {
    return {
        user: null,
        inventory: [],
        totalValue: 0,
        totalPnL: 0,
        loading: false,
        
        async init() {
            await this.fetchUser();
            await this.fetchInventory();
            await this.fetchPnL();
            this.initChart();
        },
        
        async fetchUser() {
            try {
                const response = await axios.get('/api/user');
                this.user = response.data;
            } catch (error) {
                console.error('Error fetching user:', error);
            }
        },
        
        async fetchInventory() {
            this.loading = true;
            try {
                const response = await axios.get('/api/inventory');
                this.inventory = response.data.items;
                this.totalValue = response.data.total_value;
            } catch (error) {
                console.error('Error fetching inventory:', error);
            } finally {
                this.loading = false;
            }
        },
        
        async fetchPnL() {
            try {
                const response = await axios.get('/api/pnl');
                this.totalPnL = response.data.total_pnl;
            } catch (error) {
                console.error('Error fetching P&L:', error);
            }
        },
        
        async syncInventory() {
            this.loading = true;
            try {
                await axios.post('/api/inventory/sync');
                await this.fetchInventory();
                await this.fetchPnL();
            } catch (error) {
                console.error('Error syncing inventory:', error);
            } finally {
                this.loading = false;
            }
        },
        
        async initChart() {
            // Fetch snapshot data
            const response = await axios.get('/api/snapshots');
            const snapshots = response.data;
            
            const ctx = document.getElementById('valueChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: snapshots.map(s => s.snapshot_date),
                    datasets: [{
                        label: 'Portfolio Value',
                        data: snapshots.map(s => s.total_value),
                        borderColor: 'rgb(59, 130, 246)',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        tension: 0.1,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: false
                        },
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: false,
                            ticks: {
                                callback: function(value) {
                                    return '$' + value.toFixed(2);
                                }
                            }
                        }
                    }
                }
            });
        }
    }
}
```

---

## 12.4 Responsive Design (Tailwind)

### Mobile Breakpoints:
```html
<!-- Desktop: 3 columns -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <!-- Stats cards -->
</div>

<!-- Mobile: Stack vertically -->
<div class="flex flex-col space-y-4 md:space-y-0 md:flex-row md:space-x-4">
    <!-- Content -->
</div>

<!-- Responsive text sizes -->
<h1 class="text-xl md:text-2xl lg:text-3xl">CS2 Tracker</h1>

<!-- Hide on mobile, show on desktop -->
<div class="hidden md:block">Desktop only content</div>

<!-- Show on mobile, hide on desktop -->
<div class="block md:hidden">Mobile only content</div>
```

---

## Next Steps

✅ **Lanjut ke:** [`15-Deployment-Guide.md`](15-Deployment-Guide.md) - Deploy aplikasi  
✅ **Alternative:** [`18-Testing-Strategy.md`](18-Testing-Strategy.md) - Test frontend

---

**Frontend ready! 🎨**
