<template>
    <div v-if="plugins.length !== 0" class="container mt-3">
        <h1>Plugins</h1>
        <button @click="showCreatePluginForm = !showCreatePluginForm" class="btn btn-primary">
            Create Plugin
        </button>
        <div v-if="showCreatePluginForm" class="container mt-3">
            <form @submit.prevent="createPlugin">
                <div class="form-group">
                    <label for="name">Name</label>
                    <input
                        type="text"
                        class="form-control"
                        id="name"
                        v-model="newPlugin.name"
                        required
                    />
                </div>
                <div class="form-group">
                    <label for="description">Description</label>
                    <textarea
                        class="form-control"
                        id="description"
                        v-model="newPlugin.description"
                        required
                    ></textarea>
                </div>
                <div class="form-group">
                    <label for="frequency">Default Frequency</label>
                    <input
                        type="number"
                        class="form-control"
                        id="frequency"
                        v-model="newPlugin.frequency"
                        required
                    />
                </div>
                <div class="form-group">
                    <label for="capacity">Capacity</label>
                    <input
                        type="number"
                        class="form-control"
                        id="capacity"
                        v-model="newPlugin.capacity"
                        required
                    />
                </div>
                <div class="form-group">
                    <label for="connectURL">Connection URL</label>
                    <input
                        type="text"
                        class="form-control"
                        id="connectURL"
                        v-model="newPlugin.connectURL"
                        required
                    />
                </div>
                <button
                    type="submit"
                    class="btn btn-success"
                    style="margin-top: 2em; margin-bottom: 2em"
                >
                    Create
                </button>
            </form>
        </div>
        <div class="row">
            <div class="col-md-12">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Id</th>
                            <th>Name</th>
                            <th>Description</th>
                            <th>Default frequency</th>
                            <th>Capacity</th>
                            <th>Connection URL</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="plugin in plugins" :key="plugin.id">
                            <td>{{ plugin.id }}</td>
                            <td>{{ plugin.name }}</td>
                            <td>{{ plugin.description }}</td>
                            <td>{{ plugin.frequency }}</td>
                            <td>{{ plugin.capacity }}</td>
                            <td>{{ plugin.connectURL }}</td>
                            <td>
                                <button
                                    @click="assignEditPlugin(plugin.id)"
                                    class="btn btn-light btn-sm"
                                >
                                    Edit
                                </button>
                                <button
                                    @click="deletePlugin(plugin.id)"
                                    class="btn btn-light btn-sm"
                                >
                                    Delete
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            plugins: [],
            showCreatePluginForm: false,
            newPlugin: {
                id: 0,
                name: '',
                description: '',
                frequency: 0,
                capacity: 0,
                connectURL: ''
            }
        };
    },
    mounted() {
        this.fetchPlugins();
    },
    methods: {
        fetchPlugins() {
            const url = '/api/plugins/getAllPlugins';
            axios
                .post(url, {})
                .then((response) => {
                    const responseData = response.data;
                    this.plugins = responseData.plugins;
                    console.log(this.plugins);
                })
                .catch((error) => {
                    console.log(error);
                });
        },
        createPlugin() {
            if (this.newPlugin.id !== 0) {
                this.editPlugin();
                return;
            }
            const url = '/api/pluginCreate/createPlugin';
            const payload = {
                name: this.newPlugin.name,
                description: this.newPlugin.description,
                frequency: this.newPlugin.frequency,
                capacity: this.newPlugin.capacity,
                connectURL: this.newPlugin.connectURL
            };
            axios
                .post(url, payload)
                .then((response) => {
                    console.log(response.data);
                    this.newPlugin.id = response.data.id;
                    this.plugins.push(this.newPlugin);
                    this.newPlugin = {
                        name: '',
                        description: '',
                        frequency: 0,
                        capacity: 0,
                        connectURL: ''
                    };
                })
                .catch((error) => {
                    console.log(error);
                });
        },
        assignEditPlugin(pluginId) {
            this.newPlugin = this.plugins.find((plugin) => plugin.id === pluginId);
            this.showCreatePluginForm = true;
        },
        editPlugin() {
            const url = '/api/pluginUpdate/updatePlugin';
            const payload = {
                pluginId: this.newPlugin.id,
                name: this.newPlugin.name,
                description: this.newPlugin.description,
                frequency: this.newPlugin.frequency,
                capacity: this.newPlugin.capacity,
                connectURL: this.newPlugin.connectURL
            };
            axios
                .post(url, payload)
                .then((response) => {
                    console.log(response.data);
                    this.newPlugin = {
                        id: 0,
                        name: '',
                        description: '',
                        frequency: 0,
                        capacity: 0,
                        connectURL: ''
                    };
                    this.showCreatePluginForm = false;
                })
                .catch((error) => {
                    console.log(error);
                });
        },
        deletePlugin(pluginId) {
            const url = '/api/pluginDelete/deletePlugin';
            const payload = {
                pluginId: pluginId
            };
            axios
                .post(url, payload)
                .then((response) => {
                    console.log(response.data);
                    this.plugins = this.plugins.filter((plugin) => plugin.id !== pluginId);
                })
                .catch((error) => {
                    console.log(error);
                });
        }
    }
};
</script>
