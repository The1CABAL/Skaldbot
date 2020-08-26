<template>
    <div id="KanbanCard">
        <header>#{{cardInfo.number}} - {{cardInfo.title}}</header>
    </div>
</template>

<script>
    export default {
        name: "KanbanCard",
        props: {
            contentUrl: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                cardInfo: []
            }
        },
        mounted: function () {
            this.getCardInfo();
        },
        methods: {
            async getCardInfo() {
                var url = this.contentUrl;

                await this.$store.dispatch('getCardById', url).then(() => {
                    this.cardInfo = this.$store.getters.getCardInfo;
                }).catch(() => {
                    this.$message("Error getting card info for card id " + id);
                })
            }
        }
    }
</script>

<style scoped>
    header{
        font-size: 12px;
    }
</style>