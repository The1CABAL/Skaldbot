<template>
    <div id="KanbanComments">
        <div v-for="comment in comments" :key="comment.id">
            <vue-text-area :id="comment.node_id" v-if="resizeTextarea(comment.node_id)" :is-disabled="true" :value="comment.body">{{comment.user.login}} - {{getDate(comment.created_at)}}</vue-text-area>
        </div>
    </div>
</template>

<script>
    import fieldTextArea from '@/components/CustomFields/fieldTextArea';
    export default {
        name: "KanbanComments",

        props: {
            commentUrl: {
                type: String,
                required: true
            }
        },

        components: {
            'vue-text-area': fieldTextArea
        },

        data() {
            return {
                comments: []
            }
        },

        mounted() {
            this.getComments();
        },

        methods: {
            async getComments() {
                var url = this.commentUrl;

                await this.$store.dispatch('getAllCardComments', url).then(() => {
                    this.comments = this.$store.getters.getCardComments;
                }).catch(() => {
                    this.error("Error loading comments");
                })
            },

            getDate(date) {
                let elDate = new Date(date)
                return (elDate.getMonth() + 1) + '-'
                    + elDate.getDate() + '-'
                    + elDate.getFullYear()
            },

            resizeTextarea(nodeId) {
                setTimeout(function () {
                    var textarea = document.getElementById(nodeId);
                    textarea.style.height = (textarea.scrollHeight) + 2 + 'px';
                }, 50)

                return true;
            }
        }
    }
</script>

<style scoped>
</style>