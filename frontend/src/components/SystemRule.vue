<template>
    <button type="button" class="btn btn-primary" @click="showCreatePrimaryRuleForm = true">
        Add primary rule
    </button>
    <div v-if="showCreatePrimaryRuleForm" style="margin-bottom: 2em; margin-top: 2em">
        <form @submit.prevent="createPrimaryRule">
            <div class="mb-3">
                <label for="name" class="form-label">Name:</label>
                <input type="text" class="form-control" id="name" v-model="newRule.name" required />
            </div>
            <div class="mb-3">
                <label for="description" class="form-label">Description:</label>
                <input
                    type="text"
                    class="form-control"
                    id="description"
                    v-model="newRule.description"
                    required
                />
            </div>
            <div class="mb-3">
                <label for="startTimeFrom" class="form-label">Start Time From:</label>
                <input
                    type="time"
                    class="form-control"
                    id="startTimeFrom"
                    v-model="newRule.startTimeFrom"
                    required
                />
            </div>
            <div class="mb-3">
                <label for="startTimeTo" class="form-label">Start Time To:</label>
                <input
                    type="time"
                    class="form-control"
                    id="startTimeTo"
                    v-model="newRule.startTimeTo"
                    required
                />
            </div>
            <div class="mb-3">
                <label for="logicalOperator" class="form-label">Logical Operator:</label>
                <select
                    class="form-select"
                    id="logicalOperator"
                    v-model="newRule.logicalOperator"
                    required
                >
                    <option value="AND">AND</option>
                    <option value="OR">OR</option>
                </select>
            </div>
            <h5>Plugin configuration</h5>
            <div style="margin-top: 2em; margin-bottom: 2em">
                <ul class="list-group">
                    <li
                        v-for="(item, index) in plugins"
                        :key="index"
                        class="list-group-item d-flex justify-content-between align-items-center"
                    >
                        <div>
                            {{ item.name }}
                            <small class="text-muted" style="font-size: 0.75em"
                                >(description: {{ item.description }})</small
                            >
                        </div>
                        <input
                            type="number"
                            class="form-control"
                            style="width: auto"
                            v-model="item.frequency"
                            placeholder="Frequency"
                        />
                    </li>
                </ul>
            </div>
            <button type="submit" class="btn btn-success" style="margin-right: 2em">Submit</button>
            <button
                type="button"
                class="btn btn-secondary"
                @click="showCreatePrimaryRuleForm = false"
            >
                Cancel
            </button>
        </form>
    </div>
    <div v-if="rules.length !== 0" class="container mt-3">
        <h2>Primary Rules</h2>
        <table class="table table-hover">
            <thead class="thead-dark">
                <tr>
                    <th scope="col">ID</th>
                    <th scope="col">Name</th>
                    <th scope="col">Description</th>
                    <th scope="col">Start Time From</th>
                    <th scope="col">Start Time To</th>
                    <th scope="col">Logical Operator</th>
                    <th scope="col"></th>
                </tr>
            </thead>
            <tbody>
                <tr
                    v-for="rule in rules"
                    :key="rule.id"
                    @click="selectPrimaryRule(rule.id)"
                    style="cursor: pointer"
                >
                    <td>{{ rule.id }}</td>
                    <td>{{ rule.name }}</td>
                    <td>{{ rule.description }}</td>
                    <td>{{ rule.startTimeFrom }}</td>
                    <td>{{ rule.startTimeTo }}</td>
                    <td>{{ rule.logicalOperator }}</td>
                    <td>
                        <button
                            class="btn btn-light btn-sm"
                            style="margin-right: 1em"
                            @click.stop="deleteRule(rule.id)"
                        >
                            Delete
                        </button>
                        <button class="btn btn-light btn-sm" @click.stop="assignEditRule(rule.id)">
                            Edit
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>

        <div v-if="selectedPrimaryRuleId != null">
            <button
                type="button"
                class="btn btn-primary"
                @click="showCreateConditionalRuleForm = true"
            >
                Add conditional rule
            </button>
            <div v-if="showCreateConditionalRuleForm" style="margin-bottom: 2em; margin-top: 2em">
                <form @submit.prevent="createConditionalRule">
                    <div class="mb-3">
                        <label for="name" class="form-label">Name:</label>
                        <input
                            type="text"
                            class="form-control"
                            id="name"
                            v-model="newConditionalRule.name"
                            required
                        />
                    </div>
                    <div class="mb-3">
                        <label for="description" class="form-label">Description:</label>
                        <input
                            type="text"
                            class="form-control"
                            id="description"
                            v-model="newConditionalRule.description"
                            required
                        />
                    </div>
                    <div class="mb-3">
                        <label for="pluginId" class="form-label">Plugin ID:</label>
                        <select
                            class="form-select"
                            id="pluginId"
                            v-model="newConditionalRule.pluginId"
                            required
                        >
                            <option v-for="plugin in plugins" :key="plugin.id" :value="plugin.id">
                                {{ plugin.id }}
                                {{ plugin.name }}
                            </option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label for="value" class="form-label">Value:</label>
                        <input
                            type="text"
                            class="form-control"
                            id="value"
                            v-model="newConditionalRule.value"
                            required
                        />
                    </div>
                    <div class="mb-3">
                        <label for="comparisonOperator" class="form-label"
                            >Comparison Operator:</label
                        >
                        <select
                            class="form-select"
                            id="comparisonOperator"
                            v-model="newConditionalRule.comparisonOperator"
                            required
                        >
                            <option value="EQUAL">= [EQUAL]</option>
                            <option value="NOT_EQUAL">!=< [NOT_EQUAL]</option>
                            <option value="GREATER_THAN">> [GREATER_THAN]</option>
                            <option value="LESS_THAN">< [LESS_THAN]</option>
                            <option value="GREATER_THAN_OR_EQUAL">
                                >= [GREATER_THAN_OR_EQUAL]
                            </option>
                            <option value="LESS_THAN_OR_EQUAL"><= [LESS_THAN_OR_EQUAL]</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-success" style="margin-right: 2em">
                        Submit
                    </button>
                    <button
                        type="button"
                        class="btn btn-secondary"
                        @click="showCreateConditionalRuleForm = false"
                    >
                        Cancel
                    </button>
                </form>
            </div>
            <div
                v-if="filteredConditionalRules.length == 0"
                class="alert alert-info"
                style="margin-top: 2em"
            >
                No conditional rules for Primary Rule ID: {{ selectedPrimaryRuleId }}
            </div>
            <div v-else style="margin-top: 2em">
                <h2>Conditional Rules</h2>
                <table class="table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Description</th>
                            <th>Measurement Unit</th>
                            <th>Plugin ID</th>
                            <th>Limit Value</th>
                            <th>Comparison Operator</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="rule in filteredConditionalRules" :key="rule.id">
                            <td>{{ rule.id }}</td>
                            <td>{{ rule.name }}</td>
                            <td>{{ rule.description }}</td>
                            <td>{{ rule.measurementUnit }}</td>
                            <td>{{ rule.pluginId }}</td>
                            <td>{{ rule.value }}</td>
                            <td>{{ rule.comparisonOperator }}</td>
                            <td>
                                <button
                                    class="btn btn-light btn-sm"
                                    style="margin-right: 1em"
                                    @click.stop="deleteRule(rule.id)"
                                >
                                    Delete
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <div v-else>
            <div class="alert alert-info">Select primary rule to view its conditional rule(s)</div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            showCreatePrimaryRuleForm: false,
            showCreateConditionalRuleForm: false,
            rules: [],
            conditionalRules: [],
            rulesAssignment: [],
            filteredConditionalRules: [],
            selectedPrimaryRuleId: null,
            newRule: {
                id: '',
                name: '',
                description: '',
                startTimeFrom: '',
                startTimeTo: '',
                logicalOperator: ''
            },
            newConditionalRule: {
                name: '',
                description: '',
                pluginId: '',
                measurementUnit: '',
                value: '',
                comparisonOperator: ''
            },
            plugins: [],
            originalPlugins: [],
            pluginRuleAssignments: []
        };
    },
    methods: {
        assignEditRule(ruleId) {
            this.newRule = this.rules.find((rule) => rule.id === ruleId);
            this.showCreatePrimaryRuleForm = true;
        },
        editRule() {
            const url = '/api/updatePrimaryRules/updatePrimaryRule';
            const ruleId = this.newRule.id;

            axios
                .post(url, {
                    ruleId: this.newRule.id,
                    name: this.newRule.name,
                    description: this.newRule.description,
                    startTimeFrom: this.newRule.startTimeFrom,
                    startTimeTo: this.newRule.startTimeTo,
                    logicalOperator: this.newRule.logicalOperator
                })
                .then((response) => {
                    console.log('Rule edited successfully', response.data);
                    this.newRule = {
                        id: '',
                        name: '',
                        description: '',
                        startTimeFrom: '',
                        startTimeTo: '',
                        logicalOperator: ''
                    };
                    this.showCreatePrimaryRuleForm = false;

                    this.plugins.forEach((plugin, index) => {
                        console.log('plugin', plugin);
                        if (this.hasPluginChanged(plugin, index)) {
                            console.log('plugin to change', plugin);
                            this.createOrUpdatePluginRuleAssignment(
                                ruleId,
                                plugin.id,
                                plugin.frequency
                            );
                        }
                    });
                })
                .catch((error) => {
                    console.error('There was an error editing the rule:', error);
                });
        },
        deleteRule(ruleId) {
            const url = '/api/deletePrimaryRules/deletePrimaryRule';
            axios
                .post(url, {
                    ruleId: ruleId
                })
                .then((response) => {
                    console.log('Rule deleted successfully', response.data);
                    this.rules = this.rules.filter((rule) => rule.id !== ruleId);
                })
                .catch((error) => {
                    console.error('There was an error deleting the rule:', error);
                });
        },
        createPrimaryRule() {
            const url = '/api/rules/createPrimaryRule_c';
            const formattedStartTimeFrom = `${this.newRule.startTimeFrom}:00`;
            const formattedStartTimeTo = `${this.newRule.startTimeTo}:00`;
            const payload = {
                ...this.newRule,
                startTimeFrom: formattedStartTimeFrom,
                startTimeTo: formattedStartTimeTo
            };

            axios
                .post(url, payload)
                .then((response) => {
                    const ruleId = response.data.id;
                    this.selectedPrimaryRuleId = ruleId;
                    console.log('Rule created successfully', response.data);
                    this.newRule = {
                        name: '',
                        description: '',
                        startTimeFrom: '',
                        startTimeTo: '',
                        logicalOperator: ''
                    };
                    this.showCreatePrimaryRuleForm = false;
                    this.plugins.forEach((plugin, index) => {
                        console.log('plugin', plugin);
                        if (this.hasPluginChanged(plugin, index)) {
                            console.log('plugin to change', plugin);
                            this.createOrUpdatePluginRuleAssignment(
                                ruleId,
                                plugin.id,
                                plugin.frequency
                            );
                        }
                    });
                    this.fetchPrimaryRules();
                })
                .catch((error) => {
                    console.error('There was an error creating the rule:', error);
                });
        },
        ruleAlreadyExists() {
            return this.filteredConditionalRules.some(
                (rule) =>
                    rule.pluginId === this.newConditionalRule.pluginId &&
                    rule.measurementUnit === this.newConditionalRule.measurementUnit &&
                    rule.value === this.newConditionalRule.value &&
                    rule.comparisonOperator === this.newConditionalRule.comparisonOperator
            );
        },
        async createConditionalRule() {
            if (this.ruleAlreadyExists()) {
                alert('A rule with these conditions already exists.');
                return;
            }
            const url = '/api/createConditionalRules/createConditionalRule_c';
            const payload = {
                rule: this.newConditionalRule,
                primaryRuleId: this.selectedPrimaryRuleId
            };

            try {
                const response = await axios.post(url, payload);
                console.log('Rule created successfully', response.data);
                const conditionalRule = {
                    id: response.data.id,
                    name: this.newConditionalRule.name,
                    description: this.newConditionalRule.description,
                    pluginId: this.newConditionalRule.pluginId,
                    measurementUnit: this.newConditionalRule.measurementUnit,
                    value: this.newConditionalRule.value,
                    comparisonOperator: this.newConditionalRule.comparisonOperator
                };
                this.filteredConditionalRules.push(conditionalRule);
                this.newConditionalRule = {
                    name: '',
                    description: '',
                    pluginId: '',
                    measurementUnit: '',
                    value: '',
                    comparisonOperator: ''
                };
                this.showCreateConditionalRuleForm = false;

                for (const plugin of this.plugins) {
                    if (this.hasPluginChanged(plugin)) {
                        await this.createOrUpdatePluginRuleAssignment(
                            this.selectedPrimaryRuleId,
                            plugin.id,
                            plugin.frequency
                        );
                    }
                }
            } catch (error) {
                console.error('There was an error creating the rule:', error);
            }
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
        fetchConditionalRules() {
            const url = '/api/conditionalRules/getConditionalRulesAll';
            axios
                .post(url, {})
                .then((response) => {
                    this.conditionalRules = response.data.rules;
                })
                .catch((error) => console.error('There was an error fetching the rules:', error));
        },
        fetchRulesAssignment(primaryRuleId) {
            const url = '/api/rulesAssignment/getRuleAssignmentByPrimaryRuleId';
            axios
                .post(url, {
                    primaryRuleId: primaryRuleId
                })
                .then((response) => {
                    this.rulesAssignment = response.data.assignments;
                    const associatedConditionalRuleIds = this.rulesAssignment.map(
                        (assignment) => assignment.conditionalRuleId
                    );

                    this.filteredConditionalRules = this.conditionalRules.filter((rule) =>
                        associatedConditionalRuleIds.includes(rule.id)
                    );
                    console.log(associatedConditionalRuleIds);
                    console.log(filteredConditionalRules);
                })
                .catch((error) => console.error('There was an error fetching the rules:', error));
        },
        selectPrimaryRule(primaryRuleId) {
            this.selectedPrimaryRuleId = primaryRuleId;
            this.fetchRulesAssignment(primaryRuleId);
        },
        createAssignment(primaryRuleId, conditionalRuleId) {
            const url = '/api/createRulesAssignment/createRuleAssignment';
            const payload = {
                primaryRuleId: primaryRuleId,
                conditionalRuleId: conditionalRuleId
            };
            axios
                .post(url, payload)
                .then((response) => {
                    console.log('Assignment created successfully', response.data);
                })
                .catch((error) => {
                    console.error('There was an error creating the assignment:', error);
                });
        },
        fetchPlugins() {
            const url = '/api/plugins/getAllPlugins';
            axios
                .post(url, {})
                .then((response) => {
                    const responseData = response.data;
                    this.plugins = responseData.plugins;
                    this.originalPlugins = JSON.parse(JSON.stringify(responseData.plugins));
                })
                .catch((error) => {
                    console.log(error);
                });
        },
        hasPluginChanged(plugin, index) {
            return JSON.stringify(plugin) !== JSON.stringify(this.originalPlugins[index]);
        },
        createOrUpdatePluginRuleAssignment(primaryRuleId, pluginId, frequency) {
            console.log('createOrUpdatePluginRuleAssignment', primaryRuleId, pluginId, frequency);
            const url = '/api/pluginRuleAssignment/createPluginRuleAssignment';
            const payload = {
                primaryRuleId: primaryRuleId,
                pluginId: pluginId,
                frequency: frequency
            };
            axios
                .post(url, payload)
                .then((response) => {
                    console.log('Plugin rule assignment created successfully', response.data);
                })
                .catch((error) => {
                    console.error('There was an error creating the plugin rule assignment:', error);
                });
        },
        fetchPluginRuleAssignment(primaryRuleId) {
            const url = '/api/pluginRuleAssignment/getPluginRuleAssignmentRuleId';
            axios
                .post(url, {
                    primaryRuleId: primaryRuleId
                })
                .then((response) => {
                    console.log('Plugin rule assignment fetched successfully', response.data);
                    this.pluginRuleAssignments = response.data;
                })
                .catch((error) => {
                    console.error('There was an error fetching the plugin rule assignment:', error);
                });
        }
    },
    mounted() {
        this.fetchPrimaryRules();
        this.fetchConditionalRules();
        this.fetchPlugins();
    }
};
</script>
