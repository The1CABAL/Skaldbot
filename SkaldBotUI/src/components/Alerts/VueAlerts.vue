<template>
    <div class="w-full top-3 pr-3 flex justify-end">
        <div class="w-1/4 space-y-2 z-50 right-0">
            <div v-for="notification in notifications" :key="notification.id">
                <error v-if="isError(notification)" :notification="notification" />
                <success v-if="isSuccess(notification)" :notification="notification" />
                <warning v-if="isWarning(notification)" :notification="notification" />
            </div>
        </div>
    </div>
</template>

<script>
    import VueError from './VueError';
    import VueSuccess from './VueSuccess';
    import VueWarning from './VueWarning';

    export default {
        name: "Alerts",

        components: {
            'error': VueError,
            'success': VueSuccess,
            'warning': VueWarning
        },

        data() {
            return {
                notifications: []
            }
        },

        methods: {
            isError(notification) {
                return notification.type === 'Error';
            },

            isSuccess(notification) {
                return notification.type === 'Success';
            },

            isWarning(notification) {
                return notification.type === 'Warning'
            }
        },

        watch: {
            '$store.state.notifications.notifications' (newVal, oldVal) {
                this.notifications = newVal;
            }
        }
    }
</script>