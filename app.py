<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Elite Trader Journal</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            box-sizing: border-box;
        }

        body {
            background: #0f172a;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            color: #22c55e;
        }

        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }

        .card {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid #334155;
            transition: transform 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
            border-color: #22c55e;
        }

        .card-label {
            font-size: 0.9em;
            color: #94a3b8;
            margin-bottom: 8px;
        }

        .card-value {
            font-size: 2em;
            font-weight: bold;
            color: #22c55e;
        }

        .card-value.negative {
            color: #ef4444;
        }

        form {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            border: 1px solid #334155;
        }

        .form-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
        }

        .form-group label {
            font-size: 0.85em;
            margin-bottom: 5px;
            color: #94a3b8;
        }

        input, select {
            padding: 10px;
            border-radius: 5px;
            border: 1px solid #334155;
            background: #0f172a;
            color: white;
            font-size: 1em;
            transition: border-color 0.3s ease;
        }

        input:focus, select:focus {
            outline: none;
            border-color: #22c55e;
            box-shadow: 0 0 10px rgba(34, 197, 94, 0.3);
        }

        button {
            padding: 10px 20px;
            background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
            color: #0f172a;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-weight: bold;
            font-size: 1em;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            grid-column: 1 / -1;
        }

        button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 20px rgba(34, 197, 94, 0.5);
        }

        button:active {
            transform: scale(0.95);
        }

        .charts {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }

        .chart-container {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #334155;
            position: relative;
            height: 400px;
        }

        .chart-container canvas {
            max-width: 100%;
        }

        .error {
            background: #7f1d1d;
            color: #fecaca;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border-left: 4px solid #ef4444;
            display: none;
        }

        .error.show {
            display: block;
        }

        .success {
            background: #1f5e3b;
            color: #bbf7d0;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border-left: 4px solid #22c55e;
            display: none;
            animation: slideIn 0.3s ease-out;
        }

        .success.show {
            display: block;
        }

        @keyframes slideIn {
            from {
                transform: translateY(-10px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }

        @media (max-width: 768px) {
            .charts {
                grid-template-columns: 1fr;
            }

            h1 {
                font-size: 1.8em;
            }

            .form-grid {
                grid-template-columns: 1fr;
            }

            button {
                grid-column: 1;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Elite Trader Journal</h1>

        <div id="errorMsg" class="error"></div>
        <div id="successMsg" class="success"></div>

        <div class="dashboard">
            <div class="card">
                <div class="card-label">Net Profit</div>
                <div class="card-value" id="netProfit">$0.00</div>
            </div>
            <div class="card">
                <div class="card-label">Win Rate</div>
                <div class="card-value" id="winRate">0%</div>
            </div>
            <div class="card">
                <div class="card-label">Total Trades</div>
                <div class="card-value" id="totalTrades">0</div>
            </div>
            <div class="card">
                <div class="card-label">Profit Factor</div>
                <div class="card-value" id="profitFactor">0.00</div>
            </div>
        </div>

        <form id="tradeForm">
            <div class="form-grid">
                <div class="form-group">
                    <label for="date">Date</label>
                    <input type="date" id="date" required>
                </div>
                <div class="form-group">
                    <label for="pair">Currency Pair</label>
                    <input type="text" id="pair" placeholder="e.g., EURUSD" required>
                </div>
                <div class="form-group">
                    <label for="type">Position Type</label>
                    <select id="type" required>
                        <option value="">Select Type</option>
                        <option value="Long">Long</option>
                        <option value="Short">Short</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="result">Result ($)</label>
                    <input type="number" id="result" step="0.01" placeholder="0.00" required>
                </div>
                <div class="form-group">
                    <label for="strategy">Strategy</label>
                    <select id="strategy" required>
                        <option value="">Select Strategy</option>
                        <option value="SMC">SMC</option>
                        <option value="ICT">ICT</option>
                        <option value="Liquidity">Liquidity</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="emotion">Emotion</label>
                    <select id="emotion" required>
                        <option value="">Select Emotion</option>
                        <option value="Calm">Calm</option>
                        <option value="FOMO">FOMO</option>
                        <option value="Frustrated">Frustrated</option>
                    </select>
                </div>
            </div>
            <button type="submit">Add Trade</button>
        </form>

        <div class="charts">
            <div class="chart-container">
                <canvas id="equityChart"></canvas>
            </div>
            <div class="chart-container">
                <canvas id="winLossChart"></canvas>
            </div>
            <div class="chart-container">
                <canvas id="dayChart"></canvas>
            </div>
        </div>
    </div>

    <script>
        // Global variables
        let trades = [];
        let charts = {};

        // Constants
        const STORAGE_KEY = 'traderJournalTrades';
        const CHART_CONFIG = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#e2e8f0'
                    }
                }
            },
            scales: {
                y: {
                    ticks: {
                        color: '#94a3b8'
                    },
                    grid: {
                        color: '#334155'
                    }
                },
                x: {
                    ticks: {
                        color: '#94a3b8'
                    },
                    grid: {
                        color: '#334155'
                    }
                }
            }
        };

        // Initialize application
        document.addEventListener('DOMContentLoaded', () => {
            initializeCharts();
            loadTrades();
            setupEventListeners();
            updateDashboard();
            updateCharts();
        });

        // Initialize all charts
        function initializeCharts() {
            const equityCtx = document.getElementById('equityChart');
            const winLossCtx = document.getElementById('winLossChart');
            const dayCtx = document.getElementById('dayChart');

            charts.equity = new Chart(equityCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Equity Curve',
                        data: [],
                        borderColor: '#22c55e',
                        backgroundColor: 'rgba(34, 197, 94, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    ...CHART_CONFIG,
                    plugins: {
                        ...CHART_CONFIG.plugins,
                        title: {
                            display: true,
                            text: 'Equity Curve',
                            color: '#e2e8f0'
                        }
                    }
                }
            });

            charts.winLoss = new Chart(winLossCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Wins', 'Losses'],
                    datasets: [{
                        data: [0, 0],
                        backgroundColor: ['#22c55e', '#ef4444'],
                        borderColor: '#1e293b',
                        borderWidth: 2
                    }]
                },
                options: {
                    ...CHART_CONFIG,
                    plugins: {
                        ...CHART_CONFIG.plugins,
                        title: {
                            display: true,
                            text: 'Win/Loss Ratio',
                            color: '#e2e8f0'
                        }
                    }
                }
            });

            charts.dayPerf = new Chart(dayCtx, {
                type: 'bar',
                data: {
                    labels: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
                    datasets: [{
                        label: 'Daily Performance ($)',
                        data: [0, 0, 0, 0, 0, 0, 0],
                        backgroundColor: '#3b82f6',
                        borderColor: '#1e40af',
                        borderWidth: 1
                    }]
                },
                options: {
                    ...CHART_CONFIG,
                    plugins: {
                        ...CHART_CONFIG.plugins,
                        title: {
                            display: true,
                            text: 'Performance by Day',
                            color: '#e2e8f0'
                        }
                    }
                }
            });
        }

        // Setup event listeners
        function setupEventListeners() {
            document.getElementById('tradeForm').addEventListener('submit', handleTradeSubmit);
        }

        // Handle form submission
        function handleTradeSubmit(e) {
            e.preventDefault();

            try {
                const trade = {
                    id: Date.now(),
                    date: document.getElementById('date').value,
                    pair: document.getElementById('pair').value.toUpperCase(),
                    type: document.getElementById('type').value,
                    result: parseFloat(document.getElementById('result').value),
                    strategy: document.getElementById('strategy').value,
                    emotion: document.getElementById('emotion').value
                };

                // Validation
                if (!trade.date || !trade.pair || !trade.type || isNaN(trade.result) || !trade.strategy || !trade.emotion) {
                    showError('Please fill in all fields correctly');
                    return;
                }

                trades.push(trade);
                saveTrades();
                updateDashboard();
                updateCharts();
                showSuccess('Trade added successfully!');
                this.reset();
                document.getElementById('date').focus();
            } catch (error) {
                showError('Error adding trade: ' + error.message);
                console.error(error);
            }
        }

        // Load trades from localStorage
        function loadTrades() {
            try {
                const stored = localStorage.getItem(STORAGE_KEY);
                trades = stored ? JSON.parse(stored) : [];
            } catch (error) {
                console.error('Error loading trades:', error);
                trades = [];
                showError('Could not load saved trades');
            }
        }

        // Save trades to localStorage
        function saveTrades() {
            try {
                localStorage.setItem(STORAGE_KEY, JSON.stringify(trades));
            } catch (error) {
                console.error('Error saving trades:', error);
                showError('Could not save trades');
            }
        }

        // Update dashboard metrics
        function updateDashboard() {
            if (trades.length === 0) {
                document.getElementById('netProfit').textContent = '$0.00';
                document.getElementById('totalTrades').textContent = '0';
                document.getElementById('winRate').textContent = '0%';
                document.getElementById('profitFactor').textContent = '0.00';
                return;
            }

            // Calculate metrics
            const net = trades.reduce((acc, t) => acc + t.result, 0);
            const wins = trades.filter(t => t.result > 0).length;
            const losses = trades.filter(t => t.result < 0).length;
            const totalProfit = trades.filter(t => t.result > 0).reduce((a, t) => a + t.result, 0);
            const totalLoss = Math.abs(trades.filter(t => t.result < 0).reduce((a, t) => a + t.result, 0));
            const pf = totalLoss ? (totalProfit / totalLoss) : (totalProfit > 0 ? totalProfit : 0);

            // Update DOM
            const netProfitEl = document.getElementById('netProfit');
            netProfitEl.textContent = '$' + net.toFixed(2);
            netProfitEl.classList.toggle('negative', net < 0);

            document.getElementById('totalTrades').textContent = trades.length;
            document.getElementById('winRate').textContent = ((wins / trades.length) * 100).toFixed(1) + '%';
            document.getElementById('profitFactor').textContent = pf.toFixed(2);
        }

        // Update all charts
        function updateCharts() {
            if (!charts.equity) return;

            updateEquityChart();
            updateWinLossChart();
            updateDayChart();
        }

        // Update equity curve chart
        function updateEquityChart() {
            let cumulative = 0;
            const labels = [];
            const data = [];

            trades.forEach((t, i) => {
                cumulative += t.result;
                labels.push(`Trade ${i + 1}`);
                data.push(cumulative);
            });

            charts.equity.data.labels = labels;
            charts.equity.data.datasets[0].data = data;
            charts.equity.update();
        }

        // Update win/loss chart
        function updateWinLossChart() {
            const wins = trades.filter(t => t.result > 0).length;
            const losses = trades.filter(t => t.result < 0).length;

            charts.winLoss.data.datasets[0].data = [wins, losses];
            charts.winLoss.update();
        }

        // Update performance by day chart
        function updateDayChart() {
            const dayPerf = [0, 0, 0, 0, 0, 0, 0];

            trades.forEach(t => {
                try {
                    // Parse date safely (YYYY-MM-DD format)
                    const [year, month, day] = t.date.split('-');
                    const date = new Date(year, parseInt(month) - 1, day);
                    const dayIndex = date.getDay();
                    dayPerf[dayIndex] += t.result;
                } catch (error) {
                    console.error('Error parsing date:', t.date, error);
                }
            });

            charts.dayPerf.data.datasets[0].data = dayPerf;
            charts.dayPerf.update();
        }

        // Show error message
        function showError(message) {
            const errorEl = document.getElementById('errorMsg');
            errorEl.textContent = message;
            errorEl.classList.add('show');
            setTimeout(() => errorEl.classList.remove('show'), 5000);
        }

        // Show success message
        function showSuccess(message) {
            const successEl = document.getElementById('successMsg');
            successEl.textContent = message;
            successEl.classList.add('show');
            setTimeout(() => successEl.classList.remove('show'), 3000);
        }
    </script>
</body>
</html>