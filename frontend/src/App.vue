<template>
    <div>
        <nav class="navbar navbar-dark bg-dark" style="padding: 0.5em">
            <a class="navbar-brand" href="#">Home</a>
            <button
                class="navbar-toggler"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#navbarText"
                aria-controls="navbarText"
                aria-expanded="false"
                aria-label="Toggle navigation"
            >
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarText">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item" :class="{ active: currentView === 'measurement' }">
                        <a class="nav-link" href="#" @click.prevent="currentView = 'measurement'"
                            >Measurements</a
                        >
                    </li>
                    <li class="nav-item" :class="{ active: currentView === 'rules' }">
                        <a class="nav-link" href="#" @click.prevent="currentView = 'rules'"
                            >Rules</a
                        >
                    </li>
                    <li class="nav-item" :class="{ active: currentView === 'plugins' }">
                        <a class="nav-link" href="#" @click.prevent="currentView = 'plugins'"
                            >Plugins</a
                        >
                    </li>
                    <li class="nav-item" :class="{ active: currentView === 'logger' }">
                        <a class="nav-link" href="#" @click.prevent="currentView = 'logger'"
                            >State logs</a
                        >
                    </li>
                </ul>
            </div>
        </nav>
        <div style="padding: 2em">
            <Measurement v-if="currentView === 'measurement'" />
            <Plugin v-if="currentView === 'plugins'" />
            <Rule v-if="currentView === 'rules'" />
            <Log v-if="currentView === 'logger'" />
        </div>
    </div>
</template>

<script>
import Measurement from './components/MeasurementView.vue';
import Rule from './components/SystemRule.vue';
import Log from './components/StateLog.vue';
import Plugin from './components/PluginManagement.vue';

export default {
    components: {
        Measurement,
        Rule,
        Log,
        Plugin
    },
    data() {
        return {
            currentView: 'measurement'
        };
    }
};
</script>

<style></style>
