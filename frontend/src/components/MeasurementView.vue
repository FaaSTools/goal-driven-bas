<template>
    <div v-if="paginatedMeasurements.length !== 0" class="container mt-3">
        <h1>Measurements</h1>
        <div class="view-switcher">
            <button
                class="btn btn-sm btn-outline-secondary"
                type="button"
                @click="currentView = 'table'"
                :class="{ active: currentView === 'table' }"
            >
                Table View
            </button>
            <button
                class="btn btn-sm btn-outline-secondary"
                type="button"
                @click="currentView = 'chart'"
                :class="{ active: currentView === 'chart' }"
            >
                Chart View
            </button>
        </div>
        <div v-if="currentView === 'table'" class="measurement-table">
            <table class="table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Measurement Unit</th>
                        <th>Value</th>
                        <th>Timestamp</th>
                        <th>Plugin ID</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="measurement in paginatedMeasurements" :key="measurement.id">
                        <td>{{ measurement.id }}</td>
                        <td>{{ measurement.measurementUnit }}</td>
                        <td>{{ measurement.value }}</td>
                        <td>{{ measurement.timestamp }}</td>
                        <td>{{ measurement.pluginId }}</td>
                    </tr>
                </tbody>
            </table>
            <div class="pagination">
                <button @click="prevPage" :disabled="currentPage <= 1">Previous</button>
                <span>Page {{ currentPage }} of {{ totalPages }}</span>
                <button @click="nextPage" :disabled="currentPage >= totalPages">Next</button>
            </div>
        </div>
        <div
            v-if="currentView === 'chart'"
            class="chart-container"
            style="position: relative; height: 100%; width: 100%; margin-top: 2em"
        >
            <select
                v-model="selectedPluginId"
                @change="updateChartForPluginId"
                class="form-control mb-3"
            >
                <option value="">All Plugin IDs</option>
                <option v-for="id in uniquePluginIds" :key="id" :value="id">{{ id }}</option>
            </select>
            <canvas id="measurementsChart"></canvas>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
    name: 'MeasurementTable',
    data() {
        return {
            measurements: [],
            currentPage: 1,
            pageSize: 20,
            chartInstance: null,
            currentView: 'table',
            selectedPluginId: ''
        };
    },
    computed: {
        paginatedMeasurements() {
            const start = (this.currentPage - 1) * this.pageSize;
            const end = start + this.pageSize;
            return this.measurements.slice(start, end);
        },
        totalPages() {
            return Math.ceil(this.measurements.length / this.pageSize);
        },
        uniquePluginIds() {
            const pluginIds = this.measurements.map((measurement) => measurement.pluginId);
            return [...new Set(pluginIds)];
        }
    },
    mounted() {
        this.fetchMeasurements();
        this.$nextTick(() => {
            this.updateChartForPluginId();
        });
    },
    watch: {
        currentView(newVal) {
            if (newVal === 'chart') {
                this.updateChartForPluginId();
            }
        }
    },
    methods: {
        fetchMeasurements() {
            const url = '/api/measurements/getMeasurementsAll';
            axios
                .post(url, {})
                .then((response) => {
                    this.measurements = response.data.measurements;
                })
                .catch((error) =>
                    console.error('There was an error fetching the measurements:', error)
                );
        },
        prevPage() {
            if (this.currentPage > 1) this.currentPage--;
        },
        nextPage() {
            if (this.currentPage < this.totalPages) this.currentPage++;
        },
        updateChartForPluginId() {
            const filteredMeasurements = this.selectedPluginId
                ? this.measurements.filter((m) => m.pluginId === this.selectedPluginId)
                : this.measurements;
            this.createChart(filteredMeasurements);
        },
        createChart(measurements) {
            const measurementsSorted = measurements.sort((a, b) => a.id - b.id);
            this.$nextTick(() => {
                const ctx = document.getElementById('measurementsChart').getContext('2d');
                if (this.chartInstance) {
                    this.chartInstance.destroy();
                }
                this.chartInstance = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: measurementsSorted.map((m) => m.timestamp.split(' ')[0]),
                        datasets: [
                            {
                                label: 'Measurement Value',
                                data: measurementsSorted.map((m) => m.value),
                                fill: false,
                                borderColor: 'rgb(75, 192, 192)',
                                tension: 0.1
                            }
                        ]
                    },
                    options: {
                        scales: {
                            y: {
                                beginAtZero: true
                            }
                        }
                    }
                });
            });
        }
    }
};
</script>

<style scoped>
.text-danger {
    color: #ffcccc;
}
.pagination,
.view-switcher,
.form-control {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}
button {
    margin: 0 10px;
    padding: 5px 10px;
    border-radius: 5px;
    border: 1px solid #ccc;
    background-color: #fff;
    cursor: pointer;
}
.active {
    background-color: #007bff;
    color: white;
}
</style>
