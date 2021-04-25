<template>
    <div id="KanbanComments">
        <div v-for="comment in comments" :key="comment.id">
            <p style="color: white; font-size: 12px;">{{comment.user.login}} - {{getDate(comment.created_at)}}</p>
            <textarea :id="comment.node_id" v-if="resizeTextarea(comment.node_id)" disabled>{{comment.body}}</textarea>
        </div>
    </div>
</template>

<script>
    export default {
        name: "KanbanComments",
        props: {
            commentUrl: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                comments: []
            }
        },
        mounted: function () {
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