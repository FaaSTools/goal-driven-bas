<template>
    <div v-if="paginatedLogs.length !== 0" class="container mt-3">
        <h2>Logs</h2>
        <table class="table">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Rule ID</th>
                    <th>Timestamp</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="log in paginatedLogs" :key="log.id">
                    <td>{{ log.id }}</td>
                    <td style="width: 40em">
                        <div
                            v-if="log.ruleId == 1 || log.ruleId == 2"
                            class="alert alert-danger custom-alert"
                            role="alert"
                        >
                            [Error State] {{ log.description }}
                        </div>
                        <div v-else class="alert alert-success custom-alert" role="alert">
                            [{{ getRuleName(log.ruleId) }}] {{ log.description }}
                        </div>
                    </td>
                    <td>{{ log.timestamp }}</td>
                </tr>
            </tbody>
        </table>
        <div class="pagination">
            <button @click="prevPage" :disabled="currentPage <= 1">Previous</button>
            <span>Page {{ currentPage }} of {{ totalPages }}</span>
            <button @click="nextPage" :disabled="currentPage >= totalPages">Next</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            logs: [],
            currentPage: 1,
            pageSize: 30,
            rules: []
        };
    },
    computed: {
        paginatedLogs() {
            const start = (this.currentPage - 1) * this.pageSize;
            const end = start + this.pageSize;
            return this.logs.slice(start, end);
        },
        totalPages() {
            return Math.ceil(this.logs.length / this.pageSize);
        }
    },
    methods: {
        changePage(page) {
            if (page < 1 || page > this.totalPages) return;
            this.currentPage = page;
        },
        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
            }
        },
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
            }
        },
        fetchLogs() {
            const url = '/api/logs/getLogsAll';
            axios
                .post(url, {})
                .then((response) => {
                    const responseData =
                        typeof response.data === 'string'
                            ? JSON.parse(response.data)
                            : response.data;
                    this.logs = responseData.logs;
                })
                .catch((error) => console.error('There was an error fetching the logs:', error));
        },
        fetchPrimaryRules() {
            const url = '/api/primaryRules/getPrimaryRulesAll';
            axios
                .post(url, {})
                .then((response) => {
                    this.rules = response.data.rules;
                })
                .catch((error) => console.error('There was an error fetching the rules:', error));
        },
        getRuleName(ruleId) {
            for (let i = 0; i < this.rules.length; i++) {
                if (this.rules[i].id === ruleId) {
                    return `${this.rules[i].name} - ${this.rules[i].description}`;
                }
            }
        }
    },
    mounted() {
        this.fetchLogs();
        this.fetchPrimaryRules();
    }
};
</script>

<style scoped>
.pagination {
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
.custom-alert {
    width: 40em;
}
</style>
