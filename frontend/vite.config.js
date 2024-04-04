// vite.config.js
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
    plugins: [vue()],
    server: {
        proxy: {
            '/api/limits': {
                target: 'https://7sdh7fyt73.execute-api.us-east-1.amazonaws.com/test',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/limits/, '')
            },
            '/api/measurements': {
                target: 'https://cf6ka369dk.execute-api.us-east-1.amazonaws.com/test',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/measurements/, '')
            },
            '/api/measurementslogs': {
                target: 'https://vruilq2id7.execute-api.us-east-1.amazonaws.com/test',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/measurementslogs/, '')
            },
            '/api/primaryRules': {
                target: 'https://moyvogn5hk.execute-api.us-east-1.amazonaws.com',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/primaryRules/, '')
            },
            '/api/deletePrimaryRules': {
                target: 'https://su1ckzw9b7.execute-api.us-east-1.amazonaws.com',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/deletePrimaryRules/, '')
            },
            '/api/updatePrimaryRules': {
                target: 'https://efaa7aze39.execute-api.us-east-1.amazonaws.com',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/updatePrimaryRules/, '')
            },
            '/api/conditionalRules': {
                target: 'https://tlfn5x001j.execute-api.us-east-1.amazonaws.com/test',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/conditionalRules/, '')
            },
            '/api/rulesAssignment': {
                target: 'https://880t97tleg.execute-api.us-east-1.amazonaws.com/test',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/rulesAssignment/, '')
            },
            '/api/createRulesAssignment/createRuleAssignment': {
                target: 'https://eqtocebkwh.execute-api.us-east-1.amazonaws.com',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/createRulesAssignment/, '')
            },
            '/api/logs': {
                target: 'https://4dsfm277h4.execute-api.us-east-1.amazonaws.com/test',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/logs/, '')
            },
            '/api/rules': {
                target: 'https://4qlwo7usil.execute-api.us-east-1.amazonaws.com',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/rules/, '')
            },
            '/api/createConditionalRules': {
                target: 'https://o2udxa0ch1.execute-api.us-east-1.amazonaws.com',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/createConditionalRules/, '')
            },
            '/api/plugins': {
                target: 'https://kecdxsnnig.execute-api.us-east-1.amazonaws.com',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/plugins/, '')
            },
            '/api/pluginRuleAssignment': {
                target: 'https://5c82xz0604.execute-api.us-east-1.amazonaws.com',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/pluginRuleAssignment/, '')
            },
            '/api/pluginRuleAssignmentRuleId': {
                target: 'https://l9lasralkh.execute-api.us-east-1.amazonaws.com',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/pluginRuleAssignmentRuleId/, '')
            },
            '/api/pluginCreate': {
                target: 'https://1jid7i2l2b.execute-api.us-east-1.amazonaws.com',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/pluginCreate/, '')
            },
            '/api/pluginUpdate': {
                target: 'https://jtuz8edae0.execute-api.us-east-1.amazonaws.com',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/pluginUpdate/, '')
            },
            '/api/pluginDelete': {
                target: 'https://n0pk6icudg.execute-api.us-east-1.amazonaws.com',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api\/pluginDelete/, '')
            }
        }
    }
});
